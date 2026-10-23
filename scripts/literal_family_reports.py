# coding: utf-8
"""Position-bound family clauses and partial reported son counts; no name allowlists."""
from pathlib import Path
import json,hashlib,re

def anchor(p,a):
 return isinstance(a,dict)and set(a)=={'paragraph_id','start','end','surface'}and a['paragraph_id']==p['id']and type(a['start'])is int and type(a['end'])is int and 0<=a['start']<a['end']<=len(p['text'])and p['text'][a['start']:a['end']]==a['surface']
def safe(root,path):
 r=Path(root).resolve();p=Path(path)
 if p.is_absolute()or'..'in p.parts or not p.parts or p.parts[0]!='source-evidence':raise ValueError('source path boundary')
 q=r/p
 if q.resolve()!=r/p or not q.is_file():raise ValueError('source symlink boundary')
 return q

def bound(e,b,paragraphs,chapters,root):
 cid,p=paragraphs[e['paragraph_id']];ch=chapters[cid];t=p['text'];a=b['clause_anchor']
 assert e['quote']==t and e['chapter_id']==cid and all(e[k]==ch[k]for k in ('work_id','book_id','source_id'))
 assert b['source_revision']==ch['source']['revision_id']and b['paragraph_sha256']==hashlib.sha256(t.encode()).hexdigest()
 assert b['source_layer']==p.get('text_layer')and b['source_layer']in('received_chapter','witness_appended_pei_songzhi_note')and not any(k in p for k in ('annotator','attached_note_to_paragraph_id'))
 assert anchor(p,a)and not any(x in t[max(0,a['start']-1):a['start']]for x in '非未不無')
 assert t[:a['start']].count('「')==t[:a['start']].count('」')and t[:a['start']].count('『')==t[:a['start']].count('』')and not any(x in a['surface']for x in'「」『』')
 projection=json.loads(safe(root,p['source_position']['raw_projection_ref']).read_text());u=next(x for x in projection['paragraphs']if x['paragraph_id']==p['id']);raw=safe(root,projection['raw_file']).read_bytes()
 assert hashlib.sha256(raw).hexdigest()==projection['raw_file_sha256']==ch['source']['response_sha256']and u['text']==t and ''.join(raw.decode('utf-8')[i]for i in u['raw_positions'])==t
 expected={'received_chapter':('body','received_body'),'witness_appended_pei_songzhi_note':('note','pei_annotation')}[p['text_layer']]
 assert (u['source_layer'],p['source_position']['source_layer'])==expected
 assert (u['first_line'],u['last_line'])==(p['source_position']['first_line'],p['source_position']['last_line'])
 assert not any(k in layer for layer in (ch,ch['source'],projection,u,p['source_position'])for k in ('annotator','attached_note_to_paragraph_id'))
 ms={m['id']:m for m in p['mentions']};roles={k:ms[mid]for k,mid in b['roles'].items()}
 assert all(m['kind']=='person'and t[m['start']:m['end']]==m['surface']for m in roles.values())
 return p,roles,a

def kinship_valid(a,paragraphs,chapters,root):
 try:
  q=a['qualifiers'];b=q['literal_source_binding'];e,=a['evidence'];p,r,c=bound(e,b,paragraphs,chapters,root);t=p['text'];start,end=c['start'],c['end'];rule=b['rule'];s=next(m for m in p['mentions']if m['id']==e['subject_person_mention_id']);o=next(m for m in p['mentions']if m['id']==e['object_person_mention_id'])
  if b['kind']!='position_bound_family_clause'or a['status']!='source_attested'or a.get('human_reviewed')is not False or s['person_id']!=a['subject_person_id']or o['person_id']!=a['object_person_id']or s['person_id']==o['person_id']:return False
  def w(k):return r[k]['surface']
  def literal(parts):
   pos=start;v=''
   for k,word in parts:
    word=w(k)if k else word
    if k and r[k]['start']!=pos:return False
    v+=word;pos+=len(word)
   return v==c['surface']and pos==end
  allowed={'source_term','lineage','literal_source_binding'}
  if q.get('lineage')!='paternal':return False
  child=None;parent=None;pred='father';term=None
  if rule=='head_named_father':
   if set(r)!={'child','style','parent'}or start!=0 or r['child']['start']!=0 or r['style']['person_id']!=r['child']['person_id']or r['parent']['end']!=end:return False
   middle=t[r['child']['end']:r['parent']['start']]
   if not re.fullmatch('字'+re.escape(w('style'))+r'[^曰云言「」『』非未不無]{1,16}人也父',middle)or r['style']['start']!=r['child']['end']+1:return False
   child='child';parent='parent';term='父'+w(parent)
  elif rule in('named_sons','parent_and_sons'):
   children=sorted(k for k in r if re.fullmatch('child_[1-9][0-9]*',k));children.sort(key=lambda k:int(k.split('_')[1]))
   if set(r)!={'parent',*children}or not children or children!=['child_'+str(i+1)for i in range(len(children))]:return False
   if not literal([('parent',''),(None,'及子'if rule=='parent_and_sons'else'子')]+[(k,'')for k in children]):return False
   child=next((k for k in children if r[k]['id']==s['id']),None);parent='parent';term=('及子'if rule=='parent_and_sons'else'子')+''.join(w(k)for k in children)
  elif rule=='parent_count_named_youngest':
   if set(r)!={'parent','child'}:return False
   m=re.fullmatch(re.escape(w('parent'))+r'有([一二三四五六七八九十百]+)子'+re.escape(w('child'))+'最小',c['surface'])
   if not m or not literal([('parent',''),(None,'有'+m[1]+'子'),('child',''),(None,'最小')]):return False
   child='child';parent='parent';term='最小';allowed.add('birth_order')
   if q.get('birth_order')!={'parent_person_id':r['parent']['person_id'],'scope':'sons_of_parent','ordinal':None,'position':'youngest','source_term':'最小','interpretation_status':'source_attested'}:return False
  elif rule=='grandson_before_resumed_sons':
   children=['child_1','child_2']
   if set(r)!={'grandchild','grandparent',*children}or not literal([(None,'孫'),('grandchild',''),(None,'嗣'),('grandparent',''),(None,'子')]+[(k,'')for k in children]):return False
   child='grandchild';parent='grandparent';pred='grandfather';term='孫'+w(child);allowed|={'generation_distance','parent_person_id','intermediate_person_ids'}
   if q.get('generation_distance')!=2 or q.get('parent_person_id','missing')is not None or q.get('intermediate_person_ids')!=[None]:return False
  elif rule=='named_great_grandson':
   if set(r)!={'descendant','ancestor'}or not literal([('descendant',''),('ancestor',''),(None,'之曾孫')]):return False
   child='descendant';parent='ancestor';pred='great_grandfather';term='曾孫';allowed|={'generation_distance','parent_person_id','intermediate_person_ids'}
   if q.get('generation_distance')!=3 or q.get('parent_person_id','missing')is not None or q.get('intermediate_person_ids')!=[None,None]:return False
  else:return False
  return child is not None and a['predicate']==pred and s['id']==r[child]['id']and o['id']==r[parent]['id']and q['source_term']==term and set(q)==allowed
 except(KeyError,ValueError,TypeError,StopIteration,AssertionError,OSError,IndexError):return False

def count_valid(report,paragraphs,chapters,root,parse):
 if 'received_unit_family_binding' in report:
  try:from scripts.received_unit_kinship import count_valid as unit_count_valid
  except ImportError:from received_unit_kinship import count_valid as unit_count_valid
  return unit_count_valid(report,paragraphs,chapters,root)
 if 'received_unit_count_binding' in report:
  try:from scripts.fixed_wikisource_units import unit_son_count_valid
  except ImportError:from fixed_wikisource_units import unit_son_count_valid
  return unit_son_count_valid(report,chapters.get(report.get('evidence',[{}])[0].get('chapter_id'),{}),root,parse)
 try:
  e,=report['evidence'];b=report['literal_source_binding'];p,r,c=bound(e,b,paragraphs,chapters,root);a=report['count_anchor'];n=report['source_number'];parent=r['parent'];member=r['named_child'];t=p['text']
  return (b['kind']=='position_bound_parent_sons_count'and b['rule']=='parent_has_sons_then_named_youngest'and set(r)=={'parent','named_child'}and anchor(p,a)
   and c['surface']==parent['surface']+'有'+n+'子'+member['surface']+'最小'and parent['start']==c['start']and member['start']==a['end']
   and a['surface']=='有'+n+'子'and a['start']==parent['end']and a['end']<c['end']
   and report['parent_person_id']==parent['person_id']and report['count_scope']=='sons_of_parent'and report['source_term']==a['surface']
   and type(report['reported_count'])is int and report['reported_count']>0 and parse(n)==report['reported_count']
   and report['named_member_person_ids']==[member['person_id']]and report['complete_named_list']is False
   and report['status']=='source_attested'and report['human_reviewed']is False and e['person_mention_id']==parent['id'])
 except(KeyError,ValueError,TypeError,StopIteration,AssertionError,OSError,IndexError):return False

def death_valid(event,paragraphs,chapters,root):
 try:
  e,=event['evidence'];b=event['literal_source_binding'];p,r,c=bound(e,b,paragraphs,chapters,root);da=b['date_anchor'];ta=b['death_anchor'];t=p['text'];m=r['subject']
  if b['kind']!='position_bound_death_report'or event['event_type']!='death'or event['status']!='source_attested'or event['human_reviewed']is not False or m['person_id']!=event['person_id']or e['person_mention_id']!=m['id']or not anchor(p,da)or not anchor(p,ta)or da['surface']!=event['date_expression']or ta['surface']!=event['source_term']or ta['surface']not in('卒','薨')or da['end']!=ta['start']or ta['end']!=c['end']:return False
  ids={v['id']for v in r.values()}
  if any(x['kind']=='person'and c['start']<=x['start']<c['end']and x['id']not in ids for x in p['mentions']):return False
  if m['start']!=c['start']:return False
  rule=b['rule']
  if rule=='named_subject_date_death':
   if set(r)!={'subject'}or not m['end']<=da['start']or any(v in t[m['end']:da['start']]for v in ('曰','云','詔','謂','言','「','」','『','』')):return False
   return not any(v in t[max(da['start'],ta['start']-1):ta['start']]for v in ('未','不','非'))
  fields=b.get('fields',{})
  if not all(anchor(p,a)and c['start']<=a['start']<a['end']<=c['end']for a in fields.values()):return False
  def word(k):return r[k]['surface']
  if rule=='subject_confirmed_after_nominated_alternatives':
   if set(r)!={'subject','candidate_1','candidate_2','candidate_3'}or set(fields)!={'title_1','title_2','title_3','granted_title'}:return False
   prefix=re.escape(word('subject'))+r'綱紀後事加侍中[^曰云言「」『』]{1,10}疾病遜位遷為司空固推'
   pattern=prefix+''.join(re.escape(fields['title_'+str(i)]['surface']+word('candidate_'+str(i)))for i in (1,2,3))+r'詔使使者即授印綬進爵封'+re.escape(fields['granted_title']['surface'])+r'邑[一二三四五六七八九十百千萬]+[戶戸]'+re.escape(da['surface']+ta['surface'])
   return bool(re.fullmatch(pattern,c['surface']))and len({v['person_id']for v in r.values()})==4
  if rule=='subject_joins_patron_then_ruler_recalls':
   if set(r)!={'subject','patron','ruler'}or set(fields)!={'offered_office'}:return False
   literal=word('subject')+'歸'+word('patron')+word('ruler')+'之初累召為'+fields['offered_office']['surface']+'不得南赴'+da['surface']+ta['surface']
   return c['surface']==literal and len({v['person_id']for v in r.values()})==3
  return False
 except(KeyError,ValueError,TypeError,StopIteration,AssertionError,OSError,IndexError):return False
