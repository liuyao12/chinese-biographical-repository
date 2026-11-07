import unittest,json,copy,tempfile,hashlib
from pathlib import Path
from scripts import fixed_jin098_wangdun_comparison as core
from scripts import fixed_jin098_wangdun_life as life
from scripts.life_event_groups import validated_groups
from scripts.age_context import age_context_valid
from scripts.validate_corpus import direct_source_age_valid
ROOT=Path(__file__).resolve().parents[1]
def read(root,rel):return json.loads((root/rel).read_bytes())
class Jin098LifeBasics(unittest.TestCase):
 def setUp(self):
  self.ch=read(ROOT,life.CH);self.roles=core.resolve(ROOT,self.ch);self.t=core.expand(life.fixed(ROOT,'three-basics-template.json'),self.roles);self.g=self.t['group_record']['groups'][0];self.events={e['id']:e for e in[self.t['prior_life_record'],self.t['new_life_record']['events'][0]]};self.cs={self.ch['id']:self.ch};c=read(ROOT,'corpus/jinshu/076-wangbin.json');self.cs[c['id']]=c;self.people={p['id']:p for p in read(ROOT,'registry/persons.json')['persons']}
 def test_ordinary_age_and_explicit_source_origin(self):
  self.assertEqual(core.source_errors(self.ch,ROOT),[]);age=self.ch['annotation']['age_assertions'][0];self.assertTrue(direct_source_age_valid(age));self.assertTrue(age_context_valid(age,self.events));self.assertEqual(age['value'],59);self.assertEqual(age['counting'],'unspecified_source_age');self.assertIsNone(age['birth_year']);self.assertEqual(self.t['new_address_record']['assertions'][0]['relation'],'biographical_origin');self.assertEqual(self.t['new_address_record']['assertions'][0]['place']['source_name'],'吳興')
 def test_two_raw_events_one_group_without_dates(self):
  self.assertTrue(life.group_valid(self.g,self.events,self.cs,self.people,ROOT));self.assertEqual(len(self.events),2);self.assertEqual(len(self.g['evidence']),2);self.assertIsNone(self.g['date']);self.assertEqual(self.g['status'],'editorial_provisional');self.assertIs(self.g['human_reviewed'],False)
  for e in self.events.values():self.assertIsNone(e['date_expression']);self.assertNotIn('normalized_date',e)
 def test_existing_076_direct_and_legacy_event_anchor_preserved(self):
  c=self.cs['c-jinshu-076-wangbin'];p=next(p for p in c['paragraphs']if p['id'].endswith(':line050'));m=next(m for m in p['mentions']if m['id'].endswith(':m0001'));self.assertEqual((m['start'],m['end'],m['surface']),(1,2,'敦'));self.assertEqual(self.t['prior_life_record']['evidence'][0]['person_mention_id'],p['id']+':m0022');self.assertEqual(self.g['member_bindings'][0]['person_mention_id'],m['id'])
 def test_wrong_person_type_endpoint_or_qualification_rejected(self):
  for k in['person','type','missing','representative','human','status','date']:
   g=copy.deepcopy(self.g)
   if k=='person':g['person_id']=self.roles['shenchong']
   elif k=='type':g['event_type']='birth'
   elif k=='missing':g['member_event_ids'].pop()
   elif k=='representative':g['representative_event_id']=g['member_event_ids'][0]
   elif k=='human':g['human_reviewed']=True
   elif k=='status':g['status']='source_attested'
   else:g['date']={'year':324}
   self.assertFalse(life.group_valid(g,self.events,self.cs,self.people,ROOT),k)
  people=copy.deepcopy(self.people);people[self.roles['dun']]['evidence']=[];self.assertFalse(life.group_valid(self.g,self.events,self.cs,people,ROOT))
 def test_missing_raw_event_and_false_death_paragraph_rejected(self):
  events=copy.deepcopy(self.events);events.pop(self.g['member_event_ids'][0]);self.assertFalse(life.group_valid(self.g,events,self.cs,self.people,ROOT))
  for suffix in['p023','p029']:
   g=copy.deepcopy(self.g);g['evidence'][1]['paragraph_id']=core.CID+':'+suffix;self.assertFalse(life.group_valid(g,self.events,self.cs,self.people,ROOT))
 def test_passed_context_single_end_must_match_actual_root(self):
  cs=copy.deepcopy(self.cs);p=cs[core.CID]['paragraphs'][33];m=next(m for m in p['mentions']if m['id'].endswith(':m0095'));m['person_id']=self.roles['shenchong'];self.assertFalse(life.group_valid(self.g,self.events,cs,self.people,ROOT))
 def test_source_age_not_60_boolean_birth_or_year(self):
  for k in['60','bool','birth','year']:
   ch=copy.deepcopy(self.ch);a=ch['annotation']['age_assertions'][0]
   if k=='60':a['value']=60
   elif k=='bool':a['value']=True
   elif k=='birth':a['birth_year']=266
   else:a['normalized_date']={'year':323}
   self.assertTrue(core.source_errors(ch,ROOT),k)
 def mini(self):
  t=tempfile.TemporaryDirectory();root=Path(t.name);sp=read(ROOT,core.EP+'ner-roles.json');files={life.CH,life.LIFE,life.ADDR,life.GROUP,life.OLDLIFE,'registry/persons.json',core.RAW,'corpus/jinshu/098-wangdun-comparison-assertions.json','corpus/jinshu/098-wangdun-comparison-names.json','corpus/jinshu/098-wangdun-comparison-identities.json'}|{core.EP+n for n in core.PINS}|set(life.PINS)|{s['native_path']for s in sp['existing_seeds'].values()}|{s['native_path']for s in sp['comparison_seeds'].values()}|{x['seed']['native_path']for x in sp['support_seeds']+sp['negative_identity_seeds']}
  ref=read(ROOT,core.EP+'ner-legal-precedent.json')['parallel'];files.update([ref['native_path'],ref['raw_path']])
  if read(ROOT,life.CH).get('annotation',{}).get('career_stage')=='fixed_jin098_career_p001_p019':
   from scripts import fixed_jin098_wangdun_career as career
   files.update(set(career.PINS)|{career.TITLES,career.DETAILS})
   files.add(career.fixed(ROOT,'calendar-row-proof.json')['existing_capture_path'])
  for rel in files:q=root/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes((ROOT/rel).read_bytes())
  return t,root
 def test_actual_root_sidecar_origin_drift_and_shadow_denied(self):
  for case in['origin','shadow']:
   t,r=self.mini()
   try:
    if case=='origin':p=r/life.ADDR;x=read(r,life.ADDR);x['assertions'][0]['relation']='birth_place';p.write_text(json.dumps(x,ensure_ascii=False))
    else:p=r/'corpus/jinshu/shadow-life-events.json';p.write_text(json.dumps(self.t['new_life_record'],ensure_ascii=False))
    self.assertTrue(core.source_errors(read(r,life.CH),r),case)
   finally:t.cleanup()
 def test_consistent_whole_pair_UID_rekey_not_pid_whitelist(self):
  t,r=self.mini()
  try:
   old=self.roles['dun'];new='8jk_w4v_a3t';self.assertNotIn(new,self.people)
   def replace(x):
    if isinstance(x,dict):return{k:replace(v)for k,v in x.items()}
    if isinstance(x,list):return[replace(v)for v in x]
    return new if x==old else x
   for p in r.rglob('*.json'):
    x=json.loads(p.read_bytes());y=replace(x)
    if x!=y:p.write_text(json.dumps(y,ensure_ascii=False))
   ch=read(r,life.CH);self.assertEqual(core.source_errors(ch,r),[]);roles=core.resolve(r,ch);self.assertEqual(roles['dun'],new);g=read(r,life.GROUP)['groups'][0];events={e['id']:e for rel in[life.LIFE,life.OLDLIFE]for e in read(r,rel)['events']};cs={ch['id']:ch};c=read(r,'corpus/jinshu/076-wangbin.json');cs[c['id']]=c;people={p['id']:p for p in read(r,'registry/persons.json')['persons']};self.assertTrue(life.group_valid(g,events,cs,people,r))
   p=next(p for p in c['paragraphs']if p['id'].endswith(':line050'));next(m for m in p['mentions']if m['id'].endswith(':m0001'))['person_id']=old;self.assertFalse(life.group_valid(g,events,cs,people,r))
  finally:t.cleanup()
 def test_catalog_mutation_origin_or_age_not_silently_accepted(self):
  from scripts.person_bundle import load_catalog
  people,records=load_catalog(ROOT)
  for kind in['age','origin']:
   rows=copy.deepcopy(list(records))
   if kind=='age':next(r for r in rows if r.get('id')==core.CID)['annotation']['age_assertions'][0]['value']=60
   else:next(r for r in rows if r.get('record_type')=='person_address_assertion_set'and r.get('chapter_id')==core.CID)['assertions'][0]['relation']='birth_place'
   with self.assertRaises(ValueError):validated_groups(rows,people,ROOT,person_ids={self.roles['shenchong']})
 def test_active_stage_cannot_disappear_from_passed_catalog(self):
  from scripts.person_bundle import load_catalog
  people,records=load_catalog(ROOT)
  rows=[r for r in records if r.get('record_type')!='person_life_event_group_set']
  with self.assertRaises(ValueError):validated_groups(rows,people,ROOT,person_ids={self.roles['dun']})
  rows=[r for r in rows if r.get('chapter_id')!=core.CID and r.get('id')!=core.CID]
  with self.assertRaises(ValueError):validated_groups(rows,people,ROOT,person_ids={self.roles['dun']})
 def test_legacy_empty_catalog_has_no_groups_and_malformed_rejected(self):
  with tempfile.TemporaryDirectory()as empty:self.assertEqual(validated_groups([],{},Path(empty)),[])
  self.assertEqual(validated_groups([],{},ROOT,person_ids={'unrelated-request'}),[])
  for records in[None,[None],1]:
   with self.assertRaises(ValueError):validated_groups(records,{},ROOT)
if __name__=='__main__':unittest.main()
