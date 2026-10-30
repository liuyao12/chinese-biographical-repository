"""Named minimal life/origin phase on the complete received Jin034 witness."""
from pathlib import Path
import copy,json
try:
 from scripts import fixed_jin034_yanghu_ner as core
except ImportError:
 import fixed_jin034_yanghu_ner as core
EP=core.BASE+'minimal-life-phase.json'
LP='corpus/jinshu/034-yanghu-comparison-life-events.json'
AP='corpus/jinshu/034-yanghu-comparison-addresses.json'
REF='fixed_jin034_minimal_life_ref'
PROOF_SHA='e66d58d35b6ddf3ee6e55f9cdb93a03d18304cc380f7d150910b87a49cbffbb7'
def active(root):
 exists=(Path(root)/EP).is_file()
 ch=core.read(root,core.CH)
 orphan=REF in ch.get('annotation',{})or(Path(root)/LP).exists()or(Path(root)/AP).exists()or any(x.get('id')=='age-jin034-yanghu-death58'for x in ch.get('annotation',{}).get('age_assertions',[]))
 core.need(exists or not orphan,'minimal-life orphan/缺stage')
 return exists
def proof(root):
 raw=core.path(root,EP).read_bytes();core.need(core.H(raw)==PROOF_SHA,'minimal-life phase SHA');return json.loads(raw)
def effective(parent,root):
 if not active(root):return parent
 b=proof(root);core.need(core.H(core.path(root,core.EP).read_bytes())==b['parent_ner_sha256'],'minimal-life NER前置')
 core.need(core.H(core.path(root,core.BASE+'close-kin-phase.json').read_bytes())==b['parent_close_kin_sha256'],'minimal-life 27kin/6reports前置')
 out=copy.deepcopy(parent);ann=out['chapter_template']['annotation']
 for k,v in b['annotation_additions'].items():
  if k=='age_assertions':
   prior=ann.get(k,[]);core.need(not any(x.get('id')==v[0]['id']for x in prior),'minimal-life age ID衝突');ann[k]=copy.deepcopy(prior)+copy.deepcopy(v)
  else:core.need(k not in ann,'minimal-life annotation衝突');ann[k]=copy.deepcopy(v)
 return out
def documents(root,r,ch):
 if not active(root):return None
 b=proof(root);core.need(ch['annotation'].get(REF)==EP,'minimal-life active ref')
 # Stable paragraph IDs, never narrative list indices. Exact whole paragraphs and source metadata remain bound.
 for s in b['source_units']:
  p,=[p for p in ch['paragraphs']if p['id']==s['paragraph_id']]
  core.need(core.H(p['text'].encode())==s['text_sha256']and core.same({k:v for k,v in p.items()if k!='mentions'},s['paragraph_without_mentions']),'minimal-life完整原段/層/資格')
  for a in s['subject_anchors']:
   m,=[m for m in p['mentions']if m['id']==a['id']]
   core.need(core.same({k:v for k,v in m.items()if k!='person_id'},a)and m.get('person_id')==r['yang_hu'],'minimal-life同人完整MID/字位')
 for rel,t in b['expected_documents'].items():core.need(core.same(core.read(root,rel),core.expand(t,r)),'minimal-life側車缺/額外/換人/假日期 '+rel)
 expected_age=core.expand(b['annotation_additions']['age_assertions'][0],r)
 core.need(sum(core.same(x,expected_age)for x in ch['annotation'].get('age_assertions',[]))==1,'minimal-life報齡/出生年/日期')
 return b
def guard_bundle(root,pid,people,records,r,actual,ch):
 if not active(root):return
 b=documents(root,r,ch)
 core.need(isinstance(people,dict)and isinstance(records,list),'minimal-life caller types')
 for role_pid,person in actual.items():core.need(core.same(people.get(role_pid),person),'minimal-life caller完整人物/反查')
 core.need(core.same([x for x in records if x.get('id')==core.CID],[ch]),'minimal-life caller完整章/age')
 for rel,t in b['expected_documents'].items():
  expected=core.expand(t,r)
  got=[x for x in records if x.get('record_type')==expected['record_type']and x.get('chapter_id')==core.CID]
  core.need(core.same(got,[expected]),'minimal-life caller缺stage sidecar/換引文')
