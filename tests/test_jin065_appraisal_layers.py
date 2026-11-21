import copy,hashlib,json,unittest
from pathlib import Path
from scripts.jin065_appraisal_layers import valid
R=Path(__file__).resolve().parents[1]
def read(path):return json.loads((R/path).read_text())
class Jin65Appraisals(unittest.TestCase):
 def test_original_layers(self):
  c=read('corpus/jinshu/065.json');notes=c['paragraphs'][-2:];self.assertTrue(all(valid(p,c,R) for p in notes));self.assertFalse(valid(c['paragraphs'][-3],c,R))
  for p in notes:
   wrong=copy.deepcopy(p);wrong['source_witness']['raw_line']=122 if p['source_witness']['raw_line']==120 else 120;self.assertFalse(valid(wrong,c,R))
  self.assertEqual(len(c['paragraphs']),45);self.assertEqual([p['annotation_status'] for p in c['paragraphs']],['reviewed']*45)
  inventory=read('data/corpus/six-dynasties-biographies.json')
  entries=[x for x in inventory['biographies'] if x['book_id']==c['book_id']]
  original=read('source-evidence/jin065-wang-survey/survey-review.json')['entry_work']
  self.assertEqual(len(original),12)
  self.assertTrue({x['title'] for x in original}.issubset({x['title'] for x in entries}))
  self.assertFalse(any(p['id'] in x['paragraph_ids'] for x in entries for p in notes))
 def test_historical_source_images_remain_external(self):
  media={'.jpg','.jpeg','.png','.gif','.webp','.tif','.tiff','.jp2','.pdf'}
  stored=[str(path.relative_to(R)) for directory in ('source-evidence','sources','corpus','data/corpus')
          for path in (R/directory).rglob('*') if path.suffix.lower() in media and path.is_file()]
  self.assertEqual(stored,[])
 def test_textual_references(self):
  q=read('source-evidence/jin065-wangdao-appraisal/reading.json')
  for p in q['pages']:
   self.assertEqual(p['source_url'], f"{q['pdf_url']}#page={p['pdf_page']}")
   self.assertRegex(p['capture_sha256'],r'^[0-9a-f]{64}$')
  for w in q['original_sources']:
   v=(R/w['raw_path']).read_bytes();self.assertEqual(hashlib.sha256(v).hexdigest(),w['raw_sha256']);self.assertEqual(v.decode()[w['raw_start']:w['raw_end']],w['quote'])
  self.assertEqual([s['person_id']for s in q['original_sources']],['6c9_c43_555','11e_f2d_5d2'])
  self.assertEqual(q['print_variant']['printed'],'筮水流慶');self.assertEqual(q['print_variant']['digital'],'巫水流慶')
  k=q['luqian_knife'];p=next(p for p in read(k['path'])['paragraphs']if p['id']==k['paragraph_id']);self.assertEqual(p['text'][k['start']:k['end']],k['source_quote'])
