"""Finite Nanqi006 November royal-son source gate; no runtime inference."""
import hashlib,json
from pathlib import Path
CONTEXT_SHA='c24aa1a31466e367a791210ed3bf2ff676ac1979da0a89e9bade45ff12e439b3'
CURRENT_SEEDS_SHA='0adca32ff0cf988c2027d47726b30bfd8edbe57b766e0ccb59a41a3773b1e08f'
SEED_SHA='71b5be9f691d7f8af99158e9ec5cc2b1bf1740e2e0a7055af75620029086e732'
CID='c-nanqishu-006-jianwu1-nov'
RAW='source-evidence/nanqi006-jianwu1-nov/KR2a0017_006.txt'
PROJECTION='source-evidence/nanqi006-jianwu1-nov/projection.json'
PROJECTION_SHA='089ff6751bf7f8e5c7e9515e1be3fc771f077f079b0dd6790f50097819a72e2c'
RAW_SHA='aba420da7ddecfb96742edaa962272afa2ef50b761b7b4cb4a1ef61ba16e9760'
TEXT_SHA='59000b004530bd045d07c4ee51e1185aa24c1928a13fb7c37a6ec3cce7f26ffe'
ROLES={'寳義': {'id': 'c-nanqishu-006-jianwu1-nov:p001:m0088', 'start': 88, 'end': 90, 'surface': '寳義'}, '寳𤣥': {'id': 'c-nanqishu-006-jianwu1-nov:p001:m0094', 'start': 94, 'end': 96, 'surface': '寳𤣥'}, '寳源': {'id': 'c-nanqishu-006-jianwu1-nov:p001:m0100', 'start': 100, 'end': 102, 'surface': '寳源'}, '寳寅': {'id': 'c-nanqishu-006-jianwu1-nov:p001:m0106', 'start': 106, 'end': 108, 'surface': '寳寅'}, '寳融': {'id': 'c-nanqishu-006-jianwu1-nov:p001:m0112', 'start': 112, 'end': 114, 'surface': '寳融'}, '寳攸': {'id': 'c-nanqishu-006-jianwu1-nov:p001:m0118', 'start': 118, 'end': 120, 'surface': '寳攸'}, 'monarch': {'id': 'c-nanqishu-006-jianwu1-nov:p001:m0404', 'start': 404, 'end': 405, 'surface': '上'}}

MARKS=[{'id': 'c-nanqishu-006-jianwu1-nov:p001:m0014', 'start': 14, 'end': 16, 'surface': '遥光', 'role': '遥光'}, {'id': 'c-nanqishu-006-jianwu1-nov:p001:m0025', 'start': 25, 'end': 28, 'surface': '王洪範', 'role': '王洪範'}, {'id': 'c-nanqishu-006-jianwu1-nov:p001:m0038', 'start': 38, 'end': 40, 'surface': '王晏', 'role': '王晏'}, {'id': 'c-nanqishu-006-jianwu1-nov:p001:m0053', 'start': 53, 'end': 56, 'surface': '王敬則', 'role': '王敬則'}, {'id': 'c-nanqishu-006-jianwu1-nov:p001:m0088', 'start': 88, 'end': 90, 'surface': '寳義', 'role': '寳義'}, {'id': 'c-nanqishu-006-jianwu1-nov:p001:m0094', 'start': 94, 'end': 96, 'surface': '寳𤣥', 'role': '寳𤣥'}, {'id': 'c-nanqishu-006-jianwu1-nov:p001:m0100', 'start': 100, 'end': 102, 'surface': '寳源', 'role': '寳源'}, {'id': 'c-nanqishu-006-jianwu1-nov:p001:m0106', 'start': 106, 'end': 108, 'surface': '寳寅', 'role': '寳寅'}, {'id': 'c-nanqishu-006-jianwu1-nov:p001:m0112', 'start': 112, 'end': 114, 'surface': '寳融', 'role': '寳融'}, {'id': 'c-nanqishu-006-jianwu1-nov:p001:m0118', 'start': 118, 'end': 120, 'surface': '寳攸', 'role': '寳攸'}, {'id': 'c-nanqishu-006-jianwu1-nov:p001:m0182', 'start': 182, 'end': 186, 'surface': '始安貞王', 'role': '始安貞王'}, {'id': 'c-nanqishu-006-jianwu1-nov:p001:m0189', 'start': 189, 'end': 190, 'surface': '妃', 'role': '妃'}, {'id': 'c-nanqishu-006-jianwu1-nov:p001:m0203', 'start': 203, 'end': 205, 'surface': '遥欣', 'role': '遥欣'}, {'id': 'c-nanqishu-006-jianwu1-nov:p001:m0217', 'start': 217, 'end': 219, 'surface': '遥昌', 'role': '遥昌'}, {'id': 'c-nanqishu-006-jianwu1-nov:p001:m0253', 'start': 253, 'end': 255, 'surface': '寳卷', 'role': '寳卷'}, {'id': 'c-nanqishu-006-jianwu1-nov:p001:m0316', 'start': 316, 'end': 318, 'surface': '寳𤣥', 'role': '寳𤣥'}, {'id': 'c-nanqishu-006-jianwu1-nov:p001:m0330', 'start': 330, 'end': 332, 'surface': '沈淵', 'role': '沈淵'}, {'id': 'c-nanqishu-006-jianwu1-nov:p001:m0404', 'start': 404, 'end': 405, 'surface': '上', 'role': '上'}]
def source_errors(ch,root):
 if not isinstance(ch,dict):return ['固定006來源須為物件']
 if ch.get('id')!=CID:return []
 try:
  root=Path(root).resolve();rp=root/RAW;pp=root/PROJECTION
  assert rp.resolve()==rp and pp.resolve()==pp
  b=rp.read_bytes();assert hashlib.sha256(b).hexdigest()==RAW_SHA
  pb=pp.read_bytes();assert hashlib.sha256(pb).hexdigest()==PROJECTION_SHA;d=json.loads(pb);raw=b.decode('utf-8');ps=ch['paragraphs'];assert len(ps)==1;p=ps[0]
  cb=(root/'source-evidence/nanqi006-jianwu1-nov/monarch-complete-context.json').read_bytes();assert hashlib.sha256(cb).hexdigest()==CONTEXT_SHA;context=json.loads(cb);assert raw[context['raw_start']:context['raw_end']]==context['raw_quote']and context['raw_quote'].startswith('髙宗眀皇帝諱鸞')
  assert d['raw_start']==1446 and d['raw_end']==1959 and raw[1446:].startswith('十一月癸酉')and raw[1959:].startswith('十二月壬子')
  assert p['text']==d['text']==''.join(raw[i]for i in d['raw_positions'])and hashlib.sha256(p['text'].encode()).hexdigest()==TEXT_SHA
  assert ch['work_id']=='w-nanqishu'and ch['book_id']=='b-nanqishu-006'and ch['source_id']=='s-nanqishu006-jianwu1-nov-kr787dd9a7'and ch['text_sha256']==TEXT_SHA
  assert p['source_position']['first_line']==d['first_line']==65 and p['source_position']['last_line']==d['last_line']==87
  assert p['id']==CID+':p001'and p['text_layer']=='received_chapter'
  assert p['source_position']['unit_key']=='jianwu1-nov:u001'and p['source_position']['source_layer']=='received_chapter'and p['source_position']['raw_projection_ref']==PROJECTION
  assert ch['source']['response_sha256']==RAW_SHA and ch['source']['revision_id']=='787dd9a7da495542e8f17c26c96900ce37b2c211'and ch['source']['image_verified']is False
  csb=(root/'source-evidence/nanqi006-jianwu1-nov/current-role-seeds.json').read_bytes();assert hashlib.sha256(csb).hexdigest()==CURRENT_SEEDS_SHA;seeds=json.loads(csb)
  expected={}
  for role,seed in seeds.items():
   foreign=json.loads((root/seed['path']).read_bytes());assert foreign['id']==seed['chapter_id']and foreign['source_id']==seed['source_id']and foreign['source']['revision_id']==seed['revision_id']
   fp=next(x for x in foreign['paragraphs']if x['id']==seed['paragraph_id']);assert fp['text']==seed['quote']and hashlib.sha256(fp['text'].encode()).hexdigest()==seed['paragraph_sha256']
   fm=next(m for m in fp['mentions']if m['id']==seed['mention_id']);assert fm['kind']=='person'and all(fm[k]==seed[k]for k in ('start','end','surface'));expected[role]=fm['person_id']
  people=json.loads((root/'registry/persons.json').read_bytes())['persons']
  for role in {x['role']for x in MARKS}-set(seeds):
   rolemarks=[x for x in MARKS if x['role']==role];ids=set()
   for mark in rolemarks:
    hits=[x for x in people if any(e.get('mention_id')==mark['id']and e.get('chapter_id')==CID and e.get('paragraph_id')==p['id']and e.get('quote')==mark['surface']for e in x.get('evidence',[]))and any(a.get('surface')==mark['surface']and mark['id']in a.get('mention_ids',[])for a in x.get('aliases',[]))]
    assert len(hits)==1;ids.add(hits[0]['id'])
   assert len(ids)==1;expected[role]=ids.pop()
  assertions=json.loads((root/'corpus/nanqishu/006-jianwu1-nov-assertions.json').read_bytes());assert assertions['record_type']=='person_assertion_set'and assertions['chapter_id']==CID
  assert {a['id']for a in assertions['assertions']}=={'a-nanqi006-jianwu1-nov-father-'+str(i)for i in range(1,7)}and len(assertions['assertions'])==6
  assert len(p['mentions'])==len(MARKS)
  for m,mark in zip(p['mentions'],MARKS):
   assert m['kind']=='person'and all(m[k]==mark[k]for k in ('id','start','end','surface'))and m['person_id']==expected[mark['role']]
  return []
 except(AssertionError,KeyError,TypeError,ValueError,IndexError,OSError,AttributeError,StopIteration):return ['固定006完整十一月日期單元原文／投影／來源不符']

def kinship_valid(a,paragraphs,chapters,root):
 if not isinstance(a,dict)or not isinstance(paragraphs,dict)or not isinstance(chapters,dict):return False
 try:
  q=a['qualifiers'];b=q['source_clause_binding'];slot=b['slot'];assert slot in ROLES and slot!='monarch'
  e,=a['evidence'];cid,p=paragraphs[e['paragraph_id']];ch=chapters[cid]
  assert cid==CID and not source_errors(ch,root)and p==ch['paragraphs'][0]
  assert set(b)=={'kind','rule','slot','roles'}and b['kind']=='fixed_regnal_royal_sons'and b['rule']=='fixed_nanqi006_jianwu1_nov'
  assert set(b['roles'])=={'child','monarch'}
  ms={m['id']:m for m in p['mentions']};child=ms[b['roles']['child']];father=ms[b['roles']['monarch']]
  for m,s in ((child,ROLES[slot]),(father,ROLES['monarch'])):
   assert m['kind']=='person'and isinstance(m['person_id'],str)and m['person_id']and all(m[k]==s[k]for k in ('id','start','end','surface'))
   assert p['text'][m['start']:m['end']]==m['surface']
  assert child['person_id']!=father['person_id']
  assert a['predicate']=='father'and a['status']=='source_attested'and a['human_reviewed']is False
  assert a['subject_person_id']==child['person_id']and a['object_person_id']==father['person_id']
  assert q=={'source_term':'立皇子','lineage':'paternal','source_clause_binding':b}
  assert e['chapter_id']==cid and e['quote']==p['text']and e['subject_person_mention_id']==child['id']and e['object_person_mention_id']==father['id']
  assert all(e[k]==ch[k]for k in ('work_id','book_id','source_id'))
  # Chronicle subject must agree with the fixed external canonical source seed.
  sb=(Path(root)/'source-evidence/nanqi006-jianwu1-nov/monarch-seed.json').read_bytes();assert hashlib.sha256(sb).hexdigest()==SEED_SHA;seed=json.loads(sb)
  other=json.loads((Path(root)/seed['path']).read_bytes());op=next(x for x in other['paragraphs']if x['id']==seed['paragraph_id'])
  assert hashlib.sha256(op['text'].encode()).hexdigest()==seed['paragraph_sha256']and op['text']==seed['quote']
  om=next(m for m in op['mentions']if m['id']==seed['mention_id'])
  assert om['kind']=='person'and all(om[k]==seed[k]for k in ('start','end','surface'))and om['person_id']==father['person_id']
  return True
 except(AssertionError,KeyError,TypeError,ValueError,IndexError,OSError,AttributeError,StopIteration):return False
