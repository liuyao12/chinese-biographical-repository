"""Independent synthetic HTTP-text witness: no real identity or institution whitelist."""
import unittest,tempfile,json,hashlib,copy
from pathlib import Path
from scripts.epitaph_transcription_witness import errors
class DatabaseEpitaphWitness(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
  self.text='故沈君墓誌。君名澄，未載撰刻日期。'
  sha=lambda x:hashlib.sha256(x.encode()).hexdigest()
  base='source-evidence/synthetic/';url='http://example.org/public/stone'
  self.t={'text':self.text,'length':len(self.text),'text_sha256':sha(self.text),'captured_article_field':"article: '"+self.text+"',",'fragment_sha256':sha("article: '"+self.text+"',"),'normalization':'none','human_reviewed':False,'original_stone_or_rubbing_image_verified':False}
  self.cap={'url':url,'public_http_status':200,'article_sha256':sha(self.text),'article_codepoints':len(self.text),'raw_response_sha256':sha('synthetic response'),'raw_response_bytes':10000,'source_codepoint_span':[100,100+len(self.text)],'source_utf8_byte_span':[100,100+len(self.text.encode())]}
  self.meta={'record_key':'synthetic-17','institution':'合成機構','reported_transcription_origin':'合成字串來源'}
  self.w={'kind':'institutional_database_epitaph_transcription','institution':'合成機構','database_record_id':'synthetic-17','reported_transcription_origin':'合成字串來源','transcription_path':base+'text.json','capture_path':base+'capture.json','metadata_path':base+'meta.json','original_stone_or_rubbing_image_verified':False,'underlying_rubbing_personally_accessed':False,'transcription_page_visually_checked':False,'scope':'complete_single_inscription_not_modern_article'}
  self.c={'work_id':'w-fixture','book_id':'b-fixture','source':{'transcription_witness':self.w,'revision_id':None,'url':url,'permalink':url,'image_verified':False,'text_scope':'complete_work','license_scope':'classical_inscription_text_only','rights':'合成古文測試，非原圖授權'},'annotation':{'human_reviewed':False},'paragraphs':[{'text':self.text,'text_layer':'epitaph_as_modernly_transcribed','source_position':{'kind':'institutional_database_epitaph_transcription','source_text_start':0,'source_text_end':len(self.text),'editorial_single_paragraph':True,'physical_line_divisions_inferred':False}}]}
  self.works={'w-fixture':{'work_type':'single_epitaph','books':[{}],'numbering_note':'編輯單文容器'}}
  self.books={'b-fixture':{'unit_kind':'editorial_single_text_container','number':None,'original_volume_number':None}}
 def check(self):
  for rel,data in [('text.json',self.t),('capture.json',self.cap),('meta.json',self.meta)]:
   p=self.root/'source-evidence/synthetic'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,ensure_ascii=False))
  return errors(self.c,self.root,self.works,self.books)
 def test_complete_synthetic_text_is_accepted(self):self.assertEqual(self.check(),[])
 def test_cannot_claim_original_image_collation(self):self.w['original_stone_or_rubbing_image_verified']=True;self.assertTrue(self.check())
 def test_cannot_fake_wikisource_revision(self):self.c['source']['revision_id']=42;self.assertTrue(self.check())
 def test_partial_inscription_is_not_full_work(self):self.c['source']['text_scope']='partial_chapter';self.assertTrue(self.check())
 def test_truncated_body_is_rejected(self):self.c['paragraphs'][0]['text']=self.text[:-1];self.assertTrue(self.check())
 def test_mutated_transcription_is_rejected(self):self.t['text']=self.text.replace('澄','岑');self.assertTrue(self.check())
 def test_wrong_utf8_offset_is_rejected(self):self.cap['source_utf8_byte_span'][1]-=1;self.assertTrue(self.check())
 def test_wrong_record_key_is_rejected(self):self.meta['record_key']='another';self.assertTrue(self.check())
 def test_wrong_public_url_is_rejected(self):self.cap['url']='http://example.org/other';self.assertTrue(self.check())
 def test_wrong_http_status_is_rejected(self):self.cap['public_http_status']=403;self.assertTrue(self.check())
 def test_fake_original_volume_is_rejected(self):self.books['b-fixture']['number']=1;self.assertTrue(self.check())
 def test_guessed_stone_line_divisions_are_rejected(self):self.c['paragraphs'][0]['source_position']['physical_line_divisions_inferred']=True;self.assertTrue(self.check())
 def test_path_traversal_is_rejected(self):self.w['capture_path']='source-evidence/../../foreign.json';self.assertTrue(self.check())
 def test_another_root_cannot_read_first_root_evidence(self):
  self.assertEqual(self.check(),[])
  with tempfile.TemporaryDirectory() as other:self.assertTrue(errors(self.c,Path(other),self.works,self.books))

class PublicReferenceURL(unittest.TestCase):
 def test_http_and_https(self):
  from scripts.work_provenance import public_reference_url
  for url in ('http://example.org/public/stone?id=7','https://example.org/public/stone?id=7'):
   with self.subTest(url=url):self.assertTrue(public_reference_url(url))
 def test_active_and_nonweb_schemes_are_rejected(self):
  from scripts.work_provenance import public_reference_url
  for url in ('javascript:alert(1)','data:text/html,test','ftp://example.org/file','//example.org/file'):
   with self.subTest(url=url):self.assertFalse(public_reference_url(url))
 def test_credentials_are_rejected(self):
  from scripts.work_provenance import public_reference_url
  for url in ('http://reader:secret@example.org/stone','https://reader@example.org/stone'):
   with self.subTest(url=url):self.assertFalse(public_reference_url(url))
 def test_malformed_urls_are_rejected(self):
  from scripts.work_provenance import public_reference_url
  for url in ('https://','http://example.org/\nother',None,' https://example.org/stone'):
   with self.subTest(url=url):self.assertFalse(public_reference_url(url))

if __name__=='__main__':unittest.main()
