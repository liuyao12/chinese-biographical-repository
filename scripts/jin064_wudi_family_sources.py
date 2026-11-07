"""Finite Jin064 source-role reading. No permanent person-ID identity whitelist.
Editorial judgments are not primary authority; capture bytes and current role endpoints
are checked separately. Only declared source-owned semantic leaves may rekey coherently.
"""
from pathlib import Path
import json,hashlib
try:from scripts.received_sima_family_sources import same,_caller_reverse_claim
except ImportError:from received_sima_family_sources import same,_caller_reverse_claim
REF='source-evidence/sima-family-source-bridges/jin064-source-contract.json'
SHA='404e8b3dc0523aaf8fef51fff082cb32a9a8d8d79a8722696e3fe3920c475d59'
CID='c-jinshu-064-wudi-sons-rendered'
OWNED=('corpus/jinshu/064-wudi-sons-rendered.json', 'corpus/jinshu/064-wudi-sons-name-components.json', 'corpus/jinshu/064-wudi-sons-assertions.json', 'corpus/jinshu/064-wudi-sons-rendered.xml', 'source-evidence/sima-family-source-bridges/jin064-received-units.json', 'source-evidence/sima-family-source-bridges/jin064-han-aidi-primary-reference.json', 'corpus/jinshu/064-wudi-sons-life-events.json', 'corpus/jinshu/064-wudi-sons-titles.json')
PRONOUN_RULES={'c-jinshu-064-wudi-sons-rendered:p003:m0082': {'start': 82, 'end': 83, 'surface': '之', 'source_role': 'jian_wudi_son', 'voice': 'reported_object_pronoun', 'source_reference_binding': {'kind': 'received_sima_family_pronoun', 'paragraph_id': 'c-jinshu-064-wudi-sons-rendered:p003', 'paragraph_sha256': 'f054cfed9a3a920654d45b024236d0d26b4282b705c0df33264c7b18c10b3e57', 'role': 'jian_wudi_son'}}, 'c-jinshu-064-wudi-sons-rendered:p005:m0015': {'start': 15, 'end': 16, 'surface': '之', 'source_role': 'jian_wudi_son', 'voice': 'reported_object_pronoun', 'source_reference_binding': {'kind': 'received_sima_family_pronoun', 'paragraph_id': 'c-jinshu-064-wudi-sons-rendered:p005', 'paragraph_sha256': '08827b2cbecc38d305ef40290f0e8f49ea592cc0ae2d748293cf1c73b201ee20', 'role': 'jian_wudi_son'}}, 'c-jinshu-064-wudi-sons-rendered:p013:m0021': {'start': 21, 'end': 22, 'surface': '之', 'source_role': 'xia', 'voice': 'reported_object_pronoun', 'source_reference_binding': {'kind': 'received_sima_family_pronoun', 'paragraph_id': 'c-jinshu-064-wudi-sons-rendered:p013', 'paragraph_sha256': '4af6d74e29cb89314d98d00e688e4b132dfe52d95a974b33f3c6a0b4c86aec55', 'role': 'xia'}}, 'c-jinshu-064-wudi-sons-rendered:p019:m0061': {'start': 61, 'end': 62, 'surface': '之', 'source_role': 'yan', 'voice': 'reported_object_pronoun', 'source_reference_binding': {'kind': 'received_sima_family_pronoun', 'paragraph_id': 'c-jinshu-064-wudi-sons-rendered:p019', 'paragraph_sha256': '56ea2e8b9b99e870847957873dc0726bb5ee05318dd109149691e3063a91cb95', 'role': 'yan'}}, 'c-jinshu-064-wudi-sons-rendered:p010:m0104': {'start': 104, 'end': 105, 'surface': '臣', 'source_role': 'jiong', 'voice': 'quoted_speaker_first_person', 'source_reference_binding': {'kind': 'received_sima_family_pronoun', 'paragraph_id': 'c-jinshu-064-wudi-sons-rendered:p010', 'paragraph_sha256': '1f4e1658deb5dc0c632573fae688e3f0d35a68148ccefb4f84f577b92993c99d', 'role': 'jiong'}}}
def _raw(root,p):
 root=Path(root).resolve();rel=Path(p);assert not rel.is_absolute()and'..'not in rel.parts;f=root/rel;assert f.resolve()==f;return f.read_bytes()
def installed(root):return any((Path(root)/p).exists()for p in OWNED)
def source_reference(m,text=None):
 if not isinstance(m,dict):return False
 w=PRONOUN_RULES.get(m.get('id'))
 return bool(w and m.get('kind')=='pronoun'and m.get('status')=='contextual_provisional'and isinstance(m.get('person_id'),str)and bool(m['person_id'])and all(same(m.get(k),v)for k,v in w.items())and(text is None or hashlib.sha256(text.encode()).hexdigest()==w['source_reference_binding']['paragraph_sha256']))
def _proof(raw,people=None,records=None):
 cb=raw(REF);assert hashlib.sha256(cb).hexdigest()==SHA;c=json.loads(cb);load=lambda p:json.loads(raw(p));ch=load(c['chapter_path']);ms={m['id']:(p,m)for p in ch['paragraphs']for m in p['mentions']}
 if people is None:people={p['id']:p for p in load('registry/persons.json')['persons']}
 roles={}
 for r,mids in c['role_current_mids'].items():
  proper=[ms[mid][1]for mid in mids if ms[mid][1]['kind']=='person'];assert proper;pid=proper[0]['person_id'];assert pid in people and all(ms[mid][1]['person_id']==pid for mid in mids);roles[r]=pid
 for r,b in c['new_role_identity_bindings'].items():assert same([x for x in people[roles[r]].get('source_identity_bindings',[])if x.get('chapter_id')==CID and x.get('source_role')==r],[b])
 allowed={frozenset(v)for v in c['allowed_possible_same_role_pairs']}
 rs=list(roles)
 for i,r in enumerate(rs):
  for s in rs[i+1:]:assert roles[r]!=roles[s]or frozenset((r,s))in allowed
 for r,s in c['role_seeds'].items():
  q=load(s['chapter_path']);p=next(p for p in q['paragraphs']if p['id']==s['paragraph_id']);m=next(m for m in p['mentions']if m['id']==s['marker']['id']);assert hashlib.sha256(p['text'].encode()).hexdigest()==s['paragraph_sha256']and same({k:v for k,v in m.items()if k!='person_id'},s['marker'])and m['person_id']==roles[r];assert same([e for e in people[roles[r]]['evidence']if e.get('mention_id')==m['id']],[s['reverse']])
 try:from scripts.jin002_004_imperial_openings import _proof as imperial_proof
 except ImportError:from jin002_004_imperial_openings import _proof as imperial_proof
 _,imperial_roles,_=imperial_proof(raw,people)
 assert all(roles[r]==imperial_roles['$'+s]for r,s in c['imperial_role_bridge'].items())
 def expand(x):
  if isinstance(x,str)and x.startswith('@person:'):return roles[x[8:]]
  if isinstance(x,list):return[expand(v)for v in x]
  if isinstance(x,dict):return{k:expand(v)for k,v in x.items()}
  return x
 expected={p:expand(v)for p,v in c['expected_documents'].items()}
 for p,v in expected.items():assert same(load(p),v)
 for path,key in[(c['capture_path'],'capture_sha256'),(c['primary_reference_path'],'primary_reference_sha256')]:assert hashlib.sha256(raw(path)).hexdigest()==c[key]
 cap=load(c['capture_path']);assert len(cap['units'])==len(ch['paragraphs'])and all(p['text']==u['received_text']and p['source_position']['tool_line']==u['tool_line']for p,u in zip(ch['paragraphs'],cap['units']))
 assert ch['text_sha256']==hashlib.sha256('\n\n'.join(p['text']for p in ch['paragraphs']).encode()).hexdigest()
 for r,mids in c['role_current_mids'].items():
  person=people[roles[r]]
  for mid in mids:
   p,m=ms[mid];assert p['text'][m['start']:m['end']]==m['surface'];e={'work_id':ch['work_id'],'book_id':ch['book_id'],'source_id':ch['source_id'],'chapter_id':ch['id'],'paragraph_id':p['id'],'mention_id':mid,'quote':m['surface']};assert same([x for x in person['evidence']if x.get('mention_id')==mid],[e]);aliases=[a for a in person['aliases']if mid in a.get('mention_ids',[])]
   if m['kind']=='pronoun':assert not aliases and source_reference(m,p['text'])
   else:assert len(aliases)==1 and aliases[0]['surface']==m['surface']
 if records is not None:
  selected=[d for d in records if related(d,c)];assert len(selected)==len(expected)and all(sum(same(d,v)for d in selected)==1 for v in expected.values())
 return c,roles,expected
def proof(root,people=None,records=None):return _proof(lambda p:_raw(root,p),people,records)
def related(d,c=None):
 if not isinstance(d,dict):return False
 return d.get('id')==CID or d.get('chapter_id')==CID or d.get('record_type')=='person_name_component_set'and any(isinstance(n,dict)and n.get('chapter_id')==CID for n in d.get('records',[]))or any(isinstance(m,dict)and isinstance(m.get('id'),str)and m['id'].startswith(CID+':')for p in d.get('paragraphs',[])if isinstance(p,dict)for m in p.get('mentions',[]))
def errors(root):
 if not(Path(root)/REF).exists():return['064來源或側錄已安裝但缺所屬contract']if installed(root)else[]
 try:proof(root);return[]
 except(AssertionError,KeyError,ValueError,TypeError,OSError,StopIteration):return['064接收原字/姓名字/明父母收繼/代詞反查或取得資格不符']
def guard_bundle(root,pid,people,records):
 if not(Path(root)/REF).exists():
  if installed(root)or any(related(d)for d in(records or[]))or _caller_reverse_claim(people,pid,CID):raise ValueError('Jin064 source/caller installed without contract')
  return
 cb=_raw(root,REF)
 if hashlib.sha256(cb).hexdigest()!=SHA:raise ValueError('Jin064 source contract checksum mismatch')
 c=json.loads(cb);physical=[json.loads(_raw(root,p))for p in c['expected_documents']];selected=[d for d in(records or[])if related(d)]
 def owners(ds):
  out=set()
  def visit(x,key=None):
   if isinstance(x,dict):
    for k,v in x.items():visit(v,k)
   elif isinstance(x,list):
    for v in x:visit(v,key)
   elif key in('person_id','subject_person_id','object_person_id')and isinstance(x,str):out.add(x)
  visit(ds);return out
 physical_owners=owners(physical);caller_owners=owners(selected)
 reverse_mids={mid for group in c['role_current_mids'].values()for mid in group}
 caller_reverse_claim=_caller_reverse_claim(people,pid,CID,reverse_mids)
 if pid not in physical_owners|caller_owners and not caller_reverse_claim:return
 if pid not in physical_owners or len(selected)!=len(physical)or any(sum(same(d,want)for d in selected)!=1 for want in physical):raise ValueError('Jin064 caller/physical catalogue mismatch')
 proof(root,people,records)
def applies(a):return isinstance(a,dict)and isinstance(a.get('qualifiers'),dict)and isinstance(a['qualifiers'].get('source_clause_binding'),dict)and a['qualifiers']['source_clause_binding'].get('source_scope')==CID
def family_valid(a,root):
 try:_,_,e=proof(root);return any(same(a,x)for d in e.values()if d.get('record_type')=='person_assertion_set'for x in d['assertions'])
 except(AssertionError,KeyError,ValueError,TypeError,OSError,StopIteration):return False
def validate_surname(n,names,chapters,assertions,root):
 _,_,e=proof(root);assert any(same(n,x)for d in e.values()if d.get('record_type')=='person_name_component_set'for x in d['records']);return None
