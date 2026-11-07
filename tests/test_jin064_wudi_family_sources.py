import copy,json,unittest
from pathlib import Path
from unittest.mock import patch
try:from scripts import jin064_wudi_family_sources as owner
except ImportError:import jin064_wudi_family_sources as owner
ROOT=Path(__file__).resolve().parents[1]
class ReceivedJin064FamilySources(unittest.TestCase):
 def fixture(self):
  raw=lambda p:(ROOT/p).read_bytes()
  return ROOT,raw,{p['id']:p for p in json.loads(raw('registry/persons.json'))['persons']}
 def setup(self):
  root,raw,people=self.fixture();c,roles,docs=owner._proof(raw,people);return root,raw,people,c,roles,docs
 def changed(self,rel,mutate):
  root,raw,people,c,roles,docs=self.setup();d=json.loads(raw(rel));mutate(d);b=json.dumps(d,ensure_ascii=False).encode();return lambda p:b if p==rel else raw(p),people
 def test_01_actual_full_units_roles_reverse_and_parent_owner(self):
  root,raw,people,c,roles,docs=self.setup();ch=docs[c['chapter_path']];self.assertEqual(len(ch['paragraphs']),21);self.assertEqual(len(roles),69);self.assertEqual(sum(len(p['mentions'])for p in ch['paragraphs']),217)
  try:from scripts.received_sima_family_sources import _proof as parent
  except ImportError:from received_sima_family_sources import _proof as parent
  parent(raw,people)
 def test_02_all_name_components_normal_courtesy(self):
  _,_,_,c,roles,docs=self.setup()
  try:from scripts.person_bundle import validate_courtesy_name
  except ImportError:from person_bundle import validate_courtesy_name
  for d in docs.values():
   if d.get('record_type')=='person_name_component_set':
    for n in d['records']:validate_courtesy_name(n)
 def test_03_han_aidi_primary_name_not_courtesy_or_native_fake_anchor(self):
  _,raw,_,c,roles,docs=self.setup();n=next(n for d in docs.values()for n in d.get('records',[])if n.get('person_id')==roles['han_aidi']);self.assertEqual(n['ming'],'欣');self.assertNotIn('zi',n);self.assertNotIn('source_anchor',n);self.assertEqual(n['primary_given_name_basis']['taboo_substitute_character'],'喜');self.assertFalse(n['primary_given_name_basis'].get('image_verified',False))
  cap=json.loads(raw(c['primary_reference_path']));u=cap['units'][0];a=n['primary_given_name_basis'];self.assertEqual(u['received_text'][a['start']:a['end']],'欣');self.assertTrue(all(u['actual_print_edition']is None and u['fixed_body_obtained']is False for u in cap['units']))
 def test_04_pronouns_have_no_name_alias_and_render_normally(self):
  _,_,_,c,roles,docs=self.setup();ch=docs[c['chapter_path']]
  try:from scripts.render_corpus import render
  except ImportError:from render_corpus import render
  xml=render(ch);self.assertEqual(xml.count('type="pronoun"'),5);self.assertEqual(xml.count('<persName '),212)
 def test_05_unknown_son_is_separate_from_xiang_and_has_no_personal_name(self):
  _,_,_,_,roles,docs=self.setup();self.assertNotEqual(roles['yan_unnamed_eldest'],roles['xiang']);n=next(n for d in docs.values()for n in d.get('records',[])if n.get('person_id')==roles['yan_unnamed_eldest']);self.assertIsNone(n['ming']);self.assertTrue(n['designation_not_personal_name'])
 def test_06_brother_relative_and_maternal_grandfather_existing_schema(self):
  _,_,_,_,roles,docs=self.setup();aa=[a for d in docs.values()for a in d.get('assertions',[])];a=next(a for a in aa if a['id']=='a-jin064-yan-older-brother-yun');self.assertEqual(a['predicate'],'brother');self.assertEqual(a['qualifiers']['relative_birth_order']['older_person_id'],roles['yun']);g=next(a for a in aa if a['id']=='a-jin064-qin-maternal-grandfather-hui');self.assertEqual(g['predicate'],'grandfather');self.assertEqual(g['qualifiers']['lineage'],'maternal');self.assertEqual(g['qualifiers']['mother_person_id'],roles['m_zhoufei'])
 def test_07_ritual_succession_does_not_replace_biological_father(self):
  _,_,_,_,roles,docs=self.setup();aa=[a for d in docs.values()for a in d.get('assertions',[])];self.assertEqual(len({a['id']for a in aa}),len(aa));self.assertEqual(sum(a['predicate']=='ritual_successor_of'for a in aa),10);self.assertTrue(any(a['predicate']=='father'and a['subject_person_id']==roles['min']and a['object_person_id']==roles['yan']for a in aa));self.assertTrue(any(a['predicate']=='ritual_successor_of'and a['subject_person_id']==roles['min']and a['object_person_id']==roles['jian_wudi_son']for a in aa))
 def test_08_missing_reverse_rejected(self):
  _,raw,people,c,roles,docs=self.setup();p=copy.deepcopy(people);p[roles['han_aidi']]['evidence']=[e for e in p[roles['han_aidi']]['evidence']if e.get('mention_id')not in c['role_current_mids']['han_aidi']]
  with self.assertRaises(AssertionError):owner._proof(raw,p)
 def test_09_pronoun_name_alias_rejected(self):
  _,raw,people,c,roles,docs=self.setup();p=copy.deepcopy(people);mid=next(iter(c['pronoun_rules']));r=c['pronoun_rules'][mid]['source_role'];p[roles[r]]['aliases'].append({'surface':c['pronoun_rules'][mid]['surface'],'mention_ids':[mid]})
  with self.assertRaises(AssertionError):owner._proof(raw,p)
 def test_10_human_false_is_not_zero(self):
  _,_,_,c,_,_=self.setup();rel=next(p for p in c['expected_documents']if p.endswith('-name-components.json'));raw,people=self.changed(rel,lambda d:d['records'][0].update(human_reviewed=0))
  with self.assertRaises(AssertionError):owner._proof(raw,people)
 def test_11_anchor_zero_is_not_false(self):
  _,_,_,c,_,_=self.setup();raw,people=self.changed(c['chapter_path'],lambda d:d['paragraphs'][0]['mentions'][0].update(start=False))
  with self.assertRaises(AssertionError):owner._proof(raw,people)
 def test_12_print_qualification_cannot_be_upgraded(self):
  _,_,_,c,_,_=self.setup();raw,people=self.changed(c['primary_reference_path'],lambda d:d['units'][0].update(image_verified=True))
  with self.assertRaises(AssertionError):owner._proof(raw,people)
 def test_13_maternal_not_paternal(self):
  _,_,_,c,_,_=self.setup();rel=next(p for p in c['expected_documents']if p.endswith('-assertions.json'))
  def mutate(d):next(a for a in d['assertions']if a['id']=='a-jin064-qin-maternal-grandfather-hui')['qualifiers']['lineage']='paternal'
  raw,people=self.changed(rel,mutate)
  with self.assertRaises(AssertionError):owner._proof(raw,people)
 def test_14_ritual_not_biological_or_adoptive_father(self):
  _,_,_,c,_,_=self.setup();rel=next(p for p in c['expected_documents']if p.endswith('-assertions.json'))
  def mutate(d):next(a for a in d['assertions']if a['predicate']=='ritual_successor_of')['predicate']='adoptive_father'
  raw,people=self.changed(rel,mutate)
  with self.assertRaises(AssertionError):owner._proof(raw,people)
 def test_15_wrong_person_with_all_native_reverse_still_rejected(self):
  _,raw,people,c,roles,docs=self.setup();old=roles['han_aidi'];wrong=roles['huai']
  def swap(x):
   if isinstance(x,dict):return{k:swap(v)for k,v in x.items()}
   if isinstance(x,list):return[swap(v)for v in x]
   return wrong if x==old else x
  p=copy.deepcopy(people);p[wrong]['evidence']+=p[old]['evidence'];p[wrong]['aliases']+=p[old]['aliases'];p.pop(old)
  def changed(rel):return json.dumps(swap(json.loads(raw(rel))),ensure_ascii=False).encode()if rel in c['expected_documents']else raw(rel)
  with self.assertRaises(AssertionError):owner._proof(changed,p)
 def test_16_legitimate_coherent_rekey_preserves_opaque_ids_and_captures(self):
  _,raw,people,c,roles,docs=self.setup();old=roles['han_aidi'];new='q0q_q0q_q0q';self.assertNotIn(new,people)
  def swap(x):
   if isinstance(x,dict):return{k:swap(v)for k,v in x.items()}
   if isinstance(x,list):return[swap(v)for v in x]
   return new if x==old else x
  p=swap(copy.deepcopy(people));p[new]=p.pop(old);p[new]['id']=new
  def changed(rel):
   if rel in c['expected_documents']:return json.dumps(swap(json.loads(raw(rel))),ensure_ascii=False).encode()
   return raw(rel)
  _,r,e=owner._proof(changed,p);self.assertEqual(r['han_aidi'],new)
  for rel,d in docs.items():
   if d.get('record_type')=='marked_chapter':self.assertEqual([(q['id'],q['text'],[(m['id'],m['start'],m['end'],m['surface'])for m in q['mentions']])for q in d['paragraphs']],[(q['id'],q['text'],[(m['id'],m['start'],m['end'],m['surface'])for m in q['mentions']])for q in e[rel]['paragraphs']])
   if d.get('record_type')=='person_assertion_set':self.assertEqual([a['id']for a in d['assertions']],[a['id']for a in e[rel]['assertions']])
  self.assertEqual(raw(c['capture_path']),changed(c['capture_path']));self.assertEqual(raw(c['primary_reference_path']),changed(c['primary_reference_path']))
 def test_17_caller_only_new_owner_theft_rejected(self):
  root,raw,people,c,roles,docs=self.setup();records=copy.deepcopy(list(docs.values()));fake='z9z_z9z_z9z';ch=next(d for d in records if d.get('record_type')=='marked_chapter');ch['paragraphs'][0]['mentions'][0]['person_id']=fake
  with patch.object(owner,'_raw',lambda r,p:raw(p)):
   with self.assertRaisesRegex(ValueError,'caller/physical'):owner.guard_bundle(root,fake,people,records)
 def test_18_current_caller_entry_proves_full_source(self):
  root,raw,people,c,roles,docs=self.setup()
  with patch.object(owner,'_raw',lambda r,p:raw(p)):owner.guard_bundle(root,roles['qin'],people,list(docs.values()))
 def test_19_missing_contract_caller_only_rejected(self):
  root,raw,people,c,roles,docs=self.setup();base=Path(__file__).resolve().parents[1]
  # A zero-file path is enough: this branch must see caller source even without physical installation.
  nonexistent=base/'__test_no_received_sources__'
  self.assertFalse(nonexistent.exists())
  with self.assertRaisesRegex(ValueError,'without contract'):owner.guard_bundle(nonexistent,roles['qin'],people,list(docs.values()))
 def test_20_new_role_identity_binding_missing_rejected(self):
  _,raw,people,c,roles,docs=self.setup();p=copy.deepcopy(people);p[roles['han_aidi']].pop('source_identity_bindings')
  with self.assertRaises(AssertionError):owner._proof(raw,p)
 def test_21_xml_only_installation_missing_contract_rejected(self):
  import tempfile
  with tempfile.TemporaryDirectory(prefix='jin064-owner-small-')as d:
   root=Path(d);f=root/'corpus/jinshu/064-wudi-sons-rendered.xml';f.parent.mkdir(parents=True);f.write_text('<text/>')
   self.assertTrue(owner.errors(root))
 def test_22_taboo_substitute_cannot_be_courtesy_name(self):
  _,_,_,c,_,_=self.setup();rel=next(p for p in c['expected_documents']if p.endswith('-name-components.json'))
  def mutate(d):next(n for n in d['records']if n['id']=='name-jin064-han_aidi')['zi']='喜'
  raw,people=self.changed(rel,mutate)
  with self.assertRaises(AssertionError):owner._proof(raw,people)
if __name__=='__main__':unittest.main()
