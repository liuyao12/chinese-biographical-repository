# coding:utf-8
import copy,json,hashlib,tempfile,unittest
from pathlib import Path
from scripts.fixed_kanripo_projection import errors
R=Path(__file__).resolve().parents[1];CID='c-sanguozhi-016-duji-dushu';KEY='sgz016-duji-dushu-214fcafa'
class PinnedChapter(unittest.TestCase):
 def setUp(self):
  self.c=json.loads((R/'corpus/sanguozhi/016-duji-dushu.json').read_text());self.ref=self.c['annotation']['fixed_kanripo_projection_ref'];self.d=json.loads((R/self.ref).read_text())
 def prepare(self,r):
  for rel in(self.ref,self.d['raw_file'],'scripts/fixed_kanripo_witness_pins.json'):
   q=r/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes((R/rel).read_bytes())
 def test_current_binding_and_source_valid(self):
  cfg=json.loads((R/'scripts/fixed_kanripo_witness_pins.json').read_text());self.assertEqual(cfg['chapter_bindings'][CID],KEY);self.assertEqual(errors(self.c,R),[])
 def test_delete_key_no_longer_legacy(self):
  with tempfile.TemporaryDirectory()as td:
   r=Path(td);self.prepare(r);d=copy.deepcopy(self.d);d.pop('witness_key');(r/self.ref).write_text(json.dumps(d));self.assertTrue(errors(self.c,r))
 def test_delete_key_and_coherent_raw_shift_rejected(self):
  with tempfile.TemporaryDirectory()as td:
   r=Path(td);self.prepare(r);d=copy.deepcopy(self.d);c=copy.deepcopy(self.c);d.pop('witness_key');raw='X'+(r/d['raw_file']).read_text();(r/d['raw_file']).write_text(raw);h=hashlib.sha256(raw.encode()).hexdigest();d['raw_file_sha256']=h;c['source']['response_sha256']=h;d['unit']['start']+=1;d['unit']['end']+=1
   for q in d['paragraphs']:q['raw_positions']=[n+1 for n in q['raw_positions']]
   (r/self.ref).write_text(json.dumps(d));self.assertTrue(errors(c,r))
 def test_wrong_key_even_identical_witness_rejected(self):
  with tempfile.TemporaryDirectory()as td:
   r=Path(td);self.prepare(r);d=copy.deepcopy(self.d);cfg=json.loads((r/'scripts/fixed_kanripo_witness_pins.json').read_text());cfg['witnesses']['other-key']=copy.deepcopy(cfg['witnesses'][KEY]);d['witness_key']='other-key';(r/self.ref).write_text(json.dumps(d));(r/'scripts/fixed_kanripo_witness_pins.json').write_text(json.dumps(cfg));self.assertTrue(errors(self.c,r))
 def test_unregistered_legacy_without_key_preserves_old_contract(self):
  with tempfile.TemporaryDirectory()as td:
   r=Path(td);self.prepare(r);d=copy.deepcopy(self.d);c=copy.deepcopy(self.c);d.pop('witness_key');c['id']='c-unregistered-legacy-example';(r/self.ref).write_text(json.dumps(d));self.assertEqual(errors(c,r),[])
 def test_binding_to_missing_witness_rejected(self):
  with tempfile.TemporaryDirectory()as td:
   r=Path(td);self.prepare(r);cfg=json.loads((r/'scripts/fixed_kanripo_witness_pins.json').read_text());cfg['chapter_bindings']['c-another']='missing';(r/'scripts/fixed_kanripo_witness_pins.json').write_text(json.dumps(cfg));self.assertTrue(errors(self.c,r))
if __name__=='__main__':unittest.main()
