"""Validate an explicitly recorded editorial surname inference; never populate names."""
def validate(name,names,chapters,assertions):
 if 'surname_basis'not in name:return
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
