# coding: utf-8
"""Finite received-source relationship interpretations, separate from source assertions."""
from pathlib import Path
import argparse,hashlib,json,re
ROOT=Path(__file__).resolve().parents[1]
TYPE='person_relationship_interpretation_set'
SIDECAR='corpus/nanqishu/043-xieyue-relationship-interpretations.json'
PIN='scripts/fixed_received_parentage_interpretations.json'
PIN_SHA='807641c099fd723af788d98dc5cccab54cade8368d1207b82ba65080f80fffd5'
KIND='fixed_received_named_children_parentage'
def _strict(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys()and all(_strict(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(_strict(x,y)for x,y in zip(a,b))
 return a==b
def _file(root,rel):
 p=root/rel;assert p.resolve()==p and p.is_file()and not p.is_symlink();return p.read_bytes()
def _frame(chapter,root,people):
 assert isinstance(root,(str,Path))and isinstance(chapter,dict)and isinstance(people,(dict,set))
 root=Path(root).resolve();pb=_file(root,PIN);assert hashlib.sha256(pb).hexdigest()==PIN_SHA;pin=json.loads(pb)
 assert all(chapter.get(k)==v for k,v in pin['chapter_dimensions'].items())
 source=chapter.get('source');assert isinstance(source,dict)and type(source.get('revision_id'))is int and source['revision_id']==pin['revision_id']and source.get('permalink')==pin['permalink']and source.get('wikitext_sha256')==pin['raw_sha256']
 raw=_file(root,pin['raw_path']);assert hashlib.sha256(raw).hexdigest()==pin['raw_sha256'];lines=raw.decode().splitlines()
 units=chapter.get('paragraphs');assert isinstance(units,list)and len(units)==len(pin['paragraph_ids'])and all(isinstance(p,dict)and isinstance(p.get('text'),str)for p in units)
 assert [p.get('id')for p in units]==pin['paragraph_ids'];texts=[]
 for line,p in zip(pin['raw_lines'],units):
  text=lines[line-1];assert text.startswith('　　');text=text[2:];text=text.replace('{{!|𤅢|左「氵」右「𦿈」}}','𤅢');text=re.sub(r'{{YL\|([^{}|]+)}}',r'\1',text);assert '{{'not in text and '}}'not in text and text==p['text'];texts.append(text)
 assert hashlib.sha256('\n\n'.join(texts).encode()).hexdigest()==pin['unit_text_sha256']
 p=next(p for p in units if p['id']==pin['paragraph_id']);t=p['text'];assert hashlib.sha256(t.encode()).hexdigest()==pin['paragraph_sha256']and p.get('text_layer')=='received_chapter'
 sp=p.get('source_position');assert isinstance(sp,dict)and type(sp.get('revision_id'))is int and sp['revision_id']==pin['revision_id']and sp.get('first_line')==53 and sp.get('last_line')==53
 mentions=p.get('mentions');assert isinstance(mentions,list)and all(isinstance(m,dict)for m in mentions);by={m.get('id'):m for m in mentions};assert len(by)==len(mentions)
 roles={k:by[mid]for k,mid in pin['role_mentions'].items()}
 for m in roles.values():
  assert m.get('kind')=='person'and isinstance(m.get('person_id'),str)and m['person_id']in people and type(m.get('start'))is int and type(m.get('end'))is int and 0<=m['start']<m['end']<=len(t)and t[m['start']:m['end']]==m.get('surface')
 assert roles['head']['person_id']==roles['head_resumed']['person_id']and roles['father']['person_id']==roles['naming_father']['person_id']
 assert len({roles[k]['person_id']for k in ['head','grandfather','father','first_older_brother','second_older_brother','third_older_brother','fourth_older_brother']})==7
 for s in pin['scope_segments']:assert t[s['start']:s['end']]==s['literal']
 # Named roles retain exact source positions, not just a co-shifted supplied quote.
 expected_positions={'head':(0,2),'grandfather':(14,16),'father':(22,23),'head_resumed':(31,32),'first_older_brother':(34,35),'second_older_brother':(36,37),'third_older_brother':(38,39),'fourth_older_brother':(40,41),'naming_father':(44,46)}
 assert all((roles[k]['start'],roles[k]['end'])==span for k,span in expected_positions.items())
 return pin,p,roles
RATIONAL='傳首父莊直接指𤅢；結合同段四兄具名列表與謝莊名兒句，暫將所列顥／嵷接於莊。此為AI來源作用域判讀，不冒逐人明記父莊，不推同母或絕對排行。'
def expected(chapter,root,people):
 pin,p,roles=_frame(chapter,root,people);out=[]
 for slot in pin['slots']:
  child=roles[slot['subject_role']];father=roles['naming_father'];e={k:chapter[k]for k in ['work_id','book_id','source_id']};e.update(chapter_id=chapter['id'],paragraph_id=p['id'],quote=p['text'],subject_person_mention_id=child['id'],object_person_mention_id=father['id'],role_mentions=pin['role_mentions'])
  out.append(dict(id=slot['id'],predicate='father',subject_person_id=child['person_id'],object_person_id=father['person_id'],status='contextual_provisional',interpretation_basis=KIND,qualification=dict(source_explicit_parent_for_subject=False,lineage='paternal',shared_mother='not_inferred',absolute_birth_order='not_inferred',graph_effect='source_query_only'),source_term=pin['scope_segments'][1]['literal']+pin['scope_segments'][2]['literal'],source_context=dict(kind=KIND,subject_role=slot['subject_role'],object_role='naming_father',role_mentions=pin['role_mentions'],scope_segments=pin['scope_segments'],paragraph_sha256=pin['paragraph_sha256'],revision_id=pin['revision_id'],raw_sha256=pin['raw_sha256']),evidence=[e],rationale=RATIONAL,reviewer='Codex（AI代理）',human_reviewed=False,model=None))
 return out
def valid(record,chapter,root,people):
 if not isinstance(record,dict):return False
 try:return any(_strict(record,x)for x in expected(chapter,root,people))
 except(AssertionError,KeyError,TypeError,ValueError,IndexError,StopIteration,OSError):return False
def errors(root,rows,people):
 if not isinstance(root,(str,Path))or not isinstance(rows,(list,tuple))or not isinstance(people,(dict,set)):return ['親屬來源判讀輸入型別無效']
 docs=[d for d in rows if isinstance(d,dict)and d.get('record_type')==TYPE]
 if not docs:return ['具名親屬判讀側檔的record_type無效']if (Path(root)/SIDECAR).exists()else []
 try:
  assert len(docs)==1;d,=docs;assert set(d)=={'format_version','record_type','chapter_id','records'}and d['format_version']=='0.2'and isinstance(d['records'],list)
  chapters={c['id']:c for c in rows if isinstance(c,dict)and c.get('record_type')=='marked_chapter'};ch=chapters[d['chapter_id']];want=expected(ch,root,people);assert _strict(d['records'],want)
  newids={v['id']for v in want};otherids=[]
  for x in rows:
   if x is d or not isinstance(x,dict):continue
   for field in ['assertions','records','events','holdings','decisions']:
    values=x.get(field,[])
    if isinstance(values,list):otherids.extend(v.get('id')for v in values if isinstance(v,dict))
  assert not newids.intersection(otherids)
  return []
 except(AssertionError,KeyError,TypeError,ValueError,IndexError,StopIteration,OSError):return ['固定收到親屬判讀須保完整原單元、三組語境、九角色及暫定來源資格']
def select(rows,people,root,ids):
 if not isinstance(rows,(list,tuple))or not isinstance(people,(dict,set))or not isinstance(ids,set):raise ValueError('親屬來源判讀查詢型別無效')
 docs=[d for d in rows if isinstance(d,dict)and d.get('record_type')==TYPE]
 if any(not isinstance(d.get('records'),list)for d in docs):raise ValueError('親屬來源判讀記錄須為陣列')
 relevant=[d for d in docs if any(isinstance(v,dict)and isinstance(v.get('subject_person_id'),str)and isinstance(v.get('object_person_id'),str)and ids.intersection((v['subject_person_id'],v['object_person_id']))for v in d['records'])]
 if not relevant:return []
 issues=errors(root,rows,people)
 if issues:raise ValueError(';'.join(issues))
 return [v for d in relevant for v in d['records']if ids.intersection((v['subject_person_id'],v['object_person_id']))]
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',type=Path,default=ROOT);parser.add_argument('--person-id');args=parser.parse_args();root=args.root.resolve()
 try:
  people={p['id']:p for p in json.loads((root/'registry/persons.json').read_text())['persons']};rows=[json.loads(p.read_text())for p in sorted((root/'corpus').glob('*/*.json'))];issues=errors(root,rows,people)
  if issues:raise ValueError(';'.join(issues))
  if args.person_id and args.person_id not in people:raise ValueError('未知人物 ID：'+args.person_id)
  result=select(rows,people,root,{args.person_id})if args.person_id else [v for d in rows if d.get('record_type')==TYPE for v in d['records']];print(json.dumps(result,ensure_ascii=False,indent=2));return 0
 except(ValueError,OSError,KeyError,TypeError)as exc:parser.error(str(exc))
if __name__=='__main__':main()
