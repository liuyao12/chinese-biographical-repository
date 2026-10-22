# coding: utf-8
import copy,hashlib,json,tempfile,unittest
from pathlib import Path
from scripts.biographical_death_year_chain import valid
from scripts.validate_corpus import source_age_number
ROOT=Path(__file__).resolve().parents[1]

class ReceivedDeathChainTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
  self.c=json.loads((ROOT/'corpus/songshu/064-peisongzhi.json').read_text())
  self.event=json.loads((ROOT/'corpus/songshu/064-peisongzhi-life-events.json').read_text())['events'][0]
  self.date=self.event['normalized_date'];self.b=self.date['event_evidence_binding']
  self.raw=self.c['source']['raw_path'];self.proj=self.b['received_text_projection']['path']
  for p in [self.raw,self.proj]:
   out=self.root/p;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes((ROOT/p).read_bytes())
 def ok(self):return valid(self.date,self.event,{self.c['id']:self.c},source_age_number,root=self.root)
 def update_projection(self,x):
  data=(json.dumps(x,ensure_ascii=False)+'\n').encode();(self.root/self.proj).write_bytes(data);self.b['received_text_projection']['sha256']=hashlib.sha256(data).hexdigest()
 def test_real_bytes_and_no_root_requirement_only_for_new_branch(self):
  self.assertTrue(self.ok());self.assertFalse(valid(self.date,self.event,{self.c['id']:self.c},source_age_number))
  self.assertEqual(self.date['year'],451)
  age=self.c['annotation']['age_assertions'][-1];self.assertEqual(age['value'],80);self.assertEqual(age['age_context'],{'kind':'at_death','life_event_id':self.event['id']})
 def test_digest_bytes_utf8_and_revision(self):
  original=(self.root/self.raw).read_bytes()
  for data in (original+b'x',b'\xff'+original):
   with self.subTest(data=data[:1]):
    (self.root/self.raw).write_bytes(data);self.assertFalse(self.ok())
  (self.root/self.raw).write_bytes(original);self.c['source']['revision_id']+=1;self.assertFalse(self.ok())
 def test_path_escape_symlink_and_wrong_file(self):
  for value in ('../outside','/tmp/outside','sources/../outside','sources/nonexistent'):
   with self.subTest(path=value):self.c['source']['raw_path']=value;self.assertFalse(self.ok())
  target=self.root/'sources/link';target.symlink_to(self.root/self.raw);self.c['source']['raw_path']='sources/link';self.assertFalse(self.ok())
 def test_co_shift_is_not_a_valid_source_position(self):
  proj=json.loads((self.root/self.proj).read_text())
  for p in self.c['paragraphs'][3:]:
   p['source_position']['start']+=1;p['source_position']['end']+=1
  for p in proj['paragraphs'][3:]:
   p['source_position']['start']+=1;p['source_position']['end']+=1;p['raw_positions']=[i+1 for i in p['raw_positions']]
  self.b['full_paragraphs']=[dict(paragraph_id=p['id'],quote=p['text'],source_position=p['source_position'])for p in self.c['paragraphs'][3:]]
  self.update_projection(proj);self.assertFalse(self.ok())
 def test_foreign_layers_rejected(self):
  objects=[self.c,self.c['source'],self.c['paragraphs'][3],self.c['paragraphs'][3]['source_position'],self.b['received_text_projection']]
  for obj in objects:
   for key in ('source_layer','text_layer'):
    with self.subTest(key=key):
     old=obj.get(key);obj[key]='commentary';self.assertFalse(self.ok())
     if old is None:del obj[key]
     else:obj[key]=old
 def test_non_subject_roles_are_exact_and_exhaustive(self):
  original=copy.deepcopy(self.b['non_subject_references'])
  for refs in ([],original[:1],original+original[:1]):
   self.b['non_subject_references']=refs;self.assertFalse(self.ok())
  self.b['non_subject_references']=copy.deepcopy(original)
  self.b['non_subject_references'][0]['kind']='arbitrary_other_person';self.assertFalse(self.ok())
  self.b['non_subject_references']=copy.deepcopy(original)
  self.b['non_subject_references'][1]['person_mention_id']=original[0]['person_mention_id'];self.assertFalse(self.ok())
 def test_forged_fragment_even_with_updated_projection_hash(self):
  proj=json.loads((self.root/self.proj).read_text());p=self.c['paragraphs'][3];p['source_position']['raw']='fake';proj['paragraphs'][3]['source_position']['raw']='fake'
  self.b['full_paragraphs'][0]['source_position']=p['source_position'];self.update_projection(proj);self.assertFalse(self.ok())
 def test_projection_coordinates_and_fingerprint(self):
  proj=json.loads((self.root/self.proj).read_text());proj['paragraphs'][3]['raw_positions'][0]+=1;self.update_projection(proj);self.assertFalse(self.ok())
 def test_attribution_flags_without_explicit_layer(self):
  for obj in [self.c,self.c['source'],self.c['paragraphs'][3],self.c['paragraphs'][3]['source_position']]:
   for key in ('annotator','attached_note_to_paragraph_id'):
    obj[key]='annotation';self.assertFalse(self.ok());del obj[key]
  original=json.loads((self.root/self.proj).read_text())
  for layer in ('root','source','paragraph','position'):
   for key in ('annotator','attached_note_to_paragraph_id','source_layer','text_layer'):
    proj=copy.deepcopy(original);obj=proj if layer=='root' else proj['source'] if layer=='source' else proj['paragraphs'][3] if layer=='paragraph' else proj['paragraphs'][3]['source_position'];obj[key]='annotation';self.update_projection(proj);self.assertFalse(self.ok())
 def test_outer_quote_cannot_claim_biography_subject_or_author(self):
  from scripts.biographical_work_references import references_valid
  p=copy.deepcopy(self.c['paragraphs'][-1]);subject=next(m for m in p['mentions']if m['start']==23);death=copy.deepcopy(self.b['death_anchor']);binding=copy.deepcopy(self.b)
  p['text']='「'+p['text']+'」'
  for m in p['mentions']:m['start']+=1;m['end']+=1
  for r in binding['non_subject_references']:r['anchor']['start']+=1;r['anchor']['end']+=1
  death['start']+=1;death['end']+=1
  self.assertFalse(references_valid(binding,p,subject,death))
  # Only the author phrase is quoted; the biography subject and death stay outside.
  p=copy.deepcopy(self.c['paragraphs'][-1]);subject=next(m for m in p['mentions']if m['start']==23);death=copy.deepcopy(self.b['death_anchor']);binding=copy.deepcopy(self.b)
  author=binding['non_subject_references'][1]['anchor'];lo,hi=author['start'],author['end']
  p['text']=p['text'][:lo]+'「'+p['text'][lo:hi]+'」'+p['text'][hi:]
  def shift(x):
   for k in ('start','end'):x[k]+=int(x[k]>=lo)+int(x[k]>=hi)
  for m in p['mentions']:shift(m)
  for r in binding['non_subject_references']:shift(r['anchor'])
  shift(death);self.assertFalse(references_valid(binding,p,subject,death))
 def test_praise_role_requires_sentence_boundary(self):
  from scripts.biographical_work_references import references_valid
  p=copy.deepcopy(self.c['paragraphs'][-1]);subject=next(m for m in p['mentions']if m['start']==23);binding=copy.deepcopy(self.b);lo=binding['non_subject_references'][0]['anchor']['start'];p['text']=p['text'][:lo-1]+'，'+p['text'][lo:]
  self.assertFalse(references_valid(binding,p,subject,self.b['death_anchor']))
 def test_raw_sha_alias_must_agree(self):
  self.c['source']['raw_sha256']='0'*64;self.assertFalse(self.ok())
 def test_biography_topic_must_have_real_received_text_position(self):
  topic=self.c['paragraphs'][0]
  for key,value in [('annotator','annotation'),('text_layer','commentary'),('attached_note_to_paragraph_id',self.c['paragraphs'][1]['id'])]:
   with self.subTest(key=key):
    topic[key]=value;self.assertFalse(self.ok());del topic[key]
  topic['source_position']['start']+=1;topic['source_position']['end']+=1
  self.assertFalse(self.ok())
