# coding: utf-8
"""Editorial paternal assembly from an explicit biography-opening 祖/父 list.
Raw unspecified 祖 lineage remains unspecified; no father assertion is added.
"""
def biographical_zu_fu_parent_valid(member, rows, assertions, chapters):
 c=member.get('parent_connection',{})
 near=assertions.get(c.get('nearer_ancestor_assertion_id'),{})
 far=assertions.get(c.get('farther_ancestor_assertion_id'),{})
 witness=rows.get(c.get('chain_subject_person_id'),{})
 parent=rows.get(member.get('parent_person_id'),{})
 if not (c.get('type')=='parent_between_consecutive_ancestors'
  and c.get('interpretation_basis')=='biographical_zu_fu_sequence'
  and c.get('status')=='contextual_provisional' and c.get('human_reviewed') is False
  and isinstance(c.get('rationale'),str) and c['rationale'].strip()
  and member.get('source_assertion_id') is None
  and near.get('status')==far.get('status')=='source_attested'
  and near.get('predicate')=='father' and far.get('predicate')=='grandfather'
  and near.get('subject_person_id')==far.get('subject_person_id')
  and near.get('subject_person_id') in witness.get('source_person_ids',[])
  and near.get('object_person_id') in member.get('source_person_ids',[])
  and far.get('object_person_id') in parent.get('source_person_ids',[])
  and near.get('qualifiers',{}).get('lineage') in (None,'unspecified','paternal')
  and far.get('qualifiers',{}).get('lineage') in ('unspecified','paternal')):return False
 people=[near['subject_person_id'],far['object_person_id'],near['object_person_id']]
 if len(set(people))!=3:return False
 refs=c.get('references')
 if not isinstance(refs,list) or len(refs)!=2 or any(not isinstance(x,dict) for x in refs):return False
 if {x.get('assertion_id') for x in refs}!={near['id'],far['id']}:return False
 common={(e.get('chapter_id'),e.get('paragraph_id'),e.get('source_id'),e.get('quote')) for e in near.get('evidence',[])}&{(e.get('chapter_id'),e.get('paragraph_id'),e.get('source_id'),e.get('quote')) for e in far.get('evidence',[])}
 for cid,pid,sid,quote in common:
  chapter=chapters.get(cid,{});p=next((p for p in chapter.get('paragraphs',[]) if p.get('id')==pid),None)
  if not p or p.get('text_layer')!='received_chapter' or p.get('text')!=quote or chapter.get('source_id')!=sid:continue
  if not all(x.get('scope') and (x.get('chapter_id'),x.get('paragraph_id'),x.get('source_id'),x.get('quote'))==(cid,pid,sid,quote) and x.get('url') in [chapter.get('source',{}).get('url'),chapter.get('source',{}).get('permalink')] for x in refs):continue
  mentions=[m for m in p.get('mentions',[]) if m.get('kind')=='person' and quote[m.get('start',0):m.get('end',0)]==m.get('surface')]
  if not any(m.get('person_id')==people[0] and m.get('start')==0 for m in mentions):continue
  bound=[]
  for a,role in [(far,'祖'),(near,'父')]:
   choices=[m for m in mentions if m.get('person_id')==a['object_person_id'] and m.get('start',0)>0 and quote[m['start']-1:m['start']]==role and a.get('qualifiers',{}).get('source_term','').startswith(role+m['surface']) and m['surface'] not in ['祖','父','其','之']]
   if len(choices)!=1:break
   bound.append(choices[0])
  if len(bound)!=2:continue
  g,f=bound
  if not (g['start']<f['start'] and quote[g['start']-2:g['start']]!='外祖'):continue
  # The opening ancestry list may contain 字/office text, never another named person or a transfer/alternative.
  segment=quote[:f['end']]
  if any(x in segment for x in ['外祖','母父','曰','云','非','未','不','或','「','」','『','』','。','；','！','？']):continue
  if any(m.get('person_id') not in people and m.get('start',-1)<f['end'] for m in mentions):continue
  if any(a.get('predicate')=='father' and a.get('subject_person_id') in member.get('source_person_ids',[]) and a.get('object_person_id') not in parent.get('source_person_ids',[]) for a in assertions.values()):continue
  return True
 return False
