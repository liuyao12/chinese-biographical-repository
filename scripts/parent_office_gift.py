"""A named biography parent's death, retained office and added noble rank.

No person/name/year allowlists; the father token binds the recipient. This does
not turn an unassumed office into an actual holding or imply its termination.
"""
import re

def valid(h,paragraphs,mentions,events):
 try:
  b=h['posthumous_basis'];e,=h['evidence'];cid,p=paragraphs[e['paragraph_id']];t=p['text'];ms={m['id']:m for m in p['mentions']};parent=ms[b['recipient_person_mention_id']];head=ms[b['biography_head_mention_id']];ruler=ms[b['visiting_ruler_mention_id']];event=events[b['death_event_id']]
  if(set(b)!={'kind','source_term','death_term','grant_term','recipient_person_mention_id','biography_head_mention_id','visiting_ruler_mention_id','death_event_id','evidence'}or b['kind']!='named_biography_parent_office_gift_plus_rank'or h['mode']!='posthumous_grant'or h['kind']!='noble_rank'or h.get('human_reviewed')is not False or b['evidence']!=h['evidence']or b['evidence']!=h['effective_period']['start']['evidence']):return False
  if(p.get('text_layer')!='received_chapter'or e['chapter_id']!=cid or e['quote']!=t or b['source_term']!=t or e.get('person_mention_id')!=parent['id']or h['person_id']!=parent['person_id']or head['start']!=0 or len({x['person_id']for x in(parent,head,ruler)})!=3):return False
  for m in(parent,head,ruler):
   if m['kind']!='person'or t[m['start']:m['end']]!=m['surface']:return False
  if t[parent['start']-1:parent['start']]!='父'or t[parent['end']:parent['end']+1]!='，'or t[ruler['start']:ruler['end']+2]!=ruler['surface']+'南巡'or not parent['end']<ruler['start']:return False
  if any(v in t for v in ('曰：','云：','「','」','『','』')):return False
  death=b['death_term'];grant=b['grant_term'];title=h['title']
  if death!='未之任而卒'or grant!='贈以本官，加'+title or not re.fullmatch(r'[^，。；：、\s]{1,12}(?:公|侯|伯|子|男)',title):return False
  if t.count(death)!=1 or t.count(grant)!=1:return False
  d=t.index(death);g=t.index(grant)
  if not(parent['end']<ruler['start']<d and d+len(death)+1==g and t[d+len(death):g]=='。'):return False
  # All other named people after the father are the explicitly visiting ruler;
  # a newly introduced recipient invalidates the continued parent topic.
  if any(m['kind']=='person'and parent['end']<=m['start']<g and m['id']!=ruler['id']for m in p['mentions']):return False
  if(event['event_type']!='death'or event['person_id']!=h['person_id']or event['source_term']!=death or event.get('date_expression')is not None or not any(x.get('paragraph_id')==p['id']and x.get('quote')==t and x.get('person_mention_id')==parent['id']for x in event['evidence'])):return False
  return any(a['paragraph_id']==p['id']and a['surface']==title and a['start']==g+len('贈以本官，加')and a['end']==g+len(grant)and a.get('person_mention_id')==parent['id']for a in h['attestations'])
 except(KeyError,ValueError,TypeError,IndexError,StopIteration):return False
