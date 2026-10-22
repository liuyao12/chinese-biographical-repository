"""Position-bound biography resumption; no nearest-name recipient inference."""
import hashlib

def gift_valid(h,paragraphs,mentions,events):
 try:
  b=h['posthumous_basis'];e,=b['evidence'];cid,p=paragraphs[e['paragraph_id']];t=p['text'];ms={m['id']:m for m in p['mentions']};r={k:ms[v]for k,v in b['roles'].items()};event=events[b['death_event_id']]
  if(set(b)!={'kind','source_term','death_event_id','roles','paragraph_sha256','revision_id','evidence'}or b['kind']!='resumed_biography_death_gift'or set(r)!={'brother','head','ruler','possessive'}or p.get('text_layer')!='received_chapter'or p.get('source_position',{}).get('revision_id')!=b['revision_id']or hashlib.sha256(t.encode()).hexdigest()!=b['paragraph_sha256']or e['chapter_id']!=cid or e['quote']!=t or b['source_term']!=t or h['mode']!='posthumous_grant'or h['kind']!='office'or h['title']!='金紫光祿大夫'or h['evidence']!=b['evidence']or h['effective_period']['start']!={'status':'source_event','event_type':'posthumous_grant','date_expression':None,'evidence':b['evidence']}):return False
  if r['head']['person_id']!=h['person_id']or e['person_mention_id']!=r['head']['id']or r['possessive']['person_id']!=r['brother']['person_id']or len({r[k]['person_id']for k in ['head','brother','ruler']})!=3 or r['possessive']['surface']!='其':return False
  if event['event_type']!='death'or event['person_id']!=h['person_id']or event['source_term']!='卒'or event['date_expression']!='永泰元年'or event['evidence']!=b['evidence']:return False
  chunks=[(None,'加領右軍將軍。兄'),('brother',''),(None,'在吳興，論啓公事稽晚，'),('head',''),(None,'輙代爲啓，'),('ruler',''),(None,'見非'),('possessive',''),(None,'手迹，被問，見原。轉侍中，領太子中庶子，豫州中正。永泰元年，轉散騎常侍，太子詹事。其年卒。年四十五。贈金紫光祿大夫。謚簡子。')]
  pos=0;value=''
  for role,lit in chunks:
   token=r[role]['surface']if role else lit
   if role and(r[role]['kind']!='person'or r[role]['start']!=pos or t[pos:r[role]['end']]!=token):return False
   pos+=len(token);value+=token
  if value!=t:return False
  start=t.index('贈金紫光祿大夫')+1
  return any(a.get('person_mention_id')==r['head']['id']and a.get('paragraph_id')==p['id']and a.get('start')==start and a.get('end')==start+len(h['title'])and a.get('surface')==h['title']and a.get('usage')=='posthumous_usage'for a in h['attestations'])
 except(KeyError,TypeError,ValueError,IndexError):return False

def mourning_end_valid(h,paragraphs,mentions):
 try:
  b=h['end_basis'];e,=b['evidence'];cid,p=paragraphs[e['paragraph_id']];t=p['text'];ms={m['id']:m for m in p['mentions']};r={k:ms[v]for k,v in b['roles'].items()}
  if(set(b)!={'kind','source_term','roles','paragraph_sha256','revision_id','evidence'}or b['kind']!='resumed_biography_mother_mourning_office_end'or set(r)!={'head','mother'}or p.get('text_layer')!='received_chapter'or e['quote']!=t or e['chapter_id']!=cid or b['source_term']!='母喪去官'or not t.endswith('。母喪去官。')or not t.startswith('遷司徒左長史，出爲吳興太守。')or h['title']!='吳興太守'or h['kind']!='office'or h['evidence']!=b['evidence']or h['effective_period']['end']!={'status':'source_event','event_type':'explicit_end','date_expression':None,'evidence':b['evidence']}or p.get('source_position',{}).get('revision_id')!=b['revision_id']or hashlib.sha256(t.encode()).hexdigest()!=b['paragraph_sha256']):return False
  if r['head']['person_id']!=h['person_id']or e['person_mention_id']!=r['head']['id']or r['head']['surface']in ['其','之','母']or r['mother']['surface']!='母'or r['mother']['person_id']==h['person_id']or r['mother']['start']!=len(t)-5 or t[r['head']['start']:r['head']['end']]!=r['head']['surface']:return False
  # Bound topic resumes as judicial actor and named dismissed official; the
  # separately named accused and his mother cannot replace this role.
  return (t[r['head']['start']:].startswith(r['head']['surface']+'收付縣獄考正。')and any(m.get('kind')=='person'and m['person_id']==h['person_id']and t[m['start']-4:m['start']]=='有司奏免'for m in p['mentions'])and all(a.get('person_mention_id')==r['head']['id']for a in h['attestations']))
 except(KeyError,TypeError,ValueError,IndexError):return False

def declined_valid(proposal,chapter):
 try:
  b=proposal['resumed_decline_context'];e,=proposal['evidence'];p=next(p for p in chapter['paragraphs']if p['id']==e['paragraph_id']);t=p['text'];ms={m['id']:m for m in p['mentions']};person=ms[proposal['person_mention_id']];ruler=ms[b['command_issuer_mention_id']]
  if(set(b)!={'kind','command_issuer_mention_id','command_anchor','paragraph_sha256','revision_id'}or b['kind']!='postposed_named_decliner_then_command'or proposal['proposal_kind']!='unassumed_appointment'or proposal['outcome']!='not_assumed'or proposal['status']!='contextual_provisional'or proposal['human_reviewed']is not False or proposal['non_assumption_kind']!='declined'or proposal['title']!='長兼侍中'or person['person_id']!=proposal['person_id']or ruler['person_id']==proposal['person_id']or person['kind']!='person'or ruler['kind']!='person'or p.get('text_layer')!='received_chapter'or p['source_position']['revision_id']!=b['revision_id']or hashlib.sha256(t.encode()).hexdigest()!=b['paragraph_sha256']or e['quote']!=t or any(e[k]!=chapter[k]for k in ['work_id','book_id','source_id'])or e['chapter_id']!=chapter['id']):return False
  def exact(a):return set(a)=={'paragraph_id','start','end','surface'}and a['paragraph_id']==p['id']and type(a['start'])is int and type(a['end'])is int and 0<=a['start']<a['end']<=len(t)and t[a['start']:a['end']]==a['surface']
  app,role,refusal,command=[proposal['appointment_anchor'],proposal['role_anchor'],proposal['non_assumption_anchor'],b['command_anchor']]
  if not all(exact(a)for a in [app,role,refusal,command])or app['surface']!='轉'or role['surface']!='長兼侍中'or refusal['surface']!='固辭不受'or app['end']!=role['start']or role['end']+1!=person['start']or t[role['end']:person['start']]!='。'or t[person['end']:refusal['start']]!='以晨昏有廢，'or t[refusal['end']:ruler['start']]!='。'or command['start']!=ruler['start']or command['end']!=len(t)or command['surface']!=ruler['surface']+'勑令速拜，別停朝直。':return False
  return person['surface']not in ['其','之','母']and len([m for m in p['mentions']if role['end']<=m['start']<len(t)])==2
 except(KeyError,TypeError,ValueError,IndexError,StopIteration):return False
