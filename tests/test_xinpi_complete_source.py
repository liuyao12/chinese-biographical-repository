# coding:utf-8
import unittest,json,copy,tempfile
from pathlib import Path
from scripts.fixed_kanripo_projection import errors
R=Path(__file__).resolve().parents[1];C=json.loads((R/'corpus/sanguozhi/025-xinpi.json').read_text());PS=C['paragraphs'];REG={p['id']:p for p in json.loads((R/'registry/persons.json').read_text())['persons']}
def hit(j,s):return[m for m in PS[j-1]['mentions']if m['surface']==s]
class XinpiComplete(unittest.TestCase):
 def test_complete_and_layer(self):
  self.assertEqual(len(PS),8);self.assertEqual(sum(len(p['text'])for p in PS),2620);self.assertEqual(sum(p['text_layer']=='witness_appended_pei_songzhi_note'for p in PS),4);self.assertFalse(errors(C,R));self.assertIn('133',C['source']['extent']);self.assertIn('泰始五年卒',PS[-1]['text']);self.assertIn('受誣不少',PS[3]['text'])
 def test_reverse_spans(self):
  for p in PS:
   prev=0
   for m in p['mentions']:
    self.assertEqual(p['text'][m['start']:m['end']],m['surface']);self.assertGreaterEqual(m['start'],prev);prev=m['end']
    if m['kind']=='person':self.assertTrue(any(e.get('mention_id')==m['id']for e in REG[m['person_id']]['evidence']))
 def test_preferred_brother_not_silent_emendation(self):
  self.assertIn('毗隨兄評從袁紹',PS[0]['text']);other=json.loads((R/'corpus/sanguozhi/010.json').read_text());pid=next(m['person_id']for p in other['paragraphs']for m in p['mentions']if m['surface']=='辛平');self.assertEqual(hit(1,'評')[0]['person_id'],pid)
 def test_office_and_title_syllables_not_people(self):
  p=PS[2]
  for word in['尚書','稱帝']:
   st=p['text'].index(word)+(1 if word=='稱帝'else 0);self.assertFalse(any(m['start']==st and m['kind']=='person'for m in p['mentions']))
 def test_emperor_thread(self):
  p=PS[2];cut=p['text'].index('明帝即位');before={m['person_id']for m in p['mentions']if m['surface']=='帝'and m['start']<cut};after={m['person_id']for m in p['mentions']if m['surface']=='帝'and m['start']>cut};self.assertEqual(len(before),1);self.assertEqual(len(after),1);self.assertNotEqual(before,after)
 def test_commentary_not_all_shiyu_or_historical_preferred(self):
  self.assertIn('魏畧既已難信習氏又從而載之',PS[3]['text']);self.assertIn('世語曰敞字泰雍官至衞尉毗女憲英',PS[7]['text']);self.assertEqual(hit(8,'其傳')[0]['kind'],'unresolved');self.assertEqual(hit(3,'兵法')[0]['kind'],'unresolved')
 def test_chang_not_guojia_and_new_typed_keeps_source_scope(self):
  self.assertNotEqual(hit(7,'敞')[0]['person_id'],'344_68f_98e_*A');self.assertFalse(C['annotation']['human_reviewed'])
  aa=json.loads((R/'corpus/sanguozhi/025-xinpi-assertions.json').read_text())['assertions'];father=[a for a in aa if a['predicate']=='father'];head=hit(1,'辛毗')[0]['person_id'];self.assertEqual({(a['subject_person_id'],a['object_person_id'])for a in father},{(hit(7,'敞')[0]['person_id'],head),(hit(8,'憲英')[0]['person_id'],head)});self.assertEqual(len(father),2);self.assertFalse(any(a['predicate']=='father'and a['subject_person_id']==hit(8,'琇')[0]['person_id']for a in aa))
 def test_ziyang_parallel_primary_and_local_binding(self):
  import hashlib
  e=json.loads((R/'source-evidence/sgz025-xinpi/ziyang-parallel-evidence.json').read_text());pr=e['parallel_source'];raw=(R/pr['raw_file']).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),pr['raw_file_sha256']);self.assertEqual(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),pr['git_blob']);t=raw.decode();u=pr['complete_read_unit'];self.assertEqual(t[u['start']:u['end']],u['raw'])
  for a in pr['role_anchors']:self.assertEqual(t[a['start']:a['end']],a['raw'])
  self.assertIn(e['preferred_display_name']+'字'+e['source_surface'],pr['role_anchors'][0]['raw']);l=e['local_reference'];p=next(p for p in PS if p['id']==l['paragraph_id']);self.assertEqual(p['text'][l['start']:l['end']],l['quote']);m=next(m for m in p['mentions']if m['id']==l['mention_id']);self.assertEqual(m['surface'],e['source_surface']);self.assertEqual(REG[m['person_id']]['label'],e['preferred_display_name']);self.assertFalse(pr['image_verified'])
 def test_projection_co_shift_rejected(self):
  ref=C['annotation']['fixed_kanripo_projection_ref'];d=json.loads((R/ref).read_text())
  with tempfile.TemporaryDirectory()as t:
   root=Path(t).resolve()
   for f in[ref,d['raw_file']]:q=root/f;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes((R/f).read_bytes())
   self.assertFalse(errors(C,root));d['unit']['start']+=1;(root/ref).write_text(json.dumps(d));self.assertTrue(errors(C,root))
if __name__=='__main__':unittest.main()
