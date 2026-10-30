# coding: utf-8
"""Complete received Zhou041 Wang Bao unit and finite source-role NER/letter references."""
import json,hashlib,re
from pathlib import Path
REF='source-evidence/zhou041-wangbao-ws2432538/source-ner-contract.json'
SHA='3e6008028d663e86ca0a1a2b114f584268d88a1d858dbfc03fa5a211e585149e'
CID='c-zhoushu-041-wangbao-ws2432538'
CH='corpus/zhoushu/041-wangbao-ws2432538.json'
LETTER_REFERENCES={'c-zhoushu-041-wangbao-ws2432538:p009:m0051': {'id': 'c-zhoushu-041-wangbao-ws2432538:p009:m0051', 'start': 51, 'end': 53, 'surface': '賢兄', 'kind': 'pronoun', 'status': 'resolved_contextual', 'source_role': 'zhouhongzheng', 'source_letter_role_binding': {'kind': 'fixed_zhou041_letter_reference', 'contract_ref': 'source-evidence/zhou041-wangbao-ws2432538/source-ner-contract.json', 'role_key': 'zhouhongzheng', 'paragraph_sha256': '7ebcb04a70d61d6198a73f6074af638bfb894a5e52e2e0cefc8d29037099bf8a'}}, 'c-zhoushu-041-wangbao-ws2432538:p012:m0031': {'id': 'c-zhoushu-041-wangbao-ws2432538:p012:m0031', 'start': 31, 'end': 33, 'surface': '家兄', 'kind': 'pronoun', 'status': 'resolved_contextual', 'source_role': 'zhouhongzheng', 'source_letter_role_binding': {'kind': 'fixed_zhou041_letter_reference', 'contract_ref': 'source-evidence/zhou041-wangbao-ws2432538/source-ner-contract.json', 'role_key': 'zhouhongzheng', 'paragraph_sha256': '369e808c206105105e622c48ed4a8e0786b3e56468c37f5251e07228b58d94f1'}}, 'c-zhoushu-041-wangbao-ws2432538:p010:m0000': {'id': 'c-zhoushu-041-wangbao-ws2432538:p010:m0000', 'start': 0, 'end': 1, 'surface': '弟', 'kind': 'pronoun', 'status': 'resolved_contextual', 'source_role': 'bao', 'source_letter_role_binding': {'kind': 'fixed_zhou041_letter_reference', 'contract_ref': 'source-evidence/zhou041-wangbao-ws2432538/source-ner-contract.json', 'role_key': 'bao', 'paragraph_sha256': '0527e993d3691cb8bb62a546b0786f030bb8860370e2ede147d3208dca568e8d'}}, 'c-zhoushu-041-wangbao-ws2432538:p012:m0044': {'id': 'c-zhoushu-041-wangbao-ws2432538:p012:m0044', 'start': 44, 'end': 46, 'surface': '故人', 'kind': 'pronoun', 'status': 'resolved_contextual', 'source_role': 'bao', 'source_letter_role_binding': {'kind': 'fixed_zhou041_letter_reference', 'contract_ref': 'source-evidence/zhou041-wangbao-ws2432538/source-ner-contract.json', 'role_key': 'bao', 'paragraph_sha256': '369e808c206105105e622c48ed4a8e0786b3e56468c37f5251e07228b58d94f1'}}, 'c-zhoushu-041-wangbao-ws2432538:p013:m0001': {'id': 'c-zhoushu-041-wangbao-ws2432538:p013:m0001', 'start': 1, 'end': 2, 'surface': '弟', 'kind': 'pronoun', 'status': 'resolved_contextual', 'source_role': 'bao', 'source_letter_role_binding': {'kind': 'fixed_zhou041_letter_reference', 'contract_ref': 'source-evidence/zhou041-wangbao-ws2432538/source-ner-contract.json', 'role_key': 'bao', 'paragraph_sha256': 'ae5c73d286e6f3b10b6b85eae1f3b321a8aaee8a419b09753247eac2bd070ad3'}}, 'c-zhoushu-041-wangbao-ws2432538:p013:m0068': {'id': 'c-zhoushu-041-wangbao-ws2432538:p013:m0068', 'start': 68, 'end': 69, 'surface': '弟', 'kind': 'pronoun', 'status': 'resolved_contextual', 'source_role': 'bao', 'source_letter_role_binding': {'kind': 'fixed_zhou041_letter_reference', 'contract_ref': 'source-evidence/zhou041-wangbao-ws2432538/source-ner-contract.json', 'role_key': 'bao', 'paragraph_sha256': 'ae5c73d286e6f3b10b6b85eae1f3b321a8aaee8a419b09753247eac2bd070ad3'}}, 'c-zhoushu-041-wangbao-ws2432538:p013:m0127': {'id': 'c-zhoushu-041-wangbao-ws2432538:p013:m0127', 'start': 127, 'end': 128, 'surface': '弟', 'kind': 'pronoun', 'status': 'resolved_contextual', 'source_role': 'bao', 'source_letter_role_binding': {'kind': 'fixed_zhou041_letter_reference', 'contract_ref': 'source-evidence/zhou041-wangbao-ws2432538/source-ner-contract.json', 'role_key': 'bao', 'paragraph_sha256': 'ae5c73d286e6f3b10b6b85eae1f3b321a8aaee8a419b09753247eac2bd070ad3'}}, 'c-zhoushu-041-wangbao-ws2432538:p013:m0063': {'id': 'c-zhoushu-041-wangbao-ws2432538:p013:m0063', 'start': 63, 'end': 64, 'surface': '吾', 'kind': 'pronoun', 'status': 'resolved_contextual', 'source_role': 'zhouhongrang', 'source_letter_role_binding': {'kind': 'fixed_zhou041_letter_reference', 'contract_ref': 'source-evidence/zhou041-wangbao-ws2432538/source-ner-contract.json', 'role_key': 'zhouhongrang', 'paragraph_sha256': 'ae5c73d286e6f3b10b6b85eae1f3b321a8aaee8a419b09753247eac2bd070ad3'}}, 'c-zhoushu-041-wangbao-ws2432538:p013:m0122': {'id': 'c-zhoushu-041-wangbao-ws2432538:p013:m0122', 'start': 122, 'end': 123, 'surface': '吾', 'kind': 'pronoun', 'status': 'resolved_contextual', 'source_role': 'zhouhongrang', 'source_letter_role_binding': {'kind': 'fixed_zhou041_letter_reference', 'contract_ref': 'source-evidence/zhou041-wangbao-ws2432538/source-ner-contract.json', 'role_key': 'zhouhongrang', 'paragraph_sha256': 'ae5c73d286e6f3b10b6b85eae1f3b321a8aaee8a419b09753247eac2bd070ad3'}}}

def same(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 return a==b

def source_letter_reference(m,text=None):
 if not isinstance(m,dict)or m.get('id')not in LETTER_REFERENCES:return False
 spec=LETTER_REFERENCES[m['id']]
 return (m.get('kind')=='pronoun'and isinstance(m.get('person_id'),str)and bool(m['person_id'])and all(same(m.get(k),v)for k,v in spec.items())and(text is None or hashlib.sha256(text.encode()).hexdigest()==spec['source_letter_role_binding']['paragraph_sha256']))

def project(raw,start,end):
 out=[];notes=[]
 for match in re.finditer(r'[^\n]+',raw[start:end]):
  line=match[0];a=start+match.start();z=start+match.end()
  if line=='==王褒==':continue
  assert not line.startswith('=');ix=[];i=0;pid=CID+f':p{len(out)+1:03}'
  while i<len(line):
   if line.startswith('<ref>',i):
    stop=line.index('</ref>',i)+6;nr=line[i:stop];notes.append({'paragraph_id':pid,'raw_start':a+i,'raw_end':a+stop,'raw_text':nr,'body_offset':len(ix),'text':re.sub(r'\{\{\*\|([^{}]*)\}\}',lambda m:m.group(1),nr[5:-6])});i=stop
   elif line.startswith('{{*|',i):
    stop=line.index('}}',i);assert '{{'not in line[i+4:stop];ix.extend(range(a+i+4,a+stop));i=stop+2
   elif i==0 and line[i]==':':i+=1
   else:
    assert not any(line.startswith(t,i)for t in ['{{','}}','<ref','</ref']);ix.append(a+i);i+=1
  out.append({'id':pid,'text':''.join(raw[x]for x in ix),'source_position':{'raw_start':a,'raw_end':z,'raw_character_offsets':ix,'first_line':raw.count('\n',0,a)+1,'last_line':raw.count('\n',0,z)+1,'revision_id':2432538,'projection_sha256':hashlib.sha256((json.dumps(ix,ensure_ascii=False,indent=2)+'\n').encode()).hexdigest(),'source_layer':'received_biography'}})
 return out,notes

def proof(root,ch=None,people=None):
 root=Path(root).resolve()
 def local(rel):
  p=Path(rel);assert not p.is_absolute()and '..'not in p.parts;q=(root/p).resolve();assert q.is_relative_to(root)and q.is_file();return q
 def read(rel):return json.loads(local(rel).read_bytes())
 raw_case=local(REF).read_bytes();assert hashlib.sha256(raw_case).hexdigest()==SHA;c=json.loads(raw_case);actual=read(CH);assert ch is None or same(ch,actual);ch=actual
 if people is None:people={p['id']:p for p in read('registry/persons.json')['persons']}
 anchors={m['id']:(p,m)for p in ch['paragraphs']for m in p['mentions']};roles={}
 for key,s in {**c['role_seeds'],**c['candidate_source_seeds']}.items():
  if s['kind']=='new_source_local':
   p,m=anchors[s['first_mid']];assert m['kind']=='person';pid=m['person_id'];assert pid in people
  else:
   source=read(s['path']);assert same(source['source'],s['source'])and source['id']==s['chapter_id'];p=next(p for p in source['paragraphs']if p['id']==s['paragraph_id']);m=next(m for m in p['mentions']if m['id']==s['marker']['id']);assert p['text']==s['quote']and same({k:v for k,v in m.items()if k!='person_id'},s['marker'])and m['kind']=='person';pid=m['person_id'];assert pid in people;actor=people[pid];assert [e for e in actor['evidence']if e.get('mention_id')==m['id']]==[s['reverse']];assert any(a['surface']==m['surface']and m['id']in a['mention_ids']for a in actor['aliases'])
  roles['$'+key]=pid
 older,younger=roles['$zhouhongzheng'],roles['$zhouhongrang'];ns=older.rsplit('_',1)[0]
 assert re.fullmatch('[a-z0-9]{3}_[a-z0-9]{3}_[a-z0-9]{3}',ns)and ns not in people and older==ns+'_A'and younger==ns+'_B'
 roles['$zhou_brothers_namespace']=ns
 active=[roles['$'+k]for k in c['role_seeds']];assert len(active)==len(set(active))
 def expand(x):
  if isinstance(x,str):return roles.get(x,x)
  if isinstance(x,list):return[expand(v)for v in x]
  if isinstance(x,dict):return{k:expand(v)for k,v in x.items()}
  return x
 try:from scripts.zhou041_wangbao_profile_facts import base_chapter
 except ImportError:from zhou041_wangbao_profile_facts import base_chapter
 try:from scripts import fixed_zhou041_erlu as erlu
 except ImportError:import fixed_zhou041_erlu as erlu
 try:from scripts.zhou041_imperial_name_components import source_record as imperial_names_installed
 except ImportError:from zhou041_imperial_name_components import source_record as imperial_names_installed
 imperial_names_installed(root,ch,roles)
 assert same(erlu.source_projection(base_chapter(root,ch,roles),root,roles,c),expand(c['chapter_template']))
 rawb=local(c['raw_file']).read_bytes();assert hashlib.sha256(rawb).hexdigest()==c['raw_sha256'];raw=rawb.decode();s=c['selection'];assert raw.index(s['opening_heading'])==s['start']and raw.index(s['following_heading'],s['start'])==s['end']and raw[s['start']:s['end']]==s['raw'];assert hashlib.sha256(local(c['source_unit_existing_path']).read_bytes()).hexdigest()==c['unit_sha256']and raw[s['start']:s['end']].encode()==local(c['source_unit_existing_path']).read_bytes()
 projected,notes=project(raw,s['start'],s['end']);assert len(projected)==14 and len(notes)==10 and len(projected)==len(ch['paragraphs'])
 for p,want in zip(ch['paragraphs'],projected):assert p['id']==want['id']and p['text']==want['text']and same(p['source_position'],want['source_position'])and p['text_layer']=='received_chapter'
 reports=ch['annotation']['modern_collation_reports'];assert len(reports)==10
 for r,want in zip(reports,notes):assert all(same(r[k],v)for k,v in want.items())and r['layer']=='modern_received_witness_collation_report'and r['image_verified']is False and r['human_reviewed']is False
 primaryb=local(c['primary_readings_path']).read_bytes();assert hashlib.sha256(primaryb).hexdigest()==c['primary_readings_sha256'];primary=json.loads(primaryb)
 for r in primary['rulers']:assert hashlib.sha256(r['quote'].encode()).hexdigest()==r['quote_sha256']and r['image_verified']is False and r['human_reviewed']is False
 for key,template in c['new_people'].items():
  p=people[roles['$'+key]];expected=expand(template);assert all(same(p.get(k),v)for k,v in expected.items()if k not in('aliases','evidence'));assert not p.get('id_aliases')and not p.get('family_path')
 expected_reverse={roles['$'+k]:v for k,v in c['reverse_by_role'].items()};expected_alias={roles['$'+k]:v for k,v in c['proper_aliases_by_role'].items()}
 for pid,p in people.items():
  assert same([e for e in p['evidence']if e.get('chapter_id')==CID],expected_reverse.get(pid,[]))
  aliases=[{'surface':a['surface'],'mention_ids':[mid for mid in a['mention_ids']if mid.startswith(CID+':')]}for a in p['aliases']if any(mid.startswith(CID+':')for mid in a['mention_ids'])];assert same(aliases,expected_alias.get(pid,[]))
 for p in ch['paragraphs']:
  for m in p['mentions']:
   assert p['text'][m['start']:m['end']]==m['surface']
   if m['kind']=='pronoun':assert source_letter_reference(m,p['text'])and m['person_id']==roles['$'+m['source_role']]
   elif m['kind']=='person':assert m['person_id']==roles['$'+m['source_role']]
   else:assert m['kind']=='unresolved'and m['person_id']is None and m['status']=='unresolved'
 for rel,template in c['sidecar_templates'].items():assert same(read(rel),expand(template))
 works={w['id']:w for w in read('registry/works.json')['works']};assert any(b['id']=='b-zhoushu-041'and CID in b['chapter_ids']for b in works['w-zhoushu']['books']);assert same(read('registry/work-provenance.json')['text_bases'][ch['source_id']],c['text_base_row'])
 assemblies=read('registry/family-assemblies.json')['assemblies'];assert [a for a in assemblies if a.get('id')=='family-zhou041-zhou-brothers']==[expand(c['brothers_namespace_template'])]
 erlu.validate_state(root,ch,people,roles,c)
 return ch,c,roles

def errors(ch,root):
 try:proof(root,ch);return []
 except(AssertionError,KeyError,ValueError,TypeError,OSError,IndexError,StopIteration):return ['周041完整王襃選錄、收到現代校勘層、人物/書信發話角色及反查不符；不得跨朝帝號、同名/近名或現代ref補古人']

def guard_bundle(root,pid,people,records):
 root=Path(root)
 if not(root/REF).exists():return
 # Derive ownership from true current anchors: loss of caller reverse/catalog cannot suppress this guard.
 actual=json.loads((root/CH).read_bytes());owned={m.get('person_id')for p in actual['paragraphs']for m in p['mentions']if m.get('kind')in('person','pronoun')}
 if pid not in owned and not any(e.get('chapter_id')==CID for e in people.get(pid,{}).get('evidence',[])):return
 ch,c,roles=proof(root,people=people);assert sum(same(r,ch)for r in records)==1
 def expand(x):
  if isinstance(x,str):return roles.get(x,x)
  if isinstance(x,list):return[expand(v)for v in x]
  if isinstance(x,dict):return{k:expand(v)for k,v in x.items()}
  return x
 for rel,template in c['sidecar_templates'].items():assert sum(same(r,expand(template))for r in records)==1
 try:from scripts.zhou041_wangbao_profile_facts import guard_catalog as guard_profile_facts
 except ImportError:from zhou041_wangbao_profile_facts import guard_catalog as guard_profile_facts
 guard_profile_facts(root,pid,people,records,ch,roles)
 try:from scripts.zhou041_imperial_name_components import guard_catalog as guard_imperial_names
 except ImportError:from zhou041_imperial_name_components import guard_catalog as guard_imperial_names
 guard_imperial_names(root,pid,records,ch,roles)


def brothers_namespace_members(assembly,people,assertions,chapters,root):
 """Finite full-name brother proof; no inferred common parent or permanent PID."""
 import copy
 try:
  ch,c,roles=proof(root,people=people)
  assert same(chapters[CID],ch)
  def expand(x):
   if isinstance(x,str):return roles.get(x,x)
   if isinstance(x,list):return[expand(v)for v in x]
   if isinstance(x,dict):return{k:expand(v)for k,v in x.items()}
   return x
  assert same(assembly,expand(c['brothers_namespace_template']))
  group=assembly['collateral_root_group'];aid=group['brother_assertion_id']
  wanted=[a for template in c['sidecar_templates'].values()for a in expand(template).get('assertions',[])if a['id']==aid]
  assert len(wanted)==1 and same(assertions[aid],wanted[0])
  for role,fullname in [('zhouhongzheng','周弘正'),('zhouhongrang','周弘讓')]:
   assert any(m['kind']=='person'and m['surface']==fullname and m['person_id']==roles['$'+role]for p in ch['paragraphs']for m in p['mentions'])
  return {row['person_id']:dict(copy.deepcopy(row),assembly_id=assembly['id'],root_person_id=None,namespace_id=assembly['namespace_id'],namespace_entry_person_id=assembly['entry_person_id'],collateral_root_group=copy.deepcopy(group),status=assembly['status'],human_reviewed=False)for row in assembly['members']}
 except(AssertionError,KeyError,TypeError,ValueError,OSError,StopIteration)as error:
  raise ValueError('周041原文明弟兄namespace來源或端點不符；不可補未知父母')from error
