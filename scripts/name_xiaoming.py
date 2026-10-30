# coding: utf-8
"""Typed 小名 at separately bound family or biographical name declarations."""
def biographical_xiaoming_valid(name, paragraph):
 """A complete opening name sequence; no inference from an untyped alias."""
 b=name.get('xiaoming_basis');t=paragraph.get('text','');ms={m['id']:m for m in paragraph.get('mentions',[])}
 names=['subject_anchor','ming_anchor','zi_anchor','xiaoming_anchor']
 markers=['ming_marker_anchor','zi_marker_anchor','xiaoming_marker_anchor']
 if not(isinstance(name.get('person_id'),str)and name['person_id']and isinstance(b,dict)and set(b)==set(names+markers+['clause_anchor','kind','status','human_reviewed','rationale'])
  and b.get('kind')=='explicit_biographical_name_sequence'and b.get('status')=='source_attested'
  and b.get('human_reviewed')is False and isinstance(b.get('rationale'),str)and b['rationale'].strip()):return False
 bound=[]
 for key in names+markers+['clause_anchor']:
  a=b[key];keys={'paragraph_id','start','end','surface'}|({'person_mention_id'}if key in names else set())
  if not(isinstance(a,dict)and set(a)==keys and a.get('paragraph_id')==name.get('paragraph_id')==paragraph.get('id')
   and type(a.get('start'))is int and type(a.get('end'))is int and 0<=a['start']<a['end']<=len(t)
   and t[a['start']:a['end']]==a.get('surface')):return False
  if key in names:
   m=ms.get(a['person_mention_id'])
   if not(m and m.get('kind')=='person'and m.get('person_id')==name.get('person_id')
    and all(m.get(k)==a[k]for k in ['start','end','surface'])):return False
   bound.append(m)
 subject,ming,zi,xiao=bound;mm,zm,xm=[b[k]for k in markers];cl=b['clause_anchor']
 return (len({m['id']for m in bound})==4 and subject['start']==cl['start']==0
  and subject['surface']not in('其','彼','我','君','公','父','子')
  and mm['surface']=='諱'and zm['surface']=='字'and xm['surface']=='小名'
  and subject['end']==mm['start']and mm['end']==ming['start']and ming['end']==zm['start']
  and zm['end']==zi['start']and zi['end']==xm['start']and xm['end']==xiao['start']and xiao['end']==cl['end']
  and name.get('ming')==ming['surface']and name.get('zi')==zi['surface']and name.get('xiaoming')==xiao['surface']
  and name.get('quote')==t)

def validate_xiaoming(name,paragraph=None):
 value=name.get('xiaoming');basis=name.get('xiaoming_basis')
 if value is None and basis is None:return
 def fail():raise ValueError('小名須有完整原段及小名原詞，依父子對舉或傳記諱字小名句保存同人四錨，不得冒作字／小字或取普通果名')
 if not(isinstance(value,str)and value and value==value.strip()and isinstance(paragraph,dict)and name.get('quote')==paragraph.get('text')and isinstance(basis,dict)):fail()
 if basis.get('kind')=='fixed_jin031_opening_ming_origin_xiaoming':
  try:from scripts.fixed_jin031_jia_comparison import xiaoming_valid as jia_xiaoming_valid
  except ImportError:from fixed_jin031_jia_comparison import xiaoming_valid as jia_xiaoming_valid
  if not jia_xiaoming_valid(name,paragraph):fail()
  return
 if basis.get('kind')=='explicit_biographical_name_sequence':
  if not biographical_xiaoming_valid(name,paragraph):fail()
  return
 anchors=['child_name_anchor','child_value_anchor','father_name_anchor','father_value_anchor','child_marker_anchor','father_marker_anchor','father_role_anchor','clause_anchor']
 if not(set(basis)==set(anchors)|{'kind','subject_role','status','human_reviewed','rationale'}and basis['kind']=='explicit_child_father_xiaoming'and basis['subject_role']in('child','father')and basis['status']=='source_attested'and basis['human_reviewed']is False and isinstance(basis['rationale'],str)and basis['rationale'].strip()):fail()
 t=paragraph['text'];ms={m['id']:m for m in paragraph.get('mentions',[])};bound=[]
 for i,key in enumerate(anchors):
  a=basis[key];keys={'paragraph_id','start','end','surface'}|({'person_mention_id'}if i<4 else set())
  if not(isinstance(a,dict)and set(a)==keys and a.get('paragraph_id')==name.get('paragraph_id')==paragraph.get('id')and type(a.get('start'))is int and type(a.get('end'))is int and 0<=a['start']<a['end']<=len(t)and t[a['start']:a['end']]==a.get('surface')):fail()
  if i<4:
   m=ms.get(a['person_mention_id'])
   if not(m and m.get('kind')=='person'and all(m.get(k)==a[k]for k in ['start','end','surface'])and m.get('person_id')):fail()
   bound.append(m)
 cn,cv,fn,fv=bound;cm,fm,fr,cl=[basis[k]for k in anchors[4:]]
 if not(cn['person_id']==cv['person_id'] and fn['person_id']==fv['person_id'] and cn['person_id']!=fn['person_id']
  and cn['surface']not in ('其','彼','我','父','子','弟','兄','君','公')and fn['surface']not in ('其','彼','我','父','子','弟','兄','君','公')
  and t[max(0,cn['start']-1):cn['start']]not in ('不','非','未')
  and len({m['id']for m in bound})==4 and cm['surface']==fm['surface']=='小名'and fr['surface']=='父'
  and cn['end']==cm['start']and cm['end']==cv['start']and cv['end']==fr['start']and fr['end']==fn['start']and fn['end']==fm['start']and fm['end']==fv['start']
  and cl['start']==cn['start']and cl['end']==fv['end']and cl['surface']==cn['surface']+'小名'+cv['surface']+'父'+fn['surface']+'小名'+fv['surface']):fail()
 selected=cv if basis['subject_role']=='child'else fv
 if name.get('person_id')!=selected['person_id']or value!=selected['surface']:fail()

def validate_records(root):
 """Native validation only of this new typed field; no generated exports required."""
 import json
 from pathlib import Path
 root=Path(root);errors=[]
 try:
  try:
   from scripts.person_bundle import load_catalog
  except ImportError:
   from person_bundle import load_catalog
  _,records=load_catalog(root);paragraphs={p['id']:p for c in records if c.get('record_type')=='marked_chapter'for p in c['paragraphs']}
  for r in records:
   if r.get('record_type')!='person_name_component_set':continue
   for n in r['records']:
    if 'xiaoming'in n or 'xiaoming_basis'in n:
     try:validate_xiaoming(n,paragraphs.get(n.get('paragraph_id')))
     except(ValueError,TypeError,KeyError)as e:errors.append('小名姓名組件無效：'+str(e))
 except(ValueError,TypeError,KeyError,OSError)as e:errors.append('小名來源載入失敗：'+str(e))
 return errors
