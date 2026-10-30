"""Closed source-owned collective/reference readings; never identity or occurrence aliases."""
TYPE='source_person_reference_group_set'
def validated_sets(records,people,root):
 docs=[x for x in records if x.get('record_type')==TYPE];seen=set()
 for d in docs:
  key=(d.get('owner'),d.get('chapter_id'))
  if key in seen:raise ValueError('重複來源人物群體/未決閱讀集')
  seen.add(key)
  if d.get('owner')=='fixed_jin034_yanghu_ner':
   try:from scripts.fixed_jin034_yanghu_ner import group_set_valid
   except ImportError:from fixed_jin034_yanghu_ner import group_set_valid
  elif d.get('owner')=='fixed_jin036_wei_ner':
   try:from scripts.fixed_jin036_wei_ner import group_set_valid
   except ImportError:from fixed_jin036_wei_ner import group_set_valid
  else:raise ValueError('未知來源人物群體owner')
  group_set_valid(d,people,root)
 return docs
def reading_person_ids(r):
 ids=set(r.get('candidate_person_ids',[]))
 if isinstance(r.get('subject_person_id'),str):ids.add(r['subject_person_id'])
 ids.update(m['person_id']for m in r.get('resolved_member_refs',[]))
 return ids
def for_people(records,people,root,ids):
 groups=[];readings=[];related=set()
 for d in validated_sets(records,people,root):
  for g in d['groups']:
   members={m['person_id']for m in g['members']}
   if ids&members:groups.append(g);related.update(members)
  for r in d['unresolved_readings']:
   candidates=reading_person_ids(r)
   if ids&candidates:readings.append(r);related.update(candidates)
 return groups,readings,related
