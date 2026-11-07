import unittest,json,copy,hashlib,tempfile,shutil
from pathlib import Path
from scripts.fixed_jin098_wangdun_comparison import source_errors,CID,RAW
ROOT=Path(__file__).resolve().parents[1];CH='corpus/jinshu/098-wangdun-comparison.json'
class Jin098ComparisonSource(unittest.TestCase):
 def setUp(self):self.ch=json.loads((ROOT/CH).read_bytes())
 def reject(self,x):self.assertTrue(source_errors(x,ROOT))
 def test_complete_scope_and_true_layer(self):
  self.assertEqual(source_errors(self.ch,ROOT),[]);self.assertEqual(len(self.ch['paragraphs']),41);self.assertEqual(sum(len(p['text'])for p in self.ch['paragraphs']),7827);self.assertEqual([p['id']for p in self.ch['paragraphs']if p['text_layer']=='received_compiler_appraisal'],[CID+':p041'])
 def test_no_promoted_edition_or_human(self):
  for change in [('image_verified',True),('edition','武英殿本')]:
   x=copy.deepcopy(self.ch);x['source'][change[0]]=change[1];self.reject(x)
  x=copy.deepcopy(self.ch);x['annotation']['human_reviewed']=True;self.reject(x)
 def test_embedded_false_death_edict_not_appraisal(self):
  for n in [4,7,12,22,23,24]:
   x=copy.deepcopy(self.ch);x['paragraphs'][n]['text_layer']='received_compiler_appraisal';self.reject(x)
 def test_appraisal_must_not_be_ordinary_body_or_note(self):
  for v in ['received_chapter','witness_appended_wuyingdian_collation','witness_appended_pei_songzhi_note']:
   x=copy.deepcopy(self.ch);x['paragraphs'][40]['text_layer']=v;self.reject(x)
 def test_body_and_source_role_drift(self):
  for k,v in [('work_id','w-songshu'),('book_id','b-jinshu-033'),('source_id','other'),('id','other')]:
   x=copy.deepcopy(self.ch);x[k]=v;self.reject(x)
  x=copy.deepcopy(self.ch);x['paragraphs'][0]['text']=x['paragraphs'][0]['text'].replace('基','某',1);self.reject(x)
 def test_bad_projection_or_extent(self):
  for field,val in [('raw_projection_ref','../escape.json'),('unit_key','p040'),('first_line',9999)]:
   x=copy.deepcopy(self.ch);x['paragraphs'][40]['source_position'][field]=val;self.reject(x)
  x=copy.deepcopy(self.ch);x['paragraphs'].pop();self.reject(x)
 def test_raw_actual_digest_and_boundary(self):
  with tempfile.TemporaryDirectory()as t:
   root=Path(t)
   for rel in [RAW,'source-evidence/jin098-wangdun-comparison/source-template.json','source-evidence/jin098-wangdun-comparison/projection.json','source-evidence/jin098-wangdun-comparison/extraction-exclusions.json']:
    q=root/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes((ROOT/rel).read_bytes())
   source_only=json.loads((ROOT/'source-evidence/jin098-wangdun-comparison/source-template.json').read_bytes())
   self.assertEqual(source_errors(source_only,root),[]);(root/RAW).write_bytes((root/RAW).read_bytes()+b'\n');self.assertTrue(source_errors(source_only,root))
 def test_malformed_fail_closed(self):
  for x in [None,[],1,'bad']:self.reject(x)
 def test_title_and_raw_book_order(self):
  self.assertEqual(self.ch['title'],'王敦傳');self.assertEqual(self.ch['source']['title'],'《晉書》卷九十八〈王敦傳〉')
  works=json.loads((ROOT/'registry/works.json').read_bytes());w,=[w for w in works['works']if w['id']=='w-jinshu'];b,=[b for b in w['books']if b['id']=='b-jinshu-098'];ids=b['chapter_ids'];self.assertEqual(len(ids),len(set(ids)));self.assertLess(ids.index(CID),ids.index('c-jinshu-098-huanwen'))
if __name__=='__main__':unittest.main()
