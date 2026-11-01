"""One received title batch and qualified external grant-year bridge.

Judgements are offline editorial data, not automatic historical proof. Current
people derive from stable source MIDs; raw/capture qualification stays separate.
"""
import copy,hashlib,json
from pathlib import Path
CH='corpus/jinshu/037-qiao-cheng-wuji-ws2630018.json'
REF='source-evidence/jin037-qiao-cheng-wuji/title-reading-contract.json'
SHA='bf7d9aa199182a646c3413c4b3aa7140deba0180b3a61f708c971f8d33f797fd'

def same(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 return a==b

def _loader(root):
 root=Path(root).resolve()
 def raw(rel):
  p=Path(rel);assert not p.is_absolute()and'..'not in p.parts;q=root/p;assert q.resolve()==q and q.is_file();return q.read_bytes()
 return raw

def _proof(raw,chapter=None,people=None):
 b=raw(REF);assert hashlib.sha256(b).hexdigest()==SHA;c=json.loads(b);load=lambda p:json.loads(raw(p));ch=load(CH)
 if chapter is not None:assert same(chapter,ch)
 assert all(ch[k]==v for k,v in c['dimensions'].items())and same(ch['source'],c['source_metadata'])
 assert {p['id']:hashlib.sha256(p['text'].encode()).hexdigest()for p in ch['paragraphs']}==c['paragraph_hashes']
 if people is None:people={p['id']:p for p in load('registry/persons.json')['persons']}
 ps={p['id']:p for p in ch['paragraphs']};ms={m['id']:(p,m)for p in ch['paragraphs']for m in p['mentions']};roles={}
 for role,seed in c['role_seeds'].items():
  p,m=ms[seed['marker']['id']];assert p['id']==seed['paragraph_id']and same({k:v for k,v in m.items()if k!='person_id'},seed['marker'])and m['kind']=='person'
  assert p['text'][m['start']:m['end']]==m['surface'];pid=m['person_id'];assert pid in people;actor=people[pid]
  assert [e for e in actor['evidence']if e.get('mention_id')==m['id']]==[seed['reverse']]
  assert [(a['surface'],mid)for a in actor['aliases']for mid in a['mention_ids']if mid==m['id']]==[(m['surface'],m['id'])];roles['$'+role]=pid
 assert len(set(roles.values()))==len(roles)
 def expand(v):
  if isinstance(v,str):return roles.get(v,v)
  if isinstance(v,list):return[expand(x)for x in v]
  if isinstance(v,dict):return{k:expand(x)for k,x in v.items()}
  return v
 expected=expand(c['title_template']);assert same(load(c['title_path']),expected)
 assertions=load(c['father_assertion_path'])['assertions']
 for want in expand(c['father_templates']):assert sum(same(x,want)for x in assertions)==1
 bridgeb=raw(c['bridge_path']);assert hashlib.sha256(bridgeb).hexdigest()==c['bridge_sha256'];bridge=json.loads(bridgeb)
 obb=raw(bridge['observation_path']);fb=raw(bridge['footer_path']);assert hashlib.sha256(obb).hexdigest()==bridge['observation_sha256']and hashlib.sha256(fb).hexdigest()==bridge['footer_sha256']
 ob=json.loads(obb);foot=json.loads(fb);qual=bridge['qualification']
 assert same(ob['qualification'],qual)and same(foot['qualification'],qual)
 assert qual==dict(acquisition='current_rendered_reference_only',reported_revision=2603564,fixed_body_obtained=False,original_wikitext_obtained=False,actual_print_edition=None,image_verified=False,human_reviewed=False)
 assert str(qual['reported_revision'])in foot['reported_permalink']and foot['reported_permalink']in foot['text']
 units=ob['units'];assert [u['tool_line']for u in units]==[163,164]
 for u in units:assert hashlib.sha256(u['text'].encode()).hexdigest()==u['text_sha256']
 first,award=[u['text']for u in units];assert bridge['year_expression']in first and'升壇受禪'in first and award.lstrip().startswith('丁卯')
 deriv=bridge['plain_year_quote_derivation'];assert deriv['source_observation_path']==bridge['observation_path']and deriv['source_observation_sha256']==bridge['observation_sha256']and deriv['tool_line']==163
 received=first[deriv['source_start']:deriv['source_end']];assert received==deriv['source_slice']
 edit,=deriv['edits'];assert edit==dict(start=0,end=len('【72†泰始元年】'),received='【72†泰始元年】',replacement='泰始元年',kind='tool_hyperlink_wrapper_only')and received.startswith(edit['received'])
 plain=edit['replacement']+received[edit['end']:];assert plain==deriv['plain_quote']=='泰始元年冬十二月丙寅，設壇于南郊'
 span=bridge['external_subject_grant_span_L164'];assert award[span['start']:span['end']]==span['surface']
 h,=[h for h in expected['holdings']if h['id']==bridge['native_holding_id']];assert h['person_id']==roles['$xun']and h['kind']=='noble_rank'and h['mode']=='grant'and span['surface'].endswith('爲'+h['title'])
 nd=h['effective_period']['start']['normalized_date'];assert nd['original_quote']==plain and nd['references'][0]['quote']==plain and nd['references'][0]['separate_grant_quote']==span['surface']and nd['references'][0]['quote_derivation_bridge']==c['bridge_path']
 localp,localm=ms[bridge['native_subject_mid']];assert localm['person_id']==h['person_id']and localm['id']==c['role_seeds']['xun']['marker']['id']
 a=bridge['native_grant_span'];assert a['paragraph_id']==localp['id']and localp['text'][a['start']:a['end']]==a['surface']and'封'+h['title']in a['surface']
 cal=bridge['calendar'];calraw=raw(cal['path']);assert hashlib.sha256(calraw).hexdigest()==cal['sha256']and cal['raw_row']in calraw.decode()
 assert cal['row_id']=='av474'and cal['era_name']=='泰始'and cal['polity']=='西晉'and(cal['first_ce_chinese_year'],cal['last_ce_chinese_year'])==(265,274)
 assert cal['regnal_number']=='元'and cal['regnal_year']==1 and cal['normalized_chinese_civil_year']==cal['first_ce_chinese_year']+cal['regnal_year']-1
 return ch,c,roles,expected

def source_record(root,chapter=None,roles=None):
 ch,c,r,record=_proof(_loader(root),chapter)
 if roles is not None:
  # Base owner's differently named role keys are not a PID whitelist.
  assert set(r.values()).issubset(set(roles.values()))
 return record

def supplemental(root,chapter,roles):
 if not(Path(root)/REF).exists():return{}
 record=source_record(root,chapter) # ownership independently derives native MIDs
 return {json.loads(_loader(root)(REF))['title_path']:record}

def errors(root):
 if not(Path(root)/REF).exists():
  return ['Qiao titles require their finite source contract']if(Path(root)/(CH[:-5]+'-titles.json')).exists()else[]
 try:_proof(_loader(root));return[]
 except(AssertionError,KeyError,ValueError,TypeError,OSError,IndexError,StopIteration):return ['Qiao received titles/source roles/qualified265 grant reference differ']

def _date_valid(raw,date,holding,endpoint,chapters,root=None):
 try:
  assert isinstance(date,dict)and isinstance(holding,dict)and endpoint=='start'
  ch,c,r,record=_proof(raw);assert same(chapters[ch['id']],ch)
  expected,=[h for h in record['holdings']if h['id']==date['qiao_parallel_grant_year_binding']['holding_id']]
  assert same(holding,expected)and same(date,expected['effective_period']['start']['normalized_date'])
  assert holding['person_id']==r['$xun']and holding['title']=='譙王'and holding['mode']=='grant'
  assert all(k not in date for k in ('month','day'))and date['human_reviewed']is False and date['precision']=='year'
  # Reuse ordinary metadata/CE regnal arithmetic; only external-event anchoring
  # above is new. Removing this binding prevents recursive dispatch.
  plain=copy.deepcopy(date);plain.pop('qiao_parallel_grant_year_binding')
  try:from scripts.validate_corpus import normalized_date_errors
  except ImportError:from validate_corpus import normalized_date_errors
  return not normalized_date_errors(plain,chapters,root,holding,endpoint)
 except(AssertionError,KeyError,ValueError,TypeError,OSError,IndexError,StopIteration):return False

def date_valid(date,holding,endpoint,chapters,root):
 return _date_valid(_loader(root),date,holding,endpoint,chapters,root)
