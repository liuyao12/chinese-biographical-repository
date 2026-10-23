import unittest,json,copy,tempfile,hashlib,sys,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R))
from scripts.fixed_received_career import holding_valid,nonholding_valid,local_date_valid,local_scope,recipient
from scripts.validate_corpus import normalized_date_errors
C=json.loads((R/'corpus/sanguozhi/026-guohuai.json').read_text());H=json.loads((R/'corpus/sanguozhi/026-guohuai-titles.json').read_text())['holdings'];L=json.loads((R/'corpus/sanguozhi/026-guohuai-life-events.json').read_text())['events'];A=json.loads((R/'corpus/sanguozhi/026-guohuai-addresses.json').read_text())['assertions'];D=json.loads((R/'corpus/sanguozhi/026-guohuai-source-details.json').read_text())['records'];E=json.loads((R/'corpus/sanguozhi/026-guohuai-person-events.json').read_text())['events'];HS={h['id']:h for h in H}
def holding(title):return copy.deepcopy(next(h for h in H if h['title']==title))
class FixedReceivedCareer(unittest.TestCase):
 def test_all_actual_holdings_and_nonholdings(self):
  self.assertEqual(len(H),32)
  for h in H:self.assertTrue(holding_valid(h,C,R),h['id'])
  for seq,kind in [(L,'life'),(A,'address'),(D,'detail'),(E,'succession')]:
   for x in seq:self.assertTrue(nonholding_valid(x,C,R,kind,HS),x['id'])
 def test_actual_local_years_and_no_synthetic_emperor_mention(self):
  for title,year in [('揚武將軍',231),('車騎將軍',250),('大將軍',255)]:
   h=holding(title);date=h['effective_period']['start']['normalized_date'];self.assertEqual(date['year'],year);self.assertEqual(normalized_date_errors(date,{C['id']:C},R,h,'start'),[])
  self.assertTrue(all(m['start']<m['end']for p in C['paragraphs']for m in p['mentions']))
 def test_whole_consistent_wrong_recipient(self):
  for title in ('平原府丞','門下賊曹','丞相兵曹議令史'):
   h=holding(title);p=next(p for p in C['paragraphs']if p['id']==h['evidence'][0]['paragraph_id']);other=next(m for m in p['mentions']if m.get('person_id')!=h['person_id']and m['kind']=='person');h['person_id']=other['person_id'];h['evidence'][0]['person_mention_id']=other['id'];h['attestations'][0]['person_mention_id']=other['id'];self.assertFalse(holding_valid(h,C,R))
 def test_whole_valid_date_reassigned_to_another_death(self):
  e=copy.deepcopy(next(x for x in L if x.get('normalized_date',{}).get('year')==255));p=next(p for p in C['paragraphs']if p['id']==e['evidence'][0]['paragraph_id']);other=next(m for m in p['mentions']if m['surface']=='統');e['person_id']=other['person_id'];e['evidence'][0]['person_mention_id']=other['id'];e['normalized_date']['evidence']=copy.deepcopy(e['evidence']);self.assertFalse(local_date_valid(e['normalized_date'],C,R,e,'life_event'));self.assertFalse(nonholding_valid(e,C,R,'life'))
 def test_no_borrow_death_date_for_son(self):
  parent=next(x for x in L if x.get('normalized_date',{}).get('year')==255);child=copy.deepcopy(next(x for x in L if x['source_term']=='薨'and x['date_expression']is None));child['normalized_date']=copy.deepcopy(parent['normalized_date']);child['normalized_date']['evidence']=copy.deepcopy(child['evidence']);child['date_expression']='正元二年';self.assertFalse(nonholding_valid(child,C,R,'life'))
 def test_dates_reset_and_order_are_complete(self):
  h=holding('車騎將軍');date=h['effective_period']['start']['normalized_date'];scope=date['regnal_year_mapping']['scope'];self.assertEqual(scope['full_era_anchor']['surface'],'嘉平元年');self.assertEqual([x['surface']for x in scope['ordered_dates']],['嘉平元年','二年'])
  for mutation in ('swap','omit','cross_era','number'):
   x=copy.deepcopy(date);mp=x['regnal_year_mapping'];sc=mp['scope']
   if mutation=='swap':sc['full_era_anchor'],sc['target_anchor']=sc['target_anchor'],sc['full_era_anchor']
   if mutation=='omit':sc['ordered_dates'].pop(0)
   if mutation=='cross_era':mp['era_name']='正始';mp['start_ce_year']=240;mp['end_ce_year']=249;x['year']=x['era_year']=241
   if mutation=='number':mp['regnal_year']=5;x['year']=x['era_year']=253
   self.assertFalse(local_date_valid(x,C,R,h,'start'),mutation)
 def test_new_era_stage_resets_before_bare_year(self):
  from unittest.mock import patch
  cc=copy.deepcopy(C);p=cc['paragraphs'][3];p['text']='黃初元年太和中五年';pos=p['text'].index('五年')
  with patch('scripts.fixed_received_career.witness',return_value={'path':'synthetic','sha256':'synthetic'}):
   sc=local_scope(cc,p['id'],pos,R,{})
  self.assertEqual(sc['target_anchor']['era_name'],'太和');self.assertEqual(sc['full_era_anchor']['surface'],'太和中');self.assertEqual(sc['target_anchor']['regnal_year'],5)
 def test_date_requires_bound_record_and_actual_title(self):
  h=holding('車騎將軍');d=h['effective_period']['start']['normalized_date'];self.assertTrue(normalized_date_errors(d,{C['id']:C},R,None,None));h['title']='大將軍';self.assertTrue(normalized_date_errors(d,{C['id']:C},R,h,'start'))
 def test_subsequent_appointment_cannot_borrow_opening_first_year(self):
  h=holding('前將軍');self.assertIsNone(h['effective_period']['start']['date_expression']);self.assertNotIn('normalized_date',h['effective_period']['start']);self.assertTrue(h['date_qualification']['same_year_not_asserted']);self.assertEqual(h['date_qualification']['source_term'],'其後')
  source=holding('左將軍');h['effective_period']['start']['date_expression']='正始元年';h['effective_period']['start']['normalized_date']=copy.deepcopy(source['effective_period']['start']['normalized_date']);h['effective_period']['start']['normalized_date']['evidence']=copy.deepcopy(h['evidence']);self.assertFalse(holding_valid(h,C,R));self.assertFalse(local_date_valid(h['effective_period']['start']['normalized_date'],C,R,h,'start'))
 def test_office_death_does_not_end_every_holding(self):
  self.assertTrue(all(h['effective_period']['end']==dict(status='unknown',date_expression=None,evidence=[])for h in H));h=holding('車騎將軍');h['effective_period']['end']=dict(status='source_event',event_type='death',date_expression='正元二年',evidence=h['evidence']);self.assertFalse(holding_valid(h,C,R))
 def test_confirmation_not_five_year_tenure(self):
  d=copy.deepcopy(next(d for d in D if d['kind']=='office_confirmation'));self.assertEqual(d['values']['normalized_year'],224);self.assertIsNone(d['values']['duration_years']);d['values']['duration_years']=5;self.assertFalse(nonholding_valid(d,C,R,'detail',HS))
 def test_region_not_office_tenure(self):
  d=copy.deepcopy(next(d for d in D if d['kind']=='regional_service_duration'));self.assertEqual(d['values']['bound_operator'],'gt');self.assertIsNone(d['values']['linked_holding_id']);d['values']['linked_holding_id']=H[0]['id'];self.assertFalse(nonholding_valid(d,C,R,'detail',HS))
 def test_linked_office_wrong_person_or_wrong_slot(self):
  d=copy.deepcopy(next(d for d in D if d['kind']=='office_confirmation'))
  for h in H:
   if h['title']in('大司農','射陽亭侯'):
    x=copy.deepcopy(d);x['values']['linked_holding_id']=h['id'];self.assertFalse(nonholding_valid(x,C,R,'detail',HS))
 def test_unnamed_child_not_assigned_or_assumed_biological(self):
  d=copy.deepcopy(next(d for d in D if d['kind']=='unnamed_family_title_grants'));self.assertEqual(d['values']['recipient_person_ids'],[]);self.assertFalse(d['values']['biological_children_only'])
  for key,val in [('recipient_person_ids',[L[0]['person_id']]),('biological_children_only',True)]:
   x=copy.deepcopy(d);x['values'][key]=val;self.assertFalse(nonholding_valid(x,C,R,'detail',HS))
 def test_source_location_not_native_place(self):
  for d in A:
   if d['relation']=='source_locality_designation':
    x=copy.deepcopy(d);x['relation']='biographical_origin';self.assertFalse(nonholding_valid(x,C,R,'address'))
 def test_unranked_succession_no_title_invented(self):
  for e in E:
   self.assertIsNone(e['title']);x=copy.deepcopy(e);x['title']='爵';self.assertFalse(nonholding_valid(x,C,R,'succession'))
 def test_notes_cannot_inherit_body_year(self):
  with self.assertRaises(AssertionError):local_scope(C,C['paragraphs'][13]['id'],0,R,H[0]['received_source_frame']['fixed_witness_reference'])
 def test_symlink_receipt_and_raw_co_shift_rejected(self):
  h=holding('車騎將軍');b=h['received_source_frame'];rp=b['fixed_witness_reference']['path'];raw=C['source']['raw_path']
  with tempfile.TemporaryDirectory()as tmp:
   root=Path(tmp)
   for rel in (rp,raw):q=root/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/rel,q)
   self.assertTrue(holding_valid(h,C,root));cc=copy.deepcopy(C);rr=root/raw;rr.write_bytes(b'\n'+rr.read_bytes());cc['source']['raw_file_sha256']=hashlib.sha256(rr.read_bytes()).hexdigest()
   for p in cc['paragraphs']:
    for f in p['source_position']['source_fragments']:f['line']+=1
   self.assertFalse(holding_valid(h,cc,root));link=root/'source-evidence/link';link.symlink_to((root/rp).parent,target_is_directory=True);x=copy.deepcopy(h);x['received_source_frame']['fixed_witness_reference']['path']='source-evidence/link/'+Path(rp).name;self.assertFalse(holding_valid(x,C,root))
 def test_added_hidden_date_cannot_skip_receipt(self):
  cc=copy.deepcopy(C);p=cc['paragraphs'][11];p['text']='正始三年'+p['text'];h=holding('車騎將軍');self.assertFalse(holding_valid(h,cc,R))
 def test_synthetic_ids_are_not_name_id_allowlist(self):
  cc=copy.deepcopy(C);remap={m['person_id']:'synthetic_'+str(i)for i,m in enumerate({m['person_id']:m for p in cc['paragraphs']for m in p['mentions']if m['kind']=='person'}.values())}
  for p in cc['paragraphs']:
   for m in p['mentions']:
    if m['kind']=='person':m['person_id']=remap[m['person_id']]
  h=holding('車騎將軍');h['person_id']=remap[h['person_id']];self.assertTrue(holding_valid(h,cc,R))
if __name__=='__main__':unittest.main()
