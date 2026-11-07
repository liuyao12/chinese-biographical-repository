"""Current-rendered single-year context is an explicit event association."""
import copy,hashlib,json,os,tempfile,unittest
from pathlib import Path
from scripts.validate_corpus import normalized_date_errors
from scripts.annal_year_context import life_event_year_context_valid
SOURCE=Path(os.environ.get('CBR_ANNAL_SOURCE_ROOT',Path(__file__).resolve().parents[1]))
ERA_SOURCE=Path(os.environ.get('CBR_ANNAL_ERA_SOURCE_ROOT',SOURCE))
CP='corpus/zizhitongjian/142-xietiao-death-rendered.json'
LP='corpus/zizhitongjian/142-xietiao-death-rendered-life-events.json'
class RenderedSingleYearAnnal(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
  self.ch=json.loads((SOURCE/CP).read_text());self.event=json.loads((SOURCE/LP).read_text())['events'][0];self.date=self.event['normalized_date'];self.section=self.ch['source']['annal_year_sections'][0]
  self.obpath=self.section['observation_path'];self.ob=json.loads((SOURCE/self.obpath).read_text());self.assoc=self.ch['annotation']['annal_event_year_associations'][0]
  self.work=dict(id=self.ch['work_id'],title=self.ob['units']['work_title']['text'],books=[dict(id=self.ch['book_id'],work_id=self.ch['work_id'],number=142,chapter_ids=[self.ch['id']])])
  mid=self.assoc['person_mention_id'];m=next(m for m in self.ch['paragraphs'][0]['mentions']if m['id']==mid)
  self.person=dict(id=m['person_id'],aliases=[dict(surface=m['surface'],mention_ids=[mid])],evidence=[dict(work_id=self.ch['work_id'],book_id=self.ch['book_id'],source_id=self.ch['source_id'],chapter_id=self.ch['id'],paragraph_id=self.ch['paragraphs'][0]['id'],mention_id=mid,quote=m['surface'])])
  modern=self.date['references'][0]['local_capture'];q=self.root/modern['path'];q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes((ERA_SOURCE/modern['path']).read_bytes());self.sync()
 def save(self,path,d):
  p=self.root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False))
 def sync(self):
  self.save(self.obpath,self.ob);self.section['observation_sha256']=hashlib.sha256((self.root/self.obpath).read_bytes()).hexdigest();self.date['references'][1]['section']=copy.deepcopy(self.section)
  self.save(CP,self.ch);self.save(LP,dict(record_type='person_life_event_assertion_set',chapter_id=self.ch['id'],events=[self.event]));self.save('registry/works.json',dict(works=[self.work]));self.save('registry/work-provenance.json',dict(text_bases={self.ch['source_id']:dict(source_id=self.ch['source_id'],work_id=self.ch['work_id'])}));self.save('registry/persons.json',dict(persons=[self.person]))
 def errors(self):return normalized_date_errors(self.date,{self.ch['id']:self.ch},root=self.root,bound_record=self.event,bound_role='life_event')
 def rejects(self):self.assertTrue(self.errors())
 def test_real_complete_capture_year499(self):self.assertEqual(self.errors(),[]);self.assertNotIn('永元',self.date['original_quote']);self.assertNotIn('month',self.date)
 def test_life_event_without_literal_date_requires_bound_year_context(self):
  self.assertIsNone(self.event['date_expression']);self.assertTrue(life_event_year_context_valid(self.event,{self.ch['id']:self.ch},root=self.root))
  self.ch['annotation']['annal_event_year_associations']=[];self.sync()
  self.assertFalse(life_event_year_context_valid(self.event,{self.ch['id']:self.ch},root=self.root))
 def test_life_event_context_rejects_wrong_receiver(self):
  self.event['person_id']='wrong';self.sync()
  self.assertFalse(life_event_year_context_valid(self.event,{self.ch['id']:self.ch},root=self.root))
 def test_life_event_context_is_not_a_literal_date_substitute(self):
  self.event['date_expression']='永元元年';self.sync()
  self.assertFalse(life_event_year_context_valid(self.event,{self.ch['id']:self.ch},root=self.root))
 def test_cross_year_arithmetic(self):self.date.update(year=500,era_year=500);self.sync();self.rejects()
 def test_modern_caption_cannot_be_received_year(self):self.ob['units']['year_heading']['layer']='received_chapter';self.sync();self.rejects()
 def test_modern_ce_caption_not_era_expression(self):self.date['source_expression']='公元四九九年';self.sync();self.rejects()
 def test_wrong_book(self):self.work['books'][0]['number']=143;self.sync();self.rejects()
 def test_wrong_paragraph(self):self.date['annal_year_reference']['event_paragraph_id']='other';self.sync();self.rejects()
 def test_no_automatic_year_without_association(self):self.ch['annotation']['annal_event_year_associations']=[];self.sync();self.rejects()
 def test_retrospective_scope(self):self.assoc['temporal_scope']='retrospective_or_quoted_event';self.sync();self.rejects()
 def test_acquisition_upgrade_even_both_sides(self):
  self.ob['fixed_body_obtained']=self.ch['source']['fixed_body_obtained']=True;self.sync();self.rejects()
 def test_image_upgrade_even_both_sides(self):
  self.ob['image_verified']=self.ch['source']['image_verified']=True;self.sync();self.rejects()
 def test_month_and_day_not_inferred(self):
  for k,v in [('month',8),('day',1),('day_ganzhi','乙卯')]:
   with self.subTest(field=k):self.date[k]=v;self.sync();self.rejects();self.date.pop(k)
 def test_fragmented_event_map(self):self.ob['units']['event']['character_map'].pop();self.sync();self.rejects()
 def test_same_length_map_edit(self):self.ob['units']['event']['character_map'][0]+=1;self.sync();self.rejects()
 def test_no_year_total(self):
  self.ob['units']['one_year_total']['text']='屠維單閼，二十一年。';self.ob['units']['one_year_total']['text_sha256']=hashlib.sha256(self.ob['units']['one_year_total']['text'].encode()).hexdigest();self.sync();self.rejects()
 def test_wrong_official_year(self):
  self.date['regnal_year_mapping'].update(start_ce_year=500,end_ce_year=502);self.date.update(year=500,era_year=500);self.date['references'][0]['columns'].update(first_year='500',last_year='502');self.sync();self.rejects()
 def test_wrong_receiver(self):self.event['person_id']='wrong';self.sync();self.rejects()
 def test_reverse_loss(self):self.person['evidence']=[];self.sync();self.rejects()
 def test_typed_flag(self):self.ch['source']['human_reviewed']=0;self.sync();self.rejects()
 def test_legal_metadata_enrichment(self):self.person['unknown_future']={'ok':True};self.sync();self.assertEqual(self.errors(),[])
 def test_coherent_rekey_keeps_capture_bytes(self):
  before=(self.root/self.obpath).read_bytes();old=self.event['person_id'];new='zzz_abc_123_A';self.event['person_id']=new;self.person['id']=new
  for m in self.ch['paragraphs'][0]['mentions']:
   if m.get('person_id')==old:m['person_id']=new
  self.sync();self.assertEqual(before,(self.root/self.obpath).read_bytes());self.assertEqual(self.errors(),[])
 def test_single_endpoint_rekey(self):self.person['id']='zzz_abc_123_A';self.sync();self.rejects()
 def replace_event_capture(self,text,all_shift=0,last_shift=0):
  p=self.ch['paragraphs'][0];u=self.ob['units']['event'];start=u['character_map'][0];old=p['text'];self.ob['observed_text']=self.ob['observed_text'][:start]+text+self.ob['observed_text'][start+len(old):]
  u.update(text=text,character_map=list(range(start,start+len(text))),text_sha256=hashlib.sha256(text.encode()).hexdigest());p['text']=text;self.ch['text_sha256']=hashlib.sha256(text.encode()).hexdigest()
  for m in p['mentions']:m['start']+=all_shift;m['end']+=all_shift
  mid=next(m for m in p['mentions']if m['id']==self.assoc['person_mention_id']);mid['start']+=last_shift;mid['end']+=last_shift
  a=self.assoc['event_anchor'];a.update(start=mid['start'],end=mid['end']+len(self.event['source_term'])+1);a['surface']=text[a['start']:a['end']]
  self.event['evidence'][0]['quote']=text;self.date['original_quote']=text;self.sync()
 def test_quoted_death_cannot_use_current_year(self):
  old=self.ch['paragraphs'][0]['text'];a=self.assoc['event_anchor'];self.replace_event_capture(old[:a['start']]+'「'+a['surface']+'」',last_shift=1);self.rejects()
 def test_explicit_retrospective_paragraph_refused(self):
  self.replace_event_capture('初，'+self.ch['paragraphs'][0]['text'],all_shift=2);self.rejects()
 def test_same_source_cannot_claim_raw_obtained(self):
  self.ob['raw_capture_obtained']=self.ch['source']['raw_capture_obtained']=True;self.sync();self.rejects()
 def test_annal_date_not_free_general_event_date(self):
  self.assertTrue(normalized_date_errors(self.date,{self.ch['id']:self.ch},root=self.root,bound_record=self.event,bound_role='attestation'))
 def test_inserted_other_year_boundary_with_valid_maps(self):
  pos=self.ob['units']['year_heading']['character_map'][-1]+1;insert='\nL121: ==永元二年==\n';self.ob['observed_text']=self.ob['observed_text'][:pos]+insert+self.ob['observed_text'][pos:]
  for u in self.ob['units'].values():u['character_map']=[i+len(insert)if i>=pos else i for i in u['character_map']]
  self.sync();self.rejects()
 def test_duplicate_alias_mid(self):
  self.person['aliases'][0]['mention_ids']*=2;self.sync();self.rejects()
 def test_duplicate_reverse_mid(self):
  self.person['evidence']*=2;self.sync();self.rejects()
 def test_reverse_source_metadata_wrong(self):
  self.person['evidence'][0]['source_id']='other';self.sync();self.rejects()
 def test_negative_book_anchor_not_python_slice(self):
  n=len(self.ob['units']['book_title']['text']);self.section['book_number_anchor'].update(start=1-n,end=6-n);self.sync();self.rejects()
if __name__=='__main__':unittest.main()
