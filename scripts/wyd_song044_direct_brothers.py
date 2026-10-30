"""Two source-explicit younger brothers; no shared parent or absolute ordinal."""
import json,hashlib
from pathlib import Path
CID='c-songshu-044-wyd1739-xiehui'
PATH='corpus/songshu/044-wyd1739.json'
KIND='wyd_song044_named_younger_brother'
SLOTS=(('jiao-hui','p003','m0325','m0319','㬭','晦','晦弟黃門侍郎㬭','45238af487c0fa018ffe2beb0995b83f895c0a83e9f9af32c16f73b8b9964d5b'),
       ('liudaoji-liucui','p014','m0013','m0005','道濟','劉粹','劉粹遣弟竟陵太守道濟','a1d00b86e703c8054254f7320781d728413871cff56bccb0ebd15492b4131d21'))
IDS=frozenset('a-song044-wyd-'+x[0]+'-brother'for x in SLOTS)

def records(root,chapter=None):
 try:from .wyd_song044_formal_roles import source_errors
 except ImportError:from wyd_song044_formal_roles import source_errors
 ch=chapter if chapter is not None else json.loads((Path(root)/PATH).read_bytes())
 if not isinstance(ch,dict)or ch.get('id')!=CID or source_errors(ch,root):raise ValueError('完整武英殿來源、現役角色或反向引用不符')
 ps={p['id'].split(':')[-1]:p for p in ch['paragraphs']};out=[]
 for slot,pkey,ymid,omid,ysurf,osurf,term,sha in SLOTS:
  p=ps[pkey]
  if hashlib.sha256(p['text'].encode()).hexdigest()!=sha:raise ValueError('完整段落指紋不符')
  def role(mid,surface):
   m,=[m for m in p['mentions']if m['id']==p['id']+':'+mid]
   if m.get('kind')!='person'or m['surface']!=surface or p['text'][m['start']:m['end']]!=surface:raise ValueError('雙端人物角色不符')
   return m
  young,old=role(ymid,ysurf),role(omid,osurf)
  if young['person_id']==old['person_id']or p['text'].count(term)!=1:raise ValueError('雙端自環或親屬原詞不唯一')
  i=p['text'].index(term)
  e={**{k:ch[k]for k in('work_id','book_id','source_id')},'chapter_id':CID,'paragraph_id':p['id'],'quote':p['text'],
     'relationship_anchor':{'paragraph_id':p['id'],'start':i,'end':i+len(term),'surface':term},
     'subject_person_mention_id':young['id'],'object_person_mention_id':old['id']}
  out.append({'id':'a-song044-wyd-'+slot+'-brother','subject_person_id':young['person_id'],'predicate':'brother','object_person_id':old['person_id'],'status':'source_attested',
   'qualifiers':{'source_term':term,'source_clause_binding':{'kind':KIND,'slot':slot,'paragraph_sha256':sha},
    'relative_birth_order':{'older_person_id':old['person_id'],'younger_person_id':young['person_id'],'operator':'lt','scope':'siblings','older_ordinal':None,'younger_ordinal':None}},
   'evidence':[e],'interpretation_note':'原文明稱弟，僅記兩人弟兄與相對年序；不填絕對排行、共同父母或婚配，不改家族組裝。',
   'reviewer':'Codex（AI代理）','human_reviewed':False,'model':None})
 return out

def applies(a):
 if not isinstance(a,dict):return False
 if a.get('id')in IDS:return True
 q=a.get('qualifiers');b=q.get('source_clause_binding')if isinstance(q,dict)else None
 return isinstance(b,dict)and b.get('kind')==KIND

def valid(a,paragraphs,chapters,root):
 try:
  if not isinstance(a,dict)or not isinstance(paragraphs,dict)or not isinstance(chapters,dict):return False
  ch=chapters[CID];expected=next(x for x in records(root,ch)if x['id']==a.get('id'))
  p=next(p for p in ch['paragraphs']if p['id']==expected['evidence'][0]['paragraph_id'])
  return a==expected and paragraphs.get(p['id'])==(CID,p)
 except(KeyError,TypeError,ValueError,StopIteration,AttributeError,OSError):return False
