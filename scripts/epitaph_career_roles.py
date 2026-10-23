"""Finite epitaph career clauses; named head and foreign issuer/patron remain distinct."""
import re,hashlib
KIND='epitaph_named_head_career_clause'
RULES={
 'era_initial_appointment':(r'(?P<time>[^，。非不未無]+中)，以[^，。非不未無]+，而除(?P<office>[^，。非不未無]+)。','grant','appointment',{'office'}),
 'accession_staff_service':(r'暨(?P<ruler>[^，。非不未無]+)即祚，壽春送款，君為(?P<office>[^，。非不未無]+)受降納附。','attestation','staff_service_report',{'office'}),
 'subsequent_appointment':(r'未幾，以援接之功，除(?P<office>[^，。非不未無]+)。','grant','appointment',{'office'}),
 'campaign_staff_service':(r'義陽之役，君(?P<office>參[^，。非不未無]+軍事)，職掌壘和，任屬防禦。','attestation','campaign_staff_service_report',{'office'}),
 'merit_promotion':(r'以功遷(?P<office>[^，。非不未無]+)。','transfer','promotion',{'office'}),
 'renewed_campaign_staff':(r'俄而(?P<enemy>偽臨川王[^，。非不未無]+)，敢率蟻徒殲我粱城，以君歷試惟允，復(?P<office>參[^，。非不未無]+軍事)。','attestation','renewed_campaign_staff_service_report',{'office'}),
 'era_two_staff_appointments':(r'(?P<time>[^，。非不未無]+初載)，望府啟建，寮佐之選，妙盡時英。以君為(?P<office1>[^，、。非不未無]+)、(?P<office2>參(?P<patron>[^，、。非不未無]+王)府事)。','grant','concurrent_appointment',{'office1','office2'}),
 'posthumous_two_offices':(r'詔遣謁者持節册贈(?P<office1>[^，、。非不未無]+)、(?P<office2>[^，、。非不未無]+)，所以旌崇孝德，禮也。','posthumous_grant','posthumous_office',{'office1','office2'})}
def holding_valid(h,c):
 try:
  b=h['source_career_role'];p,=c['paragraphs'];t=p['text'];ms={m['id']:m for m in p['mentions']};near=c['annotation']['epitaph_fact_binding'];head=ms[b['head_mention_id']]
  assert b['kind']==KIND and b['human_reviewed']is False and b['paragraph_sha256']==hashlib.sha256(t.encode()).hexdigest()==near['paragraph_sha256']and head['id']==near['roles']['head']and h['person_id']==head['person_id']
  assert p['text_layer']=='epitaph_as_modernly_transcribed'and c['source']['transcription_witness']['original_stone_or_rubbing_image_verified']is False
  intro=re.search(r'君姓[^，。]+，諱([^，。]+)，字[^，。]+，[^。]+人也。',t);assert intro and head['surface']==intro[1]and head['start']==intro.start(1)
  def exact(a):assert set(a)=={'paragraph_id','start','end','surface'}and a['paragraph_id']==p['id']and t[a['start']:a['end']]==a['surface'];return a['surface']
  scope=b['scope_anchor'];pattern,mode,semantic,slots=RULES[b['rule']];hit=re.fullmatch(pattern,exact(scope));assert hit and b['slot']in slots
  title=h['title'];a,=h['attestations'];e,=h['evidence'];assert title==hit[b['slot']]and a['start']==scope['start']+hit.start(b['slot'])and a['end']==scope['start']+hit.end(b['slot'])and a['surface']==title and a['person_mention_id']==head['id']and a['paragraph_id']==p['id']and a['date_expression']is None
  assert h['kind']=='office'and h['mode']==mode and h['appointment_role']==semantic and h['human_reviewed']is False and h['status']=='source_attested'
  # Nominal offices or an explicitly governed staff-service construction, never arbitrary prose.
  staff=title.startswith('參')and (title.endswith('軍事')or title.endswith('王府事'))
  assert staff or (2<=len(title)<=20 and any(title.endswith(x)for x in ['郎','長史','丞','參軍','將軍','刺史'])and not any(x in title for x in '曰云非不未欲請卒少與'))
  assert e==dict(work_id=c['work_id'],book_id=c['book_id'],source_id=c['source_id'],chapter_id=c['id'],paragraph_id=p['id'],quote=t,person_mention_id=head['id'])
  foreign={}
  for role in ['ruler','enemy','patron']:
   if role not in hit.groupdict():continue
   m=ms[b['foreign_roles'][role]];assert m['kind']=='person'and m['person_id']!=head['person_id']and m['surface']==hit[role]and (m['start'],m['end'])==(scope['start']+hit.start(role),scope['start']+hit.end(role));foreign[role]=m
  assert set(b['foreign_roles'])==set(foreign)
  for m in p['mentions']:
   if m.get('kind')=='person'and scope['start']<=m['start']<scope['end']and m['id']not in {x['id']for x in foreign.values()}:assert m['person_id']==head['person_id']
  unknown=dict(status='unknown',date_expression=None,evidence=[]);expected=unknown if mode=='attestation'else dict(status='source_event',event_type=mode,date_expression=(hit['time'].removesuffix('載')if 'time'in hit.groupdict()else None),evidence=h['evidence'])
  start=h['effective_period']['start'];base={k:v for k,v in start.items()if k!='normalized_date_range'};assert base==expected and h['effective_period']['end']==unknown and 'normalized_date'not in start
  if 'time'in hit.groupdict():
   from importlib import import_module
   try:from scripts.date_ranges import year_range_errors
   except ImportError:from date_ranges import year_range_errors
   assert 'normalized_date_range'in start and not year_range_errors(start['normalized_date_range'],h['evidence'],expected['date_expression'])
  else:assert 'normalized_date_range'not in start
  if mode=='posthumous_grant':
   life=c['annotation']['epitaph_life_binding'];assert life['death_scope']['end']<=scope['start']<life['burial_scope']['start']and h['posthumous_basis']==dict(source_term=scope['surface'],evidence=h['evidence'])
  else:assert 'posthumous_basis'not in h
  return True
 except(KeyError,TypeError,ValueError,AssertionError,StopIteration,IndexError):return False

def detail_valid(d,c):
 try:
  p,=c['paragraphs'];t=p['text'];b=d['source_career_role'];ms={m['id']:m for m in p['mentions']};head=ms[b['head_mention_id']];assert head['id']==c['annotation']['epitaph_fact_binding']['roles']['head']and d['person_id']==head['person_id']
  assert b['kind']=='epitaph_named_head_military_duty'and b['paragraph_sha256']==d['paragraph_sha256']==hashlib.sha256(t.encode()).hexdigest()and b['human_reviewed']is False
  scope=b['scope_anchor'];assert scope['paragraph_id']==p['id']and t[scope['start']:scope['end']]==scope['surface'];a=d['source_anchor'];assert a['paragraph_id']==p['id']and t[a['start']:a['end']]==a['surface']==d['source_term']
  assert d['kind']=='official_duty'and d['status']=='source_attested'and d['human_reviewed']is False and d['date_expression']is None and 'normalized_date'not in d and 'normalized_date_range'not in d
  e,=d['evidence'];assert e==dict(work_id=c['work_id'],book_id=c['book_id'],source_id=c['source_id'],chapter_id=c['id'],paragraph_id=p['id'],quote=t,person_mention_id=head['id'])
  if b['rule']=='supervise_commander':
   m=ms[b['commander_mention_id']];assert m['kind']=='person'and m['person_id']!=head['person_id']and scope['surface']=='又監別將'+m['surface']+'軍事，破偽鈞城而還。'and m['start']==scope['start']+4
   assert a['start']==scope['start']+1 and a['end']==m['end']+2 and d['values']==dict(duty_code='supervision_of_field_commander',commander_person_id=m['person_id'],office_title=None)
  elif b['rule']=='lead_cavalry':
   subject=ms[b['subject_mention_id']];assert subject['person_id']==head['person_id']and subject['surface']=='君'and subject['start']==scope['start']and scope['surface']=='君領羽林鐵騎，長驅淮滸，救其燌燒之委，收其器械之資。'
   assert a['start']==subject['end']and a['surface']=='領羽林鐵騎'and d['values']==dict(duty_code='command_of_cavalry',unit_source_name='羽林鐵騎',office_title=None)
  else:return False
  return True
 except(KeyError,TypeError,ValueError,AssertionError,StopIteration,IndexError):return False
