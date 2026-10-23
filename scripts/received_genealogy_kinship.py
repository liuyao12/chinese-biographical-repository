"""Position-bound single-paragraph patrilineal genealogy clauses; no IDs/names allowlists."""
import re,hashlib
RULES={'genealogical_preface_named_sons_list','genealogical_preface_named_birth_clause'}
def valid(a,paragraphs):
 try:
  q=a['qualifiers'];b=q['source_clause_binding'];e,=a['evidence'];cid,p=paragraphs[e['paragraph_id']];t=p['text'];ms={m['id']:m for m in p['mentions']}
  if set(q)!={'source_term','lineage','source_clause_binding'}or q['lineage']!='paternal'or a['predicate']!='father'or a['status']!='source_attested'or a['human_reviewed']is not False:return False
  if set(b)!={'kind','rule','roles','clause_start','clause_end','paragraph_sha256','revision_id','children_mention_ids','source_count'}or b['kind']!='biography_family_clause'or b['rule']not in RULES:return False
  if cid!=e['chapter_id']or e['quote']!=t or p.get('text_layer')!='received_chapter'or b['revision_id']!=p.get('source_position',{}).get('revision_id')or hashlib.sha256(t.encode()).hexdigest()!=b['paragraph_sha256']:return False
  lo,hi=b['clause_start'],b['clause_end']
  if type(lo)is not int or type(hi)is not int or not 0<=lo<hi<=len(t):return False
  if e.get('relationship_anchor')!={'paragraph_id':p['id'],'start':lo,'end':hi,'surface':t[lo:hi]}:return False
  if lo and t[lo-1]in'非不未無':return False
  if set(b['roles'])!={'parent','child'}:return False
  parent=ms[b['roles']['parent']];child=ms[b['roles']['child']];kids=[ms[mid]for mid in b['children_mention_ids']]
  if not kids or len(kids)!=len({m['id']for m in kids})or child['id']not in{m['id']for m in kids}:return False
  if a['subject_person_id']!=child['person_id']or a['object_person_id']!=parent['person_id']or child['person_id']==parent['person_id']or e['subject_person_mention_id']!=child['id']or e['object_person_mention_id']!=parent['id']:return False
  for m in [parent]+kids:
   if m['kind']!='person'or not(lo<=m['start']<m['end']<=hi)or t[m['start']:m['end']]!=m['surface']:return False
  if parent['start']!=lo or kids!=sorted(kids,key=lambda m:m['start']):return False
  s=t[lo:hi]
  if q['source_term']!=s:return False
  # The optional short biography may contain this parent's name/zi/title, but no other person.
  if b['rule']=='genealogical_preface_named_sons_list':
   pattern=re.escape(parent['surface'])+r'(?P<bio>字[^。]+。|。)?(?P<count>[一二三四五六七八九十])子：(?P<names>[^。]+)。'
   m=re.fullmatch(pattern,s)
   if not m:return False
   number='一二三四五六七八九十'.index(m['count'])+1;begin=lo+m.start('names');end=lo+m.end('names')
   if type(b['source_count'])is not int or number!=b['source_count']or len(kids)!=number or len({k['person_id']for k in kids})!=number:return False
   if '、'.join(k['surface']for k in kids)!=m['names']:return False
   cursor=begin
   for k in kids:
    if k['start']!=cursor:return False
    cursor=k['end']+1
   if kids[-1]['end']!=end:return False
  else:
   if len(kids)!=1 or b['source_count']is not None:return False
   k=kids[0];pattern=re.escape(parent['surface'])+r'字[^。]+。生(?P<office>[^。]*)'+re.escape(k['surface'])+'。'
   m=re.fullmatch(pattern,s)
   if not m or k['end']!=hi-1:return False
   begin=lo+s.index('生')+1;end=k['end']
  allowed={parent['id']}|{k['id']for k in kids}
  for mark in p['mentions']:
   if mark['kind']=='person'and lo<=mark['start']and mark['end']<=hi:
    if mark['start']<begin:
     if mark['person_id']!=parent['person_id']:return False
    elif mark['id']not in allowed:return False
  return True
 except(KeyError,TypeError,ValueError,IndexError):return False
