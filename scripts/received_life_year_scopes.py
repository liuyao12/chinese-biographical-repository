"""Opt-in trusted complete-line witnesses for retained-subject ordinal deaths.
No NLU, structural genealogy IDs, copied appointment years or birth arithmetic.
"""
from pathlib import Path
import hashlib,json,re
KIND='fixed_received_retained_topic_ordinal_death'
INDEX='scripts/fixed_received_life_date_slots.json'

def strict(a,b):
    if type(a)is not type(b):return False
    if isinstance(a,dict):return a.keys()==b.keys()and all(strict(a[k],b[k])for k in a)
    if isinstance(a,list):return len(a)==len(b)and all(strict(x,y)for x,y in zip(a,b))
    return a==b

def file_bytes(root,rel):
    p=Path(rel);root=Path(root).resolve();f=root/p
    assert not p.is_absolute()and '..'not in p.parts and f.resolve()==f and f.is_file()
    return f.read_bytes()

def slots(root):
    if not(Path(root)/INDEX).exists():return {}
    d=json.loads(file_bytes(root,INDEX));assert set(d)=={'format_version','slots'}and d['format_version']=='0.1'and isinstance(d['slots'],dict)
    return d['slots']

def witness(root,entry,chapters):
    ref=entry['proof_ref'];assert set(ref)=={'path','sha256'}and ref['path'].startswith('source-evidence/')
    rb=file_bytes(root,ref['path']);assert hashlib.sha256(rb).hexdigest()==ref['sha256'];proof=json.loads(rb)
    assert proof['format_version']=='0.1'and proof['kind']=='fixed_received_line_unit_life_scopes'and proof['human_reviewed']is False
    c=chapters[entry['chapter_id']];assert all(c.get(k)==v for k,v in proof['chapter_dimensions'].items())
    assert all(c['source'].get(k)==v for k,v in proof['source_fields'].items())
    raw=file_bytes(root,proof['raw_file']['path']);assert hashlib.sha256(raw).hexdigest()==proof['raw_file']['sha256']==c['source']['response_sha256']
    assert c['text_sha256']==proof['text_sha256']==hashlib.sha256('\n\n'.join(p['text']for p in c['paragraphs']).encode()).hexdigest()
    assert [{k:p[k]for k in ('id','text','text_layer','source_position')}for p in c['paragraphs']]==proof['paragraphs']
    assert c['source']['normalization']['selected_source_line_units']==proof['line_units']
    lines=raw.decode('utf-8').splitlines()
    assert len(proof['line_units'])==len(c['paragraphs'])
    for p,u in zip(c['paragraphs'],proof['line_units']):
        assert p['id']==u['id']and p['text']==u['text']and p['text_layer']=='received_chapter'
        assert ''.join(f['selected_text']for f in u['source_fragments'])==p['text']
        for f in u['source_fragments']:
            assert lines[f['line']-1]==f['source_text']and hashlib.sha256(f['source_text'].encode()).hexdigest()==f['source_line_sha256']
            assert f['source_text'][f['source_start']:f['source_end']]==f['selected_text']
    return c,proof

def expected(root,chapters):
    try:from scripts.relative_regnal_year import relative_regnal_year_valid
    except ImportError:from relative_regnal_year import relative_regnal_year_valid
    try:from scripts.subject_continuation import prior_subject_valid
    except ImportError:from subject_continuation import prior_subject_valid
    try:from scripts.chinese_civil_years import numeral
    except ImportError:from chinese_civil_years import numeral
    out={};loaded={}
    for key,entry in slots(root).items():
        assert set(entry)=={'proof_ref','scope_key','event_id','chapter_id','life_record_path','address_record_path'}and entry['scope_key']==key
        stamp=(entry['proof_ref']['path'],entry['proof_ref']['sha256'],entry['chapter_id'])
        if stamp not in loaded:loaded[stamp]=witness(root,entry,chapters)
        c,proof=loaded[stamp];s=proof['scopes'][key];assert s['event_id']==entry['event_id']
        ps={p['id']:p for p in c['paragraphs']};order=list(ps)
        def exact(a):
            p=ps[a['paragraph_id']];assert type(a['start'])is int and type(a['end'])is int and 0<=a['start']<a['end']<=len(p['text'])
            assert p['text'][a['start']:a['end']]==a['surface'];return a
        def person(ref):
            p=ps[ref['paragraph_id']];m,=[m for m in p['mentions']if m['id']==ref.get('person_mention_id',ref.get('mention_id'))]
            assert m.get('kind')=='person'and m.get('person_id')and p['text'][m['start']:m['end']]==m['surface'];return p,m
        _,seed=person(s['subject_seed']);local,topic=person(s['event_subject_reference']);pid=seed['person_id']
        assert seed['start']==0 and topic['start']==0 and topic['person_id']==pid
        date_a=exact(s['date_anchor']);death_a=exact(s['death_anchor']);p=ps[death_a['paragraph_id']]
        assert date_a['paragraph_id']==p['id']and date_a['surface']==s['source_date_expression']and death_a['surface']=='卒'and date_a['end']==death_a['start']
        ids=s['year_scope_paragraph_ids'];chain=s['year_chain'];era=s['era_name'];first,last=s['era_first_year'],s['era_last_year']
        assert ids==order[order.index(chain[0]['anchor']['paragraph_id']):order.index(p['id'])+1]
        assert s['full_paragraphs']==[{'paragraph_id':ps[i]['id'],'quote':ps[i]['text'],'source_position':ps[i]['source_position']}for i in ids]
        assert order.index(s['subject_seed']['paragraph_id'])<=order.index(ids[0])
        assert order.index(ids[0])<=order.index(local['id'])<=order.index(p['id'])
        roles=[]
        hi=death_a['end']if local['id']==p['id']else len(local['text'])
        for m in local['mentions']:
            if m.get('kind')=='person'and topic['start']<=m['start']<hi:
                roles.append({'mention_id':m['id'],'paragraph_id':local['id'],'start':m['start'],'end':m['end'],'surface':m['surface'],'role':'subject'if m['person_id']==pid else'other'})
        assert roles==s['local_roles']
        prior=None
        if local['id']!=p['id']:
            assert s['event_subject_reference'].get('kind')=='prior_paragraph_subject'and order.index(local['id'])+1==order.index(p['id'])
            prior={'kind':'prior_paragraph_subject','paragraph_id':local['id'],'person_mention_id':topic['id'],'quote':local['text'],'intervening_paragraph_ids':[]}
        else:assert topic['end']<=date_a['start']
        previous=None;wanted=[]
        for i,x in enumerate(chain):
            a=exact(x['anchor']);n=x['regnal_year']
            if i==0:
                assert x['kind']=='explicit_era_year'and a['surface'].startswith(era)and a['surface'].endswith('年')and numeral(a['surface'][len(era):-1])==n
                wanted.append((a['paragraph_id'],a['start']+len(era),a['end'],a['surface'][len(era):]))
            else:
                assert (x['kind']=='relative_next_year'and a['surface']=='明年'and n==previous+1)or(x['kind']=='omitted_era_ordinal'and a['surface'].endswith('年')and numeral(a['surface'][:-1])==n and n>previous)
                wanted.append((a['paragraph_id'],a['start'],a['end'],a['surface']))
            previous=n
        assert chain[-1]['anchor']==date_a and chain[-1]['regnal_year']==s['regnal_year']and s['regnal_year']==numeral(s['source_number'])
        actual=[]
        for cid in ids:
            q=ps[cid];lo=chain[0]['anchor']['start']if cid==ids[0]else 0;end=death_a['end']if cid==p['id']else len(q['text'])
            actual.extend((cid,m.start()+lo,m.end()+lo,m.group())for m in re.finditer(r'(?:元|[一二三四五六七八九十百]+)年|明年',q['text'][lo:end]))
        assert actual==wanted
        year=first+s['regnal_year']-1;assert type(first)is int and type(last)is int and first<=year<=last and year==s['resolved_chinese_calendar_year']
        def evidence(q):return {**{k:c[k]for k in ('work_id','book_id','source_id')},'chapter_id':c['id'],'paragraph_id':q['id'],'quote':q['text']}
        ev=evidence(p)
        if prior:ev['context']=prior;assert prior_subject_valid(prior,ev,pid,c)
        else:ev['person_mention_id']=topic['id']
        b={'kind':KIND,'key':key,'proof_ref':entry['proof_ref'],'life_event_id':s['event_id'],'person_id':pid,'subject_status':'contextual_preferred','human_reviewed':False}
        d={'era':'CE','era_year':year,'year':year,'calendar':'chinese_civil','year_numbering':'astronomical','precision':'year','status':'editorial_provisional',
           'source_expression':date_a['surface'],'original_quote':p['text'],'evidence':[evidence(ps[i])for i in ids],'references':[s['year_reference']],
           'regnal_year_mapping':{'kind':'relative_ce_regnal_era_span','era_name':era,'source_number':s['source_number'],'regnal_year':s['regnal_year'],'target_regnal_year':s['regnal_year'],'year_offset':0,'start_ce_year':first,'end_ce_year':last,'reference_index':0},
           'relative_year_reference':{'kind':'omitted_era_regnal_year','source_term':date_a['surface'],'antecedent_expression':date_a['surface'],'era_expression':chain[0]['anchor']['surface'],'era_evidence_index':0,'antecedent_evidence_index':len(ids)-1,'event_evidence_index':len(ids)-1},
           'rationale':'原十二年依同一本傳完整序年承接前文明示年號；數字為編輯判讀，沒有補字入原句、月日或倒算生年。','reviewer':'Codex（AI代理）','human_reviewed':False,'model':None,'event_evidence_binding':b}
        assert relative_regnal_year_valid(d,numeral,chapters)
        event={'id':s['event_id'],'person_id':pid,'event_type':'death','source_term':'卒','source_anchor':death_a,'date_expression':date_a['surface'],'status':'source_attested','evidence':[ev],
               'interpretation_note':'死亡主體依本傳具名主題及固定局部敘事承接；年號省略另欄保留前文，不以卒年結束任何官職，不補卒葬地或生年。','reviewer':'Codex（AI代理）','human_reviewed':False,'model':None,'normalized_date':d}
        age={'id':s['age_id'],'person_id':pid,'value':s['age_value'],'source_number':s['age_number'],'source_term':'時年'+s['age_number'],'source_expression':'時年'+s['age_number'],
             'counting':'unspecified_source_age','birth_year':None,'unit':'source_age_years','status':'source_attested','evidence':[ev],'age_context':{'kind':'at_death','life_event_id':s['event_id']},
             'interpretation_note':'來源報齡，未明計歲方式；不反推出生年。','reviewer':'Codex（AI代理）','human_reviewed':False,'model':None}
        assert p['text'][death_a['end']:].startswith(age['source_term'])and numeral(s['age_number'])==s['age_value']
        origin=None
        if 'origin'in s:
            o=s['origin'];op,om=person(o);oa=exact(o['anchor'])
            assert om['start']==0 and om['person_id']==pid and oa['start']==om['end']and oa['surface']==o['place']+'人'
            oe=evidence(op);oe['person_mention_id']=om['id']
            origin={'id':o['id'],'person_id':pid,'relation':'biographical_origin','place':{'source_name':o['place'],'place_id':None,'modern_identification':None},'source_term':o['source_term'],'source_anchor':oa,'date_expression':None,'status':'source_attested','evidence':[oe],
                    'interpretation_note':'本傳傳首籍貫；不是出生、居處或卒葬地，不把兄弟同族自動擴作同籍貫。','reviewer':'Codex（AI代理）','human_reviewed':False,'model':None}
        out[key]={'chapter_id':c['id'],'event':event,'age':age,'origin':origin}
    return out

def valid(date,event,chapters,parse_number=None,root=None):
    try:
        assert isinstance(date,dict)and isinstance(event,dict)and isinstance(chapters,dict)and root is not None
        b=date['event_evidence_binding'];assert b['kind']==KIND
        row=expected(root,chapters)[b['key']]
        return strict(event,row['event'])and strict(date,row['event']['normalized_date'])
    except(AssertionError,KeyError,ValueError,TypeError,IndexError,StopIteration,AttributeError,OSError):return False

def errors(root,records):
    try:
        if not slots(root):return []
        chs={r['id']:r for r in records if r.get('record_type')=='marked_chapter'}
        wanted=expected(root,chs)
        events=[e for r in records if r.get('record_type')=='person_life_event_assertion_set'for e in r['events']]
        addresses=[a for r in records if r.get('record_type')=='person_address_assertion_set'for a in r['assertions']]
        for key,row in wanted.items():
            actual,=[e for e in events if e.get('id')==row['event']['id']];assert strict(actual,row['event'])
            age,=[a for a in chs[row['chapter_id']]['annotation'].get('age_assertions',[])if a.get('id')==row['age']['id']];assert strict(age,row['age'])
            if row['origin']:
                address,=[a for a in addresses if a.get('id')==row['origin']['id']];assert strict(address,row['origin'])
        return []
    except(AssertionError,KeyError,ValueError,TypeError,IndexError,StopIteration,AttributeError,OSError):
        return ['固定本傳死亡序年須保完整原單元、所有年序與實際主體；省主語不改原字，報齡及籍貫不得漏項、移人或借年']


def native_errors(root,chapters):
    """Native gate before the later full catalog load: read only trusted sidecars."""
    try:
        entries=slots(root)
        if not entries:return []
        paths={e[k]for e in entries.values()for k in ('life_record_path','address_record_path')}
        records=list(chapters.values())+[json.loads(file_bytes(root,p))for p in paths]
        return errors(root,records)
    except(AssertionError,KeyError,ValueError,TypeError,AttributeError,OSError):
        return ['固定本傳生平側表缺失或可信路徑無效']
