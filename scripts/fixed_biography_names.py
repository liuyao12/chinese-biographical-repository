# coding: utf-8
"""Position-bound names and bounded surname readings in one fixed complete biography."""
import hashlib,re
KIND='fixed_punctuated_biography_name'
SURNAME_KIND='contextual_surname_from_fixed_biography_family'

def component_valid(n,c,root,assertions=()):
 try:
  try:from scripts.fixed_wikisource_units import source_errors
  except ImportError:from fixed_wikisource_units import source_errors
  assert c.get('annotation',{}).get('fixed_wikisource_unit_ref')and not source_errors(c,root)
  b=n['fixed_biography_name_binding'];assert set(b)=={'kind','source_revision','paragraph_sha256','mode','name_mention_id','zi_mention_id','alias_bindings','title_prefix','title_suffix'}and b['kind']==KIND
  p=next(p for p in c['paragraphs']if p['id']==n['paragraph_id']);t=p['text'];ms={m['id']:m for m in p['mentions']}
  assert n['chapter_id']==c['id']and n['quote']==t and n['human_reviewed']is False and b['source_revision']==c['source']['revision_id']==p['source_position']['revision_id']and b['paragraph_sha256']==hashlib.sha256(t.encode()).hexdigest()
  assert n.get('status')in('source_attested','editorial_provisional','contextual_provisional')
  assert not any(k in n for k in('preferred','former_ming','preferred_for_display','change_year'))
  m=ms[b['name_mention_id']];assert m['kind']=='person'and m['person_id']==n['person_id']and m['id']==n['person_mention_id']and t[m['start']:m['end']]==m['surface']
  mode=b['mode'];surname=n.get('surname');ming=n.get('ming')
  if mode=='full_name':assert surname and ming and m['surface']==surname+ming and not n.get('surname_basis')
  elif mode=='ming_only':assert ming and m['surface']==ming and(not surname or n.get('surname_basis',{}).get('kind')==SURNAME_KIND)
  elif mode=='clan_only':assert surname and ming is None and m['surface']==surname+'氏'and not n.get('surname_basis')
  elif mode=='role_only':assert surname and ming is None and n.get('surname_basis',{}).get('kind')==SURNAME_KIND
  elif mode=='surname_title':assert surname and ming is None and b['title_suffix']in('后','皇后')and m['surface']==surname+b['title_suffix']and not n.get('surname_basis')
  elif mode=='titled_given':assert surname is None and ming and ming not in('妃','后','王','侯','帝','公','氏')and re.fullmatch(r'(?:公|[^，。；「」]{1,8}(?:王|侯))',b['title_prefix'])and m['surface']==b['title_prefix']+ming
  else:raise AssertionError('unknown name mode')
  if mode!='titled_given':assert b['title_prefix']is None
  if mode!='surname_title':assert b['title_suffix']is None
  # A full surname+zi form is not silently reclassified as a given name.
  courtesy={x['surface']for pp in c['paragraphs']for x in pp['mentions']if x.get('person_id')==n['person_id']and x['start']>0 and pp['text'][x['start']-1:x['start']]=='字'}
  assert not ming or ming not in courtesy
  if b['zi_mention_id']is None:assert 'zi'not in n
  else:
   z=ms[b['zi_mention_id']];assert z['kind']=='person'and z['person_id']==n['person_id']and z['surface']==n['zi']and t[m['end']:z['start']]in('字','，字')and n['zi']!=ming
  aliases=b['alias_bindings'];assert isinstance(aliases,list)and len(aliases)<=2
  assert n.get('additional_name_components',[])==aliases
  display=[]
  for a in aliases:
   assert set(a)=={'kind','value','relation','source_marker','base_mention_id','alias_mention_id','chronology'}and a['kind']=='ming'and a['relation']=='also_called'and a['source_marker']=='一名'and a['chronology']=='unspecified'
   base=ms[a['base_mention_id']];alias=ms[a['alias_mention_id']];assert base['person_id']==alias['person_id']==n['person_id']and base['surface']==ming and alias['surface']==a['value']and t[base['end']:alias['start']]=='一名'
   display.append('一名'+a['value'])
  if aliases:assert n['additional_names']==display
  if 'source_name_usage'in n:
   u=n['source_name_usage'];assert set(u)=={'kind','source_mention_id','family_role','adoption_assertion_id','change_year','preferred','status'}and u['kind']=='received_family_name_usage'and u['source_mention_id']==m['id']and u['change_year']is None and u['preferred']is False and mode=='full_name'and u['status']in('source_attested','contextual_provisional')
   a,=[a for a in assertions if a['id']==u['adoption_assertion_id']];assert a['predicate']=='adoptive_father'and a['subject_person_id']==n['person_id']and a['qualifiers']['adoption_basis']=='named_external_grandson_posthumous_heir'
   if u['family_role']=='external_grandson_designation':assert t[max(0,m['start']-2):m['start']]=='外孫'
   else:assert u['family_role']=='heir_family_designation'
  return True
 except(AssertionError,KeyError,IndexError,TypeError,ValueError,StopIteration,AttributeError):return False

def validate_surname(n,names,chapters,assertions,root):
 try:
  b=n['surname_basis'];assert set(b)=={'kind','status','human_reviewed','rationale','seed_name_record_id','steps'}and b['kind']==SURNAME_KIND and b['status']=='contextual_provisional'and b['human_reviewed']is False and b['rationale'].strip()and n['status']=='contextual_provisional'
  ch=chapters[n['chapter_id']];assert component_valid(n,ch,root,assertions);seed,=[x for x in names if x.get('id')==b['seed_name_record_id']];assert seed['chapter_id']==ch['id']and seed['surname']==n['surname']and not seed.get('surname_basis')and component_valid(seed,ch,root,assertions)and seed['fixed_biography_name_binding']['mode']in('full_name','clan_only')
  ps={p['id']:(ch['id'],p)for p in ch['paragraphs']};aa={a['id']:a for a in assertions};assert len(aa)==len(assertions);steps=b['steps'];assert isinstance(steps,list)and 1<=len(steps)<=5
  try:from scripts.punctuated_family_frames import valid as family_valid
  except ImportError:from punctuated_family_frames import valid as family_valid
  current=seed['person_id'];seen={current};used=set();generation=0
  for s in steps:
   assert set(s)=={'assertion_id','from_person_id','to_person_id','generation_before','generation_after','traversal'}and s['assertion_id']not in used and s['from_person_id']==current and s['to_person_id']not in seen
   a=aa[s['assertion_id']];q=a['qualifiers'];assert family_valid(a,ps,{ch['id']:ch},root)and not q.get('sworn')and not q.get('adoptive')and q.get('shared_father')is not False
   assert all(e['chapter_id']==ch['id']for e in a['evidence'])
   pred=a['predicate'];sub,obj=a['subject_person_id'],a['object_person_id']
   if pred=='brother':delta=0
   elif pred=='father':delta=-1
   elif pred=='grandfather':assert q.get('lineage')=='paternal'and q['received_family_frame']['rule']=='two_granddaughters_marital_context';delta=-2
   elif pred=='great_grandfather':assert q['received_family_frame']['rule']=='named_parentage_head';delta=-3
   elif pred=='kinship_unspecified':
    assert q['lineage']=='paternal'and q['kinship_basis']=='bound_collateral_generation_term'and q['generation_difference']in(-1,-2,-3)and q['common_ancestor_person_id']is None and q['connecting_person_ids']is None;delta=q['generation_difference']
   else:raise AssertionError('No mother/spouse/adoption/maternal collateral/assembly surname route')
   if s['traversal']=='subject_to_object':assert current==sub and s['to_person_id']==obj
   elif s['traversal']=='object_to_subject':assert current==obj and s['to_person_id']==sub;delta=-delta
   else:raise AssertionError('unknown traversal')
   assert type(s['generation_before'])is int and type(s['generation_after'])is int and s['generation_before']==generation and s['generation_after']==generation+delta
   generation+=delta;current=s['to_person_id'];seen.add(current);used.add(s['assertion_id'])
  assert current==n['person_id']
 except(AssertionError,KeyError,TypeError,ValueError,StopIteration,AttributeError):raise ValueError('Surname reading requires one fixed complete source, literal full/clan-name seed and bounded source-role kinship steps; no ID/label, maternal/spouse/adoption or fabricated father route')
