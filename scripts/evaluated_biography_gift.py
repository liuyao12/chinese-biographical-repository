"""A received biography resumes its topic after another person's evaluation.
The evaluator never acquires the subsequent career, death or posthumous grant.
"""
import hashlib,re
KIND='evaluated_biography_topic_career_death_gift'
def valid(h,paragraphs,mentions,events):
 try:
  if not isinstance(h,dict):return False
  b=h['posthumous_basis'];keys={'kind','source_term','source_revision','paragraph_sha256','topic_person_mention_id','resumed_person_mention_id','evaluator_person_mention_id','description_anchor','evaluation_anchor','object_anchor','career_anchor','death_anchor','grant_anchor','death_event_id','evidence'}
  if not isinstance(b,dict)or set(b)!=keys or b['kind']!=KIND:return False
  e,=b['evidence'];cid,p=paragraphs[e['paragraph_id']];text=p['text'];topic=mentions[b['topic_person_mention_id']];resume=mentions[b['resumed_person_mention_id']];other=mentions[b['evaluator_person_mention_id']];event=events[b['death_event_id']];start=h['effective_period']['start'];end=h['effective_period']['end'];pid=h['person_id']
  if(h['mode']!='posthumous_grant'or h['kind']!='office'or h['status']!='source_attested'or p['text_layer']!='received_chapter'or e['chapter_id']!=cid or e['quote']!=text or b['source_term']!=text or b['paragraph_sha256']!=hashlib.sha256(text.encode()).hexdigest()or b['source_revision']!=p['source_position']['revision_id']or b['evidence']!=h['evidence']or b['evidence']!=start['evidence']or start!={'status':'source_event','event_type':'posthumous_grant','date_expression':None,'evidence':h['evidence']}or end!={'status':'unknown','date_expression':None,'evidence':[]}):return False
  if(any(m[:2]!=(cid,p['id'])or m[2].get('kind')!='person'or type(m[2].get('start'))is not int or type(m[2].get('end'))is not int or not 0<=m[2]['start']<m[2]['end']<=len(text)or text[m[2]['start']:m[2]['end']]!=m[2]['surface']for m in [topic,resume,other])or topic[2]['person_id']!=pid or resume[2]['person_id']!=pid or other[2]['person_id']==pid or topic[2]['start']!=0 or e['person_mention_id']!=resume[2]['id']):return False
  if(not re.match(re.escape(topic[2]['surface'])+r'字[^，。；：]{1,8}，',text)or event['event_type']!='death'or event['status']!='source_attested'or event['person_id']!=pid or event.get('date_expression')is not None or event.get('normalized_date')is not None or not any(x['chapter_id']==cid and x['paragraph_id']==p['id']and x['quote']==text and x.get('person_mention_id')==resume[2]['id']for x in event['evidence'])):return False
  def exact(a):return isinstance(a,dict)and set(a)=={'paragraph_id','start','end','surface'}and a['paragraph_id']==p['id']and type(a['start'])is int and type(a['end'])is int and 0<=a['start']<a['end']<=len(text)and text[a['start']:a['end']]==a['surface']
  desc,ev,obj,career,death,gift=[b[k]for k in ['description_anchor','evaluation_anchor','object_anchor','career_anchor','death_anchor','grant_anchor']]
  if not all(exact(a)for a in [desc,ev,obj,career,death,gift]):return False
  if(not topic[2]['end']<=resume[2]['start']==desc['start']<desc['end']==ev['start']or desc['surface'][:len(resume[2]['surface'])]!=resume[2]['surface']or not desc['surface'].endswith('。')or re.search('曰|卒|薨|死|贈|生|拜|封',desc['surface'])or ev['start']!=other[2]['start']or ev['surface']!=other[2]['surface']+'甚器之。'or obj['surface']!='之'or obj['start']!=other[2]['end']+2 or obj['end']!=ev['end']-1 or ev['end']!=career['start']or career['end']!=death['start']):return False
  office=r'[^，。；：曰贈卒薨死]{1,16}(?:尚書|僕射|領軍|將軍|內史|太守)'
  if not re.fullmatch('遷'+office+'(?:、'+office+')*，領'+office+'，出[為爲]'+office+'(?:、'+office+')*。',career['surface']):return False
  if(death['surface']!=event['source_term']or death['surface']not in('卒','薨')or text[death['end']:gift['start']]!='，'or gift['surface']!='贈'+h['title']or text[gift['end']:gift['end']+1]not in('，','。')):return False
  # Every known actor in the topic-to-gift scope must retain its exact role.
  for m in p['mentions']:
   if m.get('kind')!='person'or not topic[2]['start']<=m['start']<gift['end']:continue
   if m['id']==other[2]['id']:continue
   if m['person_id']!=pid:return False
   if m['start']>=ev['start']and not(m['surface']=='之'and m['start']==obj['start']and m['end']==obj['end']):return False
  return any(a.get('paragraph_id')==p['id']and a.get('person_mention_id')==resume[2]['id']and a.get('surface')==h['title']and a.get('start')==gift['start']+1 and a.get('end')==gift['end']and a.get('usage')=='posthumous_usage'and a.get('date_expression')is None for a in h['attestations'])
 except(KeyError,TypeError,ValueError,AssertionError,AttributeError,IndexError):return False
