"""One source-based identity join; retired ID is reserved, never resolved as alias."""
import hashlib,json
from pathlib import Path
OLD='047_850_e7d'
DID='d-sgz023-hui-explicit-xuncan-reference'
BASE='source-evidence/two-hui-identity/'
def need(ok,msg):
 if not ok:raise ValueError('裴徽同指：'+msg)
def encoded(x):return(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def read(root,rel):
 r=Path(root).resolve();p=r/rel;need(p.resolve()==p and p.is_file(),'實體檔案');return json.loads(p.read_bytes())
def digest(x):return hashlib.sha256(x).hexdigest()
def validate(root,ch=None):
 root=Path(root).resolve();review=read(root,BASE+'current-review.json');capture=(root/(BASE+'original-fields.json')).read_bytes();need(digest(capture)==review['original_fields_capture_sha256'],'前狀態完整欄位SHA');before=json.loads(capture);people={p['id']:p for p in read(root,'registry/persons.json')['persons']};need(OLD not in people,'舊號已撤除')
 ids=[]
 for spec in review['source_roles']:
  source=read(root,spec['path']);need(digest(encoded(source['source']))==spec['source_sha256'],'來源資格');p=next(p for p in source['paragraphs']if p['id']==spec['paragraph_id']);need(digest(p['text'].encode())==spec['paragraph_text_sha256'],'完整原段')
  m=next(m for m in p['mentions']if m['id']==spec['marker']['id']);need({k:v for k,v in m.items()if k!='person_id'}==spec['marker'],'固定MID與字位');ids.append(m['person_id']);actor=people.get(m['person_id'],{});need(any(a.get('surface')==m['surface']and m['id']in a.get('mention_ids',[])for a in actor.get('aliases',[]))and any(e.get('mention_id')==m['id']and e.get('quote')==m['surface']for e in actor.get('evidence',[])),'來源人物雙向')
 need(len(set(ids))==1 and ids[0]in people,'明示回指兩端須同人');pid=ids[0];need(review['current_person_id']==pid and review['historical_mapping']=={OLD:pid},'現役判讀端點');actor=people[pid]
 original_old,original_keep=before['person_records_before']
 need(actor['identity_review_history']==[{'capture_ref':BASE+'original-fields.json#/person_records_before/'+str(i),'role':'prior_source_qualified_editorial_state_not_current_negative','identity_note':p.get('identity_note'),'review':p.get('review'),'original_label':p.get('label'),'human_reviewed':False}for i,p in enumerate([original_old,original_keep])],'兩份註記/審閱資格保存')
 for original in [original_old,original_keep]:
  for key,value in original.items():
   if key not in ('id','label','aliases','evidence','identity_note'):need(actor.get(key)==value,'未知欄位或review保存')
  for e in original['evidence']:need(e in actor['evidence'],'證據聯集')
  for a in original['aliases']:need(any(all(b.get(k)==v for k,v in a.items()if k!='mention_ids')and set(a['mention_ids'])<=set(b['mention_ids'])for b in actor['aliases']),'別名與未知欄位聯集')
 need(not actor.get('id_aliases')and'先前' in actor['identity_note']and'明示' in actor['identity_note'],'現行資格說明/無redirect')
 source=read(root,'corpus/sanguozhi/023-peiqian-ws2376966.json');p=next(p for p in source['paragraphs']if p['id'].endswith(':p009'));need('潛少弟徽，字文季，冀州刺史' in p['text']and'事見荀粲、傅嘏、王弼、管輅諸傳' in p['text'],'原文明示回指，非現代連結')
 d=read(root,'corpus/sanguozhi/023-peiqian-ws2376966-identities.json');decision,=d['decisions'];need(decision['id']==DID and decision['person_id']==pid and decision['scope']=='cross_chapter'and decision['status']=='contextual_provisional'and decision['human_reviewed']is False,'可追溯身份判斷')
 receipt=read(root,BASE+'retirement-047.json');need(receipt=={'record_type':'editorial_annotation_rekey_receipt','identity_decision_id':DID,'retired_person_ids':[OLD],'retirement_policy':'audit_only_not_canonical_not_alias_not_reusable','person_aliases_created':False},'撤號資格')
 for rel in ['corpus/sanguozhi/023-peiqian-ws2376966.json','corpus/jinshu/035-pei-family.json']:
  chapter=read(root,rel);need(all(OLD not in c.get('candidate_person_ids',[])for c in chapter['annotation'].get('unresolved_identity_cases',[]))and any(c.get('person_id')==pid and c.get('identity_decision_id')==DID for c in chapter['annotation'].get('resolved_identity_reviews',[])),'先前未決已被補足')
 for row in read(root,BASE+'historical-reference-inventory.json')['records']:
  b=(root/row['path']).read_bytes();need(digest(b)==row['sha256'],'特定歷史捕獲SHA')
  for pointer in row['old_identity_value_json_pointers']:
   value=json.loads(b)
   for key in pointer.split('/')[1:]:value=value[int(key)]if isinstance(value,list)else value[key]
   need(value==OLD,'特定歷史槽')
 return pid
