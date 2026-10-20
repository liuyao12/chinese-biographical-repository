# coding: utf-8
from pathlib import Path
import copy,json,unittest
try:
 from scripts.song041_title_semantics import heading_posthumous_valid,recalled_gift_valid,enfeoffment_valid,conferment_valid,line_succession_valid,memorial_errors,source_use_errors
 from scripts.posthumous_gifts import posthumous_gift_valid
except ImportError:
 from song041_title_semantics import heading_posthumous_valid,recalled_gift_valid,enfeoffment_valid,conferment_valid,line_succession_valid,memorial_errors,source_use_errors
 from posthumous_gifts import posthumous_gift_valid
R=Path(__file__).resolve().parents[1]
class Song041TitleTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((R/'corpus/songshu/041-parents.json').read_text());cls.ps={p['id']:(cls.c['id'],p)for p in cls.c['paragraphs']};cls.ms={m['id']:(cls.c['id'],p['id'],m)for p in cls.c['paragraphs']for m in p['mentions']};cls.h={h['id']:h for h in json.loads((R/'corpus/songshu/041-parents-titles.json').read_text())['holdings']};cls.events={e['id']:e for e in json.loads((R/'corpus/songshu/041-parents-life-events.json').read_text())['events']};cls.rel=json.loads((R/'corpus/songshu/041-parents-kinship-assertions.json').read_text())['assertions'];cls.people={p['id']for p in json.loads((R/'registry/persons.json').read_text())['persons']}
 def test_explicit_grants_not_attestations_and_only_two_numeric_boundaries(self):
  for key in('xiao-yuzhang','xiao-taifei','xiao-taihuangtaihou','zhaowife-shouchang'):
   h=self.h['th-song041-'+key];self.assertTrue(conferment_valid(h,self.ps));self.assertEqual(h['mode'],'grant')
   bad=copy.deepcopy(h);bad['mode']='attestation';self.assertFalse(conferment_valid(bad,self.ps))
  self.assertEqual(self.h['th-song041-xiao-yuzhang']['effective_period']['start']['normalized_date']['year'],411)
  self.assertEqual(self.h['th-song041-yi-linhe']['effective_period']['start']['normalized_date']['year'],421)
  for key in('zhuo-jinzi','yi-jinzi','zhuo-fengyang','xiao-taifei','xiao-taihuangtaihou','zhaowife-shouchang'):self.assertNotIn('normalized_date',self.h['th-song041-'+key]['effective_period']['start'])
 def test_posthumous_notice_needs_heading_same_person_and_death(self):
  for key in('zhao-empress','zhao-shimu'):
   h=self.h['th-song041-'+key];self.assertTrue(heading_posthumous_valid(h,self.ps,self.events));self.assertFalse(heading_posthumous_valid(h,self.ps,{}))
   bad=copy.deepcopy(h);bad['person_id']='z9t_scz_pgk';self.assertFalse(heading_posthumous_valid(bad,self.ps,self.events));bad=copy.deepcopy(h);bad['effective_period']['start']['normalized_date']={'year':420};self.assertFalse(heading_posthumous_valid(bad,self.ps,self.events))
  self.assertEqual(self.h['th-song041-xiao-shiyi']['mode'],'attestation')
 def test_recalled_gifts_are_enacted_but_do_not_borrow_request_year(self):
  for key in('zhuo-jinzi','yi-jinzi'):
   h=self.h['th-song041-'+key];self.assertTrue(recalled_gift_valid(h,self.ps));bad=copy.deepcopy(h);bad['effective_period']['start']['date_expression']='永初二年';self.assertFalse(recalled_gift_valid(bad,self.ps));bad=copy.deepcopy(h);bad['person_id']='5kj_f4r_znr';self.assertFalse(recalled_gift_valid(bad,self.ps))
  self.assertFalse(posthumous_gift_valid({'posthumous_basis':None},self.ps,self.ms,{}))
 def test_enfeoffments_bind_the_named_or_continued_subject(self):
  for key in('yi-linhe','zhuo-fengyang'):
   h=self.h['th-song041-'+key];self.assertTrue(enfeoffment_valid(h,self.ps));bad=copy.deepcopy(h);bad['person_id']='lc5_nwz_ikf';self.assertFalse(enfeoffment_valid(bad,self.ps));bad=copy.deepcopy(h);bad['enfeoffment_basis']['source_term']='並宜追封開國縣侯食邑五百戸';self.assertFalse(enfeoffment_valid(bad,self.ps))
 def test_memorial_unknown_is_not_denied_and_500_households_not_enacted(self):
  qs=self.c['annotation']['title_proposals'];self.assertEqual(len(qs),6)
  for q in qs:self.assertEqual(memorial_errors(q,self.c,self.people,self.h),[])
  sun=next(q for q in qs if q['title']=='豫章郡建昌縣君');self.assertEqual(sun['outcome'],'not_reported');self.assertFalse(any(h['person_id']==sun['person_id']and h['title']==sun['title']for h in self.h.values()))
  for q in [q for q in qs if q['title']=='開國縣侯']:
   self.assertEqual(q['requested_households']['enactment_status'],'not_confirmed');bad=copy.deepcopy(q);bad['requested_households']['enactment_status']='granted';self.assertTrue(memorial_errors(bad,self.c,self.people,self.h))
 def test_source_line_root_and_ritual_predecessor_are_not_parentage(self):
  h=self.h['th-song041-xizhi-line-succession'];self.assertTrue(line_succession_valid(h,self.h,self.ps,self.rel));i=h['inheritance'];self.assertEqual(i['predecessor_person_id'],'own_emy_xoj');self.assertEqual(i['ritual_predecessor_person_id'],'bmu_ige_b8v');self.assertEqual(i['intervening_holding_status'],'not_asserted');self.assertFalse(any(a['subject_person_id']=='lc5_nwz_ikf'and a['predicate']in('father','adoptive_father')for a in self.rel))
  for key,value in [('predecessor_person_id','bmu_ige_b8v'),('intervening_holding_status','attested')]:
   bad=copy.deepcopy(h);bad['inheritance'][key]=value;self.assertFalse(line_succession_valid(bad,self.h,self.ps,self.rel))
  bad=copy.deepcopy(h);bad['effective_period']['start']['date_expression']='永初二年';self.assertFalse(line_succession_valid(bad,self.h,self.ps,self.rel))
  z=self.h['th-song041-zulian-succession'];self.assertEqual(z['effective_period']['end']['event_type'],'abolition');self.assertNotIn('normalized_date',z['effective_period']['end'])
 def test_source_uses_keep_pronouns_out_of_holdings(self):
  uses=self.c['annotation']['source_title_uses'];self.assertEqual(len(uses),22)
  for u in uses:self.assertEqual(source_use_errors(u,self.c,self.people,self.h),[])
  for u in [x for x in uses if x['usage_kind']=='contextual_pronoun']:
   self.assertFalse(u['holding_ids']);bad=copy.deepcopy(u);bad['holding_ids']=['th-song041-xiao-taifei'];self.assertTrue(source_use_errors(bad,self.c,self.people,self.h))
 def test_opaque_received_wording_and_all66_consumption(self):
  d=json.loads((R/'source-evidence/song041-titles/consumption-disposition.json').read_text());self.assertEqual(len(d['records']),66)
  allh=list(self.h.values())+json.loads((R/'corpus/songshu/001-parents-reference-titles.json').read_text())['holdings'];known={x['id']for x in allh+self.c['annotation']['title_proposals']+self.c['annotation']['source_title_uses']}|{m['id']for p in self.c['paragraphs']for m in p['mentions']}
  self.assertTrue(all(set(r['record_ids']).issubset(known)for r in d['records']))
  self.assertIn('臣等參受宋王太后號',self.c['paragraphs'][1]['text']);self.assertEqual(self.h['th-song041-xiao-songwangtaihou']['mode'],'attestation');self.assertEqual(self.h['th-song041-xiao-songwangtaihou']['effective_period']['start']['status'],'unknown')
if __name__=='__main__':unittest.main()
