"""Consecutive paternal generations explicitly bound by one complete epitaph."""
import hashlib

def valid(member,rows,assertions,chapters):
 try:
  b=member['parent_connection'];near=assertions[b['nearer_ancestor_assertion_id']];far=assertions[b['farther_ancestor_assertion_id']];subject=rows[b['chain_subject_person_id']];parent=rows[member['parent_person_id']]
  if not(b['type']=='parent_between_consecutive_ancestors'and b['interpretation_basis']=='epitaph_named_family_sequence'and b['status']=='contextual_provisional'and b['human_reviewed']is False and b['rationale']and member['source_assertion_id']is None):return False
  if not(near['predicate']=='father'and far['predicate']=='grandfather'and far['qualifiers']['lineage']=='paternal'and near['subject_person_id']==far['subject_person_id']and near['subject_person_id']in subject['source_person_ids']and near['object_person_id']in member['source_person_ids']and far['object_person_id']in parent['source_person_ids']and len({near['subject_person_id'],near['object_person_id'],far['object_person_id']})==3):return False
  if any(a.get('status')!='source_attested'or a.get('human_reviewed')is not False for a in [near,far]):return False
  refs=b['references']
  if len(refs)!=2 or {r['assertion_id']for r in refs}!={near['id'],far['id']}:return False
  en,=near['evidence'];ef,=far['evidence']
  if any(en[k]!=ef[k]for k in ['chapter_id','paragraph_id','source_id','quote']):return False
  c=chapters[en['chapter_id']];p,=c['paragraphs'];t=p['text'];binding=c['annotation']['epitaph_fact_binding'];ms={m['id']:m for m in p['mentions']};roles={k:ms[v]for k,v in binding['roles'].items()}
  if not(p['id']==en['paragraph_id']and en['quote']==t and c['source_id']==en['source_id']and p['text_layer']=='epitaph_as_modernly_transcribed'and c['source']['transcription_witness']['pdf_sha256']==binding['witness_pdf_sha256']and c['source']['transcription_witness']['original_stone_or_rubbing_image_verified']is False and hashlib.sha256(t.encode()).hexdigest()==binding['paragraph_sha256']):return False
  if binding['kind']!='epitaph_named_family_full'or binding['source_id']!=c['source_id']or binding['paragraph_id']!=p['id']:return False
  if any(en[k]!=c[k]or ef[k]!=c[k]for k in ['work_id','book_id','source_id']):return False
  if near['qualifiers']['source_clause_binding']!=binding or far['qualifiers']['source_clause_binding']!=binding:return False
  head,grand,father,zi=[roles[k]for k in ['head','grandfather','father','zi']]
  for m in [head,grand,father,zi]:
   if m['kind']!='person'or t[m['start']:m['end']]!=m['surface']:return False
  if not(head['person_id']==near['subject_person_id']==far['subject_person_id']==zi['person_id']and grand['person_id']==far['object_person_id']and father['person_id']==near['object_person_id']):return False
  if not(en['subject_person_mention_id']==ef['subject_person_mention_id']==head['id']and en['object_person_mention_id']==father['id']and ef['object_person_mention_id']==grand['id']):return False
  if not(t.startswith('晉故男子')and t[head['end']:zi['start']]=='字'and t[zi['end']:grand['start']].startswith('故')and not any(x in t[:father['end']+3]for x in ['非','不','未','無','曰','「','」'])and t[grand['end']:father['start']]=='之孫贛令'and t[father['end']:father['end']+3]=='之元子'):return False
  if near['qualifiers']['source_term']!='之元子'or far['qualifiers']['source_term']!='之孫':return False
  if near['qualifiers']['birth_order']!={'parent_person_id':father['person_id'],'scope':'sons_of_parent','ordinal':1,'position':'eldest','interpretation_status':'source_attested'}:return False
  if any(a.get('predicate')=='father'and a.get('subject_person_id')in member['source_person_ids']and a.get('object_person_id')not in parent['source_person_ids']for a in assertions.values()):return False
  for ref in refs:
   if any(ref[k]!=c[k]for k in ['work_id','book_id','source_id']):return False
   if any(ref[k]!=en[k]for k in ['chapter_id','paragraph_id','source_id','quote'])or not ref.get('scope')or ref.get('url')not in [c['source']['url'],c['source']['permalink']]:return False
  return True
 except (KeyError,TypeError,ValueError):return False
