# coding: utf-8
"""Reviewed complete received narrative grammars; no person/chapter ID allowlist.
Templates and role constraints are code-reviewed grammar, never record-supplied regex.
Source parentage, maternal appellations, care, divorce and ritual heirship stay distinct.
"""
from pathlib import Path
import json,re,hashlib
FRAMES=json.loads(Path(__file__).with_name('received_unit_kinship_frames.json').read_text())
RULE='complete_received_kinship_unit'
def unit(b,paragraphs,chapters=None,root=None):
 assert set(b)=={'kind','rule','frame','paragraphs','human_reviewed','slot'}and b['kind']=='biography_family_clause'and b['rule']==RULE and b['human_reviewed']is False
 spec=FRAMES[b['frame']];assert set(b['paragraphs'])==set(spec['paragraphs']);rs={};selected={};cid=None
 for key,template in spec['paragraphs'].items():
  v=b['paragraphs'][key];assert set(v)=={'paragraph_id','paragraph_sha256','roles'};pc,p=paragraphs[v['paragraph_id']];cid=pc if cid is None else cid;assert pc==cid
  assert p['text_layer']=='received_chapter'and hashlib.sha256(p['text'].encode()).hexdigest()==v['paragraph_sha256'];ms={m['id']:m for m in p['mentions']};cursor=0;used=set()
  for part in re.split(r'(<p[0-9]+r[0-9]+>)',template):
   if re.fullmatch(r'<p[0-9]+r[0-9]+>',part):
    k=part[1:-1];m=ms[v['roles'][k]];assert m['kind']=='person'and m.get('person_id')and m['start']==cursor and p['text'][m['start']:m['end']]==m['surface'];rs[k]=m;used.add(k);cursor=m['end']
   else:assert p['text'].startswith(part,cursor);cursor+=len(part)
  assert cursor==len(p['text'])and set(v['roles'])==used and set(v['roles'].values())=={m['id']for m in p['mentions']if m['kind']=='person'};selected[key]=p
 assert len({v['paragraph_id']for v in b['paragraphs'].values()})==len(selected)
 for group in spec['same_identity_roles']:assert len({rs[k]['person_id']for k in group})==1
 for x,y in spec['distinct_identity_roles']:assert rs[x]['person_id']!=rs[y]['person_id']
 if chapters is not None:
  ch=chapters[cid];assert [p['id']for p in ch['paragraphs']]==[v['paragraph_id']for v in b['paragraphs'].values()]
  if root is not None:
   try:from scripts.fixed_wikisource_units import source_errors
   except ImportError:from fixed_wikisource_units import source_errors
   assert not source_errors(ch,root)
 return cid,selected,rs,spec

def qualifiers(slot,rs,b):
 q={'source_term':slot['source_term'],'source_clause_binding':b};pred=slot['predicate'];s=rs[slot['subject_role']];o=rs[slot['object_role']]
 if pred=='father':q['lineage']='paternal'
 elif pred=='grandfather':q.update(lineage='paternal',generation_distance=2)
 elif pred=='maternal_role':q.update(role='mother_unspecified',biological_mother=None,father_person_id=None)
 elif pred=='brother':q['relative_birth_order']={'older_person_id':s['person_id'],'younger_person_id':o['person_id'],'operator':'lt','scope':'siblings','older_ordinal':None,'younger_ordinal':None}
 elif pred=='agnatic_senior_kin':q['kinship_structure']={'lineage':'paternal','generation_difference':-1,'collateral':True,'distance':None,'common_ancestor_person_id':None,'subject_relative_age':'unknown'}
 elif pred=='paternal_uncle':
  father=rs[slot['known_father_role']]['person_id']if slot.get('known_father_role')else None
  assert slot['source_term']in('亡叔','兄子')
  q.update(lineage='paternal',generation_difference=-1,father_person_id=father,parent_generation_relative_birth_order={'older_person_id':father,'younger_person_id':o['person_id'],'older_role':'father_of_subject','younger_role':'paternal_uncle_of_subject','operator':'lt','scope':'father_and_paternal_uncle','older_ordinal':None,'younger_ordinal':None,'source_term':slot['source_term']})
 elif pred=='ritual_successor_of':q.update(succession_kind='ritual_heir_designation',legal_adoption_status='not_stated',parentage_inference='not_inferred',reported_heir_absence={'source_term':'無子','scope':'male_heir_in_succession_context','absence_of_all_children':False})
 elif pred=='raised_by':q.update(care_basis='explicit_rearing_recalled_in_oath',legal_adoption_status='not_stated',parentage_inference='not_inferred')
 if 'marriage_termination'in slot:q['marriage_termination']=slot['marriage_termination']
 return q

def evidence(ch,ps,slot,rs):
 s=rs[slot['subject_role']];o=rs[slot['object_role']];keys=[slot['object_paragraph_key']]
 if slot['subject_paragraph_key']not in keys:keys.append(slot['subject_paragraph_key'])
 if 'evidence_paragraph_keys'in slot:keys=slot['evidence_paragraph_keys']
 result=[]
 for k in keys:
  p=ps[k];e={x:ch[x]for x in('work_id','book_id','source_id')};e.update(chapter_id=ch['id'],paragraph_id=p['id'],quote=p['text'])
  if any(m['id']==s['id']for m in p['mentions']):e['subject_person_mention_id']=s['id']
  if any(m['id']==o['id']for m in p['mentions']):e['object_person_mention_id']=o['id']
  result.append(e)
 return result

def valid(a,paragraphs,chapters=None,root=None):
 try:
  b=a['qualifiers']['source_clause_binding'];cid,ps,rs,spec=unit(b,paragraphs,chapters,root);slot=spec['slots'][b['slot']];s=rs[slot['subject_role']];o=rs[slot['object_role']]
  assert a['status']=='source_attested'and a['human_reviewed']is False and a['predicate']==slot['predicate']and a['subject_person_id']==s['person_id']!=o['person_id']==a['object_person_id']
  assert a['qualifiers']==qualifiers(slot,rs,b)
  assert any(slot['source_term']in p['text']for p in ps.values())
  if chapters is None:
   e=a['evidence'][0];ch={'id':cid,**{k:e[k]for k in('work_id','book_id','source_id')}}
  else:ch=chapters[cid]
  assert a['evidence']==evidence(ch,ps,slot,rs)
  ids=[e['paragraph_id']for e in a['evidence']]
  if len(ids)>1:assert a['context']=={'kind':'received_biography_family_unit','paragraph_ids':ids}
  else:assert 'context'not in a
  return True
 except(AssertionError,KeyError,ValueError,TypeError,StopIteration,IndexError,OSError):return False

def count_valid(v,paragraphs,chapters,root,parse=None):
 try:
  b=v['received_unit_family_binding'];cid,ps,rs,spec=unit(b,paragraphs,chapters,root);assert b['slot']=='reported_sons';s=spec['count_slot'];parent=rs[s['parent_role']];p=ps[s['count_paragraph_key']];head=next(x for x in ps.values()if any(m['id']==parent['id']for m in x['mentions']));ch=chapters[cid]
  if parse is None:
   try:from scripts.chinese_civil_years import numeral
   except ImportError:from chinese_civil_years import numeral
  else:numeral=parse
  assert numeral(s['source_number'])==s['reported_count']and numeral(s['source_named_number'])==len(s['named_member_roles'])
  assert '有'+s['source_number']+'子'in s['source_term']and '知名者'+s['source_named_number']+'人'in s['source_term']
  assert v['parent_person_id']==parent['person_id']and v['reported_count']==s['reported_count'] and v['source_number']==s['source_number']and v['source_term']==s['source_term']in p['text']and v['status']=='source_attested'and v['human_reviewed']is False
  assert v['count_scope']=='sons_of_parent'and v['named_member_person_ids']==[rs[k]['person_id']for k in s['named_member_roles']]and v['complete_named_list']is False and v['enumerated_named_count']==len(s['named_member_roles']) and v['unidentified_count']==s['reported_count']-len(s['named_member_roles'])
  ev=[]
  for x in(head,p):ev.append(dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=cid,paragraph_id=x['id'],quote=x['text']))
  assert v['evidence']==ev
  return True
 except(AssertionError,KeyError,ValueError,TypeError,StopIteration,IndexError,OSError):return False
