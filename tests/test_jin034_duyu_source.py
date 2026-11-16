# coding: utf-8
from pathlib import Path
import json,copy,hashlib,tempfile,unittest,subprocess,sys
from unittest.mock import patch
from scripts.fixed_linked_heading_biography import errors,project
ROOT=Path(__file__).resolve().parents[1];CID='c-jinshu-034-duyu'
class DuyuCompleteSource(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((ROOT/'corpus/jinshu/034-duyu.json').read_text());cls.ps={p['id'].split(':')[-1]:p for p in cls.c['paragraphs']};cls.raw=(ROOT/cls.c['source']['raw_file']).read_text();cls.proof=json.loads((ROOT/cls.c['annotation']['fixed_wikisource_unit_ref']).read_text());cls.reg={p['id']:p for p in json.loads((ROOT/'registry/persons.json').read_text())['persons']}
 def pid(self,n,surface):return next(m['person_id']for m in self.ps['p'+str(n).zfill(3)]['mentions']if m['surface']==surface and m['kind']=='person')
 def test_complete_27_4612_and_all_original_fidelity(self):
  self.assertEqual((len(self.c['paragraphs']),sum(len(p['text'])for p in self.c['paragraphs'])),(27,4612));self.assertFalse(errors(self.c,ROOT,self.proof));self.assertTrue(self.proof['selection']['raw'].endswith('\n\n'));self.assertEqual(self.proof['selection']['following_heading'],'{{footer')
 def test_source_layers_complete_quotes_and_shared_criticism(self):
  self.assertEqual([p['id']for p in self.c['paragraphs']if p['source_position']['source_layer']=='received_quoted_document'],[self.ps[x]['id']for x in ['p004','p011','p013']]);self.assertEqual([p['id']for p in self.c['paragraphs']if p['source_position']['source_layer']=='received_criticism'],[self.ps[x]['id']for x in ['p026','p027']]);self.assertIn('預先為遺令曰',self.ps['p024']['text']);self.assertIn('乃奏之曰',self.ps['p002']['text']);self.assertIn('子乂嗣',self.ps['p025']['text'])
 def test_not_truncated_at_son_or_criticism(self):
  for n in [24,25,26]:
   c=copy.deepcopy(self.c);c['paragraphs']=c['paragraphs'][:n];self.assertTrue(errors(c,ROOT,self.proof))
 def test_source_spelling_punctuation_and_no_image_claim(self):
  self.assertIn('以侯贖論，。',self.ps['p005']['text']);self.assertIn('當今討之，可不勞而定。帝乃許之。',self.ps['p014']['text']);self.assertFalse(self.c['source']['image_verified']);self.assertFalse(self.c['annotation']['human_reviewed']);self.assertIsNone(self.c['source']['edition'])
 def test_rename_word_without_projection_cannot_pass(self):
  c=copy.deepcopy(self.c);c['paragraphs'][4]['text']=c['paragraphs'][4]['text'].replace('以侯贖論，。','以侯贖論。');self.assertTrue(errors(c,ROOT,self.proof))
 def test_every_227_span_is_exact_nonoverlap_and_no_zerolength(self):
  ms=[m for p in self.c['paragraphs']for m in p['mentions']];self.assertEqual(len(ms),227);self.assertEqual(len({m['id']for m in ms}),227)
  for p in self.c['paragraphs']:
   end=0
   for m in p['mentions']:self.assertGreater(m['end'],m['start']);self.assertGreaterEqual(m['start'],end);self.assertEqual(p['text'][m['start']:m['end']],m['surface']);end=m['end']
 def test_wei_to_jin_emperors_and_later_prince_are_distinct(self):
  self.assertNotEqual(self.pid(1,'宣帝'),self.pid(1,'文帝'));self.assertNotEqual(self.pid(1,'文帝'),self.pid(8,'帝'));self.assertEqual(self.pid(7,'皇太子'),self.pid(25,'惠帝'));self.assertNotEqual(self.pid(7,'皇太子'),self.pid(25,'湣懷太子'));self.assertEqual(self.pid(26,'儲君'),self.pid(7,'皇太子'))
 def test_grandfather_father_subject_and_son_are_separate(self):
  self.assertEqual(len({self.pid(1,'杜預'),self.pid(1,'畿'),self.pid(1,'恕'),self.pid(25,'錫')}),4);self.assertEqual(self.pid(24,'錫'),self.pid(25,'錫'));self.assertNotEqual(self.pid(25,'乂'),self.pid(25,'長沙王乂'))
 def test_duyu_and_yanghu_reuse_actual_native_endpoints(self):
  c=json.loads((ROOT/'corpus/jinshu/034-yanghu.json').read_text());mm={m['id']:m for p in c['paragraphs']for m in p['mentions']};self.assertEqual(self.pid(1,'杜預'),mm['c-jinshu-034-yanghu:p028:m0006']['person_id']);self.assertEqual(self.pid(9,'羊祜'),mm['c-jinshu-034-yanghu:p001:m0000']['person_id']);self.assertEqual(self.pid(26,'羊公'),self.pid(9,'羊祜'))
 def test_shijian_is_qualified_western_jin_preference_not_later_zhao(self):
  r=json.loads((ROOT/'source-evidence/jin034-duyu/identity-review.json').read_text())['shijian'];self.assertEqual(self.pid(5,'石鑒'),r['person_id']);self.assertNotEqual(r['person_id'],'751_8id_lls');self.assertEqual(r['independent_same_office_bridge'],'not_found_in_current_material');self.assertTrue(any(x['status']=='rejected'and x['person_id']=='751_8id_lls'for x in r['candidates']))
 def test_qinwang_named_event_context_preference(self):
  c=json.loads((ROOT/'corpus/shiji/006.json').read_text());p=next(p for p in c['paragraphs']if p['id'].endswith(':p015'));pid=next(m['person_id']for m in p['mentions']if m['surface']=='秦王');self.assertEqual(self.pid(26,'秦王'),pid)
 def test_guoshi_not_assigned_mother_or_spouse(self):
  r=json.loads((ROOT/'source-evidence/jin034-duyu/identity-review.json').read_text())['guoshi'];self.assertEqual(self.pid(24,'郭氏'),r['person_id']);self.assertEqual(r['cross_chapter_identity'],'unresolved');self.assertEqual(r['not_inferred'],['mother','spouse','personal_name'])
 def test_tomb_two_sayings_not_unique_late_referent(self):
  self.assertNotEqual(self.pid(24,'祭仲'),self.pid(24,'子產'));m=next(m for m in self.ps['p024']['mentions']if m['surface']=='鄭大夫');self.assertEqual(m['kind'],'unresolved');self.assertEqual(set(m['candidate_person_ids']),{self.pid(24,'祭仲'),self.pid(24,'子產')})
 def test_no_persons_in_lexical_or_institution_words(self):
  for key,word in [('p022','耽思'),('p026','孔門'),('p026','何其斯酷'),('p025','太子中舍人')]:
   p=self.ps[key];a=p['text'].index(word);self.assertFalse(any(m['kind']=='person'and m['start']<a+len(word)and a<m['end']for m in p['mentions']))
 def test_human_pronoun_roles_do_not_reverse_killing(self):
  p=self.ps['p018'];a=p['text'].index('盡捕殺之')+3;m=next(m for m in p['mentions']if m['start']==a);self.assertEqual(m['kind'],'unresolved');self.assertIn('群體',m['note']);p=self.ps['p025'];a=p['text'].index('錫拒之')+2;m=next(m for m in p['mentions']if m['start']==a);self.assertEqual(m['person_id'],self.pid(25,'孫秀'))
 def test_works_16_marks_and_scope_of_short_chuan(self):
  ms=[m for p in self.c['paragraphs']for m in p['mentions']if m['kind']=='work'];self.assertEqual(len(ms),16);p=self.ps['p022'];left=next(m['work_id']for m in p['mentions']if m['surface']=='左傳');self.assertEqual(next(m['work_id']for m in p['mentions']if m['surface']=='傳'),left);self.assertNotEqual(next(m['work_id']for m in p['mentions']if m['surface']=='春秋左氏經傳集解'),left)
 def test_presented_calendar_is_not_falsely_authored(self):
  w=next(w for w in json.loads((ROOT/'registry/works.json').read_text())['works']if w['id']=='w-eryuan-qiandu-jin034-reference');self.assertIsNone(w['author']);self.assertIn('奏上',w['citation_qualification'])
 def test_all56_people_have_exact_bidirectional_evidence(self):
  pids={m['person_id']for p in self.c['paragraphs']for m in p['mentions']if m['kind']=='person'};self.assertEqual(len(pids),56)
  for p in self.c['paragraphs']:
   for m in p['mentions']:
    if m['kind']=='person':
     r=self.reg[m['person_id']];self.assertTrue(any(e.get('mention_id')==m['id']and e.get('quote')==m['surface']and e.get('source_id')==self.c['source_id']for e in r['evidence']));self.assertTrue(any(a['surface']==m['surface']and m['id']in a['mention_ids']for a in r['aliases']))
 def test_profile_notes_no_stale_unknown_family_or_ming(self):
  self.assertNotIn('未知家世、名、字',self.reg[self.pid(25,'乂')]['identity_note']);self.assertIn('元凱',self.reg[self.pid(1,'杜預')]['identity_note']);self.assertFalse(any('本批只做source' in self.reg[self.pid(1,'杜預')]['identity_note']for _ in[0]))
 def test_primary_sgz016_entire_du_unit_and_093_bridge(self):
  d=json.loads((ROOT/'source-evidence/jin034-duyu/supplementary-primary-reading.json').read_text());a,b=d['primary_references'];self.assertTrue(a['read_scope']['text'].startswith('杜畿字伯侯'));self.assertIn('子錫字世嘏尚書左丞',a['read_scope']['text']);self.assertIn('鎮南將軍預孫，尚書左丞錫之子',b['read_scope']['text']);self.assertFalse(d['image_verified'])
 def test_symlink_source_or_metadata_escape_rejected(self):
  with tempfile.TemporaryDirectory()as t:
   r=Path(t);(r/'sources').mkdir();(r/'sources/witnesses').symlink_to(ROOT/'sources/witnesses',target_is_directory=True);self.assertTrue(errors(self.c,r,self.proof))
 def test_raw_rehash_does_not_override_independent_pin(self):
  rawpath=ROOT/self.c['source']['raw_file'];pinpath=ROOT/'scripts/fixed_linked_heading_witnesses.json';c=copy.deepcopy(self.c);b=copy.deepcopy(self.proof);rb=b'\n'+self.raw.encode();h=hashlib.sha256(rb).hexdigest();b['raw_sha256']=h
  for k in('wikitext_sha256','raw_file_sha256'):c['source'][k]=h
  b['selection']['start']+=1;b['selection']['end']+=1
  for x in b['excluded']:x['start']+=1;x['end']+=1
  for pp in c['paragraphs']:
   v=pp['source_position'];v['raw_start']+=1;v['raw_end']+=1;v['first_line']+=1;v['last_line']+=1;v['raw_character_offsets']=[i+1 for i in v['raw_character_offsets']];v['projection_sha256']=hashlib.sha256((json.dumps(v['raw_character_offsets'],ensure_ascii=False,indent=2)+'\n').encode()).hexdigest()
  old=Path.read_bytes
  with patch.object(Path,'read_bytes',lambda p:rb if p==rawpath else old(p)):self.assertTrue(errors(c,ROOT,b))

 def test_real_main_rejects_received_text_edit_without_writing_source(self):
  code="""import runpy,json
from pathlib import Path
from unittest.mock import patch
p=Path('corpus/jinshu/034-duyu.json').resolve();d=json.loads(p.read_text());d['paragraphs'][4]['text']=d['paragraphs'][4]['text'].replace('以侯贖論，。','以侯贖論。');old=Path.read_text
def read(q,*a,**kw):return json.dumps(d,ensure_ascii=False)if q.resolve()==p else old(q,*a,**kw)
with patch.object(Path,'read_text',read):runpy.run_path('scripts/validate_corpus.py',run_name='__main__')
"""
  p=subprocess.run([sys.executable,'-c',code],cwd=ROOT,text=True,capture_output=True);self.assertEqual(p.returncode,1,p.stdout+p.stderr);self.assertNotIn('Traceback',p.stdout+p.stderr)

 def test_optional_criticism_mode_cannot_swallow_another_biography(self):
  modified=self.raw.replace('{{footer','== Other biography ==\n某人。\n{{footer')
  with self.assertRaises(AssertionError):project(modified,'杜預傳',True)
  with self.assertRaises(AssertionError):project(self.raw.replace('== 【評贊】 ==','== Other section =='),'杜預傳',True)
