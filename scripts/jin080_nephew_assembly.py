"""Source-bound grandfather assembly from an explicit uncle and that uncle's father.
No father person is created; ritual succession is never biological parentage.
"""
from pathlib import Path
import json
TYPE='fixed_jin080_paternal_nephew_to_uncle_father'
CID='c-jinshu-080-wangxizhi-comparison'
AID='family-jin080-wangkuang-near-family'
def member(root,ch,roles):
 facts=json.loads((Path(root)/'corpus/jinshu/080-wangxizhi-comparison-assertions.json').read_bytes())['assertions'];by={a['id']:a for a in facts};u=by['a-jin080-jingzhi-uncle-xianzhi'];f=by['a-jin080-xianzhi-father-xizhi']
 refs=[]
 for a in[u,f]:
  for e in a['evidence']:refs.append(dict(e,assertion_id=a['id'],scope='明叔侄及叔父明父；祖父屬可撤回編輯推導、未識父名',url=ch['source']['permalink']))
 return {'person_id':roles['jingzhi'],'representative_source_person_id':roles['jingzhi'],'source_person_ids':[roles['jingzhi']],'identity_equivalence_decision_ids':[],'parent_person_id':None,'source_assertion_id':None,'ancestor_person_id':roles['xz'],'connection':'grandfather','generation_distance':2,'intermediate_person_ids':[None],'interpretation_note':'靜之為獻之兄之子；獻之明父羲之，故以父系叔侄暫接祖父羲之。父為哪位兄長未載，不造父、不把承嗣當生父。','ancestor_connection':{'type':TYPE,'nephew_assertion_id':u['id'],'uncle_father_assertion_id':f['id'],'status':'contextual_provisional','human_reviewed':False,'references':refs,'rationale':'只由固定完整080明兄子與叔父明父兩項；原source assertions不改成直述祖孫。'}}
def ancestor_valid(row,rows,assertions,chapters,root):
 if not isinstance(row,dict)or not isinstance(rows,dict)or not isinstance(assertions,dict)or not isinstance(chapters,dict):return False
 try:
  try:from scripts.fixed_jin080_wangxizhi_comparison import validate_source,same
  except ModuleNotFoundError as error:
   if error.name != 'scripts':raise
   from fixed_jin080_wangxizhi_comparison import validate_source,same
  ch=chapters[CID];roles=validate_source(ch,root)
  if not same(row,member(root,ch,roles)):return False
  for role in['xz','xianzhi']:
   if rows.get(roles[role],{}).get('source_person_ids')!=[roles[role]]:return False
  facts=json.loads((Path(root)/'corpus/jinshu/080-wangxizhi-comparison-assertions.json').read_bytes())['assertions'];by={a['id']:a for a in facts};u=by['a-jin080-jingzhi-uncle-xianzhi'];f=by['a-jin080-xianzhi-father-xizhi']
  if not same(assertions.get(u['id']),u)or not same(assertions.get(f['id']),f):return False
  for a in assertions.values():
   if a.get('subject_person_id')!=roles['jingzhi']:continue
   if a.get('predicate')in('father','adoptive_father'):return False
   if a.get('predicate')in('grandfather','ancestor')and a.get('object_person_id')!=roles['xz']:return False
  return u['predicate']=='paternal_uncle'and u['subject_person_id']==roles['jingzhi']and u['object_person_id']==roles['xianzhi']and f['predicate']=='father'and f['subject_person_id']==roles['xianzhi']and f['object_person_id']==roles['xz']
 except (KeyError,ValueError,TypeError,OSError,StopIteration,AttributeError):return False
