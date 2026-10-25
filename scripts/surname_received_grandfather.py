"""One received Song064 paternal-grandfather surname reading; no edited parent."""
from pathlib import Path
import json,hashlib
KIND='contextual_surname_from_fixed_received_paternal_grandfather'
CID='c-songshu-064-peisongzhi';CH='corpus/songshu/064-peisongzhi.json'
REF='source-evidence/song064-peisongzhi-reading/raw-projection.json';PROJ_SHA='4650e7ab93dcfa41f34b771fedb6df0bdb62003cc313b66c1795a064c16dd02f'
RAW='sources/songshu/wikisource-1748217-raw.wikitext';RAW_SHA='aeb7f890fb1a261a285786bd19844cbc090dc96e35d7ca61cf8ca1eadf66afb8';UNIT_SHA='a9017dd5cf752bde0305379ef763d56553e939e89827a3e5432f69728b9d9744'
URL='https://zh.wikisource.org/w/index.php?title=%E5%AE%8B%E6%9B%B8%2F%E5%8D%B764&oldid=1748217'
def valid(n,names,chapters,assertions,root):
 try:
  assert isinstance(n,dict)and isinstance(names,list)and isinstance(chapters,dict)and isinstance(assertions,list)and root is not None
  root=Path(root).resolve();b=n['surname_basis'];assert set(b)=={'kind','status','human_reviewed','rationale','source_name_record_id','literal_name_record_id','assertion_id','source_role','generation_distance','evidence','source_frame'}
  assert b['kind']==KIND and b['status']=='contextual_provisional'and b['human_reviewed']is False and b['rationale']and b['source_role']=='grandfather'and type(b['generation_distance'])is int and b['generation_distance']==2
  assert n['status']=='contextual_provisional'and n['human_reviewed']is False and n['surname']=='裴'and n['ming']=='昧'and n['chapter_id']==CID
  c=chapters[CID];path=root/CH;assert path.resolve()==path and path.is_file()and json.loads(path.read_bytes())==c
  assert (c['work_id'],c['book_id'],c['source_id'])==('w-songshu','b-songshu-064','s-song064-ws1748217');s=c['source'];assert s['provider']=='Wikisource'and type(s['revision_id'])is int and s['revision_id']==1748217 and s['url']==s['permalink']==URL and s['raw_path']==RAW and s['raw_file_sha256']==s['raw_sha256']==RAW_SHA
  try:from scripts.biographical_work_references import projection_valid,_inside
  except ImportError:from biographical_work_references import projection_valid,_inside
  pb=_inside(root,REF,'source-evidence').read_bytes();assert hashlib.sha256(pb).hexdigest()==PROJ_SHA;projection=json.loads(pb)
  raw=_inside(root,RAW,'sources').read_bytes();assert hashlib.sha256(raw).hexdigest()==RAW_SHA;raw=raw.decode('utf-8')
  assert len(c['paragraphs'])==len(projection['paragraphs'])==6 and projection['unit_raw_start']==8140 and projection['unit_raw_end']==12527 and projection['unit_raw_sha256']==UNIT_SHA
  assert hashlib.sha256(raw[8140:12527].encode()).hexdigest()==UNIT_SHA and raw[8140:8163]=='== [[w:裴松之|裴-{松}-之]] =='and raw[12527:].startswith('== 何承天 ==')
  binding={'received_text_projection':dict(path=REF,sha256=PROJ_SHA,source_layer='received_text',text_layer='received_text')}
  assert projection_valid(c,c['paragraphs'],binding,root)  # existing unchanged 4-argument validator
  p=c['paragraphs'][0];assert p['id']==CID+':p001'and n['paragraph_id']==p['id']and n['quote']==p['text'];t=p['text'];ms={m['id']:m for m in p['mentions']}
  head,grand,father=[ms[p['id']+':'+k]for k in('m0000','m0016','m0024')]
  assert [(m['start'],m['end'],m['surface'],m['kind'])for m in(head,grand,father)]==[(0,3,'裴松之','person'),(16,17,'昧','person'),(24,25,'珪','person')]
  assert len({head['person_id'],grand['person_id'],father['person_id']})==3 and t[15:17]=='祖昧'and t[23:25]=='父珪'and n['person_id']==grand['person_id']and n['person_mention_id']==grand['id']
  seeds=[x for x in names if x.get('id')==b['source_name_record_id']];assert len(seeds)==1;seed=seeds[0];assert seed['surname']=='裴'and seed['ming']=='松之'and seed['person_id']==head['person_id']and seed['person_mention_id']==head['id']and seed['chapter_id']==CID and seed['paragraph_id']==p['id']and seed['quote']==t and not seed.get('surname_basis')
  literals=[x for x in names if x.get('id')==b['literal_name_record_id']];assert len(literals)==1;literal=literals[0];assert literal['surname']is None and literal['ming']=='昧'and literal['person_id']==grand['person_id']and literal['person_mention_id']==grand['id']and literal['chapter_id']==CID and literal['paragraph_id']==p['id']and literal['quote']==t and not literal.get('surname_basis')
  selected=[a for a in assertions if a.get('id')==b['assertion_id']];assert len(selected)==1;a=selected[0];assert a['id']=='a-song064-songzhi-grandfather'and a['predicate']=='grandfather'and a['status']=='source_attested'and a['human_reviewed']is False and a['subject_person_id']==head['person_id']and a['object_person_id']==grand['person_id']and a['qualifiers']==dict(source_term='祖昧',lineage='paternal')
  e,=a['evidence'];expected={k:c[k]for k in('work_id','book_id','source_id')};expected.update(chapter_id=CID,paragraph_id=p['id'],quote=t,subject_person_mention_id=head['id'],object_person_mention_id=grand['id']);assert b['evidence']==e==expected
  assert b['source_frame']==dict(source_revision=1748217,raw_sha256=RAW_SHA,paragraph_sha256=hashlib.sha256(t.encode()).hexdigest(),projection_path=REF,projection_sha256=PROJ_SHA,unit_raw_sha256=UNIT_SHA)and type(b['source_frame']['source_revision'])is int
  assert not any(x.get('person_id')==n['person_id']and x.get('surname')not in(None,'裴')and not x.get('surname_basis')for x in names)
  return True
 except(AssertionError,KeyError,TypeError,ValueError,IndexError,AttributeError,StopIteration,OSError,UnicodeError):return False

def validate(n,names,chapters,assertions,root):
 if not valid(n,names,chapters,assertions,root):raise ValueError('宋064祖昧推姓須有固定六段原見證、全文名裴松之、明祖角色與原grandfather斷言；不得改父、layer或qualifier')
