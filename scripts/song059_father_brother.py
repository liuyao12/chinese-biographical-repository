# coding: utf-8
"""A biography's named father is the named uncle's elder brother, explicitly 兄子也父某."""
import re

def explicit_father_elder_brother_valid(a,paragraphs,assertions):
 try:
  e,=a['evidence'];cid,p=paragraphs[e['paragraph_id']];t=p['text'];q=a['qualifiers'];b=q['source_clause_binding'];marks={m['id']:m for m in p['mentions']}
  f=marks[e['subject_person_mention_id']];u=marks[e['object_person_mention_id']];child=marks[b['child_person_mention_id']]
  start,end=b['start'],b['end']
  if not(a['predicate']=='brother' and a['status']=='source_attested' and a.get('human_reviewed') is False
   and set(q)=={'source_term','source_clause_binding','relative_birth_order','source_explicit_father_assertion_id'}
   and set(b)=={'kind','start','end','child_person_mention_id','father_role_start','father_role_end'}
   and b['kind']=='biography_head_uncle_xiongzi_named_father'
   and cid==e['chapter_id'] and e['quote']==t
   and len({f['person_id'],u['person_id'],child['person_id']})==3
   and f['person_id']==a['subject_person_id'] and u['person_id']==a['object_person_id']):return False
  for m in [f,u,child]:
   if not(m['kind']=='person' and type(m['start'])is int and type(m['end'])is int
     and 0<=m['start']<m['end']<=len(t) and t[m['start']:m['end']]==m['surface']):return False
  if not(type(start)is int and type(end)is int and 0<=start<end<=len(t)
   and child['start']==0 and t[child['end']:].startswith('字')
   and re.fullmatch(r'字[^曰云不未非之「」：，。；]{1,24}人[^曰云不未非之「」：，。；]{0,12}',t[child['end']:u['start']])
   and not any(m.get('kind')=='person' and child['end']<=m['start']<u['start'] and m['person_id']!=child['person_id']for m in marks.values())
   and start==u['start'] and end==f['end'] and t[u['end']:f['start']]=='兄子也父'
   and q['source_term']==t[start:end]==u['surface']+'兄子也父'+f['surface']
   and type(b['father_role_start'])is int and type(b['father_role_end'])is int
   and b['father_role_start']==f['start']-1 and b['father_role_end']==f['end']):return False
  if q['relative_birth_order']!={'operator':'lt','scope':'siblings','older_person_id':f['person_id'],'younger_person_id':u['person_id'],'older_ordinal':None,'younger_ordinal':None}:return False
  matches=[r for r in assertions if r['id']==q['source_explicit_father_assertion_id']]
  if len(matches)!=1:return False
  r=matches[0]
  if not(r['predicate']=='father' and r['status']=='source_attested' and r['subject_person_id']==child['person_id'] and r['object_person_id']==f['person_id'] and r['qualifiers']['source_term']=='父'+f['surface']):return False
  return any(x['chapter_id']==cid and x['paragraph_id']==p['id'] and x['quote']==t and x.get('subject_person_mention_id')==child['id'] and x.get('object_person_mention_id')==f['id'] for x in r['evidence'])
 except(KeyError,TypeError,ValueError,StopIteration):return False
