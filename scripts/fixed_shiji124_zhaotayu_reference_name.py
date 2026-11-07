"""One listed source-reference name parse; no generic surname or identity inference."""
from pathlib import Path
import json,hashlib
try:from scripts.validation_context import memoized
except ImportError:from validation_context import memoized
CID='c-shiji-124-youxia';CP='corpus/shiji/124.json';CASE='source-evidence/shiji124-zhaotayu/name-parse-contract.json';CASE_SHA='0dc88605d14462a7e70b05270e1514e56ad5cb26c82206e0a0f3db54983f8c93'
KIND='fixed_shiji124_suoyin_reference_name_parse';NAME='name-shiji124-zhaotayu-reference';DID='d-shiji124-zhaotayu-editorial-name-parse';RETIRED='fdm_96x_l9b'
NP='corpus/shiji/124-zhaotayu-names.json';IP='corpus/shiji/124-zhaotayu-identities.json';AP='corpus/shiji/124-addresses.json';RP='source-evidence/shiji124-zhaotayu/reference-units.json';RET='source-evidence/shiji124-zhaotayu/retirement-source-person.json'
def need(ok,msg):
 if not ok:raise ValueError('史記124釋名：'+msg)
def load(root,p):return json.loads((Path(root)/p).read_text())
def same(a,b):return json.dumps(a,ensure_ascii=False,sort_keys=True)==json.dumps(b,ensure_ascii=False,sort_keys=True)
def material(x,pid):
 if isinstance(x,dict):return{k:material(v,pid)for k,v in x.items()}
 if isinstance(x,list):return[material(v,pid)for v in x]
 return pid if x=='$person'else x
@memoized(0)
def target(root):
 c=load(root,CP);p=next(p for p in c['paragraphs']if p['id']==CID+':p015');m=next(m for m in p['mentions']if m['id']==CID+':m015-0096');return m['person_id']
@memoized(0)
def state(root):
 raw=(Path(root)/CASE).read_bytes();need(hashlib.sha256(raw).hexdigest()==CASE_SHA,'完整契約SHA');case=json.loads(raw);ch=load(root,CP);need(all(same(ch.get(k),v)for k,v in case['chapter_header'].items()),'來源metadata/原章資格')
 frame=[{k:p.get(k)for k in('id','text','annotation_status','text_layer')}|{'mentions':[{k:m.get(k)for k in('id','start','end','surface','kind','status')}for m in p['mentions']]}for p in ch['paragraphs']];need(same(frame,case['physical_source_frames']),'全17段原字/標點/MID/字位/kind')
 pid=target(root);need(isinstance(pid,str)and pid!=RETIRED,'現役owner');p=next(p for p in ch['paragraphs']if p['id']==CID+':p015')
 for a in material(case['target_markers'],pid):need(a in p['mentions']and p['text'][a['start']:a['end']]==a['surface'],'兩原錨同人/字位')
 need(p['text'][96:102]=='趙他、羽公子','原有頓號不改')
 people={x['id']:x for x in load(root,'registry/persons.json')['persons']};need(pid in people and RETIRED not in people,'current registry/撤號');person=people[pid];need(all(same(person.get(k),v)for k,v in case['keeper_qualification'].items()),'keeper來源資格/姓名')
 for a in case['target_markers']:
  need(any(x['surface']==a['surface']and a['id']in x['mention_ids']for x in person['aliases']),'原surface反查')
  need(any(x['mention_id']==a['id']and x['chapter_id']==CID and x['paragraph_id']==p['id']and x['quote']==a['surface']for x in person['evidence']),'原MID證據反查')
 docs={path:load(root,path)for path in(NP,IP,RP)}
 for path,expected in case['document_templates'].items():need(same(docs[path],material(expected,pid)),'來源/name/身份完整row與資格：'+path)
 reference=(Path(root)/RP).read_bytes();need(hashlib.sha256(reference).hexdigest()==case['reference_sha256'],'兩參考完整單元/資格SHA')
 ads=load(root,AP);selected=[a for a in ads['assertions']if a['id']in case['address_ids']];need(same(selected,material(case['address_templates'],pid)),'兩東道記錄不可刪/改quote/偷換主體')
 receipt=load(root,RET);need(same(receipt,{'record_type':'editorial_annotation_rekey_receipt','identity_decision_id':DID,'retired_person_ids':[RETIRED],'retirement_policy':'audit_only_not_canonical_not_alias_not_reusable','person_aliases_created':False}),'精確退休receipt')
 return ch,pid,case,docs

def component_valid(n,ch,root):
 try:
  actual,pid,c,docs=state(root);need(same(ch,actual),'caller完整current章');need(same(n,docs[NP]['records'][0]),'唯一reference姓名row');return True
 except(ValueError,KeyError,TypeError,OSError,StopIteration):return False

def catalog_valid(root,people,records):
 ch,pid,c,docs=state(root);need(pid in people,'caller keeper');actual=next(x for x in load(root,'registry/persons.json')['persons']if x['id']==pid);need(same(people[pid],actual),'caller完整人物主檔')
 for path,doc in docs.items():
  if path==RP:continue
  need(sum(same(x,doc)for x in records)==1,'caller catalog缺/換具名sidecar：'+path)
 need(sum(x.get('record_type')=='marked_chapter'and x.get('id')==CID and same(x,ch)for x in records)==1,'caller缺/換完整章')
 ads=[a for d in records if d.get('record_type')=='person_address_assertion_set'for a in d.get('assertions',[])if a.get('id')in c['address_ids']];need(same(ads,material(c['address_templates'],pid)),'caller缺兩地望')
 return True

def guard_bundle(root,person_id,people,records):
 if not(Path(root)/CASE).exists():
  if(Path(root)/RET).exists():raise ValueError('史記124釋名owner契約遺漏')
  return
 if person_id==target(root):catalog_valid(root,people,records)

def same_source_retirement_valid(root,decision,ids):
 try:
  _,pid,c,docs=state(root);need(ids==[RETIRED]and same(decision,docs[IP]['decisions'][0]),'samechapter退休owner/DID');return True
 except(ValueError,KeyError,TypeError,OSError,StopIteration):return False

def errors(root,chapters):
 if not(Path(root)/CASE).exists():return ['史記124釋名owner契約遺漏']if(Path(root)/RET).exists()else[]
 try:
  actual,_,_,_=state(root);need(same(chapters.get(CID),actual),'validator完整current章');return[]
 except(ValueError,KeyError,TypeError,OSError,StopIteration)as e:return[str(e)]
