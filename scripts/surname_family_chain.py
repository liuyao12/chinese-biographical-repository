"""Validate a bounded editorial surname chain through same-source explicit fathers."""
import re
KIND = 'contextual_surname_from_same_source_father_chain'
def validate(name, names, chapters, assertions):
 try:
  b=name['surname_basis']
  assert b['kind']==KIND and b['status']=='contextual_provisional' and b['human_reviewed'] is False
  assert name['status']=='contextual_provisional' and name['human_reviewed'] is False and b['rationale'].strip()
  seeds=[n for n in names if n.get('id')==b['source_name_record_id']];assert len(seeds)==1
  seed=seeds[0];assert not seed.get('surname_basis') and seed['surname'] and seed['ming'] and seed['surname']==name['surname']
  assert seed['chapter_id']==name['chapter_id']
  c=chapters[name['chapter_id']];ps={p['id']:p for p in c['paragraphs']};assert len(ps)==len(c['paragraphs'])
  def mark(p,mid,pid):
   hits=[m for m in p['mentions'] if m['id']==mid];assert len(hits)==1
   m=hits[0];assert m['kind']=='person' and m['person_id']==pid and p['text'][m['start']:m['end']]==m['surface'];return m
  sp=ps[seed['paragraph_id']];sm=mark(sp,seed['person_mention_id'],seed['person_id'])
  assert seed['quote']==sp['text']==b['source_full_quote']
  assert sm['start']==0 and sm['surface']==seed['surname']+seed['ming']
  if not re.match(r'^[，,]?字',sp['text'][sm['end']:]):
   try:from .surname_fixed_birthplace_head import valid as fixed_head_valid
   except ImportError:from surname_fixed_birthplace_head import valid as fixed_head_valid
   assert fixed_head_valid(seed,name,c,assertions)
  tp=ps[name['paragraph_id']];tm=mark(tp,name['person_mention_id'],name['person_id'])
  assert name['quote']==tp['text'] and tm['surface']==name['ming']
  steps=b['steps'];assert 1<=len(steps)<=2
  current=seed['person_id'];seen={current}
  for step in steps:
   assert step['from_person_id']==current
   matches=[a for a in assertions if a['id']==step['assertion_id']];assert len(matches)==1
   a=matches[0];assert a['predicate']=='father' and a['status']=='source_attested'
   assert a.get('qualifiers',{}).get('lineage','paternal')=='paternal'
   assert not a.get('qualifiers',{}).get('adoptive')
   child=a['subject_person_id'];father=a['object_person_id'];assert child!=father
   direction=step['traversal'];assert direction in ('child_to_father','father_to_child')
   pair=(child,father) if direction=='child_to_father' else (father,child)
   assert pair==(current,step['to_person_id']) and pair[1] not in seen
   e=step['evidence'];assert e in a['evidence'] and e['chapter_id']==c['id']
   assert e['work_id']==c['work_id'] and e['book_id']==c['book_id'] and e['source_id']==c['source_id']
   p=ps[e['paragraph_id']];assert e['quote']==p['text']
   mark(p,e['subject_person_mention_id'],child);mark(p,e['object_person_mention_id'],father)
   assert step['source_term']==a['qualifiers']['source_term'] and step['source_term'] in p['text']
   current=pair[1];seen.add(current)
  assert current==name['person_id']
 except (AssertionError,KeyError,StopIteration,TypeError,IndexError):
  raise ValueError('Same-source surname chain requires an explicit full-name anchor and one or two source-attested father edges with exact endpoints and complete evidence')
