"""A literal 祖母 role does not choose the paternal or maternal branch."""
def reported_grandmother_valid(a,paragraphs):
 try:
  q=a['qualifiers'];es=a['evidence']
  if (a['predicate']!='grandmother'or set(q)!={'source_term','lineage','generation_difference','parent_person_id','relationship_basis'}
      or q['source_term']!='祖母'or q['lineage']!='unspecified'or q['generation_difference']!=-2
      or q['parent_person_id']is not None or q['relationship_basis']!='literal_grandmother_title_clause'or len(es)!=1):return False
  e=es[0];cid,p=paragraphs[e['paragraph_id']]
  ms={m['id']:m for m in p['mentions']};child=ms[e['subject_person_mention_id']];gm=ms[e['object_person_mention_id']]
  term=child['surface']+'尊祖母'+gm['surface']
  return(cid==e['chapter_id']and e['quote']==p['text']and child.get('person_id')==a['subject_person_id']
         and gm.get('person_id')==a['object_person_id']and child['kind']==gm['kind']=='person'
         and p['text'][child['start']:gm['end']]==term and child['end']<gm['start'])
 except(KeyError,TypeError,ValueError):return False
