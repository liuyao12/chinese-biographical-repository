"""Closed source-owned collective/reference readings; never identity or occurrence aliases."""
TYPE='source_person_reference_group_set'
def _validated_sets_uncached(records,people,root):
 try:from scripts.fixed_zhou041_erlu import guard_catalog
 except ImportError:from fixed_zhou041_erlu import guard_catalog
 guard_catalog(records,people,root)
 try:from scripts.fixed_shiji130_six_roles import guard_catalog
 except ImportError:from fixed_shiji130_six_roles import guard_catalog
 guard_catalog(records,people,root)
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
  elif d.get('owner')=='fixed_zhou041_erlu':
   try:from scripts.fixed_zhou041_erlu import group_set_valid
   except ImportError:from fixed_zhou041_erlu import group_set_valid
  elif d.get('owner')=='fixed_jin054_lu_openings':
   try:from scripts.fixed_jin054_lu_openings import group_set_valid
   except ImportError:from fixed_jin054_lu_openings import group_set_valid
  elif d.get('owner')=='fixed_shiji130_six_roles':
   try:from scripts.fixed_shiji130_six_roles import group_set_valid
   except ImportError:from fixed_shiji130_six_roles import group_set_valid
  else:raise ValueError('未知來源人物群體owner')
  group_set_valid(d,people,root)
 return docs
def reading_person_ids(r):
 ids=set(r.get('candidate_person_ids',[]))
 if isinstance(r.get('subject_person_id'),str):ids.add(r['subject_person_id'])
 ids.update(m['person_id']for m in r.get('resolved_member_refs',[]))
 return ids
def for_people(records,people,root,ids):
 try:from scripts.source_group_catalog_cache import run
 except ImportError:from source_group_catalog_cache import run
 return run(root,records,people,lambda:_validated_sets_uncached(records,people,root),ids=ids)


def validated_sets(records,people,root):
 try:from scripts.source_group_catalog_cache import run
 except ImportError:from source_group_catalog_cache import run
 return run(root,records,people,lambda:_validated_sets_uncached(records,people,root))
