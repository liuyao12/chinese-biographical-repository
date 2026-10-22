"""Four explicit ancestor-role clauses, each with a punctuated career tail.

Narrow opt-in family assembly basis. No source father assertions are fabricated.
An emperor's dated-career mention is not another ancestor or new topic.
"""
import re,hashlib
BASIS='punctuated_biography_four_ancestor_office_sequence'
def valid(member,rows,assertions,chapters):
 try:
  c=member['parent_connection'];f=c['four_ancestor_frame'];near=assertions[c['nearer_ancestor_assertion_id']];far=assertions[c['farther_ancestor_assertion_id']];cid=f['chapter_id'];ch=chapters[cid];p=next(x for x in ch['paragraphs']if x['id']==f['paragraph_id']);t=p['text'];ms={m['id']:m for m in p['mentions']};head=ms[f['head_mention_id']]
  if(set(f)!={'chapter_id','paragraph_id','source_revision','paragraph_sha256','head_mention_id','entries','ruler_time_anchors'}or c['interpretation_basis']!=BASIS or c['type']!='parent_between_consecutive_ancestors'or c['status']!='contextual_provisional'or c.get('human_reviewed')is not False or not c.get('rationale')or member.get('source_assertion_id')is not None):return False
  if(p.get('text_layer')!='received_chapter'or ch['source']['revision_id']!=f['source_revision']or hashlib.sha256(t.encode()).hexdigest()!=f['paragraph_sha256']or head['kind']!='person'or head['start']!=0 or head['person_id']!=c['chain_subject_person_id']or head['person_id']not in rows[c['chain_subject_person_id']]['source_person_ids']):return False
  if len(f['entries'])!=4 or len(f['ruler_time_anchors'])>2:return False
  def anchor(a):return(isinstance(a,dict)and set(a)=={'start','end','surface'}and type(a['start'])is int and type(a['end'])is int and 0<=a['start']<a['end']<=len(t)and t[a['start']:a['end']]==a['surface'])
  chain=[];bound=[]
  for i,(entry,roles,predicate,distance)in enumerate(zip(f['entries'],[('高祖','髙祖'),('曾祖',),('祖',),('父',)],['ancestor','great_grandfather','grandfather','father'],[4,3,2,1])):
   if set(entry)!={'assertion_id','role_anchor','name_mention_id','career_anchor'}:return False
   a=assertions[entry['assertion_id']];m=ms[entry['name_mention_id']];role=entry['role_anchor'];career=entry['career_anchor'];q=a.get('qualifiers',{})
   if(not anchor(role)or not anchor(career)or role['surface']not in roles or m['kind']!='person'or t[m['start']:m['end']]!=m['surface']or role['end']!=m['start']or career['start']!=m['end']or not career['surface'].startswith('，')or not career['surface'].endswith('。')or career['surface'].count('。')!=1):return False
   if(i and bound[-1]!=role['start'])or(not i and not t[head['end']:role['start']].endswith('人也。')):return False
   if(a['status']!='source_attested'or a['predicate']!=predicate or a['subject_person_id']!=head['person_id']or a['object_person_id']!=m['person_id']or q.get('lineage')not in(None,'paternal')or q.get('source_term')!=role['surface']+m['surface']or predicate=='ancestor'and q.get('generation_distance')!=4):return False
   if not any(e.get('chapter_id')==cid and e.get('paragraph_id')==p['id']and e.get('source_id')==ch['source_id']and e.get('quote')==t and e.get('subject_person_mention_id')==head['id']and e.get('object_person_mention_id')==m['id']for e in a['evidence']):return False
   chain.append(a);bound.append(career['end'])
  familyids={head['person_id']}|{a['object_person_id']for a in chain}
  if len(familyids)!=5:return False
  segment=t[f['entries'][0]['role_anchor']['start']:bound[-1]]
  if any(x in segment for x in('母','妻','妾','兄','弟','非','未','不','無','或云','一云','又云','曰','「','」','『','』','；','？','！')):return False
  accepted_rulers=set()
  for item in f['ruler_time_anchors']:
   if set(item)!={'person_mention_id','temporal_anchor'}:return False
   m=ms[item['person_mention_id']];a=item['temporal_anchor']
   if(not anchor(a)or m['kind']!='person'or m['person_id']in familyids or m['surface']not in('太祖','高祖','髙祖','世祖','太宗','世宗','肅宗')or m['start']!=a['start']or a['surface']!=m['surface']+'時歸國'or not any(entry['career_anchor']['start']<=a['start']and a['end']<=entry['career_anchor']['end']for entry in f['entries'])):return False
   accepted_rulers.add(m['id'])
  ancestors={a['object_person_id']for a in chain}
  for m in p['mentions']:
   if m['kind']=='person'and f['entries'][0]['role_anchor']['start']<=m['start']<bound[-1]and m['person_id']not in ancestors and m['id']not in accepted_rulers:return False
  # Career tails must be plain office narratives, not an unparsed second family.
  for entry in f['entries']:
   tail=entry['career_anchor']['surface']
   for item in f['ruler_time_anchors']:tail=tail.replace(item['temporal_anchor']['surface'],'')
   if any(x in tail for x in('祖','父','子','曰','云'))or not any(x in tail for x in('仕','太守','刺史','將軍','相','尚書','侍郎')):return False
  n=next((i for i,a in enumerate(chain)if a['id']==near['id']),None);q=next((i for i,a in enumerate(chain)if a['id']==far['id']),None)
  if n is None or q is None or n!=q+1 or near['object_person_id']not in member['source_person_ids']or far['object_person_id']not in rows[member['parent_person_id']]['source_person_ids']:return False
  # Known contrary father edges remain a conflict instead of being overwritten.
  if any(a.get('predicate')=='father'and a.get('subject_person_id')in member['source_person_ids']and a.get('object_person_id')not in rows[member['parent_person_id']]['source_person_ids']for a in assertions.values()):return False
  refs=c['references']
  return(len(refs)==2 and {r['assertion_id']for r in refs}=={near['id'],far['id']}and all(r['chapter_id']==cid and r['paragraph_id']==p['id']and r['source_id']==ch['source_id']and r['quote']==t and r.get('scope')and r.get('url')in(ch['source']['url'],ch['source']['permalink'])for r in refs))
 except(KeyError,ValueError,TypeError,IndexError,StopIteration,AttributeError):return False
