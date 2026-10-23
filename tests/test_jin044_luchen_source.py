# coding:utf-8
import unittest,json,copy,tempfile,hashlib
from pathlib import Path
try:
 from scripts.fixed_wikisource_units import source_errors
 from scripts.fixed_biography_subsections import project
except ImportError:
 from fixed_wikisource_units import source_errors
 from fixed_biography_subsections import project
ROOT=Path(__file__).resolve().parents[1];REL='corpus/jinshu/044-luchen-cuiyue.json';PIN='scripts/fixed_attached_subsection_witnesses.json';J=lambda v:json.dumps(v,ensure_ascii=False,indent=2)+'\n'
class CompleteAttachedSelection(unittest.TestCase):
 def setUp(self):
  self.ch=json.loads((ROOT/REL).read_text());self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name).resolve();self.pin=json.loads((ROOT/PIN).read_text());self.ref=self.ch['annotation']['fixed_wikisource_unit_ref'];self.raw=self.ch['source']['raw_file']
  for rel in(PIN,self.ref,self.raw):
   f=self.root/rel;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes((ROOT/rel).read_bytes())
 def bad(self,c=None):self.assertTrue(source_errors(c or self.ch,self.root))
 def test_current_complete_body(self):
  self.assertEqual(source_errors(self.ch,self.root),[]);self.assertEqual(len(self.ch['paragraphs']),4);self.assertEqual([len(p['text'])for p in self.ch['paragraphs']],[164,195,112,59])
 def test_drop_ref_rejected(self):
  del self.ch['annotation']['fixed_wikisource_unit_ref'];self.bad()
 def test_changed_projection_type_no_downgrade(self):
  b=json.loads((self.root/self.ref).read_text());b['record_type']='fixed_wikisource_complete_units';(self.root/self.ref).write_text(J(b));self.bad()
 def test_wrong_level(self):
  b=json.loads((self.root/self.ref).read_text());b['selection']['opening_heading']='==志子諶==';(self.root/self.ref).write_text(J(b));self.bad()
 def test_wrong_closing_heading(self):
  b=json.loads((self.root/self.ref).read_text());b['selection']['following_heading']='==盧欽==';(self.root/self.ref).write_text(J(b));self.bad()
 def test_source_body_edit(self):self.ch['paragraphs'][0]['text']=self.ch['paragraphs'][0]['text'].replace('主薄','主簿');self.bad()
 def test_drop_final_attached_biography(self):self.ch['paragraphs'].pop();self.bad()
 def test_duplicate_paragraph_id(self):self.ch['paragraphs'][-1]['id']=self.ch['paragraphs'][0]['id'];self.bad()
 def test_wrong_raw_offset(self):self.ch['paragraphs'][0]['source_position']['raw_character_offsets'][0]+=1;self.bad()
 def test_co_shift_rehash_still_rejected(self):
  f=self.root/self.raw;f.write_bytes(b'\n'+f.read_bytes());sha=hashlib.sha256(f.read_bytes()).hexdigest();b=json.loads((self.root/self.ref).read_text());b['raw_sha256']=sha;b['selection']['start']+=1;b['selection']['end']+=1
  for k in('wikitext_sha256','raw_file_sha256'):self.ch['source'][k]=sha
  (self.root/self.ref).write_text(J(b));self.bad()
 def test_wrong_source_revision(self):self.ch['source']['revision_id']+=1;self.bad()
 def test_existing_main_heading_projection_api(self):
  raw='==甲==\n　　甲好《[[老子|老]]》，{{YL|永和六年}}。\n\n===乙===\n乙來。\n\n==丙==\n後文。\n';a,z,ps,ex=project(raw,'甲傳');self.assertEqual([p['text']for p in ps],['甲好《老》，永和六年。','乙來。']);self.assertEqual(raw[z:z+5],'==丙==')
 def test_synthetic_third_level_full_display(self):
  raw='前文\n===某子乙===\n乙讀《[[古書|短題]]》，{{YL|某年}}。\n\n===丙===\n丙來。\n\n==丁==\n別傳。';a,z,ps,ex=project(raw,'附傳選錄','===某子乙===');self.assertEqual([p['text']for p in ps],['乙讀《短題》，某年。','丙來。']);v={i for p in ps for i in p['raw_character_offsets']};x={i for q in ex for i in range(q['start'],q['end'])};self.assertFalse(v&x);self.assertEqual(v|x,set(range(a,z)))
 def test_two_headings_preserved(self):self.assertEqual([h['raw_text']for h in self.ch['annotation']['preserved_source_headings']],['===志子諶===','===崔悅==='])
 def test_place_liaoxi_not_duan_liao(self):
  p=next(p for p in self.ch['paragraphs']if p['id'].endswith(':p002'));self.assertEqual(sum(m['surface']=='遼'for m in p['mentions']),1)
  for m in p['mentions']:
   if m['surface']=='遼':self.assertNotEqual(p['text'][m['end']:m['end']+1],'西')
 def test_mother_role_not_rebound_to_from_mother(self):
  p=next(p for p in self.ch['paragraphs']if p['id'].endswith(':p001'));m=next(m for m in p['mentions']if m['surface']=='母');a=next(m for m in p['mentions']if m['surface']=='從母');w=next(m for m in p['mentions']if m['surface']=='妻');self.assertNotEqual(m['person_id'],a['person_id']);self.assertEqual(a['person_id'],w['person_id'])
 def test_work_entities_not_people(self):
  works=[m for p in self.ch['paragraphs']for m in p['mentions']if m['kind']=='work'];self.assertEqual(len(works),5);self.assertTrue(all(m['person_id']is None for m in works));self.assertEqual({m['work_id']for m in works if m['surface']in('莊','莊子')},{'w-zhuang-jin043-shantao-reference'})
 def test_ambiguous_wife_children_and_groups_unresolved(self):
  ms=[m for p in self.ch['paragraphs']for m in p['mentions']if m['surface']in('妻子','石氏','諸子','兄弟')];self.assertTrue(ms);self.assertTrue(all(m['person_id']is None for m in ms))
if __name__=='__main__':unittest.main()
