"""Position-bound received biographical family clauses, without person-ID allowlists."""
import hashlib,re
KIND='biography_family_clause'
def valid(a,paragraphs,assertions=(),chapters=None,root=None):
 if not isinstance(a, dict):return False
 q_guard=a.get('qualifiers', {})
 if not isinstance(q_guard, dict):return False
 b_guard=q_guard.get('source_clause_binding', {})
 if not isinstance(b_guard, dict) or not isinstance(b_guard.get('rule', ''), str):return False
 if b_guard.get('rule')=='fixed_jin035_registered_unit':
  try:from scripts.fixed_jin035_peixiu_peiwei_registration import family_valid
  except ImportError:from fixed_jin035_peixiu_peiwei_registration import family_valid
  return family_valid(a,paragraphs,root)
 if b_guard.get('rule')=='fixed_repository_witness_near_parent':
  try:from scripts.fixed_xintang072_wang_preface import family_valid
  except ImportError:from fixed_xintang072_wang_preface import family_valid
  return family_valid(a,paragraphs,chapters,root)
 if b_guard.get('rule')=='fixed_jin031_typed_complete_unit':
  try:from scripts.fixed_jin031_jia_typed import family_valid
  except ImportError:from fixed_jin031_jia_typed import family_valid
  return family_valid(a,paragraphs,root)
 if b_guard.get('rule')=='fixed_comparison_jin080_received_roles':
  try:from scripts.fixed_jin080_wangxizhi_comparison import family_valid
  except ImportError:from fixed_jin080_wangxizhi_comparison import family_valid
  return family_valid(a,paragraphs,root)
 if b_guard.get('rule')=='fixed_comparison_jin098_received_roles':
  try:from scripts.fixed_jin098_wangdun_comparison import family_valid
  except ImportError:from fixed_jin098_wangdun_comparison import family_valid
  return family_valid(a,paragraphs,root)
 if b_guard.get("rule")=="natural_received_head_father":
  try:
   try:from scripts.biographical_kinship import natural_parentage_errors
   except ImportError:from biographical_kinship import natural_parentage_errors
   return not natural_parentage_errors(a,(chapters or {})[a["evidence"][0]["chapter_id"]],root)
  except (KeyError,TypeError,IndexError):return False
 if a.get('qualifiers',{}).get('source_clause_binding',{}).get('rule','').startswith('layered_'):
  try:from scripts.layered_biography_titles import family_valid
  except ImportError:from layered_biography_titles import family_valid
  return family_valid(a,paragraphs,chapters or {})
 q_new=a.get('qualifiers', {})
 if not isinstance(q_new, dict):return False
 b_new=q_new.get('source_clause_binding', {})
 if not isinstance(b_new, dict)or not isinstance(b_new.get('rule', ''), str):return False
 if b_new.get('rule', '').startswith('genealogical_preface_'):
     try:
         from scripts.received_genealogy_kinship import valid as genealogy_valid
     except ImportError:
         from received_genealogy_kinship import valid as genealogy_valid
     return genealogy_valid(a, paragraphs)

 if a.get('qualifiers', {}).get('source_clause_binding', {}).get('rule', '').startswith('continued_biography_'):
     try:
         from scripts.continued_biography_family import valid as continued_valid
     except ImportError:
         from continued_biography_family import valid as continued_valid
     return continued_valid(a, paragraphs)

 # Position-bound close-family clauses; retain all older grammar contracts.
 if a.get('qualifiers', {}).get('source_clause_binding', {}).get('rule', '').startswith('close_family_'):
     try:
         from scripts.biography_close_family import valid as close_family_valid
     except ImportError:
         from biography_close_family import valid as close_family_valid
     return close_family_valid(a,paragraphs,assertions)

 try:
  q=a['qualifiers'];b=q['source_clause_binding'];e,=a['evidence'];cid,p=paragraphs[e['paragraph_id']];t=p['text'];ms={m['id']:m for m in p['mentions']}
  if(set(b)!={'kind','rule','roles','clause_start','clause_end','paragraph_sha256','revision_id'}or b['kind']!=KIND or a['status']!='source_attested'or a['human_reviewed']is not False or e['chapter_id']!=cid or e['quote']!=t or p.get('text_layer')!='received_chapter'or p.get('source_position',{}).get('revision_id')!=b['revision_id']or hashlib.sha256(t.encode()).hexdigest()!=b['paragraph_sha256']):return False
  roles={k:ms[mid]for k,mid in b['roles'].items()}
  if any(m['kind']!='person'or t[m['start']:m['end']]!=m['surface']for m in roles.values()):return False
  s=ms[e['subject_person_mention_id']];o=ms[e['object_person_mention_id']]
  if s['person_id']!=a['subject_person_id']or o['person_id']!=a['object_person_id']or s['person_id']==o['person_id']:return False
  start,end=b['clause_start'],b['clause_end'];text=t[start:end]
  if type(start)is not int or type(end)is not int or not 0<=start<end<=len(t)or(start and t[start-1]in'非不未無'):return False
  def token(k):return roles[k]['surface']
  def id(k):return roles[k]['person_id']
  def exact(pattern):return text==pattern
  def positioned(k,offset):return roles[k]['start']==start+offset
  allowed=[];older=None;younger=None;rule=b['rule'];eldest=None
  if rule=='head_named_father':
   if set(roles)!={'child','parent'}or roles['child']['start']!=0 or s['id']!=roles['child']['id']or o['id']!=roles['parent']['id']:return False
   c=roles['child'];f=roles['parent'];between=t[c['end']:f['start']]
   if not(between.startswith('字')and between.endswith('。父')and len(between.split('。'))==2 and not any(x in between for x in'非不未無')):return False
   if start!=0 or end!=f['end']or not text.endswith('父'+token('parent')):return False
   allowed=[('father','child','parent')]
  elif rule in('named_parent_son','named_child_father'):
   if set(roles)!={'child','parent'}:return False
   if rule=='named_child_father':pattern=token('child')+'父'+token('parent');order=['child','parent'];gap='父'
   else:gap='子';pattern=token('parent')+gap+token('child');order=['parent','child']
   if not exact(pattern)or not positioned(order[0],0)or not positioned(order[1],len(token(order[0]))+len(gap)):return False
   allowed=[('father','child','parent')]
  elif rule=='named_role_son':
   if set(roles)!={'child','parent'}or token('child')!='小子'or not exact(token('parent')+'小子')or not positioned('parent',0)or not positioned('child',len(token('parent'))):return False
   allowed=[('father','child','parent')]
  elif rule=='named_children_list':
   if set(roles)!={'child','parent'}:return False
   m=re.fullmatch(r'有([二三四五六七八九十])子：([^，。；]+)',text)
   if not m:return False
   number='一二三四五六七八九十'.index(m[1])+1;begin=start+text.index('：')+1
   children=[x for x in p['mentions']if x['kind']=='person'and begin<=x['start']and x['end']<=end]
   if len(children)!=number or len({x['person_id']for x in children})!=number or '、'.join(x['surface']for x in children)!=m[2]or s['id']not in{x['id']for x in children}:return False
   parent=roles['parent']
   if parent['end']!=start:
    if parent['start']>3 or parent['end']>=start or any(x['person_id']!=parent['person_id']for x in p['mentions']if x['kind']=='person'and x['end']<=start):return False
   if o['id']!=parent['id']:return False
   allowed=[('father','child','parent')]
  elif rule=='ranked_older_brothers':
   if set(roles)!={'head','first','second'}or start!=0 or not exact(token('head')+'長兄'+token('first')+'，次兄'+token('second')+'，'):return False
   offsets={'head':0,'first':len(token('head'))+2,'second':len(token('head'))+2+len(token('first'))+3}
   if not all(positioned(k,v)for k,v in offsets.items()):return False
   allowed=[('brother','first','head'),('brother','second','head'),('brother','first','second')]
  elif rule=='younger_brother':
   if set(roles)!={'elder','younger'}or not exact(token('elder')+'弟'+token('younger'))or not positioned('elder',0)or not positioned('younger',len(token('elder'))+1):return False
   allowed=[('brother','younger','elder')]
  elif rule=='home_owner_agnatic_elder_cousin':
   if set(roles)!={'owner','cousin'}or roles['owner']['start']!=0 or not t.startswith(token('owner'))or not exact('嘗營別宅，其從兄'+token('cousin')+'見而悅之，即以宅與')or not positioned('cousin',8):return False
   if any(m['person_id']!=id('owner')for m in p['mentions']if m['kind']=='person'and m['end']<=start):return False
   allowed=[('agnatic_cousin','cousin','owner')]
  elif rule=='sons_marriage_to_daughter':
   if set(roles)!={'head','son','father','bride'}or start!=0 or token('bride')!='女':return False
   pattern=token('head')+'子'+token('son')+'娶'+token('father')+'女'
   if not exact(pattern):return False
   offsets={'head':0,'son':len(token('head'))+1,'father':len(token('head'))+1+len(token('son'))+1,'bride':len(pattern)-1}
   if not all(positioned(k,v)for k,v in offsets.items()):return False
   allowed=[('spouse','son','bride'),('father','bride','father')]
  elif rule=='parallel_son_and_daughter_marriages':
   if set(roles)!={'head','son','bride_father','bride','daughter','husband_father','husband'}or start!=0 or any(token(k)!='女'for k in('bride','daughter'))or token('husband')!='子':return False
   chunks=[('head',''),(None,'長子'),('son',''),(None,'先娶'),('bride_father',''),('bride',''),(None,'，'),('daughter',''),(None,'適'),('husband_father',''),('husband',''),(None,'，')];cursor=0;pattern=''
   for role,literal in chunks:
    v=token(role)if role else literal
    if role and not positioned(role,cursor):return False
    pattern+=v;cursor+=len(v)
   if not exact(pattern):return False
   allowed=[('father','son','head'),('spouse','son','bride'),('father','bride','bride_father'),('father','daughter','head'),('spouse','daughter','husband'),('father','husband','husband_father')];eldest=(id('son'),id('head'))
  elif rule=='resumed_subject_wifes_father':
   if set(roles)!={'head','resumed','rival','self','wife','father'}or roles['head']['start']!=0 or id('head')!=id('resumed')or token('wife')!='妻':return False
   resume=roles['resumed'];tail=token('resumed')+'素知';pattern='匿于妻父'+token('father')+'家'
   bridge='素知'+token('rival')+'有望于'+token('self')+'，聞有變，單車入城，'
   if id('self')!=id('head')or t[resume['end']:start]!=bridge or roles['rival']['start']!=resume['end']+2 or roles['self']['start']!=roles['rival']['end']+3:return False
   if not t.startswith(tail,resume['start'])or resume['end']>=start or not exact(pattern)or not positioned('wife',2)or not positioned('father',4):return False
   allowed=[('spouse','head','wife'),('father','wife','father')]
  elif rule=='named_siblings_sister_husband':
   if set(roles)!={'husband','brother','sister'}or token('sister')!='妹':return False
   pattern=token('husband')+'，'+token('brother')+'妹夫也。'
   if not exact(pattern)or not positioned('husband',0)or not positioned('brother',len(token('husband'))+1)or not positioned('sister',len(token('husband'))+1+len(token('brother'))):return False
   allowed=[('sister','sister','brother'),('spouse','sister','husband')]
  elif rule=='wife_verb_takes_named_daughter':
   if set(roles)!={'husband','father','daughter'}or token('daughter')!='女':return False
   pattern=token('husband')+'妻'+token('father')+'女'
   if not exact(pattern)or not positioned('husband',0)or not positioned('father',len(token('husband'))+1)or not positioned('daughter',len(pattern)-1):return False
   allowed=[('spouse','daughter','husband'),('father','daughter','father')]
  elif rule=='son_heir_childless_younger_brother_supplies_son':
   if set(roles)!={'head','heir','brother','successor'}or start!=0 or end!=len(t):return False
   chunks=[('head',''),(None,'襲爵，官至琅邪王友，早卒。子'),('heir',''),(None,'嗣，終東陽太守。無子，弟光祿勳'),('brother',''),(None,'以子'),('successor',''),(None,'嗣，有罪，國除。')];cursor=0;pattern=''
   for role,literal in chunks:
    v=token(role)if role else literal
    if role and not positioned(role,cursor):return False
    pattern+=v;cursor+=len(v)
   if not exact(pattern)or len({id(k)for k in roles})!=4:return False
   allowed=[('father','heir','head'),('brother','brother','heir'),('father','successor','brother'),('ritual_successor_of','successor','heir')]
  elif rule=='deceased_subject_clansmans_son_successor':
   if set(roles)!={'head','clansman','son'}or roles['head']['start']!=0:return False
   m=re.fullmatch(r'竟卒于([^，。]+)，以族人'+re.escape(token('clansman'))+'子'+re.escape(token('son'))+'為嗣。',text)
   if not m:return False
   prefix=len('竟卒于'+m[1]+'，以族人')
   if not positioned('clansman',prefix)or not positioned('son',prefix+1+len(token('clansman'))):return False
   allowed=[('father','son','clansman'),('ritual_successor_of','son','head'),('kinship_unspecified','clansman','head')]
  else:return False
  matches=[(pred,x,y)for pred,x,y in allowed if pred==a['predicate']and id(x)==a['subject_person_id']and id(y)==a['object_person_id']]
  if len(matches)!=1:return False
  pred,x,y=matches[0]
  if e['subject_person_mention_id']!=roles[x]['id']or e['object_person_mention_id']!=roles[y]['id']:return False
  allowedq={'source_term','source_clause_binding'}
  if not isinstance(q.get('source_term'),str)or q['source_term']not in text:return False
  if pred=='father':
   allowedq.add('lineage')
   if q.get('lineage')!='paternal':return False
   if eldest==(a['subject_person_id'],a['object_person_id']):
    allowedq.add('birth_order');bo=q.get('birth_order',{})
    if bo!={'parent_person_id':a['object_person_id'],'scope':'sons_of_parent','ordinal':1,'position':'eldest','source_term':'長子','interpretation_status':'source_attested'}:return False
  elif pred in('brother','sister','agnatic_cousin'):
   allowedq.add('relative_birth_order');rb=q.get('relative_birth_order',{})
   if rule=='younger_brother':older=id('elder');younger=id('younger')
   elif rule=='son_heir_childless_younger_brother_supplies_son':older=id('heir');younger=id('brother')
   elif rule=='named_siblings_sister_husband':older=id('brother');younger=id('sister')
   else:older=a['subject_person_id'];younger=a['object_person_id']
   if rb!={'older_person_id':older,'younger_person_id':younger,'operator':'lt','older_ordinal':None,'younger_ordinal':None,'scope':'agnatic_cousins'if pred=='agnatic_cousin'else'siblings'}:return False
   if pred=='agnatic_cousin':
    allowedq.add('kinship_structure')
    if q.get('kinship_structure')!={'lineage':'paternal','generation_difference':0,'collateral':True,'distance':None,'common_ancestor_person_id':None,'subject_relative_age':'older'}:return False
  elif pred=='ritual_successor_of':
   allowedq|={'succession_kind','legal_adoption_status','parentage_inference'}
   if rule=='son_heir_childless_younger_brother_supplies_son':
    if q.get('succession_kind')!='childless_son_brothers_named_son_si'or q.get('legal_adoption_status')!='not_stated'or q.get('parentage_inference')!='not_inferred':return False
    if not any(xa.get('predicate')=='father'and valid(xa,paragraphs)and xa.get('subject_person_id')==id('successor')and xa.get('object_person_id')==id('brother')and xa.get('qualifiers',{}).get('source_clause_binding')==b for xa in assertions):return False
    return set(q)==allowedq
   if q.get('succession_kind')!='clansmans_named_son_weisi'or q.get('legal_adoption_status')!='not_stated'or q.get('parentage_inference')!='not_inferred':return False
   if not any(xa.get('predicate')=='father'and valid(xa,paragraphs)and xa.get('subject_person_id')==id('son')and xa.get('object_person_id')==id('clansman')and xa.get('qualifiers',{}).get('source_clause_binding',{}).get('rule')==rule for xa in assertions):return False
  elif pred=='kinship_unspecified':
   expected={'kinship_basis':'explicit_clan_member','lineage':'unspecified','generation_difference':None,'exact_distance':None,'common_ancestor_person_id':None};allowedq|=set(expected)
   if any(q.get(k)!=v for k,v in expected.items()):return False
  return set(q)==allowedq
 except(KeyError,TypeError,ValueError,IndexError,StopIteration):return False
