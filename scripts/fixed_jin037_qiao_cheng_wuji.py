"""Finite Jin037 Qiao Cheng/Wuji source-role proof; no global surname or PID rule."""
import copy,hashlib,json,re
from pathlib import Path
try:from scripts.fixed_jin073_yuyi_rendered import same,read,expand
except ImportError:from fixed_jin073_yuyi_rendered import same,read,expand
CID='c-jinshu-037-qiao-cheng-wuji-ws2630018'
CH='corpus/jinshu/037-qiao-cheng-wuji-ws2630018.json'
REF='source-evidence/jin037-qiao-cheng-wuji/source-contract.json'
SHA='51ca4049aad4c5902b081bce99a54d2c00a93f094e595c635d492bc5171e080d'
def proof(root,people=None,records=None):
 raw=read(root,REF);assert hashlib.sha256(raw).hexdigest()==SHA;c=json.loads(raw);ch=json.loads(read(root,CH));actual_ch=copy.deepcopy(ch);office_docs={}
 try:from scripts.jin037_qiao_office_reports import installed as office_installed,proof as office_proof
 except ImportError:from jin037_qiao_office_reports import installed as office_installed,proof as office_proof
 if office_installed(root):actual_ch,ch,office_docs,_,_,_=office_proof(root,people=people)
 people=people if people is not None else {p['id']:p for p in json.loads(read(root,'registry/persons.json'))['persons']};roles={}
 assert hashlib.sha256(read(root,c['primary_raw_path'])).hexdigest()==c['primary_raw_sha256']
 for key in ('capture','context','comparison'):assert hashlib.sha256(read(root,c[key+'_path'])).hexdigest()==c[key+'_sha256']
 for role,s in c['role_seeds'].items():
  if s['kind']=='source_local':p,=[p for p in ch['paragraphs']if p['id']==s['paragraph_id']];m,=[m for m in p['mentions']if m['id']==s['mid']];assert m['kind']=='person'and m['source_identity_role']==role
  else:
   source=json.loads(read(root,s['path']));assert source['id']==s['chapter_id']and same(source['source'],s['source']);p,=[p for p in source['paragraphs']if p['id']==s['paragraph_id']];m,=[m for m in p['mentions']if m['id']==s['marker']['id']];assert p['text']==s['quote']and same({k:v for k,v in m.items()if k!='person_id'},s['marker']);assert any(same(e,s['reverse'])for e in people[m['person_id']]['evidence'])
  assert m['person_id']in people;roles['$'+role]=m['person_id']
 assert len(set(roles.values()))==len(roles)
 expected=expand(c['expected_owned'],roles)
 for rel,v in expected.items():assert same(ch if rel==CH else json.loads(read(root,rel)),v)
 assert same(json.loads(read(root,'corpus/jinshu/073-yuyi-ws2296501-rendered-name-components.json')),expand(c['related073_name'],roles))
 seed=c['surname_source'];other=json.loads(read(root,seed['path']));p,=[p for p in other['paragraphs']if p['id']==seed['paragraph_id']];assert p['text']==seed['full_quote']and '姓司馬氏'in p['text'];m,=[m for m in p['mentions']if m['id']==seed['marker']['id']];assert same({k:v for k,v in m.items()if k!='person_id'},seed['marker'])and m['person_id']==roles['$xuandi']
 cap=json.loads(read(root,c['capture_path']));assert len(cap['units'])==len(ch['paragraphs'])
 for p,u in zip(ch['paragraphs'],cap['units']):
  text=re.sub(r'<ref>.*?</ref>','',u['raw_text'],flags=re.S);text=re.sub(r'\{\{YL\|([^}]+)\}\}',r'\1',text);text=text.replace("'''",'');assert text==p['text']
  end=0
  for m in p['mentions']:assert end<=m['start']<m['end']and p['text'][m['start']:m['end']]==m['surface']and m['person_id']==roles['$'+m['source_identity_role']];end=m['end']
 for n in c['negative_verb_spans']:
  p,=[p for p in ch['paragraphs']if p['id']==n['paragraph_id']];assert p['text'][n['start']:n['end']]==n['source_term'];assert not any(m['start']==n['start']for m in p['mentions'])
 reverse={};aliases={};mids={m['id']for p in ch['paragraphs']for m in p['mentions']}
 for p in ch['paragraphs']:
  for m in p['mentions']:
   pid=m['person_id'];reverse.setdefault(pid,[]).append(dict(work_id=ch['work_id'],book_id=ch['book_id'],chapter_id=CID,source_id=ch['source_id'],paragraph_id=p['id'],mention_id=m['id'],quote=m['surface']))
   if 'source_preferred_reading_binding'not in m:aliases.setdefault(pid,{}).setdefault(m['surface'],[]).append(m['id'])
 for pid,a in people.items():
  assert same([e for e in a['evidence']if e.get('chapter_id')==CID],reverse.get(pid,[]));actual={v['surface']:[mid for mid in v['mention_ids']if mid in mids]for v in a['aliases']if any(mid in mids for mid in v['mention_ids'])};assert same(actual,aliases.get(pid,{}))
 assert set(c['family_path_templates'])==set(c['family_roles'])
 for child,father in c['family_roles'].items():
  path=expand(c['family_path_templates'][child],roles);assert path['connection']=='father'and path['parent_person_id']==roles['$'+father]and same(people[roles['$'+child]].get('family_path'),path)
 ledger=c['active_ledger_leaf'];rows=json.loads(read(root,ledger['path']));assert isinstance(rows,list)and rows[55]['entity_id']==ledger['entity_id']and rows[55]['person_id']==roles['$cheng']and same({k:v for k,v in rows[55].items()if k!='person_id'},ledger['unknown_fields_before']);assert hashlib.sha256(read(root,ledger['immutable_before_capture_path'])).hexdigest()==ledger['before_capture_sha256']
 try:from scripts.jin061_two_leaf_current_ledger import proof as two_leaf_proof
 except ImportError:from jin061_two_leaf_current_ledger import proof as two_leaf_proof
 two_leaf_proof(root,people=people,expected_cheng=roles['$cheng'])
 cal=json.loads(read(root,c['calendar_contract']));assert hashlib.sha256(read(root,c['calendar_contract'])).hexdigest()==c['calendar_contract_sha256'];assert hashlib.sha256(read(root,cal['input_path'])).hexdigest()==cal['input_sha256']and cal['normalized_year']==350
 # Additive title batch, independent of the original received contract/SHA.
 try:from scripts.jin037_qiao_title_reports import supplemental
 except ImportError:from jin037_qiao_title_reports import supplemental
 expected.update(supplemental(root,actual_ch,roles))
 expected.update(office_docs)
 expected[CH]=actual_ch
 ch=actual_ch
 if records is not None:
  docs=[d for d in records if isinstance(d,dict)and(d.get('id')==CID or d.get('chapter_id')==CID or d.get('record_type')=='person_name_component_set'and any(n.get('chapter_id')==CID for n in d.get('records',[])))];assert len(docs)==len(expected)and all(sum(same(d,w)for d in docs)==1 for w in expected.values())
 return ch,c,roles,expected
def errors(ch,root):
 try:actual,c,r,w=proof(root);assert same(actual,ch);return []
 except(AssertionError,KeyError,ValueError,TypeError,StopIteration,OSError)as e:return ['晉037譙承無忌選段/姓名/親屬/生卒反查資格不符 ('+type(e).__name__+')']
def guard_bundle(root,pid,people,records):
 path=Path(root)/CH
 if not path.is_file():
  if(Path(root)/REF).exists()or any(d.get('id')==CID or d.get('chapter_id')==CID for d in records):raise ValueError('Jin037 source missing')
  return
 owners={m['person_id']for p in json.loads(path.read_bytes())['paragraphs']for m in p['mentions']}
 # A caller cannot evade the owner by claiming a foreign holder in this sidecar.
 owners.update(h.get('person_id') for d in records if d.get('record_type')=='title_holding_assertion_set' and d.get('chapter_id')==CID for h in d.get('holdings',[]) if isinstance(h,dict))
 if pid in owners:proof(root,people,records)
def validate_surname(n,names,chapters,assertions,root):
 ch,c,r,w=proof(root);expected=w[CH[:-5]+'-name-components.json']['records']+expand(c['related073_name'],r)['records'];assert sum(same(n,x)for x in expected)==1 and any(same(n,x)for x in names)and same(chapters[CID],ch)
 return None
def family_valid(a,root):
 try:ch,c,r,w=proof(root);return any(same(a,x)for x in w[CH[:-5]+'-assertions.json']['assertions'])
 except(AssertionError,KeyError,ValueError,TypeError,StopIteration,OSError):return False
def life_valid(e,ch,root):
 try:actual,c,r,w=proof(root);return same(ch,actual)and any(same(e,x)for x in w[CH[:-5]+'-life-events.json']['events'])
 except(AssertionError,KeyError,ValueError,TypeError,StopIteration,OSError):return False
