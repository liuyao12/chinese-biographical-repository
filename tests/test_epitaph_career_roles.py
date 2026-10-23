import copy,hashlib,unittest
from scripts.epitaph_career_roles import holding_valid,detail_valid

def fixture(case='grant',title=None):
 clauses={'grant':'未幾，以援接之功，除石城長史。','staff':'永平初載，望府啟建，寮佐之選，妙盡時英。以君為伏波將軍、參太尉尚陽王府事。','posthumous':'詔遣謁者持節册贈石城將軍、南州刺史，所以旌崇孝德，禮也。'}
 rules={'grant':'subsequent_appointment','staff':'era_two_staff_appointments','posthumous':'posthumous_two_offices'};modes={'grant':('grant','appointment'),'staff':('grant','concurrent_appointment'),'posthumous':('posthumous_grant','posthumous_office')}
 title=title or {'grant':'石城長史','staff':'參太尉尚陽王府事','posthumous':'南州刺史'}[case];clause=clauses[case];intro='君姓沈，諱寧，字子安，廣陵人也。';death='春秋三十，以延昌四年九月九日，於南城里第瘠甚而卒。';burial='粵以熙平二年九月二日，卜窆於本縣之舊塋焉。';t=intro+(death if case=='posthumous'else'')+clause+burial
 pid='synthetic-p';head=dict(id='synthetic-head-m',kind='person',person_id='synthetic-head',surface='寧',start=t.index('寧'),end=t.index('寧')+1);ms=[head];foreign={}
 if case=='staff':
  i=t.index('太尉尚陽王');m=dict(id='synthetic-patron-m',kind='person',person_id='synthetic-patron',surface='太尉尚陽王',start=i,end=i+len('太尉尚陽王'));ms.append(m);foreign['patron']=m['id']
 sc=dict(paragraph_id=pid,start=t.index(clause),end=t.index(clause)+len(clause),surface=clause);sha=hashlib.sha256(t.encode()).hexdigest();c=dict(id='synthetic-c',work_id='synthetic-w',book_id='synthetic-b',source_id='synthetic-s',source=dict(transcription_witness=dict(original_stone_or_rubbing_image_verified=False)),paragraphs=[dict(id=pid,text=t,text_layer='epitaph_as_modernly_transcribed',mentions=ms)],annotation=dict(epitaph_fact_binding=dict(paragraph_sha256=sha,roles=dict(head=head['id'])),epitaph_life_binding=dict(death_scope=dict(end=len(intro)+len(death)),burial_scope=dict(start=t.index(burial)))))
 e={k:c[k]for k in ['work_id','book_id','source_id']};e.update(chapter_id=c['id'],paragraph_id=pid,quote=t,person_mention_id=head['id']);unknown=dict(status='unknown',date_expression=None,evidence=[]);mode,semantic=modes[case];start=dict(status='source_event',event_type=mode,date_expression='永平初'if case=='staff'else None,evidence=[copy.deepcopy(e)])
 if case=='staff':
  start['normalized_date_range']=dict(basis='within_named_era',calendar='chinese_civil',precision='year_range',year_numbering='astronomical',status='editorial_provisional',source_expression='永平初',source_stage='初',evidence=[copy.deepcopy(e)],original_quote=t,earliest=dict(era='CE',era_year=508,year=508),latest=dict(era='CE',era_year=512,year=512),era_span_mapping=dict(kind='ce_regnal_era_span',reference_index=0,era_name='永平',polity_source_name='北魏',start_ce_year=508,end_ce_year=512),references=[dict(scope='modern_era_year_equivalence_only',quote='永平',url='https://example.org/synthetic-eras',columns=dict(dynasty='北魏',era_name='永平',first_year='508',last_year='512'))],rationale='synthetic phase range',reviewer='AI',human_reviewed=False)
 pos=t.index(title,sc['start']);h=dict(person_id=head['person_id'],title=title,kind='office',mode=mode,appointment_role=semantic,status='source_attested',human_reviewed=False,effective_period=dict(start=start,end=unknown),evidence=[e],attestations=[dict(paragraph_id=pid,start=pos,end=pos+len(title),surface=title,person_mention_id=head['id'],date_expression=None)],source_career_role=dict(kind='epitaph_named_head_career_clause',rule=rules[case],paragraph_sha256=sha,head_mention_id=head['id'],scope_anchor=sc,slot='office'if case=='grant'else'office2',foreign_roles=foreign,human_reviewed=False))
 if case=='posthumous':h['posthumous_basis']=dict(source_term=clause,evidence=h['evidence'])
 return h,c

class CareerContract(unittest.TestCase):
 def test_appointment(self):self.assertTrue(holding_valid(*fixture()))
 def test_embedded_patron_staff(self):self.assertTrue(holding_valid(*fixture('staff')))
 def test_posthumous(self):self.assertTrue(holding_valid(*fixture('posthumous')))
 def bad(self,fn,case='grant'):
  h,c=fixture(case);fn(h,c);self.assertFalse(holding_valid(h,c))
 def test_wrong_owner(self):self.bad(lambda h,c:h.update(person_id='someone'))
 def test_wrong_evidence_owner(self):self.bad(lambda h,c:h['evidence'][0].update(person_mention_id='someone'))
 def test_cut_quote(self):self.bad(lambda h,c:h['evidence'][0].update(quote='除石城長史'))
 def test_offset(self):self.bad(lambda h,c:h['attestations'][0].update(start=0))
 def test_source(self):self.bad(lambda h,c:h['evidence'][0].update(source_id='wrong'))
 def test_death_as_end(self):self.bad(lambda h,c:h['effective_period'].update(end=dict(status='source_event',event_type='death',date_expression='延昌四年',evidence=h['evidence'])))
 def test_posthumous_as_lifetime(self):self.bad(lambda h,c:h.update(mode='grant'),'posthumous')
 def test_grant_exact_death_year(self):self.bad(lambda h,c:h['effective_period']['start'].update(normalized_date=dict(year=515)),'posthumous')
 def test_range_not_single_year(self):self.bad(lambda h,c:h['effective_period']['start']['normalized_date_range'].update(year=508),'staff')
 def test_wrong_range(self):self.bad(lambda h,c:h['effective_period']['start']['normalized_date_range']['earliest'].update(year=509),'staff')
 def test_patron_not_recipient(self):self.bad(lambda h,c:h.update(person_id='synthetic-patron'),'staff')
 def test_wrong_foreign_id(self):self.bad(lambda h,c:c['paragraphs'][0]['mentions'][1].update(person_id='synthetic-head'),'staff')
 def test_no_ordinary_phrase_office(self):
  h,c=fixture();p=c['paragraphs'][0];old='石城長史';new='風流雅量';p['text']=p['text'].replace(old,new);h['title']=new;h['attestations'][0]['surface']=new;h['source_career_role']['scope_anchor']['surface']=h['source_career_role']['scope_anchor']['surface'].replace(old,new);h['evidence'][0]['quote']=p['text'];sha=hashlib.sha256(p['text'].encode()).hexdigest();h['source_career_role']['paragraph_sha256']=sha;c['annotation']['epitaph_fact_binding']['paragraph_sha256']=sha;self.assertFalse(holding_valid(h,c))


def duty_fixture(rule):
 clause='又監別將孔誠軍事，破偽鈞城而還。'if rule=='supervise_commander'else'君領羽林鐵騎，長驅淮滸，救其燌燒之委，收其器械之資。';intro='君姓沈，諱寧，字子安，廣陵人也。';t=intro+clause;pid='synthetic-p';head=dict(id='head',kind='person',person_id='one',start=t.index('寧'),end=t.index('寧')+1,surface='寧');ms=[head];sha=hashlib.sha256(t.encode()).hexdigest();sc=dict(paragraph_id=pid,start=len(intro),end=len(t),surface=clause)
 b=dict(kind='epitaph_named_head_military_duty',rule=rule,paragraph_sha256=sha,head_mention_id='head',scope_anchor=sc,human_reviewed=False)
 if rule=='supervise_commander':
  i=t.index('孔誠');m=dict(id='commander',kind='person',person_id='two',start=i,end=i+2,surface='孔誠');b['commander_mention_id']=m['id'];term='監別將孔誠軍事';v=dict(duty_code='supervision_of_field_commander',commander_person_id='two',office_title=None)
 else:
  i=len(intro);m=dict(id='resumed',kind='person',person_id='one',start=i,end=i+1,surface='君');b['subject_mention_id']=m['id'];term='領羽林鐵騎';v=dict(duty_code='command_of_cavalry',unit_source_name='羽林鐵騎',office_title=None)
 ms.append(m);c=dict(id='c',work_id='w',book_id='b',source_id='s',paragraphs=[dict(id=pid,text=t,mentions=ms)],annotation=dict(epitaph_fact_binding=dict(roles=dict(head='head'))));e={k:c[k]for k in ['work_id','book_id','source_id']};e.update(chapter_id='c',paragraph_id=pid,quote=t,person_mention_id='head');pos=t.index(term)
 d=dict(person_id='one',kind='official_duty',source_term=term,source_anchor=dict(paragraph_id=pid,start=pos,end=pos+len(term),surface=term),paragraph_sha256=sha,values=v,date_expression=None,evidence=[e],status='source_attested',human_reviewed=False,source_career_role=b)
 return d,c
class MilitaryDutyContract(unittest.TestCase):
 def test_supervision(self):self.assertTrue(detail_valid(*duty_fixture('supervise_commander')))
 def test_cavalry(self):self.assertTrue(detail_valid(*duty_fixture('lead_cavalry')))
 def bad(self,fn,rule='supervise_commander'):
  d,c=duty_fixture(rule);fn(d,c);self.assertFalse(detail_valid(d,c))
 def test_not_commander_as_subject(self):self.bad(lambda d,c:d.update(person_id='two'))
 def test_wrong_commander(self):self.bad(lambda d,c:d['values'].update(commander_person_id='one'))
 def test_not_invented_office(self):self.bad(lambda d,c:d['values'].update(office_title='監軍'))
 def test_no_inherited_year(self):self.bad(lambda d,c:d.update(date_expression='延昌四年'))
 def test_wrong_anchor(self):self.bad(lambda d,c:d['source_anchor'].update(start=0))
 def test_not_cavalry_general(self):self.bad(lambda d,c:d['values'].update(office_title='騎兵將軍'),'lead_cavalry')
if __name__=='__main__':unittest.main()
