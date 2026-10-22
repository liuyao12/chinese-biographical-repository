"""Assembly from an already role-bound unpunctuated biography head.
The person's surname 祖 at offset zero is never the grandfather role.
"""
import hashlib
BASIS='bound_unpunctuated_biography_zu_fu_sequence'
def valid(member,rows,assertions,chapters):
 try:
  c=member['parent_connection'];n=assertions[c['nearer_ancestor_assertion_id']];g=assertions[c['farther_ancestor_assertion_id']];frame=c['source_frame'];ch=chapters[frame['chapter_id']];p=next(x for x in ch['paragraphs']if x['id']==frame['paragraph_id']);t=p['text'];b=n['qualifiers']['source_clause_binding'];far=g['qualifiers']['source_clause_binding'];people=[n['subject_person_id'],n['object_person_id'],g['object_person_id']]
  if(c['type']!='parent_between_consecutive_ancestors'or c['interpretation_basis']!=BASIS or c['status']!='contextual_provisional'or c.get('human_reviewed')is not False or not c.get('rationale')or member.get('source_assertion_id')is not None or len(set(people))!=3):return False
  if(n['predicate']!='father'or g['predicate']!='grandfather'or n['status']!=g['status']or n['status']!='source_attested'or n['subject_person_id']!=g['subject_person_id']or n['subject_person_id']not in rows[c['chain_subject_person_id']]['source_person_ids']or n['object_person_id']not in member['source_person_ids']or g['object_person_id']not in rows[member['parent_person_id']]['source_person_ids']):return False
  if any(a['qualifiers'].get('lineage')not in(None,'unspecified','paternal')for a in(n,g)):return False
  if(set(frame)!={'chapter_id','paragraph_id','source_revision','raw_sha256','paragraph_sha256','source_clause_binding'}or b!=far or b!=frame['source_clause_binding']or b['rule']!='close_family_unpunctuated_head_grandfather_father'or b['kind']!='biography_family_clause'or b['revision_id']!=ch['source']['revision_id']or frame['source_revision']!=ch['source']['revision_id']or frame['raw_sha256']!=ch['source']['raw_sha256']or frame['paragraph_sha256']!=hashlib.sha256(t.encode()).hexdigest()or p.get('text_layer')!='received_chapter'):return False
  if not isinstance(frame['raw_sha256'],str)or len(frame['raw_sha256'])!=64 or any(x not in '0123456789abcdef'for x in frame['raw_sha256'])or not isinstance(frame['source_revision'],str)or not frame['source_revision']:return False
  try:from .biography_close_family import valid as source_valid
  except ImportError:from biography_close_family import valid as source_valid
  ps={p['id']:(ch['id'],p)}
  if not source_valid(n,ps)or not source_valid(g,ps):return False
  # Bind the actual source evidence roles, not just a same-paragraph mention.
  roles=b['roles'];ms={m['id']:m for m in p['mentions']};head=ms[roles['head']];father=ms[roles['father']];grand=ms[roles['grandfather']]
  if head['start']!=0 or grand['start']<=head['end']or t[grand['start']-1:grand['start']]!='祖'or t[grand['start']-2:grand['start']]=='外祖'or t[father['start']-1:father['start']]!='父':return False
  for a,role in[(n,'father'),(g,'grandfather')]:
   e,=a['evidence']
   if(e['chapter_id']!=ch['id']or e['source_id']!=ch['source_id']or e['paragraph_id']!=p['id']or e['quote']!=t or e['subject_person_mention_id']!=head['id']or e['object_person_mention_id']!=roles[role]):return False
  if any(a.get('predicate')=='father'and a.get('subject_person_id')in member['source_person_ids']and a.get('object_person_id')not in rows[member['parent_person_id']]['source_person_ids']for a in assertions.values()):return False
  refs=c['references']
  return(len(refs)==2 and {r['assertion_id']for r in refs}=={n['id'],g['id']}and all(r['chapter_id']==ch['id']and r['source_id']==ch['source_id']and r['paragraph_id']==p['id']and r['quote']==t and r.get('scope')and r.get('url')in[ch['source']['url'],ch['source']['permalink']]for r in refs))
 except(KeyError,TypeError,ValueError,IndexError,StopIteration,AttributeError):return False
