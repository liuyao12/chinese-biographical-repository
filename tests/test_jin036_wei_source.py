from pathlib import Path
import unittest,tempfile,shutil,json,copy,hashlib
from scripts import fixed_jin036_wei_comparison as h
ROOT=Path(__file__).resolve().parents[1]
class WeiSource(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)/'root';self.root.mkdir();self.original={}
  for rel in [h.CH]+[h.BASE+x for x in h.PINS]:
   src=ROOT/rel;self.original[rel]=hashlib.sha256(src.read_bytes()).hexdigest();dest=self.root/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest);self.assertNotEqual(src.stat().st_ino,dest.stat().st_ino)
  self.addCleanup(self.unchanged)
  source_only=json.loads((self.root/(h.BASE+'contract.json')).read_bytes())['chapter_template']
  (self.root/h.CH).write_text(json.dumps(source_only,ensure_ascii=False,indent=2)+'\n')
  self.ch=json.loads((self.root/h.CH).read_bytes())
 def unchanged(self):
  for rel,sha in self.original.items():self.assertEqual(hashlib.sha256((ROOT/rel).read_bytes()).hexdigest(),sha)
 def reject(self,ch=None):self.assertTrue(h.source_errors(self.ch if ch is None else ch,self.root,source_path=self.root/h.CH))
 def test_complete_source_and_projection(self):
  self.assertEqual(h.source_errors(self.ch,self.root,source_path=self.root/h.CH),[]);self.assertEqual(self.ch['annotation']['status'],'in_progress');self.assertEqual(len(self.ch['paragraphs']),21);self.assertEqual(sum(len(p['text'])for p in self.ch['paragraphs']),7129);self.assertTrue(all(p['mentions']==[]and p['annotation_status']=='pending'for p in self.ch['paragraphs']))
 def test_four_styles_complete_not_heading_or_note(self):
  texts=[p['text']for p in self.ch['paragraphs']];full,=[x for x in texts if x.startswith('昔在黃帝，創制造物。')];self.assertIn('邕作《篆勢》曰',full);self.assertIn('作《隸勢》曰',full);self.assertIn('崔瑗作《草書勢》曰',full);self.assertTrue(full.endswith('略舉大較，仿佛若斯。」'));self.assertFalse(any(x in ['衛瓘','子 恆','恆子 璪','璪弟 玠']for x in texts))
 def test_modern_digital_note_not_received_date(self):
  note,=self.ch['annotation']['modern_collation_reports'];self.assertEqual(note['raw_text'],'《武帝纪》：泰始七年八月丙戌任命');self.assertFalse(note['human_reviewed']);self.assertFalse(note['image_verified']);self.assertNotIn('[1]',''.join(p['text']for p in self.ch['paragraphs']));self.assertNotIn(note['raw_text'],''.join(p['text']for p in self.ch['paragraphs']));self.assertNotIn('normalized_date',json.dumps(self.ch))
 def test_received_letter_and_four_styles_remain_body(self):
  self.assertTrue(all(p['text_layer']=='received_chapter'for p in self.ch['paragraphs']));self.ch['paragraphs'][13]['text_layer']='witness_appended_pei_songzhi_note';self.reject()
 def test_text_or_truncation_rejected(self):
  d=copy.deepcopy(self.ch);d['paragraphs'][0]['text']=d['paragraphs'][0]['text'].replace('高祖','曾祖');self.reject(d);d=copy.deepcopy(self.ch);d['paragraphs'].pop();self.reject(d)
 def test_new_marker_not_silent_ner(self):
  self.ch['paragraphs'][0]['mentions']=[{'id':h.CID+':p001:m0000','start':0,'end':2,'surface':'衛瓘','kind':'person','person_id':'fake'}];self.reject()
 def test_source_header_and_qualification_rejected(self):
  for key,val in [('id','c-wrong'),('book_id','b-jinshu-037'),('source_id','s-wrong')]:
   d=copy.deepcopy(self.ch);d[key]=val;self.reject(d)
  d=copy.deepcopy(self.ch);d['annotation']={};d['id']='c-wrong';d['source_id']='s-wrong';self.reject(d)
  for key,val in [('edition','武英殿'),('image_verified',True),('preferred_text_base',True),('capture_kind','original_wikitext')]:
   d=copy.deepcopy(self.ch);d['source'][key]=val;self.reject(d)
 def test_note_relocation_or_insertion_rejected(self):
  self.ch['annotation']['modern_collation_reports'][0]['capture_note_start']+=1;self.reject();d=json.loads((self.root/h.CH).read_bytes());d['paragraphs'][2]['text']+='泰始七年八月丙戌任命';self.reject(d)
 def test_pin_and_projection_tamper_rejected(self):
  p=self.root/(h.BASE+'projection.json');d=json.loads(p.read_bytes());d['units'][0]['capture_character_offsets'][0]+=1;p.write_text(json.dumps(d));self.reject()
 def test_pending_source_progress_not_completed(self):
  progress=json.loads((ROOT/'corpus/progress.json').read_bytes());entry,=[x for x in progress['books']if x.get('chapter_id')==h.CID];self.assertEqual(entry['person_status'],'in_progress');self.assertIs(entry['complete'],False);self.assertTrue(all(p['annotation_status']=='pending'for p in self.ch['paragraphs']))
 def test_capture_path_escape_rejected(self):
  p=self.root/(h.BASE+'rendered-extract.txt');other=Path(self.tmp.name)/'outside.txt';other.write_bytes(p.read_bytes());p.unlink();p.symlink_to(other);self.reject()
 def test_missing_contract_rejected_foreign_chapter_unchanged(self):
  (self.root/(h.BASE+'contract.json')).unlink();self.reject();self.assertEqual(h.source_errors({'id':'c-other','source_id':'s-other','annotation':{}},self.root),[])
if __name__=='__main__':unittest.main()
