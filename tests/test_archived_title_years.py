"""Synthetic immutable-annal title-event binding tests; not historical source evidence."""
import unittest,tempfile,hashlib,copy
from pathlib import Path
from scripts.archived_title_years import valid,project,has_intervening_year
class ArchivedTitleYears(unittest.TestCase):
 def fixture(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);root=Path(self.tmp.name)
  raw='太和元年春正月甲事四年春二月癸巳以大將軍曹真為大司馬夏四月乙事';path='source-evidence/sgz009-titles/synthetic.txt';p=root/path;p.parent.mkdir(parents=True);p.write_text(raw)
  def a(q):
   i=raw.index(q);return {'start':i,'end':i+len(q),'quote':q}
  ev=[{'chapter_id':'c','paragraph_id':'p','quote':'曹真四年遷大司馬'}]
  d={'calendar':'chinese_civil','era':'CE','era_year':230,'year':230,'original_quote':ev[0]['quote'],'evidence':ev,'references':[{'scope':'modern_era_year_equivalence_only','quote':'太和','columns':{'era_name':'太和','first_year':'227','last_year':'233'}}],'regnal_year_mapping':{'kind':'archived_parallel_title_ce_span','era_name':'太和','source_number':'四','regnal_year':4,'start_ce_year':227,'end_ce_year':233,'reference_index':0},'archived_title_year':{'holding_id':'h','person_id':'person','role':'start','source_event_quote':'遷大司馬','event_relation':'same_explicit_appointment','reference':{'path':path,'sha256':hashlib.sha256(raw.encode()).hexdigest(),'revision_id':'a'*40,'file':'synthetic.txt','url':'https://raw.githubusercontent.com/kanripo/KR2a0012/'+'a'*40+'/synthetic.txt','era_heading':a('太和元年'),'year_heading':a('四年春二月'),'event':a('以大將軍曹真為大司馬'),'actor':a('曹真'),'title':a('大司馬')}}}
  ref=d['archived_title_year']['reference'];d['basis']={'kind':'parallel_event','source_event_quote':'遷大司馬','reference_url':ref['url'],'reference_event_quote':ref['event']['quote'],'reference_year_quote':raw[ref['era_heading']['start']:ref['year_heading']['end']]}
  h={'id':'h','person_id':'person','title':'大司馬','kind':'office','effective_period':{'start':{'status':'source_event','event_type':'transfer','evidence':ev,'normalized_date':d}}}
  chapters={'c':{'paragraphs':[{'mentions':[{'person_id':'person','surface':'曹真'}]}]}}
  return d,h,chapters,root
 def test_explicit_same_title_and_person(self):
  d,h,c,r=self.fixture();self.assertTrue(valid(d,h,'start',c,r))
 def test_other_person_or_holding_cannot_borrow_date(self):
  for k in ['person_id','id']:
   d,h,c,r=self.fixture();h[k]='other';self.assertFalse(valid(d,h,'start',c,r))
 def test_wrong_year_and_calendar_rejected(self):
  for k,v in [('year',231),('era_year',231),('calendar','gregorian')]:
   d,h,c,r=self.fixture();d[k]=v;self.assertFalse(valid(d,h,'start',c,r))
 def test_foreign_path_or_changed_raw_rejected(self):
  for k,v in [('path','../elsewhere'),('sha256','0'*64),('revision_id','latest')]:
   d,h,c,r=self.fixture();d['archived_title_year']['reference'][k]=v;self.assertFalse(valid(d,h,'start',c,r))
 def test_borrowing_former_title_anchor_rejected(self):
  d,h,c,r=self.fixture();ref=d['archived_title_year']['reference'];ref['title']=dict(ref['title'],start=ref['title']['start']-1);self.assertFalse(valid(d,h,'start',c,r))
 def test_death_is_not_office_termination(self):
  d,h,c,r=self.fixture();h['effective_period']['start']['event_type']='death';self.assertFalse(valid(d,h,'start',c,r))
 def test_annotations_are_excluded_and_original_glyphs_retained(self):
  self.assertEqual(project('甲(元年春(古注))乙¶ <pb:folio>眀年将'),'甲乙眀年将');self.assertIsNone(project('甲(乙'))
class ConservativeYearBoundaries(unittest.TestCase):
 def test_bare_and_month_years_cannot_be_crossed(self):
  for q in ['為齊公三年', '立為齊王景初三年正月丁亥朔', '二年春', '十年十二月', '元年']:
   self.assertTrue(has_intervening_year(q))
 def test_real_archived_bare_year_and_year_month(self):
  root=Path(__file__).resolve().parents[1]
  for n,head,tail in [('003','黄初二年','為平原王'),('004','青龍三年','帝病甚')]:
   raw=(root/('source-evidence/sgz009-titles/fixed-'+n+'.txt')).read_text();t=project(raw);start=t.index(head)+len(head);end=t.index(tail,start);part=t[start:end]
   self.assertTrue(has_intervening_year(part))
 def test_no_year_statement_is_not_rejected(self):
  self.assertFalse(has_intervening_year('十二月甲申以曹真為大司馬'))
if __name__=='__main__':unittest.main()
