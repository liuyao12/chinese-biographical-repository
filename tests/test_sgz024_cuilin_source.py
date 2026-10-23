# coding:utf-8
"""Complete-source and optional witness-pin regression, not historical proof."""
import copy,hashlib,json,tempfile,unittest
from pathlib import Path
from scripts.fixed_kanripo_projection import errors
ROOT=Path(__file__).resolve().parents[1]
class CuilinSource(unittest.TestCase):
 def setUp(self):
  self.chapter=json.loads((ROOT/'corpus/sanguozhi/024-cuilin.json').read_text())
 def test_actual_complete_unit_and_literal_token(self):
  self.assertEqual(errors(self.chapter,ROOT),[])
  self.assertEqual(len(self.chapter['paragraphs']),10)
  self.assertEqual(sum(p['text_layer']=='witness_appended_pei_songzhi_note'for p in self.chapter['paragraphs']),5)
  self.assertIn('&KR0564;',self.chapter['paragraphs'][4]['text'])
 def fixture(self):
  # Independent synthetic people-free source, fixed revision and physical temp root.
  temp=tempfile.TemporaryDirectory();root=Path(temp.name);base=root/'source-evidence/synthetic';base.mkdir(parents=True);(root/'scripts').mkdir()
  raw='正文甲(注文乙)\n下一傳\n';b=raw.encode();sha=hashlib.sha256(b).hexdigest();rp='source-evidence/synthetic/raw.txt';ref='source-evidence/synthetic/projection.json';(root/rp).write_bytes(b)
  c={'id':'c-synthetic','source':{'revision_id':'fixed-commit','source_commit':'fixed-commit','response_sha256':sha,'url':'https://example.test/raw','permalink':'https://example.test/raw'},'annotation':{'fixed_kanripo_projection_ref':ref},'paragraphs':[]};qs=[]
  for n,(text,pos,layer)in enumerate([('正文甲',[0,1,2],'body'),('注文乙',[4,5,6],'note')]):
   pid='c-synthetic:p'+str(n);c['paragraphs'].append({'id':pid,'text':text,'text_layer':'received_chapter'if layer=='body'else'witness_appended_pei_songzhi_note','source_position':{'first_line':1,'last_line':1,'source_layer':'received_body'if layer=='body'else'pei_annotation','raw_projection_ref':ref}});qs.append({'paragraph_id':pid,'text':text,'raw_positions':pos,'first_line':1,'last_line':1,'source_layer':layer})
  d={'record_type':'fixed_kanripo_complete_unit_projection','witness_key':'synthetic','raw_file':rp,'raw_file_sha256':sha,'source_revision':'fixed-commit','unit':{'first_line':1,'last_line':1,'start':0,'end':9,'raw':raw[:9],'next_line':'下一傳'},'paragraphs':qs};pin={'revision_id':'fixed-commit','raw_sha256':sha,'raw_file':rp,'url':'https://example.test/raw','first_line':1,'last_line':1,'next_line':'下一傳'}
  (root/ref).write_text(json.dumps(d));(root/'scripts/fixed_kanripo_witness_pins.json').write_text(json.dumps({'format_version':'0.1','witnesses':{'synthetic':pin}}));return temp,root,c,d,ref,rp
 def test_synthetic_valid_and_unpinned_legacy(self):
  temp,r,c,d,ref,rp=self.fixture()
  with temp:
   self.assertEqual(errors(c,r),[]);del d['witness_key'];(r/ref).write_text(json.dumps(d));(r/'scripts/fixed_kanripo_witness_pins.json').unlink();self.assertEqual(errors(c,r),[])
 def test_body_change_rejected_even_if_projected_text_agrees(self):
  temp,r,c,d,ref,rp=self.fixture()
  with temp:
   c['paragraphs'][0]['text']='正文改';d['paragraphs'][0]['text']='正文改';(r/ref).write_text(json.dumps(d));self.assertTrue(errors(c,r))
 def test_raw_coedit_and_rehash_rejected_by_pin(self):
  temp,r,c,d,ref,rp=self.fixture()
  with temp:
   raw=(r/rp).read_text().replace('正文甲','正文改');(r/rp).write_text(raw);sha=hashlib.sha256(raw.encode()).hexdigest();c['source']['response_sha256']=d['raw_file_sha256']=sha;d['unit']['raw']=raw[:9];c['paragraphs'][0]['text']=d['paragraphs'][0]['text']='正文改';(r/ref).write_text(json.dumps(d));self.assertTrue(errors(c,r))
 def test_unit_boundary_and_missing_pin_rejected(self):
  temp,r,c,d,ref,rp=self.fixture()
  with temp:
   d['unit']['next_line']='別傳';(r/ref).write_text(json.dumps(d));self.assertTrue(errors(c,r));(r/'scripts/fixed_kanripo_witness_pins.json').unlink();self.assertTrue(errors(c,r))
 def test_book_word_not_quote_word_and_distinct_wang_roles(self):
  p=self.chapter['paragraphs'];yi=[m for m in p[4]['mentions']if m['kind']=='work'and m['surface']=='易'];self.assertEqual(len(yi),1);self.assertEqual(p[4]['text'][yi[0]['end']],'曰')
  m=p[1]['mentions'];get=lambda surface:next(x['person_id']for x in m if x['surface']==surface)
  self.assertEqual(get('雄'),get('王雄'));self.assertNotEqual(get('渾'),get('乂'));self.assertNotEqual(get('戎'),get('衍'));self.assertNotEqual(get('衍'),get('澄'))
if __name__=='__main__':unittest.main()
