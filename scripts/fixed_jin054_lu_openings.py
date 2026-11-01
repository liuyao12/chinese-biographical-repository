# coding: utf-8
"""Three received Jin054 short units, mutable source roles and closed local references."""
import json,hashlib,re
from pathlib import Path
REF='source-evidence/jin054-lu-openings/source-native-contract.json'
SHA='13a938721f2895f2c61a614cad81d712035401e494c0b2effe57ceec5756d144'
CID='c-jinshu-054-lu-openings-ws2605147'
CH='corpus/jinshu/054-lu-openings-ws2605147.json'
PRONOUNS={'c-jinshu-054-lu-openings-ws2605147:p001:m0035': {'id': 'c-jinshu-054-lu-openings-ws2605147:p001:m0035', 'start': 35, 'end': 36, 'surface': '其', 'kind': 'pronoun', 'status': 'resolved_contextual', 'source_role': 'ji', 'interpretation_note': '來源詞與發話角色限定；非姓名，不進姓名aliases。', 'source_reference_binding': {'kind': 'fixed_jin054_local_reference', 'contract_ref': 'source-evidence/jin054-lu-openings/source-native-contract.json', 'role_key': 'ji', 'paragraph_sha256': '5c268becc06e3102a128f1a0cac5992d0eb2625f7b4990ccef095898b20ec0c5'}}, 'c-jinshu-054-lu-openings-ws2605147:p001:m0064': {'id': 'c-jinshu-054-lu-openings-ws2605147:p001:m0064', 'start': 64, 'end': 65, 'surface': '父', 'kind': 'pronoun', 'status': 'resolved_contextual', 'source_role': 'kang', 'interpretation_note': '來源詞與發話角色限定；非姓名，不進姓名aliases。', 'source_reference_binding': {'kind': 'fixed_jin054_local_reference', 'contract_ref': 'source-evidence/jin054-lu-openings/source-native-contract.json', 'role_key': 'kang', 'paragraph_sha256': '5c268becc06e3102a128f1a0cac5992d0eb2625f7b4990ccef095898b20ec0c5'}}, 'c-jinshu-054-lu-openings-ws2605147:p001:m0138': {'id': 'c-jinshu-054-lu-openings-ws2605147:p001:m0138', 'start': 138, 'end': 139, 'surface': '其', 'kind': 'pronoun', 'status': 'resolved_contextual', 'source_role': 'ji', 'interpretation_note': '來源詞與發話角色限定；非姓名，不進姓名aliases。', 'source_reference_binding': {'kind': 'fixed_jin054_local_reference', 'contract_ref': 'source-evidence/jin054-lu-openings/source-native-contract.json', 'role_key': 'ji', 'paragraph_sha256': '5c268becc06e3102a128f1a0cac5992d0eb2625f7b4990ccef095898b20ec0c5'}}, 'c-jinshu-054-lu-openings-ws2605147:p002:m0062': {'id': 'c-jinshu-054-lu-openings-ws2605147:p002:m0062', 'start': 62, 'end': 63, 'surface': '卿', 'kind': 'pronoun', 'status': 'resolved_contextual', 'source_role': 'ji', 'interpretation_note': '來源詞與發話角色限定；非姓名，不進姓名aliases。', 'source_reference_binding': {'kind': 'fixed_jin054_local_reference', 'contract_ref': 'source-evidence/jin054-lu-openings/source-native-contract.json', 'role_key': 'ji', 'paragraph_sha256': '109089883fea0749c11b1065d2b9d4b813ac1116dadbe297ade3f4847120acf7'}}, 'c-jinshu-054-lu-openings-ws2605147:p002:m0143': {'id': 'c-jinshu-054-lu-openings-ws2605147:p002:m0143', 'start': 143, 'end': 144, 'surface': '君', 'kind': 'pronoun', 'status': 'resolved_contextual', 'source_role': 'ji', 'interpretation_note': '來源詞與發話角色限定；非姓名，不進姓名aliases。', 'source_reference_binding': {'kind': 'fixed_jin054_local_reference', 'contract_ref': 'source-evidence/jin054-lu-openings/source-native-contract.json', 'role_key': 'ji', 'paragraph_sha256': '109089883fea0749c11b1065d2b9d4b813ac1116dadbe297ade3f4847120acf7'}}, 'c-jinshu-054-lu-openings-ws2605147:p002:m0153': {'id': 'c-jinshu-054-lu-openings-ws2605147:p002:m0153', 'start': 153, 'end': 154, 'surface': '君', 'kind': 'pronoun', 'status': 'resolved_contextual', 'source_role': 'luzhi', 'interpretation_note': '來源詞與發話角色限定；非姓名，不進姓名aliases。', 'source_reference_binding': {'kind': 'fixed_jin054_local_reference', 'contract_ref': 'source-evidence/jin054-lu-openings/source-native-contract.json', 'role_key': 'luzhi', 'paragraph_sha256': '109089883fea0749c11b1065d2b9d4b813ac1116dadbe297ade3f4847120acf7'}}, 'c-jinshu-054-lu-openings-ws2605147:p002:m0195': {'id': 'c-jinshu-054-lu-openings-ws2605147:p002:m0195', 'start': 195, 'end': 196, 'surface': '我', 'kind': 'pronoun', 'status': 'resolved_contextual', 'source_role': 'ji', 'interpretation_note': '來源詞與發話角色限定；非姓名，不進姓名aliases。', 'source_reference_binding': {'kind': 'fixed_jin054_local_reference', 'contract_ref': 'source-evidence/jin054-lu-openings/source-native-contract.json', 'role_key': 'ji', 'paragraph_sha256': '109089883fea0749c11b1065d2b9d4b813ac1116dadbe297ade3f4847120acf7'}}, 'c-jinshu-054-lu-openings-ws2605147:p003:m0039': {'id': 'c-jinshu-054-lu-openings-ws2605147:p003:m0039', 'start': 39, 'end': 40, 'surface': '之', 'kind': 'pronoun', 'status': 'resolved_contextual', 'source_role': 'ji', 'interpretation_note': '來源詞與發話角色限定；非姓名，不進姓名aliases。', 'source_reference_binding': {'kind': 'fixed_jin054_local_reference', 'contract_ref': 'source-evidence/jin054-lu-openings/source-native-contract.json', 'role_key': 'ji', 'paragraph_sha256': 'c1ea636c40d08520d008b2a15278070e6cd87367cec2f2dfc8cd407065c4e6e9'}}, 'c-jinshu-054-lu-openings-ws2605147:p003:m0060': {'id': 'c-jinshu-054-lu-openings-ws2605147:p003:m0060', 'start': 60, 'end': 61, 'surface': '之', 'kind': 'pronoun', 'status': 'resolved_contextual', 'source_role': 'yun', 'interpretation_note': '來源詞與發話角色限定；非姓名，不進姓名aliases。', 'source_reference_binding': {'kind': 'fixed_jin054_local_reference', 'contract_ref': 'source-evidence/jin054-lu-openings/source-native-contract.json', 'role_key': 'yun', 'paragraph_sha256': 'c1ea636c40d08520d008b2a15278070e6cd87367cec2f2dfc8cd407065c4e6e9'}}, 'c-jinshu-054-lu-openings-ws2605147:p003:m0167': {'id': 'c-jinshu-054-lu-openings-ws2605147:p003:m0167', 'start': 167, 'end': 168, 'surface': '其', 'kind': 'pronoun', 'status': 'resolved_contextual', 'source_role': 'yun', 'interpretation_note': '來源詞與發話角色限定；非姓名，不進姓名aliases。', 'source_reference_binding': {'kind': 'fixed_jin054_local_reference', 'contract_ref': 'source-evidence/jin054-lu-openings/source-native-contract.json', 'role_key': 'yun', 'paragraph_sha256': 'c1ea636c40d08520d008b2a15278070e6cd87367cec2f2dfc8cd407065c4e6e9'}}}
def same(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 return a==b
def expand(x,roles):
 if isinstance(x,str):return roles.get(x,x)
 if isinstance(x,list):return[expand(v,roles)for v in x]
 if isinstance(x,dict):return{k:expand(v,roles)for k,v in x.items()}
 return x
def source_reference(m,text=None):
 if not isinstance(m,dict)or m.get('id')not in PRONOUNS:return False
 want=PRONOUNS[m['id']]
 return isinstance(m.get('person_id'),str)and bool(m['person_id'])and all(same(m.get(k),v)for k,v in want.items())and(text is None or hashlib.sha256(text.encode()).hexdigest()==want['source_reference_binding']['paragraph_sha256'])
def project(raw,a,b):
 line=raw[a:b];ix=[];i=0
 while i<len(line):
  if line.startswith('-{',i):z=line.index('}-',i);ix.extend(range(a+i+2,a+z));i=z+2
  elif line.startswith('[[',i):z=line.index(']]',i);assert'|'not in line[i:z];ix.extend(range(a+i+2,a+z));i=z+2
  else:ix.append(a+i);i+=1
 return ''.join(raw[x]for x in ix),ix

def proof(root,ch=None,people=None):
 root=Path(root).resolve()
 def local(rel):
  p=Path(rel);assert not p.is_absolute()and'..'not in p.parts;q=(root/p).resolve();assert q.is_relative_to(root)and q.is_file();return q
 def read(rel):return json.loads(local(rel).read_bytes())
 rawc=local(REF).read_bytes();assert hashlib.sha256(rawc).hexdigest()==SHA;c=json.loads(rawc);actual=read(CH);assert ch is None or same(ch,actual);ch=actual
 if people is None:people={p['id']:p for p in read('registry/persons.json')['persons']}
 anchors={m['id']:(p,m)for p in ch['paragraphs']for m in p['mentions']};roles={}
 for key,s in c['role_seeds'].items():
  if s['kind']=='new_source_local':p,m=anchors[s['first_mid']];assert m['kind']=='person';pid=m['person_id'];assert pid in people
  else:
   src=read(s['path']);assert src['id']==s['chapter_id']and same(src['source'],s['source']);p=next(p for p in src['paragraphs']if p['id']==s['paragraph_id']);m=next(m for m in p['mentions']if m['id']==s['marker']['id']);assert p['text']==s['quote']and same({k:v for k,v in m.items()if k!='person_id'},s['marker']);pid=m['person_id'];assert pid in people;actor=people[pid];assert[e for e in actor['evidence']if e.get('mention_id')==m['id']]==[s['reverse']];assert any(a['surface']==m['surface']and m['id']in a['mention_ids']for a in actor['aliases'])
  roles['$'+key]=pid
 assert len(roles)==len(set(roles.values()))and same(ch,expand(c['chapter_template'],roles))
 rawb=local(c['raw_file']).read_bytes();assert hashlib.sha256(rawb).hexdigest()==c['raw_sha256'];raw=rawb.decode();assert hashlib.sha256(local(c['raw_capture_qualification_path']).read_bytes()).hexdigest()==c['raw_capture_qualification_sha256'];assert len(ch['paragraphs'])==len(c['selection'])==3
 for p,(a,b)in zip(ch['paragraphs'],c['selection']):
  assert raw[a-1]=='\n'and raw[b]=='\n';text,ix=project(raw,a,b);assert p['text']==text and p['source_position']['raw_character_offsets']==ix and p['source_position']['raw_start']==a and p['source_position']['raw_end']==b
 for key,template in c['new_people'].items():
  p=people[roles['$'+key]];want=expand(template,roles);assert all(same(p.get(k),v)for k,v in want.items()if k not in('aliases','evidence'));assert not p.get('id_aliases')
  if p.get('family_path'):
   try:from scripts.lu_near_paternal_family import family_path_valid
   except ImportError:from lu_near_paternal_family import family_path_valid
   assert family_path_valid(root,roles['$'+key],p['family_path'])
 rev={roles['$'+k]:v for k,v in c['reverse_by_role'].items()};aliases={roles['$'+k]:v for k,v in c['proper_aliases_by_role'].items()}
 for pid,p in people.items():
  assert same([e for e in p['evidence']if e.get('chapter_id')==CID],rev.get(pid,[]))
  own=[{'surface':a['surface'],'mention_ids':[mid for mid in a['mention_ids']if mid.startswith(CID+':')]}for a in p['aliases']if any(mid.startswith(CID+':')for mid in a['mention_ids'])];assert same(own,aliases.get(pid,[]))
 for p in ch['paragraphs']:
  end=0
  for m in p['mentions']:
   assert end<=m['start']<m['end']<=len(p['text'])and p['text'][m['start']:m['end']]==m['surface'];end=m['end']
   if m['kind']in('person','pronoun'):
    assert m['person_id']==roles['$'+m['source_role']]
    if m['kind']=='pronoun':assert source_reference(m,p['text'])
   else:assert m['kind']=='unresolved'and m['person_id']is None
 for rel,t in c['sidecar_templates'].items():assert same(read(rel),expand(t,roles))
 w=next(w for w in read('registry/works.json')['works']if w['id']=='w-jinshu');book=next(b for b in w['books']if b['id']=='b-jinshu-054');assert book['work_id']=='w-jinshu'and book['number']==54 and CID in book['chapter_ids']
 assert same(read('registry/work-provenance.json')['text_bases'][ch['source_id']],c['text_base_row'])
 assert[p for p in read('corpus/progress.json')['books']if p['chapter_id']==CID]==[c['progress_row']]
 return ch,c,roles

def errors(ch,root):
 try:proof(root,ch);return[]
 except(AssertionError,KeyError,TypeError,ValueError,OSError,StopIteration,IndexError):return['晉054三完整短單元/原字投影/人物與引語發話角色、姓名親等或反查不符，不得以同字/引古比擬或SGZ參校擴充本源']
def guard_bundle(root,pid,people,records):
 root=Path(root)
 if not(root/REF).exists():return
 actual=json.loads((root/CH).read_bytes());owned={m.get('person_id')for p in actual['paragraphs']for m in p['mentions']if m['kind']in('person','pronoun')}
 if pid not in owned and not any(e.get('chapter_id')==CID for e in people.get(pid,{}).get('evidence',[])):return
 ch,c,r=proof(root,people=people);assert sum(same(x,ch)for x in records)==1
 for rel,t in c['sidecar_templates'].items():assert sum(same(x,expand(t,r))for x in records)==1

def name_valid(n,root):
 try:
  ch,c,r=proof(root);want=[x for t in c['sidecar_templates'].values()for x in expand(t,r).get('records',[])];return sum(same(n,x)for x in want)==1
 except(AssertionError,KeyError,ValueError,TypeError,OSError,StopIteration):return False

def group_set_valid(d,people,root):
 ch,c,r=proof(root,people=people);wanted=[expand(t,r)for t in c['sidecar_templates'].values()if t.get('record_type')=='source_person_reference_group_set'];assert len(wanted)==1 and same(d,wanted[0]);return d
