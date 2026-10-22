"""Literal family clauses across a complete biography; no invented name anchors."""
import hashlib,re

def valid(a,paragraphs,assertions=()):
 try:
  q=a['qualifiers'];b=q['source_clause_binding'];e,=a['evidence'];cid,p=paragraphs[e['paragraph_id']];t=p['text'];ms={m['id']:m for m in p['mentions']};r={k:ms[v]for k,v in b['roles'].items()};s=ms[e['subject_person_mention_id']];o=ms[e['object_person_mention_id']]
  if(set(b)!={'kind','rule','roles','clause_start','clause_end','paragraph_sha256','revision_id'}or b['kind']!='biography_family_clause'or a['status']!='source_attested'or a['human_reviewed']is not False or e['chapter_id']!=cid or e['quote']!=t or p.get('text_layer')!='received_chapter'or p['source_position']['revision_id']!=b['revision_id']or hashlib.sha256(t.encode()).hexdigest()!=b['paragraph_sha256']or s['person_id']!=a['subject_person_id']or o['person_id']!=a['object_person_id']or s['person_id']==o['person_id']):return False
  start,end=b['clause_start'],b['clause_end']
  if type(start)is not int or type(end)is not int or not 0<=start<end<=len(t):return False
  text=t[start:end];allowed=[]
  def word(k):return r[k]['surface']
  def pid(k):return r[k]['person_id']
  def literal(chunks):
   pos=start;out=''
   for role,lit in chunks:
    w=word(role)if role else lit
    if role and(r[role]['kind']!='person'or r[role]['start']!=pos or t[pos:r[role]['end']]!=w):return False
    pos+=len(w);out+=w
   return text==out
  rule=b['rule']
  if rule=='continued_biography_comma_head_grandfather_father':
   if set(r)!={'head','father','grandfather'}or start!=0 or len({pid(k)for k in r})!=3:return False
   pattern=re.escape(word('head'))+r'字[^，。：「」]+，[^，。：「」]+人也。祖'+re.escape(word('grandfather'))+r'，[^，。：「」]+，父'+re.escape(word('father'))+r'，[^，。：「」]+，並有名前代。'
   if not re.fullmatch(pattern,text)or r['head']['start']!=0 or t[r['grandfather']['start']-1]!='祖'or t[r['father']['start']-1]!='父':return False
   allowed=[('father','head','father'),('grandfather','head','grandfather')];term=('父'+word('father'))if a['predicate']=='father'else('祖'+word('grandfather'))
  elif rule=='continued_biography_resumed_elder_then_named_younger':
   if set(r)!={'head','younger'}or not literal([('head',''),(None,'內圖止足，且實避事。弟'),('younger',''),(None,'，時爲吏部尚書。')]):return False
   allowed=[('brother','younger','head')];term='弟'+word('younger')
  elif rule=='continued_biography_unassumed_named_recipient_stays_with_mother':
   if set(r)!={'head','mother','ruler'}or word('mother')!='母'or start!=0 or len({pid(k)for k in r})!=3:return False
   if not literal([(None,'建武四年，詔徵爲侍中、中書令，遂抗表不應召。遣諸子還京師，獨與'),('mother',''),(None,'留，築室郡之西郭。'),('ruler',''),(None,'下詔曰：「夫超然榮觀，風流自遠；蹈彼幽人，英華罕值。故長揖楚相，見稱南國；高謝漢臣，取貴良史。新除侍中、中書令'),('head','')]):return False
   allowed=[('maternal_role','head','mother')];term='獨與母留'
  else:return False
  hit=[(pred,x,y)for pred,x,y in allowed if pred==a['predicate']and r[x]['id']==s['id']and r[y]['id']==o['id']]
  if len(hit)!=1 or q['source_term']!=term:return False
  expected={'source_term','source_clause_binding'}
  if a['predicate']in ('father','grandfather'):
   expected.add('lineage')
   if q.get('lineage')!='paternal':return False
  elif a['predicate']=='brother':
   expected.add('relative_birth_order')
   if q.get('relative_birth_order')!={'older_person_id':a['object_person_id'],'younger_person_id':a['subject_person_id'],'operator':'lt','older_ordinal':None,'younger_ordinal':None,'scope':'siblings'}:return False
  else:
   expected|={'role','biological_mother','father_person_id'}
   if q.get('role')!='mother_unspecified'or q.get('biological_mother')is not None or q.get('father_person_id')is not None:return False
  return set(q)==expected
 except(KeyError,TypeError,IndexError,ValueError):return False

def children_errors(a,ch):
 try:
  ctx=a['context'];ids=ctx['paragraph_ids'];ps=ch['paragraphs'];order=[p['id']for p in ps];by={p['id']:p for p in ps};b=ctx['secondary_child_clause'];e=a['evidence']
  if(ctx['kind']!='biographical_child_continuation'or set(b)!={'kind','first_mention_id','second_mention_id'}or b['kind']!='named_son_and_second_son_follow_biography'or len(ids)!=2 or ids!=[x['paragraph_id']for x in e]or order.index(ids[1])!=order.index(ids[0])+1 or a['predicate']!='father'or a['status']!='source_attested'or ctx['status']!='contextual_provisional'or ctx['human_reviewed']is not False or not ctx['rationale']):return ['連續子附傳格式不符']
  before,last=[by[i]for i in ids]
  try:
   from scripts.biographical_kinship import received_paragraphs_contiguous
  except ImportError:
   from biographical_kinship import received_paragraphs_contiguous
  if not received_paragraphs_contiguous(ch,before,last):return ['連續子附傳不可跳原文']
  for p,ee in zip([before,last],e):
   if p.get('text_layer')!='received_chapter'or p['source_position']['revision_id']!=ch['source']['revision_id']or ee['quote']!=p['text']or ee['chapter_id']!=ch['id']or any(ee[k]!=ch[k]for k in ['work_id','book_id','source_id']):return ['連續子附傳見證或引文不符']
  parent=next(m for m in before['mentions']if m['id']==ctx['parent_mention_id']);ms={m['id']:m for m in last['mentions']};first,second=[ms[b[k]]for k in ['first_mention_id','second_mention_id']];child=ms[ctx['child_mention_id']]
  if parent['person_id']!=a['object_person_id']or parent['kind']!='person'or not before['text'].endswith(parent['surface']+'所著書及文章，並行於世。')or parent['end']!=len(before['text'])-len('所著書及文章，並行於世。'):return ['父名須為前傳末明示傳主']
  text='子'+first['surface']+'，官至司徒右長史，坐殺牛免官，卒於家。次子'+second['surface']+'，頗有文才，仕至晉安太守，卒官。'
  if last['text']!=text or first['start']!=1 or second['start']!=text.index('次子')+2 or len({parent['person_id'],first['person_id'],second['person_id']})!=3 or any(x['kind']!='person'for x in [first,second])or child['person_id']!=a['subject_person_id']:return ['子附傳明名／次序／角色不符']
  q=a['qualifiers'];term='子'if child['id']==first['id']else'次子';expected={'source_term','lineage'}
  if child['id']==second['id']:
   expected.add('birth_order')
   if q.get('birth_order')!={'parent_person_id':a['object_person_id'],'scope':'sons_of_parent','ordinal':2,'position':'unspecified','interpretation_status':'source_attested'}:return ['次子僅記父系子序二']
  if set(q)!=expected or q['lineage']!='paternal'or q['source_term']!=term:return ['子附傳不補長子或母']
  return []
 except(KeyError,TypeError,IndexError,ValueError,StopIteration):return ['連續子附傳資料不完整']
