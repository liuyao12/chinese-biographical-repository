"""Qualified surname across two independently verified complete received units.
Only the same source subject or one literal natal-father edge is supported.
No registry label, structural ID, adoption, spouse, dynasty surname or NLU.
"""
from pathlib import Path
import json,hashlib
KIND='contextual_surname_from_fixed_cross_source_subject_or_father'
UNITS={
 'c-jinshu-035-peiwei':dict(native_path='corpus/jinshu/035-peiwei.json',work_id='w-jinshu',book_id='b-jinshu-035',source_id='s-jinshu-035-ws2506399-peiwei',title='裴頠傳',source_title='《晉書》卷三十五子頠完整附傳選錄',revision=2506399,raw_path='sources/witnesses/jin035-ws2506399.wikitext',raw_sha256='b27aa9fc386b5f40990822d615febffcb8b8cd6df3fe6f74585274ff733c12be'),
 'c-jinshu-043-leguang':dict(native_path='corpus/jinshu/043-leguang.json',work_id='w-jinshu',book_id='b-jinshu-043',source_id='s-jinshu-043-ws2618531-leguang',title='樂廣傳',source_title='《晉書》卷四十三樂廣傳完整敘事單元',revision=2618531,raw_path='sources/witnesses/jin043-ws2618531.wikitext',raw_sha256='d9ab0781004dc723ae243bb2bac47695d2736fd7b595ec472d5ffde62a04d0fe')}
TARGETS={'c-jinshu-035-peiwei:p001:m0000':('c-jinshu-035-peiwei:p001',0,1,'頠','same_canonical_source_subject'),
 'c-jinshu-035-peiwei:p015:m0069':('c-jinshu-035-peiwei:p015',69,70,'嵩','one_explicit_natal_father'),
 'c-jinshu-035-peiwei:p015:m0071':('c-jinshu-035-peiwei:p015',71,72,'該','one_explicit_natal_father')}
PARAGRAPHS={'c-jinshu-035-peiwei:p001':'873cf6d6ed964fb0ad020a5744359dc24d56161a14474dd707e05ddd645448fe','c-jinshu-035-peiwei:p015':'94e37a418e1ef099ce75d0633046b78c7f0481eb44210265b11e5c16abbd2021','c-jinshu-043-leguang:p005':'dedffad4f71255d8ddb5c5a17b1af87d3ccb0d28334eae2c1c7442778d21bcf7'}
def unit_ref(cid):return dict(chapter_id=cid,**UNITS[cid])
def frame(c,p):
 return dict(work_id=c['work_id'],book_id=c['book_id'],source_id=c['source_id'],chapter_id=c['id'],paragraph_id=p['id'],source_revision=c['source']['revision_id'],raw_file=c['source']['raw_file'],raw_file_sha256=c['source']['raw_file_sha256'],paragraph_sha256=hashlib.sha256(p['text'].encode()).hexdigest(),quote=p['text'])
def validate(n,names,chapters,assertions,root):
 try:
  assert root is not None;root=Path(root).resolve();b=n['surname_basis']
  assert set(b)=={'kind','status','human_reviewed','rationale','seed_name_record_id','source_units','seed_frame','target_frame','target_original_components','target_name_mention_id','derivation_role','steps','scope','cross_source_identity_status'}
  assert b['kind']==KIND and b['status']==n['status']=='contextual_provisional'and b['human_reviewed']is n['human_reviewed']is False and b['rationale'].strip()
  assert b['scope']=='listed_name_records_only'and b['cross_source_identity_status']=='existing_canonical_identification_not_new_merge'
  assert b['source_units']==[unit_ref(cid)for cid in sorted(UNITS)]
  try:from scripts.fixed_wikisource_units import source_errors
  except ImportError:from fixed_wikisource_units import source_errors
  cs={}
  for cid,u in UNITS.items():
   path=root/u['native_path'];assert path.resolve()==path and path.is_file();c=json.loads(path.read_bytes());assert c==chapters[cid]and c['id']==cid
   assert all(c[k]==u[k]for k in ('work_id','book_id','source_id','title'));s=c['source'];assert s['title']==u['source_title']and s['revision_id']==u['revision']and s['raw_file']==u['raw_path']and s['raw_file_sha256']==u['raw_sha256']
   raw=root/u['raw_path'];assert raw.resolve()==raw and raw.is_file()and hashlib.sha256(raw.read_bytes()).hexdigest()==u['raw_sha256'];assert c['annotation'].get('fixed_wikisource_unit_ref')and not source_errors(c,root);cs[cid]=c
  seed,=[v for v in names if v.get('id')==b['seed_name_record_id']];assert seed['chapter_id']=='c-jinshu-043-leguang'and seed['paragraph_id']=='c-jinshu-043-leguang:p005'and seed['person_mention_id']=='c-jinshu-043-leguang:p005:m0028'and seed['surname']=='裴'and seed['ming']=='頠'and not seed.get('surname_basis')
  sc=cs[seed['chapter_id']];sp,=[p for p in sc['paragraphs']if p['id']==seed['paragraph_id']];sm,=[m for m in sp['mentions']if m['id']==seed['person_mention_id']]
  assert sm['kind']=='person'and sm['person_id']==seed['person_id']and(sm['start'],sm['end'],sm['surface'])==(28,30,'裴頠')and sp['text'][28:30]=='裴頠'
  assert hashlib.sha256(sp['text'].encode()).hexdigest()==PARAGRAPHS[sp['id']]
  sf=frame(sc,sp);sf.update(name_record_id=seed['id'],person_mention_id=sm['id'],start=28,end=30,surface='裴頠',person_id=seed['person_id']);assert b['seed_frame']==sf
  assert n['chapter_id']=='c-jinshu-035-peiwei'and n['surname']==seed['surname']and n['person_mention_id']==b['target_name_mention_id']
  pid,lo,hi,ming,role=TARGETS[n['person_mention_id']];assert pid==n['paragraph_id']and n['ming']==ming and b['derivation_role']==role
  tc=cs[n['chapter_id']];tp,=[p for p in tc['paragraphs']if p['id']==pid];tm,=[m for m in tp['mentions']if m['id']==n['person_mention_id']]
  assert tm['kind']=='person'and tm['person_id']==n['person_id']and(tm['start'],tm['end'],tm['surface'])==(lo,hi,ming)and tp['text'][lo:hi]==ming
  assert n['quote']==tp['text']and hashlib.sha256(tp['text'].encode()).hexdigest()==PARAGRAPHS[pid]and b['target_frame']==frame(tc,tp)
  assert b['target_original_components']==dict(surname=None,ming=ming,zi=n.get('zi'))
  try:from scripts.fixed_biography_names import component_valid
  except ImportError:from fixed_biography_names import component_valid
  assert component_valid(seed,sc,root,assertions)and component_valid(n,tc,root,assertions)
  # A new contrary literal surname cannot be silently resolved by this fill-missing rule.
  for other in names:
   if other['person_id']==n['person_id']and other.get('surname')and not other.get('surname_basis'):assert other['surname']==n['surname']
  if role=='same_canonical_source_subject':assert n['person_id']==seed['person_id']and b['steps']==[]
  else:
   step,=b['steps'];assert set(step)=={'direction','assertion_id','from_person_id','to_person_id','generation_before','generation_after','assertion_snapshot'}
   assert step['direction']=='father_to_child'and type(step['generation_before'])is int and step['generation_before']==0 and type(step['generation_after'])is int and step['generation_after']==1
   assert step['from_person_id']==seed['person_id']and step['to_person_id']==n['person_id']and n['person_id']!=seed['person_id']
   a,=[a for a in assertions if a['id']==step['assertion_id']];assert a==step['assertion_snapshot']and a['predicate']=='father'and a['status']=='source_attested'and a['subject_person_id']==n['person_id']and a['object_person_id']==seed['person_id']
   assert a['qualifiers']==dict(source_term='二子嵩、該',source_interpretation_status='explicit_source_wording',lineage='paternal')
   e,=a['evidence'];father,=[m for m in tp['mentions']if m['id']=='c-jinshu-035-peiwei:p015:m0010'];assert father['kind']=='person'and father['person_id']==seed['person_id']and(father['start'],father['end'],father['surface'])==(10,11,'頠')and tp['text'][67:72]=='二子嵩、該'
   assert e==dict(work_id=tc['work_id'],book_id=tc['book_id'],source_id=tc['source_id'],chapter_id=tc['id'],paragraph_id=tp['id'],quote=tp['text'],subject_person_mention_id=tm['id'],object_person_mention_id=father['id'])
   try:from scripts.fixed_witness_fact_slots import valid
   except ImportError:from fixed_witness_fact_slots import valid
   assert valid(a,tc,root)
 except(AssertionError,KeyError,ValueError,TypeError,IndexError,StopIteration,AttributeError,OSError):
  raise ValueError('跨源補姓須逐驗兩完整固定見證、原全文名同人或一步明生父；不由標籤、ID、母／配偶／收養或改字推姓')
