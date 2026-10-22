from pathlib import Path
import unittest,json,re,hashlib,copy
from scripts.houhan_text_layers import layer_errors
R=Path(__file__).resolve().parents[1]
class LuzhiCompleteSource(unittest.TestCase):
 def setUp(self):
  self.c=json.loads((R/'corpus/houhanshu/064-luzhi.json').read_text());self.ps={p['id'].split(':')[-1]:p for p in self.c['paragraphs']};self.raw=(R/self.c['source']['raw_file']).read_text();self.proj=json.loads((R/'source-evidence/houhan064-luzhi/projection.json').read_text())
 def test_all_visible_characters_and_positions(self):
  self.assertEqual(len(self.ps),60);positions=[]
  for p in self.ps.values():
   pp=self.proj['paragraph_raw_positions'][p['id']];self.assertEqual(''.join(self.raw[i]for i in pp),p['text']);positions+=pp
  lo,hi=self.proj['raw_selected_bounds'];raw=self.raw[lo:hi];raw=raw.split('\n',1)[1];visible=re.sub(r'<pb:[^>]+>','',raw);visible=''.join(c for c in visible if c not in '\n\r¶/ \t　()');unitpositions=sorted(i for i in positions if lo<=i<hi);self.assertEqual(''.join(self.raw[i]for i in unitpositions),visible);self.assertEqual(len(positions),len(set(positions)))
 def test_all_spans_nonoverlap(self):
  for p in self.ps.values():
   prev=0
   for m in p['mentions']:self.assertEqual(p['text'][m['start']:m['end']],m['surface']);self.assertGreaterEqual(m['start'],prev);prev=m['end']
 def test_tang_song_qing_layers_and_negatives(self):
  for p in self.ps.values():self.assertEqual(layer_errors(p),[])
  for key in ['note001','note004','qing470']:
   p=copy.deepcopy(self.ps[key]);p['layer_attribution']['period']='wrong';self.assertTrue(layer_errors(p))
  self.assertEqual(self.ps['note004']['text_layer'],'witness_appended_liuban_collation');self.assertEqual(self.ps['qing471']['text_layer'],'witness_appended_qing_siku_collation')
 def test_jians_death_instruction_is_not_person(self):
  p=self.ps['p007'];self.assertIn('敕其子儉葬',p['text']);self.assertFalse(any('儉'in m['surface']for m in p['mentions']));self.assertIsNone(next(m for m in p['mentions']if m['surface']=='其子')['person_id'])
 def test_no_silent_collation(self):
  self.assertIn('中郎',self.ps['note043']['text']);self.assertNotIn('中書郎',self.ps['note043']['text']);self.assertIn('毛本作中書郎',self.ps['qing471']['text']);self.assertIn('遂隱於上谷',self.ps['p006']['text']);self.assertIn('毛本作山',self.ps['qing470']['text'])
 def test_book_number_and_raw_author(self):
  self.assertEqual(self.c['book_id'],'b-houhanshu-064');self.assertEqual(self.c['source']['physical_file_juan'],94);self.assertIn('范　煜',self.c['source']['author_heading_raw']);self.assertFalse(self.c['source']['image_verified']);self.assertFalse(self.c['annotation']['human_reviewed'])
 def test_same_names_are_not_merged(self):
  ws=json.loads((R/'registry/persons.json').read_text())['persons'];han=next(m['person_id']for m in self.ps['p003']['mentions']if m['surface']=='韓說');jia=next(m['person_id']for m in self.ps['p002']['mentions']if m['surface']=='賈逵');self.assertIn('東觀',next(p['label']for p in ws if p['id']==han));self.assertIn('中興',next(p['label']for p in ws if p['id']==jia));f=next(m for m in self.ps['note002']['mentions']if m['surface']=='范獻子');self.assertEqual(f['person_id'],'rf6_xhq_gm3');self.assertNotIn('candidate_person_ids',f);self.assertIn('說話主客差異',f['interpretation_note'])
 def test_book_titles_are_not_person_substrings(self):
  for key,s in [('p006','卓傳'),('note048','何進傳'),('qing470','盧植傳'),('note045','老子')]:self.assertEqual(next(m['kind']for m in self.ps[key]['mentions']if m['surface']==s),'work')
 def test_new_work_provenance_and_reverse_attestations(self):
  ws={w['id']:w for w in json.loads((R/'registry/works.json').read_text())['works']};pr=json.loads((R/'registry/work-provenance.json').read_text())
  for p in self.ps.values():
   for m in p['mentions']:
    if m['kind']=='work':self.assertIn(dict(chapter_id=self.c['id'],source_id=self.c['source_id'],paragraph_id=p['id'],mention_id=m['id'],quote=p['text']),ws[m['work_id']]['reference_attestations']);self.assertIn(m['work_id'],pr['works'])
 def test_names_when_adopted(self):
  path=R/'corpus/houhanshu/064-luzhi-name-components.json'
  if not path.exists():self.skipTest('separate optional name plan not adopted')
  ns=json.loads(path.read_text())['records'];self.assertEqual([(n['surname'],n['ming'],n['zi'])for n in ns],[('盧','植','子幹'),(None,'毓','子家')]);self.assertTrue(all(n['human_reviewed']is False for n in ns))
 def author_case(self):
  ws={w['id']:w for w in json.loads((R/'registry/works.json').read_text())['works']};w=ws['w-wuxingzhuan-hhs064-luzhi-reference'];e=copy.deepcopy(w['source_author_attributions'][0]);return e
 def author_errors(self,e,c=None):
  from scripts.source_author_prefix import source_author_errors
  c=c or self.c;return source_author_errors({e['referenced_work_id']:{'source_author_attributions':[e]}},{c['id']:c})
 def test_title_author_suffix_actual(self):
  e=self.author_case();self.assertEqual(e['author_name'],'劉向');self.assertEqual(e['authorship_syntax']['kind'],'title_author_suo_zhu');self.assertEqual(self.author_errors(e),[])
 def test_title_author_not_biography_subject_or_second_same_name(self):
  e=self.author_case();e['author_person_id']=next(m['person_id']for m in self.ps['p001']['mentions']if m['surface']=='盧植');self.assertTrue(self.author_errors(e));e=self.author_case();p=self.ps['note026'];second=[m for m in p['mentions']if m['surface']=='劉向'][1];e['author_mention_id']=second['id'];self.assertTrue(self.author_errors(e))
 def test_title_author_wrong_roles_quote_and_definition(self):
  for mutate in [lambda e:e.update(work_id=e['referenced_work_id']),lambda e:e.update(quote=e['quote'][:-1]),lambda e:e['authorship_syntax'].update(following_explanation=dict(start=0,end=2,quote='朓者'))]:
   e=self.author_case();mutate(e);self.assertTrue(self.author_errors(e))
 def test_title_author_negation_consistent_anchors_rejected(self):
  e=self.author_case();c=copy.deepcopy(self.c);p=next(p for p in c['paragraphs']if p['id']==e['paragraph_id']);at=3;p['text']=p['text'][:at]+'非'+p['text'][at:]
  for m in p['mentions']:
   if m['start']>=at:m['start']+=1;m['end']+=1
  e['quote']=p['text'];cl=e['authorship_syntax']['authorship_clause'];cl['end']+=1;cl['quote']=p['text'][:cl['end']];q=e['authorship_syntax']['following_explanation'];q['start']+=1;q['end']+=1;self.assertTrue(self.author_errors(e,c))
 def test_title_author_generic_no_historical_id_whitelist(self):
  e=self.author_case();c=copy.deepcopy(self.c);p=next(p for p in c['paragraphs']if p['id']==e['paragraph_id']);old=e['author_person_id'];p['text']=p['text'].replace('劉向','甲乙').replace('五行傳','丙丁戊')
  for m in p['mentions']:
   if m.get('person_id')==old:m['person_id']='synthetic-author';m['surface']='甲乙'
   if m.get('kind')=='work':m['surface']='丙丁戊';m['work_id']='synthetic-work'
  e.update(author_person_id='synthetic-author',author_name='甲乙',author_surface='甲乙',referenced_work_id='synthetic-work',quote=p['text']);e['authorship_syntax']['authorship_clause']['quote']='丙丁戊甲乙所著';self.assertEqual(self.author_errors(e,c),[])
 def test_weiren_scope_not_extended(self):
  p=self.ps['note046'];self.assertEqual(p['text'],'孟賁多力者也夏育勇者也並衞人荆荆軻也諸專諸也');scope=json.loads((R/'source-evidence/houhan064-luzhi/source-reading.json').read_text())['qualified_geographic_reading'];self.assertEqual(scope['quote'],p['text']);self.assertEqual(scope['applies_to'],['孟賁','夏育']);self.assertEqual(scope['does_not_extend_to'],['荆軻','專諸'])
