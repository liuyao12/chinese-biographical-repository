import copy,json,tempfile,shutil,unittest
from pathlib import Path
from scripts import fixed_wuyingdian_jin040_jiachong as m
ROOT=Path(__file__).resolve().parents[1]
CH=json.loads((ROOT/'corpus/jinshu/040-wyd1739-jiachong.json').read_bytes())
class Jin040QiCorrection(unittest.TestCase):
 def test_exact_one_glyph_and_preserved_children(self):
  self.assertTrue(m.validate_source(CH,ROOT));p=CH['paragraphs'][21];self.assertEqual(p['text'][48],'係');self.assertIn('大子斃於金酒',p['text']);self.assertIn('小子困於枯木',p['text'])
  raw=(ROOT/(m.BASE+'transcription-columns.txt')).read_bytes();old=(ROOT/(m.BASE+'historical/transcription-columns-before-4b1ca3bc.txt')).read_bytes();self.assertEqual(len(raw),len(old));self.assertEqual([(a,b)for a,b in zip(old.decode(),raw.decode())if a!=b],[('繫','係')]);self.assertEqual(sum(len(p['text'])for p in CH['paragraphs']),5016)
 def bad(self,ch):
  with self.assertRaises(ValueError):m.validate_source(ch,ROOT)
 def test_wrong_dazi_or_xiaozi_rejected(self):
  for phrase in ['大子','小子']:
   ch=copy.deepcopy(CH);p=ch['paragraphs'][21];i=p['text'].index(phrase)+1;p['text']=p['text'][:i]+'女'+p['text'][i+1:];self.bad(ch)
 def test_no_general_character_conversion(self):
  for value in ['繫','系']:
   ch=copy.deepcopy(CH);p=ch['paragraphs'][21];p['text']=p['text'][:48]+value+p['text'][49:];self.bad(ch)
  self.assertEqual(CH['source']['normalization']['character_conversion'],{})
 def fixture(self):
  from tests.test_cbr_jin040_complete_unit import current_source_fixture_paths
  td=tempfile.TemporaryDirectory();self.addCleanup(td.cleanup);root=Path(td.name)
  for rel in current_source_fixture_paths(ROOT):
   out=root/rel;out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/rel,out)
  self.assertTrue(m.validate_source(CH,root))
  return root
 def test_wrong_raw_column_rejected(self):
  root=self.fixture();path=root/(m.BASE+'transcription-columns.txt');lines=path.read_text().splitlines(keepends=True);s=lines[207];lines[207]=s[:6]+'係'+s[7:];path.write_text(''.join(lines))
  with self.assertRaises(ValueError):m.validate_source(CH,root)
 def test_wrong_pdf_or_position_evidence_rejected(self):
  root=self.fixture();path=root/(m.BASE+'ai-transcription-correction-pdf92-r3.json');old=path.read_bytes()
  for mutate in [lambda d:d.update(source_pdf_sha256='0'*64),lambda d:d['correction'].update(raw_line_1based=208),lambda d:d['correction'].update(physical_column_from_right_1based=4)]:
   d=json.loads(old);mutate(d);path.write_text(json.dumps(d,ensure_ascii=False))
   with self.assertRaises(ValueError):m.validate_source(CH,root)
  path.write_bytes(old)
 def test_pending_and_source_flags_not_upgraded(self):
  witness=json.loads((ROOT/(m.BASE+'transcription-witness-contract.json')).read_bytes())
  pending=copy.deepcopy(CH);pending['annotation']=copy.deepcopy(witness['required_annotation']);pending['paragraphs']=copy.deepcopy(witness['paragraphs'])
  self.assertTrue(m.validate_source(pending,ROOT))
  self.assertTrue(all(p['mentions']==[]and p['annotation_status']=='pending'for p in pending['paragraphs']))
  self.assertEqual(CH['annotation']['formal_phase'],m.C40_PHASE)
  self.assertIs(pending['annotation']['human_reviewed'],False);self.assertIsNone(pending['annotation']['model']);self.assertIs(pending['source']['image_verified'],False)
  self.assertIs(CH['annotation']['human_reviewed'],False);self.assertIsNone(CH['annotation']['model']);self.assertIs(CH['source']['image_verified'],False)
  for mutate in [lambda c:c.update(source_id='other'),lambda c:c['source'].update(image_verified=True),lambda c:c['source'].update(raw_sha256='0'*64)]:
   ch=copy.deepcopy(CH);mutate(ch);self.bad(ch)
if __name__=='__main__':unittest.main()
