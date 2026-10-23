# coding: utf-8
"""Real fixed source and small physical counterexamples; no writes to repository."""
from pathlib import Path
import unittest,json,copy,tempfile,hashlib
from scripts.fixed_kanripo_projection import errors
from scripts.literal_family_reports import kinship_valid
from scripts.age_context import age_context_valid
ROOT=Path(__file__).resolve().parents[1]
class FixedWenhui(unittest.TestCase):
 def setUp(self):
  self.ch=json.loads((ROOT/'corpus/sanguozhi/015-wenhui.json').read_text());self.ref=self.ch['annotation']['fixed_kanripo_projection_ref'];self.proj=json.loads((ROOT/self.ref).read_text());self.raw=(ROOT/self.proj['raw_file']).read_bytes()
 def fixture(self,mutate):
  # A real private temporary directory, never a directory symlink to the shared tree.
  with tempfile.TemporaryDirectory(prefix='wenhui-source-')as temp:
   root=Path(temp).resolve();assert not Path(temp).is_symlink();ch=copy.deepcopy(self.ch);d=copy.deepcopy(self.proj);raw=self.raw
   raw=mutate(ch,d,raw)or raw
   for name,data in [(self.ref,json.dumps(d,ensure_ascii=False).encode()),(self.proj['raw_file'],raw)]:
    dest=root/name;assert dest.resolve().is_relative_to(root);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
   return errors(ch,root)
 def test_actual_complete_unit(self):self.assertEqual(errors(self.ch,ROOT),[])
 def test_co_shift_every_offset_and_lines(self):
  def mutate(c,d,b):
   d['unit']['start']+=1;d['unit']['end']+=1;d['unit']['first_line']+=1;d['unit']['last_line']+=1
   for p,q in zip(c['paragraphs'],d['paragraphs']):
    q['raw_positions']=[i+1 for i in q['raw_positions']]
    for v in (p['source_position'],q):v['first_line']+=1;v['last_line']+=1
  self.assertTrue(self.fixture(mutate))
 def test_retained_fragment_is_not_whole_note(self):
  def mutate(c,d,b):
   p,q=c['paragraphs'][-1],d['paragraphs'][-1];p['text']=p['text'][:-1];q['text']=p['text'];q['raw_positions']=q['raw_positions'][:-1]
  self.assertTrue(self.fixture(mutate))
 def test_layer_confusion(self):
  def mutate(c,d,b):c['paragraphs'][-1]['text_layer']='received_chapter'
  self.assertTrue(self.fixture(mutate))
 def test_disguised_attached_note(self):
  def mutate(c,d,b):c['paragraphs'][0]['source_position']['attached_note_to_paragraph_id']='x'
  self.assertTrue(self.fixture(mutate))
 def test_raw_changed_even_outside_retained_fragment(self):
  def mutate(c,d,b):return b.replace(b'#+TITLE:',b'#+TITLX:',1)
  self.assertTrue(self.fixture(mutate))
 def test_false_next_unit_boundary(self):
  def mutate(c,d,b):d['unit']['next_line']='別傳'
  self.assertTrue(self.fixture(mutate))
 def test_escape_raw_path(self):
  # Do not write an escaped fixture; production reader alone receives the invalid reference.
  c=copy.deepcopy(self.ch);d=copy.deepcopy(self.proj)
  with tempfile.TemporaryDirectory()as temp:
   root=Path(temp);f=root/self.ref;f.parent.mkdir(parents=True);d['raw_file']='../private-raw.txt';f.write_text(json.dumps(d));self.assertTrue(errors(c,root))
 def test_actual_two_fathers_and_wrong_subject(self):
  a=json.loads((ROOT/'corpus/sanguozhi/015-wenhui-assertions.json').read_text())['assertions'];ps={p['id']:(self.ch['id'],p)for p in self.ch['paragraphs']};cs={self.ch['id']:self.ch}
  for r in a:self.assertTrue(kinship_valid(r,ps,cs,ROOT))
  bad=copy.deepcopy(a[1]);bad['subject_person_id']=a[0]['object_person_id'];self.assertFalse(kinship_valid(bad,ps,cs,ROOT))
 def test_ages_distinct_no_birth_inference(self):
  aa=self.ch['annotation']['age_assertions'];ev=json.loads((ROOT/'corpus/sanguozhi/015-wenhui-life-events.json').read_text())['events'];es={e['id']:e for e in ev}
  self.assertEqual([x['value']for x in aa],[15,45]);self.assertEqual(aa[0]['age_context'],{'kind':'during_life'})
  self.assertTrue(age_context_valid(aa[1],es));self.assertTrue(all(x['birth_year']is None for x in aa));self.assertTrue(all(e['date_expression']is None for e in ev))
  bad=copy.deepcopy(aa[1]);bad['age_context']['life_event_id']=ev[0]['id'];self.assertFalse(age_context_valid(bad,es))
 def test_source_year_is_use_not_tenure(self):
  hs=json.loads((ROOT/'corpus/sanguozhi/015-wenhui-titles.json').read_text())['holdings'];dated=[h for h in hs if 'normalized_date'in h['attestations'][0]]
  self.assertEqual(len(dated),3)
  for h in dated:
   self.assertEqual(h['mode'],'attestation');self.assertEqual(h['attestations'][0]['normalized_date']['year'],219);self.assertEqual(h['effective_period']['start']['status'],'unknown');self.assertEqual(h['effective_period']['end']['status'],'unknown')
 def test_all_typed_office_surfaces_and_shared_suffix_scope(self):
  hs=json.loads((ROOT/'corpus/sanguozhi/015-wenhui-titles.json').read_text())['holdings'];ps={p['id']:p for p in self.ch['paragraphs']};self.assertEqual(len(hs),20)
  for h in hs:
   a=h['attestations'][0];p=ps[a['paragraph_id']];self.assertEqual(p['text'][a['start']:a['end']],h['title']);m=next(m for m in p['mentions']if m['id']==a['person_mention_id']);self.assertEqual(m['person_id'],h['person_id'])
  self.assertEqual([(h['title'],h['jurisdictions'][0]['source_name'])for h in hs if'jurisdictions'in h],[('令','鄢陵'),('令','廣川'),('相','彭城'),('相','魯')])
if __name__=='__main__':unittest.main()
