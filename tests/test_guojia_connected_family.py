# coding: utf-8
import unittest,json,copy,hashlib,tempfile
from pathlib import Path
from scripts.person_bundle import load_catalog,bundle
from scripts.family_assemblies import load_assemblies
from scripts.retired_person_ids import retired_person_ids,allocation_conflicts,assert_not_retired
from scripts.person_ids import allocate_child_id
R=Path(__file__).resolve().parents[1];OLD=['nnw_j0s_5au','odr_hn1_oxu','zyd_bs5_fiv'];ROOT='344_68f_98e';NEW=[ROOT+'_AA',ROOT+'_AAA',ROOT+'_*A'];FAMILY='family-yingchuan-guo-jia-core';BASE='source-evidence/guojia-family-assembly';read=lambda p:json.loads(p.read_bytes())
class GuojiaConnectedFamily(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.cat=load_catalog(R);cls.source,cls.assembled=load_assemblies(R,cls.cat);cls.family=next(f for f in read(R/'registry/family-assemblies.json')['assemblies']if f['id']==FAMILY);cls.aa=read(R/'corpus/sanguozhi/014-guojia-assertions.json')['assertions']
 def test_five_nodes_direct_and_missing_parent(self):
  rows={m['person_id']:m for m in self.family['members']};self.assertEqual(set(rows),{ROOT,ROOT+'_A',*NEW});self.assertEqual(rows[NEW[0]]['parent_person_id'],ROOT+'_A');self.assertEqual(rows[NEW[1]]['parent_person_id'],NEW[0]);x=rows[NEW[2]];self.assertIsNone(x['parent_person_id']);self.assertEqual((x['ancestor_person_id'],x['connection'],x['generation_distance']),(ROOT,'grandfather',2));self.assertEqual(x['intermediate_person_ids'],[None]);self.assertNotIn(ROOT+'_*',self.cat[0])
 def test_old_two_members_and_other_guoyi(self):
  rows={m['person_id']:m for m in self.family['members']};self.assertEqual(rows[ROOT]['source_assertion_id'],None);self.assertEqual(rows[ROOT+'_A']['source_assertion_id'],'a-sanguozhi027-wangchang-012');self.assertIn('r02_hoi_pu7_ACA',self.cat[0]);self.assertNotIn('r02_hoi_pu7_ACA',rows)
 def test_actual_source_links_not_editorial_fathers(self):
  for pid,aid in zip(NEW,['a-sgz014-guo-2','a-sgz014-guo-3','a-sgz014-guo-4']):
   row=self.assembled[pid];a=next(a for a in self.aa if a['id']==aid);self.assertEqual(row['source_assertion_id'],aid);self.assertEqual(a['subject_person_id'],pid);self.assertNotIn('parent_connection',row)
  self.assertFalse(any(a['predicate']=='father'and a['subject_person_id']==NEW[2]for a in self.aa))
 def test_retirement_not_alias_or_query(self):
  retired=retired_person_ids(R)
  for pid in OLD:
   self.assertIn(pid,retired);self.assertNotIn(pid,self.cat[0]);self.assertTrue(allocation_conflicts(pid+'_A',retired))
   with self.assertRaises(ValueError):assert_not_retired(pid,R)
   with self.assertRaises(ValueError):allocate_child_id(pid,set(self.cat[0]),root=R)
   with self.assertRaises(ValueError):bundle(pid,R,True,catalog=self.cat)
  self.assertFalse(any(pid in p.get('id_aliases',[])for p in self.cat[0].values()for pid in OLD))
 def test_typed_data_and_complete_name_chain_survive(self):
  for pid,label in zip(NEW,['郭深','郭獵','郭敞']):
   b=bundle(pid,R,True,catalog=self.cat);self.assertTrue(any(n['surname']+n['ming']==label for n in b['name_components']));self.assertEqual(b['canonical_person_id'],pid)
  chang=bundle(NEW[2],R,True,catalog=self.cat);self.assertFalse(chang['address_assertions']);self.assertTrue(any(t['title']=='散騎常侍'for t in chang['title_holdings']));self.assertFalse(any(r['predicate']=='father'and r['subject_person_id']==NEW[2]for r in chang['relations']))
 def test_historical_review_exact_and_current_projection(self):
  q=read(R/(BASE+'/historical-capture-qualification.json'));spec,=q['historical_files'];raw=(R/spec['path']).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),spec['sha256']);initial=json.loads(raw);current=read(R/q['current_review_path']);self.assertTrue(initial['no_rekey']);self.assertTrue(current['historical_initial_import_no_rekey']);self.assertEqual(current['identities']['郭敞']['person_id'],NEW[2]);self.assertEqual(initial['identities']['郭敞']['person_id'],OLD[2]);self.assertFalse(current['current_endpoint_qualification']['person_aliases_created']);self.assertEqual(read(R/'corpus/sanguozhi/014-guojia.json')['annotation']['identity_review_path'],q['current_review_path'])
 def test_forged_known_father_and_generation_rejected(self):
  doc=read(R/'registry/family-assemblies.json');good=dict(format_version=doc['format_version'],record_type=doc['record_type'],assemblies=[copy.deepcopy(self.family)])
  for mutation in('father','generation'):
   bad=copy.deepcopy(good);x=next(m for m in bad['assemblies'][0]['members']if m['person_id']==NEW[2])
   if mutation=='father':x['parent_person_id']=ROOT+'_A'
   else:x['generation_distance']=1
   with tempfile.TemporaryDirectory()as d:
    p=Path(d).resolve();self.assertFalse(p.is_symlink());q=p/'registry/family-assemblies.json';self.assertTrue(q.resolve().is_relative_to(p));q.parent.mkdir();q.write_text(json.dumps(good));self.assertEqual(len(load_assemblies(p,self.cat)[1]),5);q.write_text(json.dumps(bad))
    with self.assertRaisesRegex(ValueError,'缺代'):load_assemblies(p,self.cat)
 def test_native_words_and_anchors_still_fixed(self):
  c=read(R/'corpus/sanguozhi/014-guojia.json');self.assertEqual(sum(len(p['text'])for p in c['paragraphs']),2471);self.assertEqual(sum(m['kind']=='person'for p in c['paragraphs']for m in p['mentions']),236)
  for p in c['paragraphs']:
   for m in p['mentions']:self.assertEqual(p['text'][m['start']:m['end']],m['surface'])
if __name__=='__main__':unittest.main()
