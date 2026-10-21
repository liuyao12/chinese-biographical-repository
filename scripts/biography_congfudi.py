# coding: utf-8
"""Narrow received-biography head; classical nomenclature, not genetic proof."""
import re
KIND='biography_head_named_congfudi_of_named_reference'
STRUCTURE={'lineage':'paternal','generation_difference':0,'collateral':True,'distance':{'kind':'paternal_first_cousins','common_ancestor_depth':{'subject':2,'reference':2}},'common_ancestor_person_id':None,'subject_relative_age':'younger'}
LITERARY_USAGE={
 'kind':'literary_usage',
 'qualification':'preferred_normal_classical_usage_not_genetic_verification',
 'citations':[
  {'work':'爾雅','layer':'received_text','repository':'kanripo/KR1j0002','commit':'d05339be5792db658c46460693891d9c8fc6a2b7','path':'KR1j0002_004.txt','line':24,'quote':'兄之子弟之子相謂爲從父晜弟','raw_file_sha256':'a39110fdf91a7ce10fa9845434baea54a82881376586500a7d72c64af7416091'},
  {'work':'儀禮','layer':'Zheng_Xuan_commentary','repository':'kanripo/KR1d0026','commit':'02e56def7356f6bba1ed17b319818923df906491','path':'KR1d0026_011.txt','line':264,'quote':'世父叔父/之子也其','raw_file_sha256':'b5c756cc386dd75826a6aeba84f5311985e6755a04986aa6c6548e7f95a846f5'}]}
def biography_congfudi_valid(a,paragraphs):
 try:
  q=a['qualifiers'];b=q['source_clause_binding'];k=q['kinship_structure']
  if (a['predicate']!='agnatic_cousin' or a['status']!='source_attested'
      or type(a.get('human_reviewed'))is not bool
      or set(q)!={'source_term','kinship_structure','source_clause_binding','literary_usage'}
      or k!=STRUCTURE or k['collateral']is not True or type(k['generation_difference'])is not int
      or type(k['distance']['common_ancestor_depth']['subject'])is not int
      or type(k['distance']['common_ancestor_depth']['reference'])is not int
      or q['literary_usage']!=LITERARY_USAGE
      or set(b)!={'kind','start','end','source_layer'}
      or b['kind']!=KIND or b['source_layer']!='received_text'):return False
  e,=a['evidence'];cid,p=paragraphs[e['paragraph_id']];t=p['text']
  position=p.get('source_position',{})
  if not isinstance(position,dict):return False
  if position.get('source_layer') not in (None,'received_text','received_body','received_biography'):return False
  if p.get('text_layer') not in (None,'received_chapter'):return False
  # Real corpus Pei-note metadata remains decisive even without a layer label.
  for metadata in (p,position):
   if 'annotator' in metadata or 'attached_note_to_paragraph_id' in metadata:return False
  ms={m['id']:m for m in p['mentions']}
  s=ms[e['subject_person_mention_id']];o=ms[e['object_person_mention_id']]
  if(p.get('source_layer','received_text')!='received_text'
     or e.get('source_layer','received_text')!='received_text'
     or e['chapter_id']!=cid or e['quote']!=t
     or s['person_id']!=a['subject_person_id']
     or o['person_id']!=a['object_person_id']
     or s['person_id']==o['person_id']):return False
  for m in [s,o]:
   if(m['kind']!='person' or type(m['start'])is not int
      or type(m['end'])is not int or not 0<=m['start']<m['end']<=len(t)
      or t[m['start']:m['end']]!=m['surface']):return False
  start,end=b['start'],b['end']
  if(type(start)is not int or type(end)is not int or start!=0
     or not start<end<=len(t) or s['start']!=0
     or q['source_term']!=t[start:end]):return False
  # Exact complete head, no intervening topic/negation/alternative speech.
  prefix=t[s['end']:o['start']]
  if not re.fullmatch('字[^，。；：、曰云不未非或「」『』\\s]{1,4}，',prefix):return False
  return(t[o['end']:end]=='從父弟也。'
         and q['source_term']==s['surface']+prefix+o['surface']+'從父弟也。')
 except(KeyError,TypeError,ValueError,IndexError):return False
