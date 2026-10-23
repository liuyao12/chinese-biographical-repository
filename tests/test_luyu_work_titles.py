import unittest,json,copy,hashlib
from pathlib import Path
from scripts.source_author_prefix import source_author_errors
R=Path(__file__).resolve().parents[1]
class LuyuWorkTitles(unittest.TestCase):
 def setUp(self):
  self.c=json.loads((R/'corpus/sanguozhi/022-luyu.json').read_text());self.ws={w['id']:w for w in json.loads((R/'registry/works.json').read_text())['works']};self.es=[e for w in self.ws.values()for e in w.get('source_author_attributions',[])if e['chapter_id']==self.c['id'] and e['authorship_syntax']['kind']=='resumed_biographical_subject_named_works']
 def checkev(self,e):return source_author_errors({e['referenced_work_id']:{'source_author_attributions':[e]}},{self.c['id']:self.c})
 def test_exact_two_reported_authors(self):
  self.assertEqual(len(self.es),2)
  for e in self.es:self.assertEqual(self.checkev(e),[]);self.assertIn('續漢書',e['qualification']);self.assertIn('未親見',e['qualification'])
 def test_wrong_person_and_reporter_not_author(self):
  for orig in self.es:
   for key,val in [('author_person_id','other'),('quote',orig['quote'][:-1])]:
    e=copy.deepcopy(orig);e[key]=val;self.assertTrue(self.checkev(e))
   e=copy.deepcopy(orig);e['authorship_syntax']['reporting_work_mention_id']=e['work_mention_id'];self.assertTrue(self.checkev(e))
 def test_exact_source_file_and_anchor(self):
  d=json.loads((R/'source-evidence/luyu-work-title-author-qualification/review.json').read_text())
  for s in d['sources']:
   t=(R/s['path']).read_text();self.assertEqual(hashlib.sha256(t.encode()).hexdigest(),s['sha256']);a=s['anchor'];self.assertEqual(t[a['start']:a['end']],a['quote'])
  ref=d['parallel_title_variant'];t=(R/ref['path']).read_text();self.assertEqual(hashlib.sha256(t.encode()).hexdigest(),ref['sha256']);a=ref['anchor'];self.assertEqual(t[a['start']:a['end']],a['quote'])
  p=next(p for p in self.c['paragraphs']if p['id']==d['native_citation_frame']['paragraph_id']);self.assertEqual(p['text'],d['native_citation_frame']['quote'])
  for dec in d['decisions']:
   a=dec['native_anchor'];self.assertEqual(p['text'][a['start']:a['end']],a['quote']);m=next(m for m in p['mentions']if m['id']==dec['work_mention_id']);self.assertEqual(m['work_id'],dec['work_id']);self.assertLessEqual(a['start'],m['start']);self.assertGreaterEqual(a['end'],m['end'])
 def test_titles_and_unknown_authors_not_promoted(self):
  for k,t in [('shi','詩經'),('li','禮記'),('ji','禮記'),('shu','尚書')]:self.assertEqual(self.ws['w-'+k+'-sgz022-luyu-reference']['citation_title'],t)
  for k in ('xuhanshu','jinzhugongzan','chen-biezhuan'):self.assertIsNone(self.ws['w-'+k+'-sgz022-luyu-reference']['author'])
  self.assertIn('不等於',self.ws['w-shu-sgz022-luyu-reference']['citation_qualification'])
 def test_same_contract_without_historical_person_whitelist(self):
  e=copy.deepcopy(self.es[0]);c=copy.deepcopy(self.c);p=next(p for p in c['paragraphs']if p['id']==e['paragraph_id']);old=e['author_person_id'];p['text']=p['text'].replace('植','甲')
  for m in p['mentions']:
   if m.get('person_id')==old:m['person_id']='synthetic-author'
   if m['surface']=='植':m['surface']='甲'
  e.update(author_person_id='synthetic-author',author_surface='甲',author_name='甲',quote=p['text']);e['authorship_syntax']['scope_quote']=e['authorship_syntax']['scope_quote'].replace('植','甲');w={e['referenced_work_id']:{'source_author_attributions':[e]}};self.assertEqual(source_author_errors(w,{c['id']:c}),[])
  a=next(m for m in p['mentions']if m['id']==e['author_mention_id']);a['start']+=1;self.assertTrue(source_author_errors(w,{c['id']:c}))
 def test_intervening_person_rejected(self):
  e=copy.deepcopy(self.es[0]);c=copy.deepcopy(self.c);p=next(p for p in c['paragraphs']if p['id']==e['paragraph_id']);start=p['text'].index('博士');p['mentions'].append(dict(id='synthetic-other',kind='person',person_id='other',surface='博士',start=start,end=start+2));self.assertTrue(source_author_errors({e['referenced_work_id']:{'source_author_attributions':[e]}},{c['id']:c}))
 def test_yuyu_is_explicit_prefix_not_modern_jinshu(self):
  w=self.ws['w-jinshu-yuyu-sgz022-luyu-reference'];es=w['source_author_attributions'];self.assertEqual(len(es),1);e=es[0];self.assertEqual(e['author_surface'],'虞預');self.assertEqual(e['authorship_syntax']['kind'],'author_title_prefix');self.assertEqual(source_author_errors({w['id']:w},{self.c['id']:self.c}),[])
