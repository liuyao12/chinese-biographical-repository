# coding: utf-8
"""Literal named-son / numbered-son / recalled-sons / same-mother clauses.

These rules bind actual source positions and grammatical roles, never a person,
chapter or surname allowlist. They do not infer an unnamed mother or ordering.
"""
import re,hashlib
PREFIX='close_family_direct_'
def valid(a,paragraphs):
 try:
  q=a['qualifiers'];b=q['source_clause_binding'];e,=a['evidence'];cid,p=paragraphs[e['paragraph_id']];t=p['text'];ms={m['id']:m for m in p['mentions']};roles={r:ms[mid]for r,mid in b['roles'].items()};start,end=b['clause_start'],b['clause_end'];rule=b['rule'];subject=ms[e['subject_person_mention_id']];obj=ms[e['object_person_mention_id']]
  if set(b)!={'kind','rule','roles','clause_start','clause_end','paragraph_sha256','revision_id'}or b['kind']!='biography_family_clause'or not rule.startswith(PREFIX)or e['quote']!=t or e['chapter_id']!=cid or p.get('text_layer')!='received_chapter'or p.get('source_position',{}).get('revision_id')!=b['revision_id']or hashlib.sha256(t.encode()).hexdigest()!=b['paragraph_sha256']or a['status']!='source_attested'or a.get('human_reviewed')is not False:return False
  if any(k in p for k in ['annotator','attached_note_to_paragraph_id']):return False
  if type(start)is not int or type(end)is not int or not 0<=start<end<=len(t):return False
  text=t[start:end]
  # A source clause must be outside every outer quotation. Names inside quoted
  # demands or analogies cannot establish this biographical parentage.
  if t[:start].count('「')!=t[:start].count('」')or t[:start].count('『')!=t[:start].count('』')or any(c in text for c in '「」『』'):return False
  if any(m.get('kind')!='person'or t[m['start']:m['end']]!=m['surface']for m in roles.values()):return False
  if subject['person_id']!=a['subject_person_id']or obj['person_id']!=a['object_person_id']or subject['person_id']==obj['person_id']:return False
  def w(r):return roles[r]['surface']
  def at(r,n):return roles[r]['start']==start+n
  def permitted(pred,x,y):return a['predicate']==pred and subject['id']==roles[x]['id']and obj['id']==roles[y]['id']
  allowed={'source_term','source_clause_binding'}
  if rule in (PREFIX+'head_son',PREFIX+'head_ordinal_son'):
   if set(roles)!={'child','parent'}or start!=0 or not at('child',0):return False
   pat=re.escape(w('child'))+r'，字([^，。：「」『』]+)，'+re.escape(w('parent'))+(r'之子也。'if rule.endswith('head_son')else r'第([一二三四五六七八九十]+)子也。')
   m=re.fullmatch(pat,text)
   if not m or not at('parent',len(w('child'))+2+len(m[1])+1)or not permitted('father','child','parent'):return False
   allowed.add('lineage')
   if q.get('lineage')!='paternal':return False
   if rule.endswith('head_son'):
    if q['source_term']!=w('parent')+'之子也':return False
   else:
    number=m[2];digits='一二三四五六七八九'
    if number not in digits:return False
    term='第'+number+'子';allowed.add('birth_order')
    if q['source_term']!=term or q.get('birth_order')!={'scope':'sons_of_parent','ordinal':digits.index(number)+1,'source_term':term,'parent_person_id':obj['person_id'],'position':'unspecified','interpretation_status':'source_attested'}:return False
  elif rule==PREFIX+'recalled_three_sons':
   if set(roles)!={'parent','first','second','third'}or len({m['person_id']for m in roles.values()})!=4:return False
   time=re.match(r'[^，。：「」『』]{2,5}初，',text);time=time.group()if time else''
   prefix=time+'詔以'+w('parent')+'輕陷重刑，前勳不宜堙沒，乃赦其三子';pattern=prefix+'、'.join(w(r)for r in ['first','second','third'])+'還第'
   if start!=0 or text!=pattern or not at('parent',len(time)+2)or not at('first',len(prefix))or not at('second',len(prefix)+len(w('first'))+1)or not at('third',len(prefix)+len(w('first'))+len(w('second'))+2):return False
   if not any(permitted('father',r,'parent')for r in ['first','second','third']):return False
   allowed.add('lineage')
   if q.get('lineage')!='paternal'or q['source_term']!='三子'+'、'.join(w(r)for r in ['first','second','third']):return False
  elif rule==PREFIX+'same_mother_after_execution':
   if set(roles)!={'subject','sibling'}or text!=w('sibling')+'既誅，'+w('subject')+'以同母'or not at('sibling',0)or not at('subject',len(w('sibling'))+3)or not permitted('brother','subject','sibling'):return False
   allowed.add('shared_mother')
   if q.get('shared_mother')is not True or q['source_term']!=w('subject')+'以同母':return False
  elif rule==PREFIX+'son_after_named_murder':
   if set(roles)!={'parent','actor','child'}or len({m['person_id']for m in roles.values()})!=3 or not permitted('father','child','parent'):return False
   pat='詔'+re.escape(w('parent'))+r'兼[^。：「」『』非未無不]{1,20}，以[^。：「」『』非未無不]{1,40}，至[^，。：「」『』非未無不]{1,12}，為'+re.escape(w('actor'))+'前鋒所害。贈[^。：「」『』非未無不]{1,20}。子'+re.escape(w('child'))+'立。'
   if not re.fullmatch(pat,text)or not at('parent',1)or roles['actor']['end']>=roles['child']['start']or not text.endswith('子'+w('child')+'立。')or roles['child']['end']!=end-2:return False
   # Reject a hidden extra named actor/relative inside this complete clause.
   if any(m.get('kind')=='person'and start<=m['start']<end and m['id']not in{r['id']for r in roles.values()}for m in p['mentions']):return False
   allowed.add('lineage')
   if q.get('lineage')!='paternal'or q['source_term']!='子'+w('child'):return False
  else:return False
  return set(q)==allowed
 except(KeyError,TypeError,ValueError,IndexError,StopIteration):return False
