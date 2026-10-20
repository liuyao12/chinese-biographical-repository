"""限定傳文母稱與話語回指的從弟；不推生母或精確親等。"""
def parts(a,paragraphs):
 e,=a['evidence'];cid,p=paragraphs[e['paragraph_id']];t=p['text'];q=a['qualifiers'];b=q['source_clause_binding'];ms={m['id']:m for m in p['mentions']};s=ms[e['subject_person_mention_id']];o=ms[e['object_person_mention_id']]
 if e['chapter_id']!=cid or e['quote']!=t or a['status']!='source_attested' or a['human_reviewed']is not False:raise ValueError('unbound quote')
 for m,k in [(s,'subject_person_id'),(o,'object_person_id')]:
  if m['kind']!='person' or m['person_id']!=a[k] or t[m['start']:m['end']]!=m['surface']:raise ValueError('endpoint')
 if s['person_id']==o['person_id'] or set(b)!={'kind','start','end'} or type(b['start'])is not int or type(b['end'])is not int or not 0<=b['start']<b['end']<=len(t)or t[b['start']:b['end']]!=q['source_term']:raise ValueError('term')
 return t,q,b,ms,s,o

def mother_valid(a,paragraphs):
 try:
  t,q,b,ms,s,o=parts(a,paragraphs)
  if a['predicate']!='maternal_role' or set(q)!={'source_term','role','biological_mother','father_person_id','source_clause_binding'}or q['role']!='mother_unspecified'or q['biological_mother']is not None or q['father_person_id']is not None:return False
  if b['kind']=='biography_head_mother_following_named_father':
   return s['start']==0 and t[s['end']:].startswith('，字') and '之孽子也。其母' in t[s['end']:o['start']] and t[o['start']-2:o['start']]=='其母'and b['start']==o['start']-2 and b['end']==o['end'] and not any(z in t[:o['start']]for z in '曰云「『不未非')
  if b['kind']=='opening_mother_death_child_burial_resumption':
   return b['start']==0 and b['end']==o['end']+1 and t[:o['start']]=='母'and t[o['end']:].startswith('卒，上疏解職，欲送葬')and t[s['end']:].startswith('葬畢視事')and s['start']>o['end']and not any(z in t[o['end']:s['start']].replace('諡曰敬','')for z in '曰云「『')
  if b['kind']=='named_child_mother_in_title_formula':
   return b['start']==s['start'] and b['end']==o['end'] and t[s['end']:o['start']]=='母'and t[s['start']-1:s['start']]=='崇'and t[o['end']:].startswith('為宣城太妃')
  return False
 except(KeyError,TypeError,ValueError,StopIteration):return False

def cousin_valid(a,paragraphs):
 try:
  t,q,b,ms,s,o=parts(a,paragraphs);k=q['kinship_structure'];order=q['relative_birth_order']
  if a['predicate']!='agnatic_cousin'or set(q)!={'source_term','source_clause_binding','kinship_structure','relative_birth_order'}or k!={'lineage':'paternal','generation_difference':0,'collateral':True,'distance':None,'common_ancestor_person_id':None,'subject_relative_age':'older'}or type(k['generation_difference'])is not int:return False
  if order!={'operator':'lt','scope':'agnatic_cousins','older_person_id':s['person_id'],'younger_person_id':o['person_id'],'older_ordinal':None,'younger_ordinal':None}:return False
  if b['kind']=='speaker_self_report_congdi':
   return t[s['end']:o['start']]=='曰：「臣門著恩荊楚，從弟'and b['start']==s['start']and b['end']==o['end']and t[o['end']:].startswith('末雖篡位')
  if b['kind']=='biography_head_an_reports_to_its_congdi':
   return s['start']==0 and t[s['end']:].startswith('，幼有令名')and q['source_term']=='其從弟'+o['surface']and b['start']==o['start']-3 and b['end']==o['end']and t[b['start']-3:b['start']]=='安以語'and t[o['end']:].startswith('，'+o['surface']+'以問之，'+s['surface']+'曰：')and '謝安嘗訪以世務，默然不答，安甚怪之。他日，'==t[b['start']-len('謝安嘗訪以世務，默然不答，安甚怪之。他日，安以語'):b['start']-3]
  return False
 except(KeyError,TypeError,ValueError,StopIteration):return False
