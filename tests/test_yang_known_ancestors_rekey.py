import unittest,json,copy,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class YangAncestorTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.f=next(x for x in json.loads((R/'registry/family-assemblies.json').read_text())['assemblies']if x['id']=='family-hongnong-yang-jie-close');cls.rows={x['person_id']:x for x in cls.f['members']};cls.c=json.loads((R/'corpus/weishu-weishou/058-yangbo-yangkan.json').read_text());cls.a={x['id']:x for x in json.loads((R/'corpus/weishu-weishou/058-yangbo-yangkan-assertions.json').read_text())['assertions']};cls.ch={cls.c['id']:cls.c};cls.inferred=[x for x in cls.f['members']if x.get('parent_connection',{}).get('interpretation_basis')=='punctuated_biography_four_ancestor_office_sequence']
 def test_three_editorial_edges_valid(self):
  from scripts.punctuated_ancestor_offices import valid
  self.assertEqual(len(self.inferred),3)
  for m in self.inferred:self.assertTrue(valid(m,self.rows,self.a,self.ch))
 def test_source_predicates_not_rewritten_as_fathers(self):
  self.assertEqual(len(self.a),13);self.assertEqual([self.a['a-weishu058-yang-'+x]['predicate']for x in ['004','003','002','001']],['ancestor','great_grandfather','grandfather','father'])
  for m in self.inferred:self.assertIsNone(m['source_assertion_id']);self.assertFalse(any(a['predicate']=='father'and a['subject_person_id']==m['person_id']for a in self.a.values()))
 def test_wrong_near_far_or_parent_rejected(self):
  from scripts.punctuated_ancestor_offices import valid
  m=copy.deepcopy(self.inferred[0]);m['parent_connection']['nearer_ancestor_assertion_id']='a-weishu058-yang-001';self.assertFalse(valid(m,self.rows,self.a,self.ch))
  m=copy.deepcopy(self.inferred[0]);m['parent_person_id']=self.inferred[1]['person_id'];self.assertFalse(valid(m,self.rows,self.a,self.ch))
 def test_contrary_father_rejected(self):
  from scripts.punctuated_ancestor_offices import valid
  a=copy.deepcopy(self.a);a['synthetic']={'predicate':'father','subject_person_id':self.inferred[0]['person_id'],'object_person_id':'synthetic-other'};self.assertFalse(valid(self.inferred[0],self.rows,a,self.ch))
 def test_role_mutation_with_consistent_hash_quote_rejected(self):
  from scripts.punctuated_ancestor_offices import valid
  for old,new in [('曾祖','曾父'),('高祖','外祖')]:
   m=copy.deepcopy(self.inferred[0]);ch=copy.deepcopy(self.ch);a=copy.deepcopy(self.a);p=ch[self.c['id']]['paragraphs'][0];p['text']=p['text'].replace(old,new,1);frame=m['parent_connection']['four_ancestor_frame'];frame['paragraph_sha256']=hashlib.sha256(p['text'].encode()).hexdigest()
   for e in frame['entries']:
    for key in ['role_anchor','career_anchor']:
     z=e[key];z['surface']=p['text'][z['start']:z['end']]
   for x in a.values():
    for e in x['evidence']:
     if e.get('paragraph_id')==p['id']:e['quote']=p['text']
   for e in m['parent_connection']['references']:e['quote']=p['text']
   self.assertFalse(valid(m,self.rows,a,ch))
 def test_emperor_time_not_ancestor_or_unqualified_intruder(self):
  from scripts.punctuated_ancestor_offices import valid
  m=copy.deepcopy(self.inferred[0]);m['parent_connection']['four_ancestor_frame']['ruler_time_anchors']=[];self.assertFalse(valid(m,self.rows,self.a,self.ch))
  ch=copy.deepcopy(self.ch);p=ch[self.c['id']]['paragraphs'][0];em=next(x for x in p['mentions']if x['surface']=='太祖');em['person_id']=self.f['root_person_id'];self.assertFalse(valid(self.inferred[0],self.rows,self.a,ch))
 def test_new_named_topic_in_career_rejected(self):
  from scripts.punctuated_ancestor_offices import valid
  ch=copy.deepcopy(self.ch);p=ch[self.c['id']]['paragraphs'][0];n=p['text'].index('上谷');p['mentions'].append({'id':'synthetic-intruder','kind':'person','person_id':'synthetic-other','surface':'上谷','start':n,'end':n+2});self.assertFalse(valid(self.inferred[0],self.rows,self.a,ch))
 def test_retired_prefixes_not_reusable_and_no_alias(self):
  from scripts.retired_person_ids import retired_person_ids,allocation_conflicts
  old=['f6l_n1n_fwc','jl7_5su_pdu','3av_6ul_756','3av_6ul_756_A','3av_6ul_756_AA','3av_6ul_756_AAA','3av_6ul_756_AAB'];ret=retired_person_ids(R);reg={x['id']:x for x in json.loads((R/'registry/persons.json').read_text())['persons']}
  for x in old:self.assertIn(x,ret);self.assertNotIn(x,reg);self.assertTrue(allocation_conflicts(x+'_A',ret))
 def test_historical_bytes_qualified_current_projection(self):
  q=json.loads((R/'source-evidence/yang-known-ancestor-family/historical-captures.json').read_text())
  for x in q['captures']:self.assertEqual(hashlib.sha256((R/x['path']).read_bytes()).hexdigest(),x['sha256']);self.assertTrue((R/x['current_projection_path']).is_file())
 def test_old_unpunctuated_basis_unchanged(self):
  from scripts.ancestry_chain import explicit_four_ancestor_sequence_valid
  for m in self.inferred:
   x=m['parent_connection'];self.assertFalse(explicit_four_ancestor_sequence_valid(self.a[x['nearer_ancestor_assertion_id']],self.a[x['farther_ancestor_assertion_id']],self.a,self.ch))
 def test_no_person_id_allowlist(self):
  from scripts.punctuated_ancestor_offices import valid
  ids={m['person_id']for p in self.c['paragraphs']for m in p['mentions']if m['kind']=='person'};mapping={x:'synthetic-'+str(n)for n,x in enumerate(sorted(ids))}
  def remap(v):
   if isinstance(v,str):return mapping.get(v,v)
   if isinstance(v,list):return[remap(x)for x in v]
   if isinstance(v,dict):return{mapping.get(k,k):remap(x)for k,x in v.items()}
   return v
  for m in self.inferred:self.assertTrue(valid(remap(m),remap(self.rows),remap(self.a),remap(self.ch)))

 def test_malformed_qualifier_fails_closed(self):
  from scripts.punctuated_ancestor_offices import valid
  a=copy.deepcopy(self.a);a['a-weishu058-yang-004']['qualifiers']=[];self.assertFalse(valid(self.inferred[0],self.rows,a,self.ch))

 def test_original_three_edges_and_expanded_family_all_load(self):
  expected={(self.a['a-weishu058-yang-'+near]['object_person_id'],'a-weishu058-yang-'+near,'a-weishu058-yang-'+far)for near,far in [('003','004'),('002','003'),('001','002')]}
  actual={(m['person_id'],m['parent_connection']['nearer_ancestor_assertion_id'],m['parent_connection']['farther_ancestor_assertion_id'])for m in self.inferred};self.assertEqual(actual,expected)
  from scripts.person_bundle import load_catalog
  from scripts.family_assemblies import load_assemblies
  source_map,assembled=load_assemblies(R,load_catalog(R));self.assertGreaterEqual(len(self.f['members']),19)
  for m in self.f['members']:
   self.assertIn(m['person_id'],assembled)
   for pid in m['source_person_ids']:self.assertEqual(source_map[pid]['person_id'],m['person_id'])
