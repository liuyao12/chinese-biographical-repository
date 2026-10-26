"""Validate an explicitly recorded editorial surname inference; never populate names."""
def validate(name,names,chapters,assertions,root=None):
 # fixed-wyd045-surname
 if isinstance(name,dict)and isinstance(name.get('surname_basis'),dict)and name['surname_basis'].get('kind')=='contextual_surname_from_wyd_song045_kinship':
  try:from scripts.wyd_song045_roles import validate_surname
  except ImportError:from wyd_song045_roles import validate_surname
  return validate_surname(name,names,chapters,assertions,root)
 if isinstance(name,dict) and name.get('surname_basis',{}).get('kind')=='contextual_surname_from_wyd_song051_named_path':
  try:from .fixed_wuyingdian_song051_family_phase import validate_surname
  except ImportError:from fixed_wuyingdian_song051_family_phase import validate_surname
  return validate_surname(name,names,chapters,assertions,root)
 if name.get('surname_basis',{}).get('kind')=='contextual_surname_from_wyd_song044_kinship':
  try:from .wyd_song044_names import validate_surname
  except ImportError:from wyd_song044_names import validate_surname
  return validate_surname(name,names,chapters,assertions,root)
 if name.get('surname_basis',{}).get('kind')=='contextual_surname_from_fixed_received_kinship':
  try:from .received_family_names import validate as received_names_validate
  except ImportError:from received_family_names import validate as received_names_validate
  return received_names_validate(name,names,chapters,assertions,root)
 if name.get("surname_basis",{}).get("kind")=="contextual_surname_from_bound_received_family_units":
  try:from .surname_received_family_units import validate as units_validate
  except ImportError:from surname_received_family_units import validate as units_validate
  return units_validate(name,names,chapters,assertions,root)
 if 'surname_basis'not in name:return
 if name['surname_basis'].get('kind')=='contextual_surname_from_bound_paternal_ancestor':
  try:from .surname_bound_ancestor import validate as ancestor_validate
  except ImportError:from surname_bound_ancestor import validate as ancestor_validate
  return ancestor_validate(name,names,chapters,assertions)
 if name['surname_basis'].get('kind')=='contextual_surname_from_bounded_named_family_path':
  try:from .surname_named_family_path import validate as named_path_validate
  except ImportError:from surname_named_family_path import validate as named_path_validate
  return named_path_validate(name,names,chapters,assertions)
 if name['surname_basis'].get('kind')=='contextual_surname_from_same_source_father_chain':
  try:
   from .surname_family_chain import validate as chain_validate
  except ImportError:
   from surname_family_chain import validate as chain_validate
  return chain_validate(name,names,chapters,assertions)
 try:
  b=name['surname_basis'];assert b['kind']=='contextual_surname_from_explicit_father'and b['status']=='contextual_provisional'and b['human_reviewed']is False
  assert name['status']=='contextual_provisional'and name['human_reviewed']is False and b['rationale'].strip()
  parent=next(n for n in names if n.get('id')==b['father_name_record_id'])
  assert parent['person_id']==b['father_person_id']and parent['surname']==name['surname']and parent['surname']and parent['ming']and not parent.get('surname_basis')
  c=chapters[name['chapter_id']];ps={p['id']:p for p in c['paragraphs']}
  fp=ps[parent['paragraph_id']];cp=ps[name['paragraph_id']]
  assert b['father_full_quote']==fp['text']and b['child_context_quote']==cp['text']and name['quote']==cp['text']
  def mark(p,mid,pid):
   m=next(m for m in p['mentions']if m['id']==mid)
   assert m['kind']=='person'and m['person_id']==pid and p['text'][m['start']:m['end']]==m['surface'];return m
  fm=mark(fp,b['father_full_mention_id'],b['father_person_id']);assert fm['start']==0 and fm['surface']==parent['surname']+parent['ming']and fp['text'].startswith(fm['surface']+'字')
  cm=mark(cp,name['person_mention_id'],name['person_id']);assert cm['surface']==name['ming']
  pm=mark(cp,b['father_context_mention_id'],b['father_person_id']);assert pm['surface']==parent['ming']and pm['end']<cm['start']
  term=b['source_term'];assert term in('子'+name['ming'],'長子'+name['ming'])and cp['text'][cm['start']-len(term)+len(name['ming']):cm['end']]==term
  a=next(a for a in assertions if a['id']==b['father_assertion_id'])
  assert a['predicate']=='father'and a['status']=='source_attested'and a['subject_person_id']==name['person_id']and a['object_person_id']==b['father_person_id']and a['qualifiers']['lineage']=='paternal'and a['qualifiers']['source_term']==term
  assert any(e['paragraph_id']==cp['id']and e['quote']==cp['text']and e['subject_person_mention_id']==cm['id']and e['object_person_mention_id']==pm['id']for e in a['evidence'])
 except (AssertionError,KeyError,StopIteration,TypeError):raise ValueError('Contextual surname requires full named-father and explicit child evidence; no family-ID or label inference')
