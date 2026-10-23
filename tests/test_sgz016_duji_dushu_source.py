# coding:utf-8
import copy,hashlib,json,tempfile,unittest
from pathlib import Path
from scripts.fixed_kanripo_projection import errors
R=Path(__file__).resolve().parents[1];CH='corpus/sanguozhi/016-duji-dushu.json'
class DuJiDuShuSource(unittest.TestCase):
 def setUp(self):
  self.ch=json.loads((R/CH).read_text());self.ps=self.ch['paragraphs'];self.ref=self.ch['annotation']['fixed_kanripo_projection_ref'];self.proj=json.loads((R/self.ref).read_text())
 def fixture(self,root):
  for rel in [self.ref,self.proj['raw_file'],'scripts/fixed_kanripo_witness_pins.json']:
   dest=root/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((R/rel).read_bytes())
 def test_complete44_and_exact7174(self):
  self.assertEqual(len(self.ps),44);self.assertEqual(sum(len(p['text'])for p in self.ps),7174);self.assertEqual(errors(self.ch,R),[])
  self.assertTrue(self.ps[-1]['text'].endswith('王衍時為領軍哭之甚慟'));self.assertNotIn('鄭渾字文公',''.join(p['text']for p in self.ps))
 def test_two_source_layers_and_full_offsets(self):
  self.assertEqual(sum(p['text_layer']=='received_chapter'for p in self.ps),22)
  self.assertEqual(sum(p['text_layer']=='witness_appended_pei_songzhi_note'for p in self.ps),22)
  for p in self.ps:
   for m in p['mentions']:self.assertEqual(p['text'][m['start']:m['end']],m['surface'])
 def test_no_horse_person_or_sima_office_person(self):
  p=self.ps[6];a=p['text'].index('與馬征');self.assertFalse(any(m['start']<a+3 and a<m['end']for m in p['mentions']))
  p=self.ps[37];a=p['text'].index('司馬宋權');self.assertFalse(any(m['kind']=='person'and m['start']==a for m in p['mentions']))
 def test_lvyu_duyu_are_distinct(self):
  a=next(m['person_id']for m in self.ps[27]['mentions']if m['surface']=='預');b=next(m['person_id']for m in self.ps[43]['mentions']if m['surface']=='元凱');self.assertNotEqual(a,b)
 def test_old_jinshu_not_tang_and_author_separate(self):
  a=next(m['work_id']for m in self.ps[31]['mentions']if m['surface']=='晉書');b=next(m['work_id']for m in self.ps[43]['mentions']if m['surface']=='晉書');self.assertNotEqual(a,b);self.assertNotEqual(a,'w-jinshu');self.assertNotEqual(b,'w-jinshu')
  self.assertTrue(any(m['kind']=='person'and m['surface']=='王隐'for m in self.ps[43]['mentions']))
 def test_deletion_or_layer_swap_rejected(self):
  c=copy.deepcopy(self.ch);c['paragraphs']=c['paragraphs'][:-1];self.assertTrue(errors(c,R))
  c=copy.deepcopy(self.ch);c['paragraphs'][1]['text_layer']='received_chapter';self.assertTrue(errors(c,R))
 def test_coherent_raw_metadata_offset_shift_rejected_by_pin(self):
  with tempfile.TemporaryDirectory()as td:
   r=Path(td);self.fixture(r);c=copy.deepcopy(self.ch);d=copy.deepcopy(self.proj);raw=(r/d['raw_file']).read_text();raw='X'+raw;(r/d['raw_file']).write_text(raw);h=hashlib.sha256(raw.encode()).hexdigest();d['raw_file_sha256']=h;c['source']['response_sha256']=h;d['unit']['start']+=1;d['unit']['end']+=1
   for p,q in zip(c['paragraphs'],d['paragraphs']):q['raw_positions']=[x+1 for x in q['raw_positions']]
   (r/self.ref).write_text(json.dumps(d));self.assertTrue(errors(c,r))
 def test_symlink_raw_metadata_or_pin_rejected(self):
  for which in ['raw','metadata','pin']:
   with self.subTest(which=which),tempfile.TemporaryDirectory()as td:
    r=Path(td);self.fixture(r);rel={'raw':self.proj['raw_file'],'metadata':self.ref,'pin':'scripts/fixed_kanripo_witness_pins.json'}[which];q=r/rel;b=q.read_bytes();q.unlink();outside=r/'outside.txt';outside.write_bytes(b);q.symlink_to(outside);self.assertTrue(errors(self.ch,r))
if __name__=='__main__':unittest.main()
