# coding:utf-8
import copy,hashlib,json,tempfile,unittest
from pathlib import Path
from scripts.fixed_kanripo_projection import errors
class PinBindings(unittest.TestCase):
 def fixture(self,bound=True):
  tmp=tempfile.TemporaryDirectory();r=Path(tmp.name);base=r/'source-evidence/synthetic';base.mkdir(parents=True);(r/'scripts').mkdir();raw='正文甲(注文乙)\n下一傳\n';sha=hashlib.sha256(raw.encode()).hexdigest();rp='source-evidence/synthetic/raw.txt';ref='source-evidence/synthetic/projection.json';(r/rp).write_text(raw)
  c={'id':'c-synthetic','source':{'revision_id':'fixed','source_commit':'fixed','response_sha256':sha,'url':'https://example.test/raw','permalink':'https://example.test/raw'},'annotation':{'fixed_kanripo_projection_ref':ref},'paragraphs':[]};qs=[]
  for n,(text,pos,layer)in enumerate([('正文甲',[0,1,2],'body'),('注文乙',[4,5,6],'note')]):
   pid='c-synthetic:p'+str(n);c['paragraphs'].append({'id':pid,'text':text,'text_layer':'received_chapter'if layer=='body'else'witness_appended_pei_songzhi_note','source_position':{'first_line':1,'last_line':1,'source_layer':'received_body'if layer=='body'else'pei_annotation','raw_projection_ref':ref}});qs.append({'paragraph_id':pid,'text':text,'raw_positions':pos,'first_line':1,'last_line':1,'source_layer':layer})
  d={'record_type':'fixed_kanripo_complete_unit_projection','witness_key':'key-a','raw_file':rp,'raw_file_sha256':sha,'source_revision':'fixed','unit':{'first_line':1,'last_line':1,'start':0,'end':9,'raw':raw[:9],'next_line':'下一傳'},'paragraphs':qs};pin={'revision_id':'fixed','raw_sha256':sha,'raw_file':rp,'url':'https://example.test/raw','first_line':1,'last_line':1,'next_line':'下一傳'};cfg={'format_version':'0.1','witnesses':{'key-a':pin,'key-b':copy.deepcopy(pin)},'chapter_bindings':{'c-synthetic':'key-a'}if bound else{}}
  (r/ref).write_text(json.dumps(d));(r/'scripts/fixed_kanripo_witness_pins.json').write_text(json.dumps(cfg));return tmp,r,c,d,cfg,ref,rp
 def coedit(self,r,c,d,ref,rp):
  raw=(r/rp).read_text().replace('正文甲','正文改');(r/rp).write_text(raw);sha=hashlib.sha256(raw.encode()).hexdigest();c['source']['response_sha256']=d['raw_file_sha256']=sha;d['unit']['raw']=raw[:9];c['paragraphs'][0]['text']=d['paragraphs'][0]['text']='正文改';(r/ref).write_text(json.dumps(d))
 def test_bound_valid(self):
  t,r,c,d,cfg,ref,rp=self.fixture()
  with t:self.assertEqual(errors(c,r),[])
 def test_delete_key_rejected(self):
  t,r,c,d,cfg,ref,rp=self.fixture()
  with t:del d['witness_key'];(r/ref).write_text(json.dumps(d));self.assertTrue(errors(c,r))
 def test_delete_key_coedit_rehash_rejected(self):
  t,r,c,d,cfg,ref,rp=self.fixture()
  with t:del d['witness_key'];self.coedit(r,c,d,ref,rp);self.assertTrue(errors(c,r))
 def test_other_valid_pin_key_cannot_replace_binding(self):
  t,r,c,d,cfg,ref,rp=self.fixture()
  with t:d['witness_key']='key-b';(r/ref).write_text(json.dumps(d));self.assertTrue(errors(c,r))
 def test_unbound_legacy_no_key_unchanged(self):
  t,r,c,d,cfg,ref,rp=self.fixture(False)
  with t:del d['witness_key'];(r/ref).write_text(json.dumps(d));self.assertEqual(errors(c,r),[])
 def test_explicit_trust_boundary_config_removal_is_not_source_proof(self):
  t,r,c,d,cfg,ref,rp=self.fixture()
  with t:
   del d['witness_key'];self.coedit(r,c,d,ref,rp);cfg['chapter_bindings'].clear();(r/'scripts/fixed_kanripo_witness_pins.json').write_text(json.dumps(cfg));self.assertEqual(errors(c,r),[])
 def test_second_registered_chapter_uses_same_generic_contract(self):
  t,r,c,d,cfg,ref,rp=self.fixture()
  with t:
   c['id']='c-other';d['witness_key']='key-b';cfg['chapter_bindings']['c-other']='key-b';(r/ref).write_text(json.dumps(d));(r/'scripts/fixed_kanripo_witness_pins.json').write_text(json.dumps(cfg));self.assertEqual(errors(c,r),[])
 def test_malformed_binding_rejected(self):
  t,r,c,d,cfg,ref,rp=self.fixture()
  with t:cfg['chapter_bindings']['c-synthetic']='missing';(r/'scripts/fixed_kanripo_witness_pins.json').write_text(json.dumps(cfg));self.assertTrue(errors(c,r))
if __name__=='__main__':unittest.main()
