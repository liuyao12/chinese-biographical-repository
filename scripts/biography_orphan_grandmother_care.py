# coding: utf-8
"""A complete biography-head clause binds child, deceased mother and grandmother."""
import re
KIND='biography_head_birth_mother_dies_grandmother_care'

def valid(a,paragraphs):
 try:
  q=a['qualifiers'];b=q['source_clause_binding'];es=a['evidence']
  if a['status']!='source_attested' or type(a.get('human_reviewed'))is not bool or len(es)!=1 or set(b)!={'kind','mother_person_mention_id','clause_anchor'} or b['kind']!=KIND:return False
  e=es[0];cid,p=paragraphs[e['paragraph_id']];text=p['text'];ms={m['id']:m for m in p['mentions']}
  if len(ms)!=len(p['mentions'])or cid!=e['chapter_id']or e['quote']!=text:return False
  for obj in (p,p.get('source_position',{})):
   if any(obj.get(k,'received_text')!='received_text'for k in ('source_layer','text_layer'))or 'annotator'in obj or 'attached_note_to_paragraph_id'in obj:return False
  child=ms[e['subject_person_mention_id']];gm=ms[e['object_person_mention_id']];mother=ms[b['mother_person_mention_id']]
  for m in (child,gm,mother):
   if any(m.get(k,'received_text')!='received_text'for k in ('source_layer','text_layer'))or 'annotator'in m or 'attached_note_to_paragraph_id'in m:return False
   if m['kind']!='person'or not m.get('person_id')or type(m['start'])is not int or type(m['end'])is not int or not 0<=m['start']<m['end']<=len(text)or text[m['start']:m['end']]!=m['surface']:return False
  if child['person_id']!=a['subject_person_id']or gm['person_id']!=a['object_person_id']or len({m['person_id']for m in (child,gm,mother)})!=3 or child['start']!=0:return False
  anchor=b['clause_anchor']
  if set(anchor)!={'paragraph_id','start','end','surface'}or anchor['paragraph_id']!=p['id']or anchor['start']!=0 or type(anchor['end'])is not int or not 0<anchor['end']<=len(text)or text[:anchor['end']]!=anchor['surface']:return False
  expected=re.escape(child['surface'])+r'字[^，。；！？：「」『』\s]{1,8}，生而母'+re.escape(mother['surface'])+'亡，為祖母'+re.escape(gm['surface'])+'所養。'
  if re.fullmatch(expected,anchor['surface'])is None:return False
  # Exact positions distinguish names in this clause from later repeated forms.
  if text[child['end']:mother['start']].count('生而母')!=1 or not text[child['end']:mother['start']].endswith('，生而母')or text[mother['end']:gm['start']]!='亡，為祖母'or text[gm['end']:anchor['end']]!='所養。':return False
  allowed={child['id'],mother['id'],gm['id']}
  # The courtesy-name occurrence may identify the same child; no fourth actor.
  if any(m.get('kind')=='person'and m['start']<anchor['end']and m['id']not in allowed and not(m.get('person_id')==child['person_id']and child['end']<m['start']<m['end']<=mother['start'])for m in p['mentions']):return False
  if a['predicate']=='grandmother':
   return(set(q)=={'source_term','lineage','generation_difference','parent_person_id','relationship_basis','source_clause_binding'}and q['source_term']=='祖母'and q['lineage']=='unspecified'and type(q['generation_difference'])is int and q['generation_difference']==-2 and q['parent_person_id']is None and q['relationship_basis']==KIND)
  if a['predicate']=='raised_by':
   return(set(q)=={'source_term','care_basis','legal_adoption_status','source_clause_binding'}and q['source_term']=='為祖母'+gm['surface']+'所養'and q['care_basis']==KIND and q['legal_adoption_status']=='not_stated')
  return False
 except(KeyError,ValueError,TypeError,IndexError,AttributeError):return False
