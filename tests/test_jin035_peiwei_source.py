"""Actual pinned full attached quotation and source role failures, no historical ID whitelist."""
import copy,json,tempfile,unittest
from pathlib import Path
from scripts.fixed_biography_subsections import project
from scripts.fixed_attached_subsection_selection import errors,required_ref_error
ROOT=Path(__file__).resolve().parents[1]
CID='c-jinshu-035-peiwei';CP='corpus/jinshu/035-peiwei.json'
class PeiweiSource(unittest.TestCase):
 def setUp(self):
  self.ch=json.loads((ROOT/CP).read_text());self.pin=json.loads((ROOT/'scripts/fixed_attached_subsection_witnesses.json').read_text())['chapters'][CID]
  self.ref=self.pin['projection_ref'];self.proof=json.loads((ROOT/self.ref).read_text());self.raw=(ROOT/self.pin['raw_file']).read_text()
 def check(self,c=None,pin=None,raw=None,proof=None):
  with tempfile.TemporaryDirectory()as td:
   r=Path(td);p=pin or self.pin
   seed=p['embedded_document']['subject_resolution_seed']['chapter_path'];sf=r/seed;sf.parent.mkdir(parents=True,exist_ok=True);sf.write_bytes((ROOT/seed).read_bytes())
   for rel,data in [(p['raw_file'],self.raw if raw is None else raw),(self.ref,json.dumps(proof or self.proof,ensure_ascii=False)),('scripts/fixed_attached_subsection_witnesses.json',json.dumps({'format_version':'0.1','chapters':{CID:p}}))]:
    f=r/rel;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(data)
   return errors(c or self.ch,r,proof or self.proof)
 def test_complete_received_container(self):
  self.assertEqual(self.check(),[]);self.assertEqual(len(self.ch['paragraphs']),15)
  e=self.ch['annotation']['embedded_documents'][0];ps={p['id']:p for p in self.ch['paragraphs']};self.assertEqual(sum(len(ps[k]['text'])for k in e['paragraph_ids']),1640)
 def test_wrong_known_work(self):
  c=copy.deepcopy(self.ch);e=c['annotation']['embedded_documents'][0];m=next(m for p in c['paragraphs']for m in p['mentions']if m['id']==e['work_anchor']['mention_id']);m['work_id']='w-jinshu';self.assertTrue(self.check(c))
 def test_wrong_author_and_subject(self):
  for which in ['author','subject']:
   c=copy.deepcopy(self.ch);e=c['annotation']['embedded_documents'][0]
   m=next(m for p in c['paragraphs']for m in p['mentions']if m['id']==e['author_anchor']['mention_id'])if which=='author'else c['paragraphs'][0]['mentions'][0]
   other=next(x['person_id']for p in c['paragraphs']for x in p['mentions']if x.get('person_id')and x['person_id']!=m['person_id'])
   m['person_id']=other;self.assertTrue(self.check(c))
 def test_joint_subject_author_replacement(self):
  c=copy.deepcopy(self.ch);e=c['annotation']['embedded_documents'][0];subject=next(m for p in c['paragraphs']for m in p['mentions']if m['id']==e['subject_anchor']['mention_id']);author=next(m for p in c['paragraphs']for m in p['mentions']if m['id']==e['author_anchor']['mention_id']);other=next(x['person_id']for p in c['paragraphs']for x in p['mentions']if x.get('person_id')and x['person_id']!=subject['person_id']);subject['person_id']=author['person_id']=other;self.assertTrue(self.check(c))
 def test_author_mid_or_title_offset(self):
  for field in ['author_anchor','work_anchor']:
   c=copy.deepcopy(self.ch);c['annotation']['embedded_documents'][0][field]['start']+=1;self.assertTrue(self.check(c))
 def test_wrong_layer_and_truncated_document(self):
  for index in [0,8]:
   c=copy.deepcopy(self.ch);c['paragraphs'][index]['source_position']['source_layer']='received_quoted_document'if index==0 else'received_biography';self.assertTrue(self.check(c))
  c=copy.deepcopy(self.ch);c['paragraphs'].pop();self.assertTrue(self.check(c))
 def test_source_changed_or_co_shift_rehashed(self):
  import hashlib
  self.assertTrue(self.check(raw=self.raw+'異'))
  c=copy.deepcopy(self.ch);p=copy.deepcopy(self.proof);raw='移'+self.raw;h=hashlib.sha256(raw.encode()).hexdigest();c['source']['wikitext_sha256']=c['source']['raw_file_sha256']=h;p['raw_sha256']=h;p['selection']['start']+=1;p['selection']['end']+=1;self.assertTrue(self.check(c,raw=raw,proof=p))
 def test_required_ref_and_features(self):
  c=copy.deepcopy(self.ch);c['annotation'].pop('fixed_wikisource_unit_ref');self.assertTrue(self.check(c))
  p=copy.deepcopy(self.pin);p['projection_features'].append('arbitrary_markup');self.assertTrue(self.check(pin=p))
 def test_default_legacy_and_bad_template(self):
  raw='==例==\n甲[[乙|丙]]{{YL|元年}}\n==後==\n丁';self.assertEqual(project(raw,'例傳')[2][0]['text'],'甲丙元年')
  with self.assertRaises((AssertionError,ValueError)):project(self.raw,'裴頠傳',self.pin['opening_heading'],self.pin['following_heading'])
  for token,replacement in [('{{quote|','{{quote|{{quote|'),('}}','')]:
   i=self.raw.index(token,self.pin['raw_start']);r=self.raw[:i]+replacement+self.raw[i+len(token):]
   with self.assertRaises((AssertionError,ValueError)):project(r,'裴頠傳',self.pin['opening_heading'],self.pin['following_heading'],self.pin['projection_features'])
 def test_ordinary_words_any_kind_full_overlap(self):
  for phrase in ['遂易門肆','中節','心非事也']:
   p=next(p for p in self.ch['paragraphs']if phrase in p['text']);a=p['text'].index(phrase);b=a+len(phrase)
   def safe(ms):return not any(m['start']<b and m['end']>a for m in ms)
   self.assertTrue(safe(p['mentions']))
   for kind in ['person','work']:
    for x,y in [(a,b),(a-1,a+1),(b-1,b+1)]:self.assertFalse(safe(p['mentions']+[{'kind':kind,'start':x,'end':y}]))
 def test_raw_every_character_responsible(self):
  a,z,ps,classes=project(self.raw,self.ch['title'],self.pin['opening_heading'],self.pin['following_heading'],self.pin['projection_features']);v=[i for p in ps for i in p['raw_character_offsets']];e=[i for q in classes for i in range(q['start'],q['end'])]
  self.assertEqual(len(v)+len(e),z-a);self.assertEqual(set(v)|set(e),set(range(a,z)));self.assertFalse(set(v)&set(e))
if __name__=='__main__':unittest.main()
