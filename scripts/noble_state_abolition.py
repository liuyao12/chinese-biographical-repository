"""A complete received son/heir/supplied-son chain binds 國除 to its last heir."""
def valid(event, paragraphs):
 try:
  keys={'id','person_id','event_type','status','date_expression','source_term','title','holding_id','source_clause_binding','evidence','interpretation_note','reviewer','human_reviewed','model'}
  if event.get('event_type')=='noble_title_succession':keys|={'mode','predecessor_person_id'}
  if set(event)!=keys:return False
  e,=event['evidence'];cid,p=paragraphs[e['paragraph_id']];t=p['text'];b=event['source_clause_binding'];ms={m['id']:m for m in p['mentions']};roles={k:ms[v]for k,v in b['roles'].items()}
  if(set(b)!={'kind','roles'}or b['kind']!='son_heir_childless_younger_brother_supplies_son' or set(roles)!={'head','heir','brother','successor'} or event['event_type']not in ('noble_state_abolition','noble_title_succession')or event['status']!='source_attested'or event['human_reviewed']is not False or e['chapter_id']!=cid or e['quote']!=t or p.get('text_layer')!='received_chapter'or event.get('date_expression')is not None or 'normalized_date'in event or 'normalized_date_range'in event or event.get('title')is not None or event.get('holding_id')is not None ):return False
  if any(m['kind']!='person'or t[m['start']:m['end']]!=m['surface']for m in roles.values())or len({m['person_id']for m in roles.values()})!=4:return False
  chunks=[('head',''),(None,'襲爵，官至琅邪王友，早卒。子'),('heir',''),(None,'嗣，終東陽太守。無子，弟光祿勳'),('brother',''),(None,'以子'),('successor',''),(None,'嗣，有罪，國除。')];cursor=0;pattern=''
  for role,literal in chunks:
   v=roles[role]['surface']if role else literal
   if role and roles[role]['start']!=cursor:return False
   pattern+=v;cursor+=len(v)
  if t!=pattern:return False
  if event['event_type']=='noble_title_succession':
   return(event['source_term']=='襲爵'and event.get('mode')=='accession'and event.get('predecessor_person_id')is None and event['person_id']==roles['head']['person_id']and e['person_mention_id']==roles['head']['id'])
  return(event['source_term']=='有罪，國除'and 'mode'not in event and 'predecessor_person_id'not in event and event['person_id']==roles['successor']['person_id']and e['person_mention_id']==roles['successor']['id'])
 except(KeyError,TypeError,ValueError,IndexError):return False
