"""Finite owner dispatch; preserve existing owner validation and reject orphan/unknown reports."""
TYPE='source_family_count_report_set'
OWNERS=('fixed_jin036_wei_ner','fixed_jin034_yanghu_ner')
def _modules():
 try:
  from scripts import fixed_jin036_wei_ner as wei,fixed_jin034_core_kinship as yang
 except ImportError:
  import fixed_jin036_wei_ner as wei,fixed_jin034_core_kinship as yang
 return (wei,yang)
def close_kin_counts(records,people,root,ids):
 docs=[r for r in records if r.get('record_type')==TYPE]
 if any(r.get('owner')not in OWNERS for r in docs):raise ValueError('未知來源親屬報數owner')
 result=[]
 for owner,module in zip(OWNERS,_modules()):
  selected=[r for r in records if r.get('record_type')!=TYPE or r.get('owner')==owner]
  fn=module.close_kin_counts if owner==OWNERS[0]else module.counts
  result+=fn(selected,people,root,ids)
 return result
def close_kin_guard_bundle(root,pid,people,records):
 wei,yang=_modules();wei.close_kin_guard_bundle(root,pid,people,records);yang.guard_bundle(root,pid,people,records)
