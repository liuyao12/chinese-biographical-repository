# coding: utf-8
"""Explicit biography-head 兄子 and named collective 從兄; no inferred father."""
import re
try:
 from scripts.historical_family_clauses import _parts
except ImportError:
 from historical_family_clauses import _parts

def inverse_xiongzi_valid(a,paragraphs):
 try:
  t,q,b,ms,s,o,start,end=_parts(a,paragraphs)
  return (a['predicate']=='paternal_uncle' and set(q)=={'source_term','source_clause_binding'}
   and set(b)=={'kind','start','end'} and b['kind']=='biography_head_named_uncle_xiongzi'
   and s['start']==0 and t[s['end']:].startswith('字')
   and re.fullmatch(r'字[^曰云不未非之「」：，。；]{1,24}人[^曰云不未非之「」：，。；]{0,12}',t[s['end']:o['start']]) is not None
   and o['start']==start and q['source_term']==o['surface']+'兄子也' and t[o['end']:end]=='兄子也'
   and not any(m.get('kind')=='person' and s['end']<=m['start']<o['start'] and m['person_id']!=s['person_id'] for m in ms.values()))
 except (KeyError,TypeError,ValueError,StopIteration):return False

def named_congxiong_group_valid(a,paragraphs):
 try:
  t,q,b,ms,s,o,start,end=_parts(a,paragraphs); k=q['kinship_structure'];group=[ms[i] for i in b['group_member_mention_ids']]
  if not (a['predicate']=='agnatic_cousin' and set(q)=={'source_term','kinship_structure','source_clause_binding'}
   and set(k)=={'lineage','generation_difference','collateral','distance','common_ancestor_person_id','subject_relative_age'}
   and k=={'lineage':'paternal','generation_difference':0,'collateral':True,'distance':None,'common_ancestor_person_id':None,'subject_relative_age':'younger'}
   and type(k['generation_difference'])is int and k['collateral']is True
   and set(b)=={'kind','start','end','group_member_mention_ids'} and b['kind']=='named_subject_congxiong_group'
   and s['start']==start and group and len({m['person_id']for m in group})==len(group)
   and o['id'] in b['group_member_mention_ids']):return False
  at=s['end']+len('少與從兄')
  if t[s['end']:at]!='少與從兄':return False
  for m in group:
   if m['kind']!='person' or m['person_id']==s['person_id'] or m['start']!=at or t[m['start']:m['end']]!=m['surface']:return False
   at=m['end']
  return t[at:end]=='齊名' and q['source_term']==s['surface']+'少與從兄'+''.join(m['surface']for m in group)+'齊名'
 except(KeyError,TypeError,ValueError,StopIteration):return False
