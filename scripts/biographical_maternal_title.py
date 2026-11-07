"""Only explicit biography-opening 母 and child尊母 title clauses."""
def maternal_title_scope_valid(a,paragraphs):
 try:
  q=a['qualifiers'];e=a['evidence'][0];cid,p=paragraphs[e['paragraph_id']];t=p['text'];ms={m['id']:m for m in p['mentions']};s=ms[e['subject_person_mention_id']];o=ms[e['object_person_mention_id']]
  if (a['predicate']!='maternal_role'or set(q)!={'source_term','role','biological_mother','father_person_id'}
      or q['role']!='mother_unspecified'or q['biological_mother']is not None or q['father_person_id']is not None
      or q['source_term']!='母'+o['surface']or t[o['start']-1:o['end']]!=q['source_term']
      or s['person_id']!=a['subject_person_id']or o['person_id']!=a['object_person_id']or (s['kind']!='person'or o['kind']!='person')
      or cid!=e['chapter_id']or e['quote']!=t or len(a['evidence'])!=1):return False
  # A named child immediately precedes 尊母. It cannot be a different emperor earlier in the paragraph.
  if s['end']+2==o['start']and t[s['end']:o['start']]=='尊母':return True
  # This biography's opening personal name and explicit parent formula precede 母.
  opening=next((m for m in p['mentions']if m['start']==0 and m['person_id']==a['subject_person_id']),None)
  if not opening:return False
  prefix=t[opening['end']:o['start']]
  return(prefix.startswith('諱')and prefix.endswith('中子也母')and len(prefix)<=32
         and not any(ch in prefix for ch in '曰云：：「『')
         and any(m['person_id']==a['subject_person_id']and opening['end']<=m['start']<o['start']for m in p['mentions']))
 except(KeyError,TypeError,StopIteration):return False
