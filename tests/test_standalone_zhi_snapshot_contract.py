"""The retyped anchors retain exact source positions and registry evidence."""
import copy,json,unittest
from pathlib import Path
from scripts.snapshot_test_expectations import ROWS,current_snapshot,historical_snapshot
R=Path(__file__).resolve().parents[1]
PEI_PATH='corpus/jinshu/035-pei-family.json'
PEI_CID='c-jinshu-035-peikai-family'
# Only these four historical slots moved in the reviewed Pei family rekey.
# The current identities come from explicit proper-name roles, never an ID map.
REKEY_ROLES={'p003:m0019':'kai','p012:m0056':'xian','p012:m0100':'kai','p016:m0178':'dun'}
ROLE_SEEDS={
 'kai':(('p003:m0011',11,12,'楷'),('p003:m0046',46,47,'楷')),
 'xian':(('p012:m0000',0,1,'憲'),('p012:m0002',2,4,'景思'),('p012:m0063',63,65,'裴憲')),
 'dun':(('p016:m0015',15,16,'盾'),('p016:m0042',42,43,'盾'),('p016:m0138',138,139,'盾'),('p016:m0156',156,157,'盾')),
}
def source_state():
 people={p['id']:p for p in json.loads((R/'registry/persons.json').read_bytes())['persons']}
 chapters={path:json.loads((R/path).read_bytes()) for path in {row['path'] for row in ROWS.values()}}
 return people,chapters

def current_roles(chapters,people):
 ch=chapters[PEI_PATH];ps={p['id']:p for p in ch['paragraphs']};roles={}
 for role,seeds in ROLE_SEEDS.items():
  endpoints=[]
  for suffix,start,end,surface in seeds:
   mid=PEI_CID+':'+suffix;p=ps[mid.rsplit(':',1)[0]]
   # These paragraphs themselves are frozen by the original 338-slot fixture.
   assert p['text']==next(row['text'] for row in ROWS.values() if row['paragraph_id']==p['id'])
   m,=[m for m in p['mentions'] if m['id']==mid]
   assert (m['start'],m['end'],m['surface'],m['kind'])==(start,end,surface,'person')
   assert p['text'][start:end]==surface and m['person_id'] in people
   actor=people[m['person_id']]
   expected={k:ch[k] for k in ('work_id','book_id','source_id')}
   expected.update(chapter_id=ch['id'],paragraph_id=p['id'],mention_id=mid,quote=surface)
   assert [e for e in actor['evidence'] if e.get('mention_id')==mid]==[expected]
   assert sum(mid in a.get('mention_ids',[]) and a.get('surface')==surface for a in actor['aliases'])==1
   endpoints.append(m['person_id'])
  assert len(set(endpoints))==1
  roles[role]=endpoints[0]
 assert len(set(roles.values()))==len(roles)
 return roles

def check_snapshot(people,chapters):
 assert len(ROWS)==338
 roles=current_roles(chapters,people)
 aliases={mid for actor in people.values() for a in actor['aliases'] for mid in a.get('mention_ids',[]) if mid in ROWS}
 assert not aliases
 reverse_owners={}
 for pid,actor in people.items():
  for e in actor['evidence']:
   if e.get('mention_id') in ROWS:reverse_owners.setdefault(e['mention_id'],[]).append(pid)
 for mid,row in ROWS.items():
  ch=chapters[row['path']];p,=[p for p in ch['paragraphs'] if p['id']==row['paragraph_id']]
  m,=[m for m in p['mentions'] if m['id']==mid]
  assert p['text']==row['text']
  expected=copy.deepcopy(row['mention']);suffix=mid.removeprefix(PEI_CID+':')
  if row['path']==PEI_PATH and suffix in REKEY_ROLES:expected['person_id']=roles[REKEY_ROLES[suffix]]
  assert m==expected
  assert p['text'][m['start']:m['end']]=='之' and m['kind']=='pronoun'
  actor=people[m['person_id']]
  assert reverse_owners.get(mid,[])==[m['person_id']]
  reverse=[e for e in actor['evidence'] if e.get('mention_id')==mid]
  assert len(reverse)==1
  expected_reverse=dict(chapter_id=ch['id'],paragraph_id=p['id'],mention_id=mid,quote='之')
  assert all(reverse[0].get(k)==v for k,v in expected_reverse.items())
  # Existing captures have four or seven fields; retain both documented forms.
  assert set(reverse[0]) in (set(expected_reverse),set(expected_reverse)|{'work_id','book_id','source_id'})
  for k in ('work_id','book_id','source_id'):
   if k in reverse[0]:assert reverse[0][k]==ch[k]
 return roles

class StandaloneZhiSnapshotContract(unittest.TestCase):
 def test_exact_338_source_anchors_and_reverse_evidence(self):
  import hashlib
  self.assertEqual(hashlib.sha256((R/'tests/fixtures/standalone-zhi-current-anchors.json').read_bytes()).hexdigest(),'a6c578b1066b59e1cf9333ab7d53e622571f3fecfa8770ef910a86b0801c846f')
  people,chapters=source_state();roles=check_snapshot(people,chapters)
  # The ordinary source guard supplies the independent current Kai identity;
  # source-position snapshots are not a second permanent identity authority.
  from scripts.sgz023_pei_name_components import proof
  proof(R)
  from scripts.fixed_sgz023_works import proof as source_proof
  ch=source_proof(R)['chapter'];paragraph=next(p for p in ch['paragraphs'] if p['id'].endswith(':p009'))
  slots={m['id']:m for m in paragraph['mentions']}
  for role,suffix in (('kai','m0487'),('xian','m0738'),('dun','m0655')):
   self.assertEqual(slots[ch['id']+':p009:'+suffix]['person_id'],roles[role])

 def test_contract_rejects_endpoint_theft_even_with_moved_reverse(self):
  people,chapters=source_state();roles=current_roles(chapters,people)
  p=next(p for p in chapters[PEI_PATH]['paragraphs'] if p['id'].endswith(':p003'))
  m=next(m for m in p['mentions'] if m['id'].endswith(':m0019'))
  old=people[roles['kai']];new=people[roles['xian']]
  e,=[e for e in old['evidence'] if e.get('mention_id')==m['id']]
  old['evidence'].remove(e);new['evidence'].append(e);m['person_id']=roles['xian']
  with self.assertRaises(AssertionError):check_snapshot(people,chapters)

 def test_current_proper_role_cannot_be_reassigned_by_one_anchor(self):
  people,chapters=source_state();roles=current_roles(chapters,people)
  p=next(p for p in chapters[PEI_PATH]['paragraphs'] if p['id'].endswith(':p003'))
  m=next(m for m in p['mentions'] if m['id'].endswith(':m0011'))
  old=people[roles['kai']];new=people[roles['xian']]
  e,=[e for e in old['evidence'] if e.get('mention_id')==m['id']]
  old['evidence'].remove(e);new['evidence'].append(e)
  for a in old['aliases']:
   if m['id'] in a.get('mention_ids',[]):a['mention_ids'].remove(m['id'])
  new['aliases'].append({'surface':m['surface'],'mention_ids':[m['id']]});m['person_id']=roles['xian']
  with self.assertRaises(AssertionError):check_snapshot(people,chapters)

 def test_contract_rejects_source_kind_reverse_and_alias_corruption(self):
  people,chapters=source_state();mid=PEI_CID+':p003:m0019'
  p=next(p for p in chapters[PEI_PATH]['paragraphs'] if p['id'].endswith(':p003'))
  m=next(m for m in p['mentions'] if m['id']==mid);actor=people[m['person_id']]
  for key,value in (('start',m['start']+1),('kind','person'),('surface','楷'),('person_id','not-registered')):
   with self.subTest(field=key):
    old=m[key];m[key]=value
    with self.assertRaises(AssertionError):check_snapshot(people,chapters)
    m[key]=old
  old=p['text'];p['text']=old+'。'
  with self.assertRaises(AssertionError):check_snapshot(people,chapters)
  p['text']=old
  e,=[e for e in actor['evidence'] if e.get('mention_id')==mid]
  for key,value in (('quote','楷'),('chapter_id','wrong'),('source_id','wrong')):
   with self.subTest(reverse=key):
    old=e[key];e[key]=value
    with self.assertRaises(AssertionError):check_snapshot(people,chapters)
    e[key]=old
  actor['evidence'].remove(e)
  with self.assertRaises(AssertionError):check_snapshot(people,chapters)
  actor['evidence'].append(e)
  other=people[current_roles(chapters,people)['dun']]
  other['aliases'].append({'surface':'之','mention_ids':[mid]})
  with self.assertRaises(AssertionError):check_snapshot(people,chapters)

 def test_complete_reference_rekey_does_not_change_historical_capture(self):
  people,chapters=source_state();roles=current_roles(chapters,people)
  mapping={pid:'zhr_k29_tst_'+chr(65+i) for i,pid in enumerate(roles.values())}
  self.assertFalse(set(mapping.values()) & set(people))
  def rewrite(x):
   if isinstance(x,str):return mapping.get(x,x)
   if isinstance(x,list):return [rewrite(v) for v in x]
   if isinstance(x,dict):return {mapping.get(k,k):rewrite(v) for k,v in x.items()}
   return x
  check_snapshot(rewrite(people),rewrite(chapters))
  self.assertEqual(ROWS[PEI_CID+':p003:m0019']['mention']['person_id'],'530_f9d_4bd')

 def test_only_explicit_mids_and_standalone_glyph_are_normalized(self):
  row=copy.deepcopy(next(iter(ROWS.values()))['mention']);old=historical_snapshot(row);self.assertEqual(old['kind'],'person');self.assertEqual(current_snapshot(old),row)
  for change in [{'id':'unregistered-mid'},{'surface':'王羲之'}]:
   value=dict(old,**change);self.assertEqual(current_snapshot(value),value)
  value=dict(old,start=old['start']+1)
  with self.assertRaises(AssertionError):current_snapshot(value)

 def test_split_xuxianzhi_is_name_fragment_not_pronoun(self):
  c=json.loads((R/'corpus/songshu/044-wyd1739.json').read_bytes());ps={p['id'].split(':')[-1]:p for p in c['paragraphs']};self.assertTrue(ps['p007']['text'].endswith('晦同産以下羡'));self.assertTrue(ps['p008']['text'].startswith('之諸姪咸無所染'))
  m=next(m for m in ps['p008']['mentions'] if m['id'].endswith(':m0000'));self.assertEqual(m['kind'],'person');self.assertEqual(m['person_id'],'4y6_myv_ojh');self.assertEqual(m['surface'],'之')
