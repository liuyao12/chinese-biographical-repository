"""Explicit name readings in one fixed WYD witness, resolved through current MIDs.
Only these recorded readings are compiled. No surname is guessed from an ID,
registry label, spouse, or a global first-character rule.
"""
from pathlib import Path
import hashlib,json
CID='c-songshu-044-wyd1739-xiehui'
BINDING='fixed_wyd_song044_name_component'
KIND='contextual_surname_from_wyd_song044_kinship'
# role: surname, ming, source form, full-name seed role, supporting assertions.
SPECS={
 'hui':('謝','晦','full_name',None,()),
 'lang':('謝','朗','contextual_surname','hui',('hui-grandfather',)),
 'chong':('謝','重','contextual_surname','hui',('hui-father',)),
 'xuan-brother':('謝','絢','contextual_surname','hui',('xuan-brother',)),
 'shixiu':('謝','世休','contextual_surname','hui',('shixiu-father',)),
 'shiji':('謝','世基','contextual_surname','hui',('xuan-brother','shiji-father')),
 'shao':('謝','紹','contextual_surname','hui',('shao-uncle',)),
 'xiedun':('謝','遯','full_name',None,()),
 'shiyou':('謝','世猷','full_name',None,()),
 'shangxuanshi':('商','玄石','full_name',None,()),
 'huaifu':('商','懷福','contextual_surname','shangxuanshi',('huaifu-father',)),
 'wife-cao':('曹',None,'wife_clan',None,('wife-cao',)),
 'zongshuxian':(None,'獻','ming_unknown_clan',None,()),
}
try:
 from scripts.validation_context import memoized
except ImportError:
 from validation_context import memoized

@memoized(0)
def _context(root):
 try:
  from .wyd_song044_nephew import _context as source_context
  from .wyd_song044_formal_roles import source_errors
  from .wyd_song044_kinship import assertions
 except ImportError:
  from wyd_song044_nephew import _context as source_context
  from wyd_song044_formal_roles import source_errors
  from wyd_song044_kinship import assertions
 ch,contract,roles=source_context(root)
 if source_errors(ch,root):raise ValueError('姓名須依完整固定原文與雙向人物錨')
 actual=json.loads((Path(root)/'corpus/songshu/044-wyd1739-assertions.json').read_text())
 byid={a['id']:a for a in actual['assertions']}
 for a in assertions(ch,roles)['assertions']:
  if byid.get(a['id'])!=a:raise ValueError('姓名推定所依親屬原詞／方向／資格已變')
 return ch,roles,byid

@memoized(0)
def records(root):
 ch,roles,facts=_context(root);result=[]
 for role,(surname,ming,form,seed,proof)in SPECS.items():
  hits=[(p,m)for p in ch['paragraphs']for m in p['mentions']if m.get('source_role_key')==role]
  if form=='full_name':p,m=next((p,m)for p,m in hits if m['surface']==surname+ming)
  else:p,m=hits[0]
  if form=='contextual_surname' and m['surface']!=ming:raise ValueError('本名錨不符，不能以組裝ID補姓')
  if form=='wife_clan' and p['text'][m['start']-1:m['end']]!='妻曹':raise ValueError('曹氏須有妻曹原詞')
  if form=='ming_unknown_clan' and (m['surface']!='獻' or p['text'][m['start']-2:m['start']]!='宗叔'):raise ValueError('宗叔不是姓名，姓氏未知')
  binding={'kind':BINDING,'source_role_key':role,'name_form':form,'source_revision':ch['source']['revision_id'],'raw_sha256':ch['source']['raw_sha256'],'paragraph_sha256':hashlib.sha256(p['text'].encode()).hexdigest()}
  n={'id':'name-song044-wyd-'+role,'person_id':roles[role],'surname':surname,'ming':ming,'additional_names':[],'chapter_id':CID,'paragraph_id':p['id'],'person_mention_id':m['id'],'quote':p['text'],'status':'contextual_provisional','human_reviewed':False,'model':None,'component_source_binding':binding}
  if form=='contextual_surname':
   n['surname_basis']={'kind':KIND,'source_name_record_id':'name-song044-wyd-'+seed,'relationship_assertion_ids':['a-song044-wyd-'+x for x in proof],'status':'contextual_provisional','human_reviewed':False,'rationale':'本源傳首全名或明示全名及所列明父子／祖／兄弟／父系兄子語境的氏姓判讀；不新增父親、不從家族ID或配偶推姓。'}
  if role=='hui':
   assert p['text'][m['end']:m['end']+3]=='字宣明'
   n['zi']='宣明';binding['courtesy_anchor']={'paragraph_id':p['id'],'start':m['end']+1,'end':m['end']+3,'surface':'宣明'}
  if form=='wife_clan':
   n['clan_style']={'kind':'bound_wyd_wife_clan_appellation','value':'曹氏','source_term':'妻曹','assertion_ids':['a-song044-wyd-wife-cao'],'status':'editorial_provisional','rationale':'原文妻曹按此時代婦女氏稱記曹氏；本名未載，不由丈夫姓或子女生母推得。','human_reviewed':False}
  if form=='ming_unknown_clan':n['note']='獻是名；宗叔所屬及氏姓未明，不補王姓、謝姓或虛構宗姓。'
  result.append(n)
 return result

def component_valid(n,ch,root):
 try:
  if not isinstance(n,dict)or ch.get('id')!=CID or not isinstance(n.get('component_source_binding'),dict):return False
  if n['component_source_binding'].get('kind')!=BINDING:return False
  expected=records(root);row,=[r for r in expected if r['id']==n.get('id')]
  current=json.loads((Path(root)/'corpus/songshu/044-wyd1739.json').read_text())
  return ch==current and n==row
 except(KeyError,TypeError,ValueError,OSError,StopIteration,AttributeError):return False

def validate_surname(n,names,chapters,assertions,root):
 try:
  assert component_valid(n,chapters[n['chapter_id']],root)
  b=n['surname_basis'];assert b['kind']==KIND
  expected={r['id']:r for r in records(root)};seed,=[r for r in names if r.get('id')==b['source_name_record_id']]
  assert seed==expected[seed['id']] and seed['component_source_binding']['name_form']=='full_name' and seed['surname']==n['surname']
  _,_,facts=_context(root);aa={a['id']:a for a in assertions if 'id' in a}
  for aid in b['relationship_assertion_ids']:
   assert aa.get(aid)==facts[aid]
   q=facts[aid]['qualifiers'];assert not any(q.get(k)for k in('adoptive','sworn','same_mother_only'))and q.get('shared_father')is not False and q.get('lineage')not in('maternal','non_paternal')
 except(AssertionError,KeyError,TypeError,ValueError,OSError,StopIteration,AttributeError):raise ValueError('武英殿宋044氏姓須有原名種子、固定本源及具名近系原詞，不借父系組裝或婚配補姓')

def clan_valid(n,p,relations):
 try:
  st=n['clan_style'];binding=n['component_source_binding'];assert binding['kind']==BINDING and binding['source_role_key']=='wife-cao' and binding['name_form']=='wife_clan'
  assert n['chapter_id']==CID and n['surname']=='曹' and n['ming']is None and st['value']=='曹氏' and st['kind']=='bound_wyd_wife_clan_appellation' and st['status']=='editorial_provisional'and st['human_reviewed']is False
  m,=[m for m in p['mentions']if m['id']==n['person_mention_id']];assert m['kind']=='person' and m['person_id']==n['person_id'] and m['source_role_key']=='wife-cao'and m['surface']=='曹'and p['text'][m['start']-1:m['end']]=='妻曹'
  a,=[a for a in relations if a['id']=='a-song044-wyd-wife-cao'];assert st['assertion_ids']==[a['id']]and a['predicate']=='spouse'and a['object_person_id']==n['person_id']and a['subject_person_id']!=n['person_id']and a['qualifiers']['source_term']=='妻曹'
  e,=a['evidence'];assert e['paragraph_id']==p['id']==n['paragraph_id']and e['quote']==n['quote']==p['text']and e['object_person_mention_id']==m['id'];return True
 except(AssertionError,KeyError,TypeError,ValueError,StopIteration,AttributeError):return False
