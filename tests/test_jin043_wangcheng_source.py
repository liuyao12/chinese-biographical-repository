import unittest,json,copy,hashlib
from pathlib import Path
from unittest.mock import patch
try:
 from scripts.fixed_attached_subsection_selection import errors,required_ref_error
except ImportError:
 from fixed_attached_subsection_selection import errors,required_ref_error
ROOT=Path(__file__).resolve().parents[1]
class WangChengSource(unittest.TestCase):
 def setUp(self):
  self.ch=json.loads((ROOT/'corpus/jinshu/043-wangcheng.json').read_text());self.b=json.loads((ROOT/self.ch['annotation']['fixed_wikisource_unit_ref']).read_text())
 def test_full_selected_seven_not_guoshu(self):
  self.assertEqual(errors(self.ch,ROOT,self.b),[]);self.assertEqual([len(p['text'])for p in self.ch['paragraphs']],[103,117,151,145,478,112,274]);self.assertIn('杜弢為主，，',self.ch['paragraphs'][4]['text']);self.assertEqual(self.ch['source']['text_scope'],'partial_chapter')
 def test_no_body_rewrite_even_with_new_text_hash(self):
  ch=copy.deepcopy(self.ch);ch['paragraphs'][4]['text']=ch['paragraphs'][4]['text'].replace('主，，','主，');ch['text_sha256']=hashlib.sha256('\n\n'.join(x['text']for x in ch['paragraphs']).encode()).hexdigest();self.assertTrue(errors(ch,ROOT,self.b))
 def test_wrong_close_and_missing_last_paragraph(self):
  b=copy.deepcopy(self.b);b['selection']['following_heading']='==樂廣==';self.assertTrue(errors(self.ch,ROOT,b));ch=copy.deepcopy(self.ch);ch['paragraphs'].pop();self.assertTrue(errors(ch,ROOT,self.b))
 def test_cannot_drop_source_binding(self):
  ch=copy.deepcopy(self.ch);ch['annotation'].pop('fixed_wikisource_unit_ref');self.assertTrue(required_ref_error(ch,ROOT))
 def test_coshift_new_raw_and_hash_not_trusted(self):
  ch=copy.deepcopy(self.ch);b=copy.deepcopy(self.b);data=(ROOT/b['raw_file']).read_bytes();new=b'\n'+data;digest=hashlib.sha256(new).hexdigest();ch['source']['raw_file_sha256']=ch['source']['wikitext_sha256']=digest;b['raw_sha256']=digest
  original=Path.read_bytes
  with patch.object(Path,'read_bytes',lambda f:new if f==ROOT/b['raw_file']else original(f)):
   self.assertTrue(errors(ch,ROOT,b))
 def test_marks_precise_and_core_identity_not_new_duplicate(self):
  people={x['id']:x for x in json.loads((ROOT/'registry/persons.json').read_text())['persons']}
  for p in self.ch['paragraphs']:
   for m in p['mentions']:
    self.assertEqual(p['text'][m['start']:m['end']],m['surface'])
    if m.get('person_id'):self.assertIn(m['person_id'],people)
  first=self.ch['paragraphs'][0]['mentions'][0];self.assertEqual(first['surface'],'澄');self.assertEqual(first['person_id'],'ehx_cqg_nfx_BB')
