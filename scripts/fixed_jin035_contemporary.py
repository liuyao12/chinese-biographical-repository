"""Finite complete-source 035 contemporary successor; first person is never a name."""
from pathlib import Path
import json,hashlib,copy
CASE='source-evidence/jin035-peixiu-peiwei/contemporary-ner-contract.json'
CASE_SHA='d38a50bc1e6897d049136dd6f1c8d7f62dfa4c08ef1a96a230a87c5d43883b4a'
FIRST_PERSON=[{'id': 'c-jinshu-035-peixiu-peiwei:p006:m0079', 'start': 79, 'end': 80, 'surface': '朕', 'paragraph_sha256': 'cc47179e5e3effbf497f31e1366e27daa6470bb91a5cf8b4c9482ed7229542b8', 'source_voice': 'wudi_edict'}, {'id': 'c-jinshu-035-peixiu-peiwei:p011:m0103', 'start': 103, 'end': 104, 'surface': '朕', 'paragraph_sha256': '390cffd611ac0ad04f699aeba831c3ea5c49886f5180c7b651ac71c0c5973650', 'source_voice': 'wudi_death_edict'}, {'id': 'c-jinshu-035-peixiu-peiwei:p012:m0091', 'start': 91, 'end': 92, 'surface': '臣', 'paragraph_sha256': '7b5596d3ddb557d9d9a583cc8c6cb28e7ec1dc275884a3725125f988bbc41580', 'source_voice': 'peixiu_unsubmitted_memorial'}, {'id': 'c-jinshu-035-peixiu-peiwei:p015:m0080', 'start': 80, 'end': 81, 'surface': '吾', 'paragraph_sha256': '67df61ad24a536f6e5c2216f5f306ba12570939fd3c93f4b0a095f3149554fe1', 'source_voice': 'liuyu_question'}, {'id': 'c-jinshu-035-peixiu-peiwei:p019:m0071', 'start': 71, 'end': 72, 'surface': '臣', 'paragraph_sha256': '48daf341c4fb61dd84c8f6224d3eed8d8c10bcbd706bd450406363073f0587c0', 'source_voice': 'peiwei_memorials'}, {'id': 'c-jinshu-035-peixiu-peiwei:p019:m0151', 'start': 151, 'end': 152, 'surface': '臣', 'paragraph_sha256': '48daf341c4fb61dd84c8f6224d3eed8d8c10bcbd706bd450406363073f0587c0', 'source_voice': 'peiwei_memorials'}]

def source_first_person(mention,text=None):
 if not isinstance(mention,dict)or mention.get('kind')!='pronoun'or mention.get('source_reference_owner')!='jin035-contemporary-first-person':return False
 row=next((r for r in FIRST_PERSON if r['id']==mention.get('id')),None)
 if row is None or any(mention.get(k)!=row[k]for k in ('id','start','end','surface','source_voice')):return False
 return text is None or hashlib.sha256(text.encode()).hexdigest()==row['paragraph_sha256']

def same(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 return a==b

def validate_successor(root):
 root=Path(root).resolve();read=lambda rel:json.loads((root/rel).read_text());raw=(root/CASE).read_bytes();assert hashlib.sha256(raw).hexdigest()==CASE_SHA;case=json.loads(raw)
 assert hashlib.sha256((root/case['parent_contract_path']).read_bytes()).hexdigest()==case['parent_contract_sha256']
 ch=read(case['chapter_path']);people={p['id']:p for p in read('registry/persons.json')['persons']};roles={}
 for key,s in case['known_seeds'].items():
  d=read(s['chapter_path']);assert same(d['source'],s['source'])and same({k:d[k]for k in s['dimensions']},s['dimensions'])
  p=next(p for p in d['paragraphs']if p['id']==s['paragraph_id']);m=next(m for m in p['mentions']if m['id']==s['marker']['id']);assert p['text']==s['quote']and same({k:v for k,v in m.items()if k!='person_id'},s['marker'])
  pid=m['person_id'];assert m['kind']=='person'and pid in people;roles['$'+key]=pid;assert [e for e in people[pid]['evidence']if e.get('mention_id')==m['id']]==[s['reverse']];assert any(a['surface']==m['surface']and m['id']in a['mention_ids']for a in people[pid]['aliases'])
 def expand(x):
  if isinstance(x,str):return roles.get(x,x)
  if isinstance(x,list):return[expand(v)for v in x]
  if isinstance(x,dict):return{k:expand(v)for k,v in x.items()}
  return x
 assert same(ch,expand(case['chapter_template']));sidecars={rel:expand(t)for rel,t in case['sidecars'].items()}
 for rel,t in sidecars.items():assert same(read(rel),t)
 added=set(case['new_marker_ids']);assert len(added)==119
 counts={'person':0,'pronoun':0,'unresolved':0}
 for p in ch['paragraphs']:
  for m in p['mentions']:
   if m['id']not in added:continue
   counts[m['kind']]+=1;assert p['text'][m['start']:m['end']]==m['surface']
   if m['kind']=='unresolved':assert m['surface']=='遺孤'and m['person_id']is None and all(pid in people for pid in m['candidate_person_ids']);continue
   person=people[m['person_id']];e={k:ch[k]for k in ('work_id','book_id','source_id')};e.update(chapter_id=ch['id'],paragraph_id=p['id'],mention_id=m['id'],quote=m['surface']);assert [x for x in person['evidence']if x.get('mention_id')==m['id']]==[e]
   if m['kind']=='pronoun':
    assert source_first_person(m,p['text']);assert not any(m['id']in a['mention_ids']for v in people.values()for a in v['aliases'])
   else:assert any(a['surface']==m['surface']and m['id']in a['mention_ids']for a in person['aliases'])
 assert counts=={'person':112,'pronoun':6,'unresolved':1}
 old=copy.deepcopy(ch);old['annotation']=expand(case['parent_annotation'])
 for p in old['paragraphs']:p['mentions']=[m for m in p['mentions']if m['id']not in added];p['annotation_status']=case['parent_paragraph_annotation_status'][p['id']]
 assert {m['id']for p in old['paragraphs']for m in p['mentions']}==set(case['preserved_parent_marker_ids'])
 return {'chapter':ch,'parent_chapter':old,'sidecars':sidecars,'case':case}
