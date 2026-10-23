from pathlib import Path
import unittest,tempfile,json,hashlib,copy
from scripts.fixed_plain_wikisource_biography import project,KIND
from scripts.fixed_wikisource_units import source_errors
class FixedPlainBiography(unittest.TestCase):
 def fixture(self,root):
  raw='==前傳==\n　　他人。\n\n==沈寧==\n　　沈寧，字子安，廣陵人也。\n\n　　{{YL|太康八年}}卒。\n\n==李平==\n　　後傳。\n';title='沈寧傳';a,z,pp=project(raw,title);sha=hashlib.sha256(raw.encode()).hexdigest();rr='sources/raw.txt';ref='source-evidence/fixed.json'
  c=dict(id='synthetic-chapter',title=title,source=dict(revision_id=7,raw_file=rr,raw_path=rr,wikitext_sha256=sha,raw_file_sha256=sha),annotation=dict(fixed_wikisource_unit_ref=ref),paragraphs=[])
  for i,p in enumerate(pp):c['paragraphs'].append(dict(id='p'+str(i),text=p['text'],text_layer='received_chapter',source_position=dict(**{k:v for k,v in p.items()if k!='text'},revision_id=7,projection_sha256=hashlib.sha256((json.dumps(p['raw_character_offsets'],ensure_ascii=False,indent=2)+'\n').encode()).hexdigest(),source_layer='received_biography')))
  b=dict(record_type=KIND,chapter_id=c['id'],source_revision=7,raw_file=rr,raw_sha256=sha,selection=dict(start=a,end=z,opening_heading='==沈寧==',following_heading='==李平==',raw=raw[a:z]))
  for rel,v in [(rr,raw),(ref,json.dumps(b,ensure_ascii=False))]:p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(v)
  return c,b,ref
 def run_case(self,mutator=None):
  with tempfile.TemporaryDirectory()as tmp:
   r=Path(tmp);c,b,ref=self.fixture(r)
   if mutator:mutator(c,b);(r/ref).write_text(json.dumps(b,ensure_ascii=False))
   return source_errors(c,r)
 def test_production_hook(self):self.assertEqual(self.run_case(),[])
 def test_body_rehash(self):self.assertTrue(self.run_case(lambda c,b:c['paragraphs'][0].update(text='沈寧，字子平，廣陵人也。')))
 def test_move_offsets_rehash(self):
  def bad(c,b):
   p=c['paragraphs'][0]['source_position'];p['raw_character_offsets']=[i+1 for i in p['raw_character_offsets']];p['projection_sha256']=hashlib.sha256((json.dumps(p['raw_character_offsets'],ensure_ascii=False,indent=2)+'\n').encode()).hexdigest()
  self.assertTrue(self.run_case(bad))
 def test_boundary(self):self.assertTrue(self.run_case(lambda c,b:b['selection'].update(end=b['selection']['end']+1)))
 def test_wrong_following_heading(self):self.assertTrue(self.run_case(lambda c,b:b['selection'].update(following_heading='==別傳==')))
 def test_omit_paragraph(self):self.assertTrue(self.run_case(lambda c,b:c['paragraphs'].pop()))
 def test_wrong_revision(self):self.assertTrue(self.run_case(lambda c,b:c['source'].update(revision_id=8)))
 def test_wrong_sha(self):self.assertTrue(self.run_case(lambda c,b:c['source'].update(raw_file_sha256='0'*64)))
 def test_unknown_markup(self):
  with self.assertRaises(AssertionError):project('==沈寧==\n　　{{unknown|沈寧}}。\n==李平==\n','沈寧傳')
 def test_template_suffix_not_lost(self):
  _,_,ps=project('==沈寧==\n　　{{YL|太康八年}}卒。其子尚存。\n==李平==\n','沈寧傳');self.assertEqual(ps[0]['text'],'太康八年卒。其子尚存。')
