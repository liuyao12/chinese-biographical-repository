"""Finite exact title holdings and ruler-title references for Songshu 51 p014–p017."""
from pathlib import Path
import copy, json, hashlib

CID = 'c-songshu-051-wyd1739-zongshi'
CHAPTER = 'corpus/songshu/051-wyd1739.json'
TITLE_PATH = 'corpus/songshu/051-wyd1739-p014-p017-titles.json'
YONGCHU = 'source-evidence/song045-wyd1739-liucui/nobles-moe-yongchu-row.json'
YUANHUI = 'source-evidence/song051-wyd1739-zongshi/p014-p017-yuanhui-calendar-row.json'
UNKNOWN = {'status':'unknown','date_expression':None,'evidence':[]}
TITLE_KIND = 'fixed_wyd_song051_p014_p017_exact_title'
PROPOSAL_KIND = 'fixed_wyd_song051_p015_not_assumed_appointment'

# id, p-number, person_id, subject mention ID, title, kind, mode, unique local context, exact anchor, date
SPECS = [
('th-song051-p014-yizong-xinyu-nan','p014','3qs_nqa_ioa_AABD','c-songshu-051-wyd1739-zongshi:p014:m0001','新渝縣男','noble_rank','grant','賜爵新渝縣男','新渝縣男',None),
('th-song051-p014-yizong-hou','p014','3qs_nqa_ioa_AABD','c-songshu-051-wyd1739-zongshi:p014:m0001','侯','noble_rank','grant','永初元年進爵為侯','侯','永初元年'),
('th-song051-p014-yizong-huangmen','p014','3qs_nqa_ioa_AABD','c-songshu-051-wyd1739-zongshi:p014:m0001','黃門侍郎','office','attestation','歷黃門侍郎太子左衞率','黃門侍郎',None),
('th-song051-p014-yizong-taizi-zuoweishuai','p014','3qs_nqa_ioa_AABD','c-songshu-051-wyd1739-zongshi:p014:m0001','太子左衞率','office','attestation','歷黃門侍郎太子左衞率','太子左衞率',None),
('th-song051-p014-yizong-shizhong','p014','3qs_nqa_ioa_AABD','c-songshu-051-wyd1739-zongshi:p014:m0001','侍中','office','attestation','又為侍中太子詹事','侍中',None),
('th-song051-p014-yizong-taizi-zhanshi','p014','3qs_nqa_ioa_AABD','c-songshu-051-wyd1739-zongshi:p014:m0001','太子詹事','office','attestation','又為侍中太子詹事','太子詹事',None),
('th-song051-p014-yizong-sanqi','p014','3qs_nqa_ioa_AABD','c-songshu-051-wyd1739-zongshi:p014:m0001','散騎常侍','honorific','attestation','加散騎常侍征虜將軍南兗州刺史','散騎常侍',None),
('th-song051-p014-yizong-zhenglu','p014','3qs_nqa_ioa_AABD','c-songshu-051-wyd1739-zongshi:p014:m0001','征虜將軍','office','attestation','加散騎常侍征虜將軍南兗州刺史','征虜將軍',None),
('th-song051-p014-yizong-nanyang','p014','3qs_nqa_ioa_AABD','c-songshu-051-wyd1739-zongshi:p014:m0001','南兗州刺史','office','attestation','加散騎常侍征虜將軍南兗州刺史','南兗州刺史',None),
('th-song051-p014-yizong-pingbei-posthumous','p014','3qs_nqa_ioa_AABD','c-songshu-051-wyd1739-zongshi:p014:m0001','平北將軍','office','posthumous_grant','追贈散騎常侍平北將軍','平北將軍',None),
('th-song051-p014-yizong-hou-posthumous','p014','3qs_nqa_ioa_AABD','c-songshu-051-wyd1739-zongshi:p014:m0001','惠侯','honorific','posthumous_naming','諡曰惠侯','惠侯',None),
('th-song051-p014-jie-hou','p014','3qs_nqa_ioa_AABDA','c-songshu-051-wyd1739-zongshi:p014:m0164','懷侯','noble_rank','accession','子懷侯玠嗣','懷侯',None),
('th-song051-p014-jie-taishou','p014','3qs_nqa_ioa_AABDA','c-songshu-051-wyd1739-zongshi:p014:m0164','琅邪秦郡太守','office','attestation','琅邪秦郡太守','琅邪秦郡太守',None),
('th-song051-p014-jie-sanqi-posthumous','p014','3qs_nqa_ioa_AABDA','c-songshu-051-wyd1739-zongshi:p014:m0164','散騎常侍','office','posthumous_grant','為元凶所殺追贈散騎常侍','散騎常侍',None),
('th-song051-p014-bing-zhuzuo','p014','3qs_nqa_ioa_AABDB','c-songshu-051-wyd1739-zongshi:p014:m0186','著作郎','office','attestation','初為著作郎歷羽林監越騎校尉','著作郎',None),
('th-song051-p014-bing-yulin','p014','3qs_nqa_ioa_AABDB','c-songshu-051-wyd1739-zongshi:p014:m0186','羽林監','office','attestation','初為著作郎歷羽林監越騎校尉','羽林監',None),
('th-song051-p014-bing-yueqi','p014','3qs_nqa_ioa_AABDB','c-songshu-051-wyd1739-zongshi:p014:m0186','越騎校尉','office','attestation','初為著作郎歷羽林監越騎校尉','越騎校尉',None),
('th-song051-p015-bing-shizhong','p015','3qs_nqa_ioa_AABDB','c-songshu-051-wyd1739-zongshi:p015:m0039','侍中','office','attestation','泰始初為侍中頻徙左衞將軍丹陽尹太子詹事吏部尚書','侍中',None),
('th-song051-p015-bing-zuowei','p015','3qs_nqa_ioa_AABDB','c-songshu-051-wyd1739-zongshi:p015:m0039','左衞將軍','office','attestation','頻徙左衞將軍丹陽尹太子詹事吏部尚書','左衞將軍',None),
('th-song051-p015-bing-danyang','p015','3qs_nqa_ioa_AABDB','c-songshu-051-wyd1739-zongshi:p015:m0039','丹陽尹','office','attestation','頻徙左衞將軍丹陽尹太子詹事吏部尚書','丹陽尹',None),
('th-song051-p015-bing-taizi-zhanshi','p015','3qs_nqa_ioa_AABDB','c-songshu-051-wyd1739-zongshi:p015:m0039','太子詹事','office','attestation','頻徙左衞將軍丹陽尹太子詹事吏部尚書','太子詹事',None),
('th-song051-p015-bing-libushangshu','p015','3qs_nqa_ioa_AABDB','c-songshu-051-wyd1739-zongshi:p015:m0039','吏部尚書','office','attestation','頻徙左衞將軍丹陽尹太子詹事吏部尚書','吏部尚書',None),
('th-song051-p015-bing-mishujian','p015','3qs_nqa_ioa_AABDB','c-songshu-051-wyd1739-zongshi:p015:m0204','祕書監','office','attestation','復為侍中守祕書監領太子詹事未拜','祕書監',None),
('th-song051-p015-bing-zuopushe','p015','3qs_nqa_ioa_AABDB','c-songshu-051-wyd1739-zongshi:p015:m0204','尚書左僕射','office','attestation','未拜留為尚書左僕射參選','尚書左僕射',None),
('th-song051-p015-bing-houjiangjun','p015','3qs_nqa_ioa_AABDB','c-songshu-051-wyd1739-zongshi:p015:m0204','後將軍','office','attestation','還使持節都督南徐徐兗豫青冀六州諸軍事後將軍南徐州刺史','後將軍',None),
('th-song051-p015-bing-nanxu','p015','3qs_nqa_ioa_AABDB','c-songshu-051-wyd1739-zongshi:p015:m0204','南徐州刺史','office','attestation','還使持節都督南徐徐兗豫青冀六州諸軍事後將軍南徐州刺史','南徐州刺史',None),
('th-song051-p015-bing-sanqi','p015','3qs_nqa_ioa_AABDB','c-songshu-051-wyd1739-zongshi:p015:m0204','散騎常侍','honorific','attestation','加散騎常侍後廢帝即位改都督','散騎常侍',None),
('th-song051-p016-bing-danyang','p016','3qs_nqa_ioa_AABDB','c-songshu-051-wyd1739-zongshi:p016:m0085','丹陽尹','office','grant','二年加散騎常侍丹陽尹解吏部','丹陽尹','二年'),
('th-song051-p016-bing-dangyang-hou','p016','3qs_nqa_ioa_AABDB','c-songshu-051-wyd1739-zongshi:p016:m0085','當陽縣侯','noble_rank','grant','封當陽縣侯食邑千戶','當陽縣侯','二年'),
('th-song051-p016-bing-zhongshuling','p016','3qs_nqa_ioa_AABDB','c-songshu-051-wyd1739-zongshi:p016:m0085','中書令','office','grant','四年遷中書令加撫軍將軍','中書令','四年'),
('th-song051-p016-bing-fujun','p016','3qs_nqa_ioa_AABDB','c-songshu-051-wyd1739-zongshi:p016:m0085','撫軍將軍','office','grant','四年遷中書令加撫軍將軍','撫軍將軍','四年'),
('th-song051-p016-bing-shangshuling','p016','3qs_nqa_ioa_AABDB','c-songshu-051-wyd1739-zongshi:p016:m0085','尚書令','office','attestation','順帝即位轉尚書令中領軍將軍如故','尚書令',None),
('th-song051-p016-bing-zhonglingjun','p016','3qs_nqa_ioa_AABDB','c-songshu-051-wyd1739-zongshi:p016:m0085','中領軍將軍','office','attestation','順帝即位轉尚書令中領軍將軍如故','中領軍將軍',None),
]

TITLE_USES = [
('tu-song051-p014-gaozu','p014','m0005','高祖','3qs_nqa_ioa_AAA','contextual_named_ancestor_title'),
('tu-song051-p014-yuanxiong','p014','m0173','元凶','fof_k8v_7md','specific_posthumous_epithet_title'),
('tu-song051-p015-taizong-1','p015','m0005','太宗','cti_o52_4nz','posthumous_imperial_title'),
('tu-song051-p015-taizong-2','p015','m0052','太宗','cti_o52_4nz','posthumous_imperial_title'),
('tu-song051-p015-houfeidi','p015','m0123','後廢帝','91d_607_b0a','posthumous_reign_title'),
('tu-song051-p015-guiyangwang','p015','m0188','桂陽王','fjv_3dz_w0m','noble_rank_title'),
('tu-song051-p016-shundi','p016','m0061','順帝','6y2_apj_l05','posthumous_reign_title'),
('tu-song051-p016-qiwang-1','p016','m0032','齊王','47p_kjh_ez7','reign_specific_royal_title'),
('tu-song051-p016-qiwang-2','p016','m0077','齊王','47p_kjh_ez7','reign_specific_royal_title'),
('tu-song051-p016-qiwang-3','p016','m0110','齊王','47p_kjh_ez7','reign_specific_royal_title'),
('tu-song051-p017-qiwang-1','p017','m0015','齊王','47p_kjh_ez7','reign_specific_royal_title'),
('tu-song051-p017-qiwang-2','p017','m0022','齊王','47p_kjh_ez7','reign_specific_royal_title'),
('tu-song051-p017-taizong','p017','m0206','太宗','cti_o52_4nz','posthumous_imperial_title'),
('tu-song051-p017-shizu','p017','m0194','世祖','hx8_st4_jdd','posthumous_imperial_title'),
]

def load_chapter(root):
    return json.loads((Path(root)/CHAPTER).read_text(encoding='utf-8'))

def _anchor(p, context, surface):
    if context not in p['text'] or p['text'].count(context) != 1:
        raise ValueError(f'稱號上下文不唯一：{p["id"]} {context}')
    start=p['text'].index(context)
    offset=context.find(surface)
    if offset < 0 or context.count(surface) != 1:
        raise ValueError(f'稱號錨不唯一：{p["id"]} {surface}')
    start += offset
    return {'paragraph_id':p['id'],'start':start,'end':start+len(surface),'surface':surface}

def _evidence(ch,p,mid):
    return {'work_id':ch['work_id'],'book_id':ch['book_id'],'source_id':ch['source_id'],
            'chapter_id':CID,'paragraph_id':p['id'],'quote':p['text'],'person_mention_id':mid}

def title_records(ch,root):
    paragraphs={p['id'].rsplit(':',1)[-1]:p for p in ch['paragraphs']}
    out=[]
    yrow=json.loads((Path(root)/YONGCHU).read_text(encoding='utf-8'))
    ysha=hashlib.sha256((Path(root)/YONGCHU).read_bytes()).hexdigest()
    yr=json.loads((Path(root)/YUANHUI).read_text(encoding='utf-8'))
    yrsha=hashlib.sha256((Path(root)/YUANHUI).read_bytes()).hexdigest()
    for ident,pno,pid,mid,title,kind,mode,context,surface,date in SPECS:
        p=paragraphs[pno]
        subject=next((m for m in p['mentions'] if m['id']==mid and m['person_id']==pid),None)
        if subject is None: raise ValueError(f'稱號受任者錨缺漏：{ident}')
        anchor=_anchor(p,context,surface);ev=_evidence(ch,p,mid)
        if mode=='attestation':
            start={'status':'unknown','date_expression':None,'evidence':[]}
        else:
            start={'status':'source_event','event_type':mode,'date_expression':date,'evidence':[ev]}
        contextual=None
        if date=='永初元年':
            ref={'title':'教育部《重編國語辭典修訂本》中國歷代年號表','url':yrow['url'],'quote':'永初','scope':'modern_era_year_equivalence_only','columns':copy.deepcopy(yrow['columns']),'fixed_row_reference':{'path':YONGCHU,'sha256':ysha},'image_verified':False}
            start['normalized_date']={'era':'CE','year':420,'era_year':420,'year_numbering':'astronomical','precision':'year','calendar':'chinese_civil','source_expression':'永初元年','original_quote':p['text'],'evidence':[ev],'references':[ref],'regnal_year_mapping':{'kind':'ce_regnal_era_span','era_name':'永初','source_number':'元','regnal_year':1,'start_ce_year':420,'end_ce_year':422,'reference_index':0},'status':'editorial_provisional','rationale':'本源明載永初元年進爵為侯；教育部年號表列永初420–422，換為中國曆420年，只記年、不推月日。','reviewer':'Codex（AI代理）','human_reviewed':False,'model':None}
        elif date=='二年':
            ref={'title':'教育部《重編國語辭典修訂本》中國歷代年號表','url':yr['url'],'quote':'元徽','scope':'modern_era_year_equivalence_only','columns':copy.deepcopy(yr['columns']),'fixed_row_reference':{'path':YUANHUI,'sha256':yrsha},'image_verified':False}
            contextual={'kind':'contextual_ce_regnal_year','year':474,'era':'元徽','source_expression':'二年','basis_paragraph_id':paragraphs['p015']['id'],'basis_quote':paragraphs['p015']['text'],'basis_anchor':_anchor(paragraphs['p015'],'元徽元年領吏部','元徽元年'),'calendar_reference':ref,'rationale':'p016承接p015「元徽元年領吏部」；本段「二年」依同一紀年脈絡解作元徽二年。年號表列元徽473–477，故為474年。','human_reviewed':False}
        h={'id':ident,'person_id':pid,'title':title,'kind':kind,'mode':mode,'status':'source_attested',
           'appointment_role':'acting' if ident=='th-song051-p015-bing-mishujian' else 'source_report','source_career_role':{'kind':TITLE_KIND,'record_id':ident,'paragraph_id':p['id'],'subject_mention_id':mid,'source_anchor':anchor,'context_anchor':{'paragraph_id':p['id'],'start':p['text'].index(context),'end':p['text'].index(context)+len(context),'surface':context},'source_revision':ch['source']['revision_id'],'human_reviewed':False},
           'evidence':[ev],'attestations':[{'id':'att-song051-p014-p017-'+ident.removeprefix('th-song051-p014-p017-'),'paragraph_id':p['id'],'start':anchor['start'],'end':anchor['end'],'surface':surface,'person_mention_id':mid,'usage':'narrative','date_expression':date}],
           'effective_period':{'start':start,'end':copy.deepcopy(UNKNOWN)},
           'interpretation_note':'只記原文所見職稱／爵稱與本段明載事件。未拜、辭不拜者不作實任；不以卒日推定終期；「侯」不補封縣。',
           'reviewer':'Codex（AI代理）','human_reviewed':False,'model':None}
        if contextual:h['contextual_date_resolution']=contextual
        if mode=='posthumous_grant':h['posthumous_basis']={'source_term':context,'evidence':[ev]}
        if mode=='posthumous_naming':h['naming_basis']={'source_term':context,'death_term':'二十一年卒','evidence':[ev]}
        out.append(h)
    return {'format_version':'0.2','record_type':'title_holding_assertion_set','chapter_id':CID,'holdings':out}

def title_holding_valid(h,ch,root=None):
    try:
        if root is None or ch.get('id')!=CID:return False
        docs=title_records(ch,root);expected={x['id']:x for x in docs['holdings']}
        return h.get('source_career_role',{}).get('kind')==TITLE_KIND and h['id'] in expected and h==expected[h['id']]
    except (KeyError,TypeError,ValueError,StopIteration,OSError):return False

def source_title_use_valid(use,ch):
    try:
        if ch.get('id')!=CID or use.get('usage_kind')!='title_reference' or use.get('human_reviewed') is not False:return False
        entry=next(x for x in TITLE_USES if x[0]==use['id'])
        _,pno,short,surface,pid,basis=entry
        p=next(p for p in ch['paragraphs'] if p['id'].endswith(':'+pno))
        mid=f'{p["id"]}:{short}'
        m=next(m for m in p['mentions'] if m['id']==mid)
        a=use['source_anchor'];e,=use['evidence']
        expected={'id':entry[0],'person_id':pid,'person_mention_id':mid,'source_term':surface,
          'source_anchor':{'paragraph_id':p['id'],'start':m['start'],'end':m['end'],'surface':surface},
          'usage_kind':'title_reference','holding_ids':[],
          'evidence':[{'work_id':ch['work_id'],'book_id':ch['book_id'],'source_id':ch['source_id'],'chapter_id':CID,'paragraph_id':p['id'],'quote':p['text'],'person_mention_id':mid}],
          'source_use_binding':{'kind':'fixed_wyd_song051_p014_p017_title_reference','basis':basis,'interpretation_note':'原文以君主稱號指向在位人物；保留稱號與用人ID的對照，稱號不作姓名別名。'},
          'human_reviewed':False}
        return (m['kind']=='person' and m['person_id']==pid and m['surface']==surface
                and p['text'][m['start']:m['end']]==surface and use==expected)
    except (KeyError,TypeError,ValueError,StopIteration,IndexError):return False

def title_uses(ch):
    paragraphs={p['id'].rsplit(':',1)[-1]:p for p in ch['paragraphs']}
    out=[]
    for ident,pno,short,surface,pid,basis in TITLE_USES:
        p=paragraphs[pno];mid=f'{p["id"]}:{short}'
        m=next(m for m in p['mentions'] if m['id']==mid and m['surface']==surface and m['person_id']==pid)
        out.append({'id':ident,'person_id':pid,'person_mention_id':mid,'source_term':surface,
          'source_anchor':{'paragraph_id':p['id'],'start':m['start'],'end':m['end'],'surface':surface},
          'usage_kind':'title_reference','holding_ids':[],
          'evidence':[{'work_id':ch['work_id'],'book_id':ch['book_id'],'source_id':ch['source_id'],'chapter_id':CID,'paragraph_id':p['id'],'quote':p['text'],'person_mention_id':mid}],
          'source_use_binding':{'kind':'fixed_wyd_song051_p014_p017_title_reference','basis':basis,'interpretation_note':'原文以君主稱號指向在位人物；保留稱號與用人ID的對照，稱號不作姓名別名。'},
          'human_reviewed':False})
    return out

PROPOSAL_SPECS = (
 ('tp-song051-p015-qianjiangjun','前將軍','出為','不拜','五年'),
 ('tp-song051-p015-huainan-xuancheng-taishou','淮南宣城二郡太守','出為','不拜','五年'),
 ('tp-song051-p015-taizi-zhanshi','太子詹事','領','未拜','復為侍中守祕書監'),
 ('tp-song051-p015-yingzhou-cishi','郢州刺史','改都督','未拜','後廢帝即位'),
 ('tp-song051-p015-weiwei','衞尉','領','辭不拜','元徽元年領吏部'),
)

def title_proposals(ch):
    p=next(p for p in ch['paragraphs'] if p['id'].endswith(':p015'))
    person=next(m for m in p['mentions'] if m['surface']=='秉' and m['person_id']=='3qs_nqa_ioa_AABDB')
    out=[]
    for ident,title,appointment,refusal,context in PROPOSAL_SPECS:
        start=p['text'].index(title,p['text'].index(context));r=p['text'].index(refusal,start)
        if appointment=='出為': astart=p['text'].rfind(appointment,p['text'].index(context),start)
        elif appointment=='改都督': astart=p['text'].rfind(appointment,p['text'].index(context),start)
        else: astart=p['text'].rfind(appointment,p['text'].index(context),start)
        if astart<0: raise ValueError(f'未承任提議缺任用詞：{ident}')
        def anchor(i,j):return {'paragraph_id':p['id'],'start':i,'end':j,'surface':p['text'][i:j]}
        cs=p['text'].index(context);quote=p['text'][cs:r+len(refusal)]
        out.append({'id':ident,'person_id':person['person_id'],'person_mention_id':person['id'],'title':title,'kind':'office',
          'proposal_kind':'unassumed_appointment','outcome':'not_assumed','appointment_stage':'appointment',
          'role_anchor':anchor(start,start+len(title)),'appointment_anchor':anchor(astart,astart+len(appointment)),
          'non_assumption_anchor':anchor(r,r+len(refusal)),'non_assumption_kind':'declined' if refusal=='辭不拜' else 'did_not_take_up',
          'evidence':[{'work_id':ch['work_id'],'book_id':ch['book_id'],'source_id':ch['source_id'],'chapter_id':ch['id'],'paragraph_id':p['id'],'quote':quote,'person_mention_id':person['id']}],
          'date_expression':'五年' if context=='五年' else None,
          'source_appointment_context':{'kind':PROPOSAL_KIND,'reviewed_context':context,'human_reviewed':False},
          'status':'contextual_provisional','interpretation_note':'原文明記未拜／辭不拜，保存職稱但不列為實授；「五年」未有明確年號背景，不換算西元。',
          'reviewer':'Codex（AI代理）','human_reviewed':False,'model':None})
    return out

def proposal_errors(proposal,ch):
    try:
        expected={p['id']:p for p in title_proposals(ch)}
        return [] if expected.get(proposal.get('id'))==proposal else ['宋051未承任提議錨點不符']
    except (KeyError,ValueError,StopIteration):return ['宋051未承任提議錨點不符']
