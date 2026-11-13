"""固定武英殿《宋書》卷五十一 p020–p028 人物、親屬、籍貫、生卒與稱號資料。"""
from __future__ import annotations
import copy, hashlib, json
from pathlib import Path

CID = 'c-songshu-051-wyd1739-zongshi'
CHAPTER_PATH = 'corpus/songshu/051-wyd1739.json'
CONTRACT_PATH = 'source-evidence/song051-wyd1739-zongshi/yixin-complete-unit-contract.json'
YIXI_PATH = 'source-evidence/song051-wyd1739-zongshi/yixi-era-row.json'
NEW_IDS = {
    '桓謐': 'iiw_d7b_igi', '蔡猛': 'ozs_uc6_hp2', '劉基': 'xb9_tyd_qty',
    '劉遵': '98q_ohs_xh7', '桓道兒': 'u9s_w6j_8mc_AACA',
}

def load(root, rel):
    return json.loads((Path(root) / rel).read_text(encoding='utf-8'))

def paragraphs(ch):
    return {p['id'].rsplit(':', 1)[-1]: p for p in ch['paragraphs']
            if p['id'].split(':')[-1] in {f'p{i:03d}' for i in range(20, 29)}}

def mention(ch, para, surface, occurrence=0):
    p = paragraphs(ch)[para]
    hits = [m for m in p.get('mentions', []) if m.get('surface') == surface]
    if occurrence >= len(hits):
        raise ValueError(f'{para} 缺人物錨：{surface} #{occurrence}')
    return hits[occurrence]

def evidence(ch, p, mids):
    return {'work_id': ch['work_id'], 'book_id': ch['book_id'], 'source_id': ch['source_id'],
            'chapter_id': CID, 'paragraph_id': p['id'], 'quote': p['text'],
            **({'subject_person_mention_id': mids[0], 'object_person_mention_id': mids[1]} if len(mids) == 2 else {})}

def assertions(ch):
    ps = paragraphs(ch)
    # 桓歆—道兒為本傳明言父子；單獨依直接父名句接入桓氏家系。
    p = ps['p026']; child = mention(ch, 'p026', '道兒'); father = mention(ch, 'p026', '桓歆')
    parent = {'id': 'a-song051-p020-p028-huan-xin-father-daoer',
              'subject_person_id': NEW_IDS['桓道兒'], 'object_person_id': 'u9s_w6j_8mc_AAC',
              'predicate': 'father', 'status': 'source_attested',
              'qualifiers': {'lineage': 'paternal', 'source_term': '桓歆子道兒',
                             'source_child_term': '子', 'source_child_sex': 'male',
                             'source_clause_binding': {'kind': 'song051_p020_p028_explicit_father',
                                'start': 90, 'end': 90 + len('桓歆子道兒'), 'paragraph_sha256': hashlib.sha256(p['text'].encode()).hexdigest(),
                                'source_revision': ch['source']['revision_id']},
                             'interpretation_note': '原文於同一短句明載父桓歆與子道兒；只據此記一代父子，不由同姓擴接他人。'},
              'evidence': [evidence(ch, p, [child['id'], father['id']])],
              'human_reviewed': False, 'model': None}
    # 「道規從母兄」以劉遵為較年長的母系同輩旁親；不連入劉氏父系祖先。
    p = ps['p027']; cousin = mention(ch, 'p027', '遵', 2); daogui = mention(ch, 'p027', '道規', 0)
    start = p['text'].index('道規從母兄'); end = start + len('道規從母兄')
    maternal = {'id': 'a-song051-p020-p028-liu-zun-older-maternal-cousin-of-daogui',
                'subject_person_id': NEW_IDS['劉遵'], 'object_person_id': '3qs_nqa_ioa_AAC',
                'predicate': 'maternal_cousin', 'status': 'source_attested',
                'qualifiers': {'source_term': '道規從母兄',
                  'kinship_structure': {'lineage': 'maternal', 'generation_difference': 0,
                    'collateral': True, 'distance': None, 'common_ancestor_person_id': None,
                    'subject_relative_age': 'older', 'maternal_path': 'mother_sister_son'},
                  'relative_birth_order': {'operator': 'lt', 'scope': 'maternal_cousins',
                    'older_person_id': NEW_IDS['劉遵'], 'younger_person_id': '3qs_nqa_ioa_AAC',
                    'older_ordinal': None, 'younger_ordinal': None},
                  'source_clause_binding': {'kind': 'song051_named_congmu_xiong', 'start': start, 'end': end,
                    'source_revision': ch['source']['revision_id'],
                    'paragraph_sha256': hashlib.sha256(p['text'].encode()).hexdigest()},
                  'interpretation_note': '「從母兄」記同代、母系旁親及來源所稱較長；未名母親、姨母與共祖均不補，故不加入父系家族。「蕭氏舅也」另存原句，不推定或新造未具名蕭氏人物。'},
                'evidence': [evidence(ch, p, [cousin['id'], daogui['id']])],
                'human_reviewed': False, 'model': None}
    return {'format_version': '0.2', 'record_type': 'person_assertion_set', 'chapter_id': CID,
            'assertions': [parent, maternal]}

def identity_decisions(ch, root):
    ps = paragraphs(ch); by_pid = {}
    for p in ps.values():
        for m in p.get('mentions', []):
            if m.get('kind') == 'person': by_pid.setdefault(m['person_id'], []).append((p, m))
    people = {p['id']: p for p in load(root, 'registry/persons.json')['persons']}
    out = []
    for pid, hits in sorted(by_pid.items()):
        # Existing p024/p025 identity decisions already cover their exact MIDs; only the new occurrences enter this extension.
        if pid == 'mvk_2p2_qe8':
            hits = [(p,m) for p,m in hits if m['id'] not in {
                f'{CID}:p024:m0030', f'{CID}:p024:m0037', f'{CID}:p024:m0097', f'{CID}:p024:m0099',
                f'{CID}:p025:m0039', f'{CID}:p025:m0100', f'{CID}:p025:m0138', f'{CID}:p025:m0175'}]
        if pid == 'u9s_w6j_8mc_AEB':
            hits = [(p,m) for p,m in hits if m['id'] not in {
                f'{CID}:p024:m0064', f'{CID}:p024:m0074', f'{CID}:p024:m0103', f'{CID}:p024:m0137',
                f'{CID}:p025:m0037', f'{CID}:p025:m0083', f'{CID}:p025:m0095', f'{CID}:p025:m0159', f'{CID}:p025:m0172'}]
        if not hits: continue
        surfaces = list(dict.fromkeys(m['surface'] for p,m in hits))
        cids = [CID]; ev = []
        for p,_ in hits:
            item = {'work_id': ch['work_id'], 'book_id': ch['book_id'], 'source_id': ch['source_id'],
                    'chapter_id': CID, 'paragraph_id': p['id'], 'quote': p['text']}
            if item not in ev: ev.append(item)
        rationale = '只依《宋書》卷五十一固定武英殿本逐段上下文配對全名與省稱；原字、來源層次及未決身份均保留，不以同姓推親。'
        scope = 'same_chapter'
        if pid == 'aot_lni_dfq':
            jin = load(root, 'corpus/jinshu/099-huanxuan.json')
            jp = next(p for p in jin['paragraphs'] if p['id'].endswith(':p032'))
            jm = next(m for m in jp['mentions'] if m.get('surface') == '馮遷')
            cids.append(jin['id']); scope='cross_chapter'
            ev.append({'work_id':jin['work_id'],'book_id':jin['book_id'],'source_id':jin['source_id'],
                       'chapter_id':jin['id'],'paragraph_id':jp['id'],'quote':jp['text']})
            rationale='《宋書》此處記馮遷斬桓玄；《晉書》卷九十九桓玄傳同一事件以馮遷為斬玄者，取現役馮遷 ID aot_lni_dfq。另有宋書卷45馮遷為不同時段人物，未合併。'
        out.append({'id':f'd-song051-p020-p028-{pid.replace("_","-")}', 'person_id':pid,
          'surfaces':surfaces,'scope':scope,'chapter_ids':cids,'status':'contextual_provisional',
          'confidence_level':'high','identification_basis':{'kind':'source_context','target_mention_ids':[m['id'] for _,m in hits]},
          'evidence':ev,'rationale':rationale,'human_reviewed':False,'model':None})
    return {'format_version':'0.2','record_type':'person_identity_decision_set','chapter_id':CID,'decisions':out}

def name_components(ch):
    ps=paragraphs(ch); p25=ps['p025']; full=mention(ch,'p025','劉遵'); p26=ps['p026']; father=mention(ch,'p026','桓歆'); child=mention(ch,'p026','道兒'); p27=ps['p027']; zun=mention(ch,'p027','遵',2)
    bind={'kind':'explicit_parent_and_child_in_one_source_clause','paragraph_id':p26['id'],'start':90,'end':90+len('桓歆子道兒'),
          'surface':'桓歆子道兒','paragraph_sha256':hashlib.sha256(p26['text'].encode()).hexdigest(),
          'source_revision':ch['source']['revision_id'],'father_mention_id':father['id'],'child_mention_id':child['id'],
          'assertion_id':'a-song051-p020-p028-huan-xin-father-daoer'}
    records=[
      {'id':'name-song051-p020-p028-liu-zun','person_id':NEW_IDS['劉遵'],'surname':'劉','ming':'遵','zi':'慧明','additional_names':[],
       'chapter_id':CID,'paragraph_id':p25['id'],'person_mention_id':full['id'],'quote':p25['text'],
       'source_term':'劉遵；遵字慧明','status':'source_attested','human_reviewed':False,'model':None,
       'interpretation_note':'p025明載全名劉遵；p027明言「遵字慧明」，名、字分欄，字之原文位置另作固定錨點。',
       'source_zi_binding':{'kind':'explicit_zi_yue_form','paragraph_id':p27['id'],'start':77,'end':80,
          'surface':'字慧明','person_mention_id':zun['id'],'human_reviewed':False}},
      {'id':'name-song051-p020-p028-huan-xin','person_id':'u9s_w6j_8mc_AAC','surname':'桓','ming':'歆','additional_names':[],
       'chapter_id':CID,'paragraph_id':p26['id'],'person_mention_id':father['id'],'quote':p26['text'],
       'status':'source_attested','human_reviewed':False,'model':None,
       'interpretation_note':'本段逐字見桓歆全名；只作道兒父親姓名的本源構件錨。'},
      {'id':'name-song051-p020-p028-huan-daoer','person_id':NEW_IDS['桓道兒'],'surname':'桓','ming':'道兒','additional_names':[],
       'chapter_id':CID,'paragraph_id':p26['id'],'person_mention_id':child['id'],'quote':p26['text'],
       'status':'contextual_provisional','human_reviewed':False,'model':None,
       'surname_basis':{'kind':'contextual_surname_from_explicit_named_father_clause','status':'contextual_provisional',
          'human_reviewed':False,'rationale':'「桓歆子道兒」在同一固定原句明列父姓桓與子名道兒；只據這一父子句復姓，不以家族ID或同姓推導。',
          'source_term':'桓歆子道兒','father_person_id':'u9s_w6j_8mc_AAC','father_name_record_id':'name-song051-p020-p028-huan-xin',
          'father_mention_id':father['id'],'child_mention_id':child['id'],'assertion_id':'a-song051-p020-p028-huan-xin-father-daoer',
          'paragraph_id':p26['id'],'start':90,'end':90+len('桓歆子道兒'),'paragraph_sha256':hashlib.sha256(p26['text'].encode()).hexdigest(),
          'source_revision':ch['source']['revision_id']}}
    ]
    return {'format_version':'0.2','record_type':'person_name_component_set','chapter_id':CID,'records':records}

def addresses(ch):
    ps=paragraphs(ch);p27=ps['p027'];zun=mention(ch,'p027','遵',2);dao=mention(ch,'p027','道規',0)
    origin='臨淮海西';i=p27['text'].index(origin);death='京師';j=p27['text'].index(death)
    def row(ident,pid,relation,term,placename,anchor_start,anchor_end,mid,note):
        return {'id':ident,'person_id':pid,'relation':relation,'source_term':term,
          'place':{'source_name':placename,'modern_place_id':None},'date_expression':None,'status':'source_attested',
          'evidence':[{'work_id':ch['work_id'],'book_id':ch['book_id'],'source_id':ch['source_id'],'chapter_id':CID,
            'paragraph_id':p27['id'],'quote':p27['text'],'person_mention_id':mid,
            'place_anchor':{'paragraph_id':p27['id'],'start':anchor_start,'end':anchor_end,'surface':placename}}],
          'interpretation_note':note,'human_reviewed':False}
    return {'format_version':'0.2','record_type':'person_address_assertion_set','chapter_id':CID,'assertions':[
      row('ad-song051-p020-p028-liu-zun-origin',NEW_IDS['劉遵'],'biographical_origin','臨淮海西人',origin,i,i+len(origin),zun['id'],
          '本傳明載劉遵「臨淮海西人」；原文籍貫照錄，不判定今地、不作出生地。'),
      row('ad-song051-p020-p028-daogui-death-place','3qs_nqa_ioa_AAC','death_place','薨于京師',death,j,j+len(death),dao['id'],
          '本傳明載道規薨於京師；照錄原地稱，不推今日轄區或精確地址。') ]}

def life_events(ch,root):
    ps=paragraphs(ch);p27=ps['p027'];p28=ps['p028'];zun=mention(ch,'p027','遵',2);dao=mention(ch,'p027','道規',0)
    era=load(root,YIXI_PATH);ref={'title':era['title'],'url':era['url'],'quote':era['era_name'],
      'scope':'modern_era_year_equivalence_only','columns':{'dynasty':era['dynasty'],'era_name':era['era_name'],
      'first_year':str(era['first_ce_year']),'last_year':str(era['last_ce_year'])},
      'fixed_row_reference':{'path':YIXI_PATH,'sha256':hashlib.sha256((Path(root)/YIXI_PATH).read_bytes()).hexdigest()},
      'image_verified':False}
    def normalized(year,expr,p,mid,note,explicit_era=False):
        date={'era':'CE','era_year':year,'year':year,'year_numbering':'astronomical','precision':'year',
          'source_expression':expr,'original_quote':p['text'],'evidence':[{**evidence(ch,p,[mid]),'person_mention_id':mid}],
          'references':[copy.deepcopy(ref)],'status':'editorial_provisional','rationale':note,
          'reviewer':'Codex（AI代理）','human_reviewed':False,'model':None}
        if explicit_era:
            date.update({'calendar':'chinese_civil','regnal_year_mapping':{'kind':'ce_regnal_era_span',
              'era_name':'義熙','start_ce_year':405,'end_ce_year':418,'regnal_year':10,
              'source_number':'十','source_era_name':'義熙','reference_index':0}})
        else:
            date['contextual_era_interpretation']={'kind':'same_biography_omitted_era_after_regnal_year_sequence',
              'era_name':'義熙','era_year':8,'equivalence_reference_index':0,
              'source_expression':'八年閏月','interpretation_note':note}
        return date
    events=[
      {'id':'le-song051-p020-p028-liu-zun-death','person_id':NEW_IDS['劉遵'],'event_type':'death','status':'source_attested',
       'date_expression':'義熙十年','source_term':'義熙十年卒','evidence':[{**evidence(ch,p27,[zun['id']]),'person_mention_id':zun['id']}],
       'normalized_date':normalized(414,'義熙十年',p27,zun['id'],'教育部年號表列義熙元年405至418年；本句明記義熙十年卒，換算西元414年，只記年，不推月日。',True),
       'interpretation_note':'原文精確語為義熙十年卒，換算西元414年；未記年齡、出生年或母名。','reviewer':'Codex（AI代理）','human_reviewed':False,'model':None},
      {'id':'le-song051-p020-p028-daogui-death','person_id':'3qs_nqa_ioa_AAC','event_type':'death','status':'source_attested',
       'date_expression':'八年閏月','source_term':'八年閏月薨','evidence':[{**evidence(ch,p27,[dao['id']]),'person_mention_id':dao['id']}],
       'normalized_date':normalized(412,'八年閏月',p27,dao['id'],'此處省略年號；本傳在劉遵卒句後返回道規主語，依道規寢疾、改任、不拜的連續敘事，並由相鄰「義熙十年」紀年關係判作義熙八年，即公元412年。閏月保留原詞，不換公曆月日。'),
       'interpretation_note':'年號在相鄰劉遵死亡句後省略；依本傳主語與敘事回到劉道規，按義熙八年換算412年。報齡「時年四十三」另存，不倒推出生年。','reported_age':{'value':43,'source_term':'時年四十三','age_basis':'source_reported','birth_year_inferred':False},
       'reviewer':'Codex（AI代理）','human_reviewed':False,'model':None},
    ]
    return {'format_version':'0.2','record_type':'person_life_event_assertion_set','chapter_id':CID,'events':events}

def titles(ch):
    ps=paragraphs(ch); specs=[]
    # Identity anchor is an actual name mention in the same full source passage; office words are separate title holdings.
    def add(ident,pno,pid,person_mid,title,kind,mode,usage='narrative'):
        p=ps[pno];start=p['text'].find(title)
        if start<0:raise ValueError(f'{pno} missing title {title}')
        if not any(m.get('person_id')==pid for m in p.get('mentions',[])):
            raise ValueError(f'{pno} no person anchor for {title}')
        ev={'work_id':ch['work_id'],'book_id':ch['book_id'],'source_id':ch['source_id'],
            'chapter_id':CID,'paragraph_id':p['id'],'quote':p['text'],'person_mention_id':person_mid}
        start_status={'status':'unknown','date_expression':None,'evidence':[]}
        if mode!='attestation':start_status={'status':'source_event','event_type':mode,'date_expression':None,'evidence':[copy.deepcopy(ev)]}
        specs.append({'id':ident,'person_id':pid,'title':title,'kind':kind,'mode':mode,'status':'source_attested',
          'appointment_role':'source_report','evidence':[ev],
          'attestations':[{'id':'att-'+ident,'paragraph_id':p['id'],'start':start,'end':start+len(title),
             'surface':title,'person_mention_id':person_mid,'usage':'posthumous_usage' if mode in ('posthumous_grant','posthumous_enfeoffment','posthumous_naming') else usage,'date_expression':None}],
          'effective_period':{'start':start_status,'end':{'status':'unknown','date_expression':None,'evidence':[]}},
          'interpretation_note':'保留來源原稱與職爵類別；原文未給可定始終年的記作未知，不由後文生卒補職期。',
          'human_reviewed':False,'model':None})
        if mode == 'posthumous_grant':
            phrase = ('追贈撫軍將軍追封監利縣侯食邑七百戶' if pno == 'p027'
                      else '四十三追贈侍中司徒')
            specs[-1]['posthumous_basis']={'source_term':phrase,'evidence':[copy.deepcopy(ev)]}
        if mode == 'posthumous_enfeoffment':
            if pno == 'p027':
                source_term='追封'+title
                death_event_id='le-song051-p020-p028-liu-zun-death'
                specs[-1]['enfeoffment_basis']={'kind':'explicit_posthumous_enfeoffment','source_term':source_term,
                  'death_event_id':death_event_id,'evidence':[copy.deepcopy(ev)]}
            else:
                prev=ps['p027']; death_mid=mention(ch,'p027','道規',0)['id']
                specs[-1]['enfeoffment_basis']={'kind':'explicit_posthumous_enfeoffment_after_named_subject_death_previous_paragraph',
                  'source_term':'追封'+title,'death_event_id':'le-song051-p020-p028-daogui-death',
                  'death_context':{'paragraph_id':prev['id'],'quote':prev['text'],'person_mention_id':death_mid,
                    'source_revision':ch['source']['revision_id'],'paragraph_sha256':hashlib.sha256(prev['text'].encode()).hexdigest()},
                  'evidence':[copy.deepcopy(ev)]}
    # Liu Daogui's life and posthumous titles; the final 豫州刺史 is intentionally excluded as the text says 以疾不拜.
    m=mention(ch,'p023','道規',0)
    add('th-song051-p020-p028-daogui-fuguo','p023','3qs_nqa_ioa_AAC',m['id'],'輔國將軍','office','attestation')
    add('th-song051-p020-p028-daogui-bingzhou','p023','3qs_nqa_ioa_AAC',m['id'],'并州刺史','office','attestation')
    add('th-song051-p020-p028-daogui-yichang','p023','3qs_nqa_ioa_AAC',m['id'],'義昌太守','office','attestation')
    add('th-song051-p020-p028-daogui-huarong','p023','3qs_nqa_ioa_AAC',m['id'],'華容縣公','noble_rank','grant')
    m=mention(ch,'p027','道規',0)
    add('th-song051-p020-p028-daogui-zhengxi','p027','3qs_nqa_ioa_AAC',m['id'],'征西大將軍','office','grant')
    add('th-song051-p020-p028-daogui-kaifu','p027','3qs_nqa_ioa_AAC',m['id'],'開府儀同三司','office','grant')
    add('th-song051-p020-p028-daogui-sanjichangshi','p027','3qs_nqa_ioa_AAC',m['id'],'散騎常侍','office','grant')
    add('th-song051-p020-p028-daogui-dasima-post','p028','3qs_nqa_ioa_AAC',mention(ch,'p028','道規',0)['id'],'大司馬','office','attestation')
    add('th-song051-p020-p028-daogui-situ-post','p028','3qs_nqa_ioa_AAC',mention(ch,'p028','王',0)['id'],'司徒','office','posthumous_grant')
    add('th-song051-p020-p028-daogui-shizhong-post','p028','3qs_nqa_ioa_AAC',mention(ch,'p028','王',0)['id'],'侍中','office','posthumous_grant')
    add('th-song051-p020-p028-daogui-liewu-post','p028','3qs_nqa_ioa_AAC',mention(ch,'p028','王',0)['id'],'烈武公','honorific','attestation')
    add('th-song051-p020-p028-daogui-nanjun','p028','3qs_nqa_ioa_AAC',mention(ch,'p028','道規',0)['id'],'南郡公','noble_rank','grant')
    add('th-song051-p020-p028-daogui-linchuanwang','p028','3qs_nqa_ioa_AAC',mention(ch,'p028','道規',0)['id'],'臨川王','royal_rank','posthumous_enfeoffment')
    # Liu Zun source career and posthumous titles.
    zm=mention(ch,'p027','遵',2)
    add('th-song051-p020-p028-liu-zun-youjiangjun','p027',NEW_IDS['劉遵'],zm['id'],'右將軍','office','attestation')
    add('th-song051-p020-p028-liu-zun-xuancheng','p027',NEW_IDS['劉遵'],zm['id'],'宣城內史','office','attestation')
    add('th-song051-p020-p028-liu-zun-huainan','p027',NEW_IDS['劉遵'],zm['id'],'淮南太守','office','attestation')
    add('th-song051-p020-p028-liu-zun-fujun-post','p027',NEW_IDS['劉遵'],zm['id'],'撫軍將軍','office','posthumous_grant')
    add('th-song051-p020-p028-liu-zun-jianli-post','p027',NEW_IDS['劉遵'],zm['id'],'監利縣侯','noble_rank','posthumous_enfeoffment')
    # Do not convert an office explicitly declined due to illness into a holding.
    return {'format_version':'0.2','record_type':'title_holding_assertion_set','chapter_id':CID,
            'holdings':specs,'interpretation_note':'保留年號或省年、後贈與未拜；不由卒年倒推任期，且不把「以疾不拜」的豫州刺史列為已受任。','human_reviewed':False,'model':None}

def build_all(root, ch=None):
    ch=ch or load(root,CHAPTER_PATH)
    return {
      'corpus/songshu/051-wyd1739-p020-p028-assertions.json':assertions(ch),
      'corpus/songshu/051-wyd1739-p020-p028-identities.json':identity_decisions(ch,root),
      'corpus/songshu/051-wyd1739-p020-p028-name-components.json':name_components(ch),
      'corpus/songshu/051-wyd1739-p020-p028-addresses.json':addresses(ch),
      'corpus/songshu/051-wyd1739-p020-p028-life-events.json':life_events(ch,root),
      'corpus/songshu/051-wyd1739-p020-p028-titles.json':titles(ch),
    }

def applies(assertion):
    return assertion.get('id') == 'a-song051-p020-p028-huan-xin-father-daoer'

def family_valid(assertion, paragraphs_by_id, chapters, root):
    try:
        ch=load(root,CHAPTER_PATH); p=next(p for p in ch['paragraphs'] if p['id'].endswith(':p026'))
        child=next(m for m in p['mentions'] if m.get('surface')=='道兒' and m.get('person_id')==NEW_IDS['桓道兒'])
        father=next(m for m in p['mentions'] if m.get('surface')=='桓歆' and m.get('person_id')=='u9s_w6j_8mc_AAC')
        e=assertion['evidence'][0]; q=assertion['qualifiers']; b=q['source_clause_binding']
        return (applies(assertion) and assertion['predicate']=='father' and assertion['status']=='source_attested'
          and assertion['subject_person_id']==NEW_IDS['桓道兒'] and assertion['object_person_id']=='u9s_w6j_8mc_AAC'
          and q['lineage']=='paternal' and q['source_term']=='桓歆子道兒' and b['kind']=='song051_p020_p028_explicit_father'
          and p['text'][b['start']:b['end']]=='桓歆子道兒' and b['paragraph_sha256']==hashlib.sha256(p['text'].encode()).hexdigest()
          and b['source_revision']==ch['source']['revision_id'] and e['quote']==p['text'] and e['paragraph_id']==p['id']
          and e['subject_person_mention_id']==child['id'] and e['object_person_mention_id']==father['id']
          and child['start']>father['end'] and paragraphs_by_id[e['paragraph_id']][0]==CID
          and chapters[CID]['source_id']==ch['source_id'])
    except (KeyError,StopIteration,TypeError,ValueError):
        return False

def life_event_valid(event, root):
    try:
        ch=load(root,CHAPTER_PATH)
        expected={e['id']:e for e in life_events(ch,root)['events']}[event['id']]
        return event==expected
    except (KeyError,StopIteration,TypeError,ValueError,OSError):
        return False
