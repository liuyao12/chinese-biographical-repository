"""Finite WYD063 role layer. Source-only validation remains a separate strict gate."""
import copy,hashlib,json
from pathlib import Path
CID='c-songshu-063-wyd1739-wangtanshou'
PATH='corpus/songshu/063-wyd1739-wangtanshou.json'
CONTRACT='source-evidence/song063-wyd1739-wangtanshou/ner-role-contract.json'
CONTRACT_SHA='e9be0651e883361b79dd82a01498327aeec76a7c9d7c1e6e7c3e7fe393d7946c'
KEY='fixed_ner_role_layer'
LAYER={'kind':'wuyingdian_song063_complete_selected_roles','status':'ai_provisional','human_reviewed':False,'coverage':'complete_selected_text_named_roles_first_pass_with_explicit_unresolved'}
def need(ok,message):
 if not ok:raise ValueError('宋063人物層：'+message)
def load_contract(root):
 root=Path(root).resolve();p=(root/CONTRACT).resolve();need(p.is_relative_to(root/'source-evidence'),'契約路徑越界');raw=p.read_bytes();need(hashlib.sha256(raw).hexdigest()==CONTRACT_SHA,'契約SHA');return json.loads(raw)
def reverse(person,ch,p,m):
 if not isinstance(person,dict)or not isinstance(person.get('aliases'),list)or not isinstance(person.get('evidence'),list):return False
 return any(a.get('surface')==m['surface']and isinstance(a.get('mention_ids'),list)and m['id']in a['mention_ids']for a in person.get('aliases',[])if isinstance(a,dict))and any(all(e.get(k)==v for k,v in {'work_id':ch['work_id'],'book_id':ch['book_id'],'source_id':ch['source_id'],'chapter_id':ch['id'],'paragraph_id':p['id'],'mention_id':m['id'],'quote':m['surface']}.items())for e in person.get('evidence',[])if isinstance(e,dict))
def foreign_role(root,seed,people):
 root=Path(root).resolve();p=(root/seed['path']).resolve();need(p.is_relative_to(root/'corpus'),'seed越界');ch=json.loads(p.read_bytes());need(all(ch.get(k)==seed[k]for k in('chapter_id','source_id','work_id','book_id')if k!='chapter_id')and ch.get('id')==seed['chapter_id'],'seed來源維度');need(hashlib.sha256(json.dumps(ch['source'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()==seed['source_sha256'],'seed來源SHA');ps=[p for p in ch['paragraphs']if p['id']==seed['paragraph_id']];need(len(ps)==1,'seed段唯一');p=ps[0];need(hashlib.sha256(p['text'].encode()).hexdigest()==seed['paragraph_sha256'],'seed全段SHA');ms=[m for m in p['mentions']if m['id']==seed['mention_id']];need(len(ms)==1,'seedMID唯一');m=ms[0];need(m.get('kind')=='person'and all(m.get(k)==seed[k]for k in('start','end','surface'))and p['text'][m['start']:m['end']]==m['surface'],'seed角色');pid=m.get('person_id');need(pid in people and reverse(people[pid],ch,p,m),'seed反向');return pid
def resolve_roles(ch,root,contract=None,return_people=False):
 need(isinstance(ch,dict),'章須物件');c=contract or load_contract(root);reg=json.loads((Path(root)/'registry/persons.json').read_bytes());people={p['id']:p for p in reg['persons']};need(len(people)==len(reg['persons']),'registry重複');out={r:foreign_role(root,s,people)for r,s in c['foreign_seeds'].items()}
 ps={p['id']:p for p in ch['paragraphs']}
 for spec in c['paragraphs']:
  p=ps[spec['id']];need(hashlib.sha256(p['text'].encode()).hexdigest()==spec['paragraph_sha256'],'本源全段SHA');actual={m['id']:m for m in p['mentions']};need(len(actual)==len(p['mentions']),'重複MID')
  for expected in spec['mentions']:
   role=expected.get('role_key')
   if role is None:continue
   m=actual.get(expected['id']);need(isinstance(m,dict)and m.get('kind')=='person','角色須人物');pid=m.get('person_id');need(pid in people and reverse(people[pid],ch,p,m),'本源反向缺失')
   if role in out:need(out[role]==pid,'本源/跨源角色或單端改號不一致')
   else:out[role]=pid
 need(len(out)==len(set(out.values())),'不同來源角色不可無判讀合併');return (out,people)if return_people else out

def source_only_projection(ch,root):
 need(isinstance(ch,dict),'章須物件');c=load_contract(root);need(ch.get('id')==CID,'章ID');a=ch.get('annotation');need(isinstance(a,dict)and isinstance(a.get(KEY),dict)and a.get(KEY)==LAYER and a[KEY].get('human_reviewed')is False,'人物層資格');base=copy.deepcopy(a);base.pop(KEY);expected_annotation={**c['base_annotation'],**c['ner_annotation_overrides']};need(base==expected_annotation,'其他annotation不可漂移');roles,people=resolve_roles(ch,root,c,return_people=True);need(len(ch['paragraphs'])==len(c['paragraphs']),'段數');out=copy.deepcopy(ch)
 for p,s in zip(ch['paragraphs'],c['paragraphs']):
  need(p['id']==s['id']and p.get('annotation_status')=='named_mentions_first_pass','段界或進度');expected=[]
  for e in s['mentions']:
   m=copy.deepcopy(e);r=m.pop('role_key',None)
   if r is not None:m['person_id']=roles[r]
   expected.append(m)
  need(p.get('mentions')==expected,'固定MID/字位/角色/未定漂移')
 need(ch.get('cross_chapter_references')==c['cross_chapter_references'],'明互見記錄漂移')
 for role,seed in c['xref_role_seeds'].items():need(foreign_role(root,seed,people)==roles[role],'互見目標同人/明父橋不符')
 out['annotation']=copy.deepcopy(c['base_annotation'])
 for p in out['paragraphs']:p['mentions']=[];p['annotation_status']='pending'
 return out
