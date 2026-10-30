"""Validate a bounded editorial surname chain through same-source explicit fathers."""
import re
KIND = 'contextual_surname_from_same_source_father_chain'
def validate(name, names, chapters, assertions):
 try:
  b=name['surname_basis']
  assert b['kind']==KIND and b['status']=='contextual_provisional' and b['human_reviewed'] is False
  assert name['status']=='contextual_provisional' and name['human_reviewed'] is False and b['rationale'].strip()
  seeds=[n for n in names if n.get('id')==b['source_name_record_id']];assert len(seeds)==1
  seed=seeds[0];assert not seed.get('surname_basis') and seed['surname'] and seed['ming'] and seed['surname']==name['surname']
  assert seed['chapter_id']==name['chapter_id']
  c=chapters[name['chapter_id']];ps={p['id']:p for p in c['paragraphs']};assert len(ps)==len(c['paragraphs'])
  def mark(p,mid,pid):
   hits=[m for m in p['mentions'] if m['id']==mid];assert len(hits)==1
   m=hits[0];assert m['kind']=='person' and m['person_id']==pid and p['text'][m['start']:m['end']]==m['surface'];return m
  sp=ps[seed['paragraph_id']];sm=mark(sp,seed['person_mention_id'],seed['person_id'])
  assert seed['quote']==sp['text']==b['source_full_quote']
  assert sm['start']==0 and sm['surface']==seed['surname']+seed['ming']
  if not re.match(r'^[，,]?字',sp['text'][sm['end']:]):
   try:from .surname_fixed_birthplace_head import valid as fixed_head_valid
   except ImportError:from surname_fixed_birthplace_head import valid as fixed_head_valid
   assert fixed_head_valid(seed,name,c,assertions)
  tp=ps[name['paragraph_id']];tm=mark(tp,name['person_mention_id'],name['person_id'])
  assert name['quote']==tp['text'] and tm['surface']==name['ming']
  steps=b['steps'];assert 1<=len(steps)<=2
  current=seed['person_id'];seen={current}
  for step in steps:
   assert step['from_person_id']==current
   matches=[a for a in assertions if a['id']==step['assertion_id']];assert len(matches)==1
   a=matches[0];assert a['predicate']=='father' and a['status']=='source_attested'
   assert a.get('qualifiers',{}).get('lineage','paternal')=='paternal'
   assert not a.get('qualifiers',{}).get('adoptive')
   child=a['subject_person_id'];father=a['object_person_id'];assert child!=father
   direction=step['traversal'];assert direction in ('child_to_father','father_to_child')
   pair=(child,father) if direction=='child_to_father' else (father,child)
   assert pair==(current,step['to_person_id']) and pair[1] not in seen
   e=step['evidence'];assert e in a['evidence'] and e['chapter_id']==c['id']
   assert e['work_id']==c['work_id'] and e['book_id']==c['book_id'] and e['source_id']==c['source_id']
   p=ps[e['paragraph_id']];assert e['quote']==p['text']
   mark(p,e['subject_person_mention_id'],child);mark(p,e['object_person_mention_id'],father)
   assert step['source_term']==a['qualifiers']['source_term'] and step['source_term'] in p['text']
   current=pair[1];seen.add(current)
  assert current==name['person_id']
 except (AssertionError,KeyError,StopIteration,TypeError,IndexError):
  raise ValueError('Same-source surname chain requires an explicit full-name anchor and one or two source-attested father edges with exact endpoints and complete evidence')

CROSS_KIND='contextual_surname_from_cross_chapter_same_canonical_family_path'
def validate_cross_chapter(name,names,chapters,assertions,root):
    import hashlib,json
    from pathlib import Path
    try:
        b=name['surname_basis'];assert set(b)=={'kind','status','human_reviewed','rationale','source_name_record_id','source_full_name_record','seed_evidence','same_person_bridge','assertion_id','traversal','fixed_witness_reference'}and b['kind']==CROSS_KIND and b['status']=='contextual_provisional'and b['human_reviewed']is False and b['rationale']and name['status']=='contextual_provisional'and name['human_reviewed']is False
        seed,=[n for n in names if n.get('id')==b['source_name_record_id']];assert seed==b['source_full_name_record']and not seed.get('surname_basis')and seed['surname']==name['surname']and seed['surname']and seed['ming']
        sc=chapters[seed['chapter_id']];sp=next(p for p in sc['paragraphs']if p['id']==seed['paragraph_id']);sm,=[m for m in sp['mentions']if m['id']==seed['person_mention_id']];assert sm['kind']=='person'and sm['person_id']==seed['person_id']and sm['surface']==seed['surname']+seed['ming']and sp['text'][sm['start']:sm['end']]==sm['surface']and seed['quote']==sp['text']
        c=chapters[name['chapter_id']];p=next(p for p in c['paragraphs']if p['id']==name['paragraph_id']);tm,=[m for m in p['mentions']if m['id']==name['person_mention_id']];assert name['quote']==p['text']and tm['kind']=='person'and tm['person_id']==name['person_id']and tm['surface']==name['ming']and p['text'][tm['start']:tm['end']]==name['ming']
        a,=[a for a in assertions if a['id']==b['assertion_id']]
        try:from .biographical_kinship import natural_parentage_errors,natural_parentage_context
        except ImportError:from biographical_kinship import natural_parentage_errors,natural_parentage_context
        assert not natural_parentage_errors(a,c,root);spec,roles=natural_parentage_context(a,c,root)
        ar=(a.get('context',{}).get('source_continuity',{}).get('fixed_witness_reference')or a['qualifiers']['source_clause_binding']['fixed_witness_reference']);assert b['fixed_witness_reference']==ar
        hp,head=roles['head'];bridge=b['same_person_bridge'];assert bridge==dict(seed_chapter_id=sc['id'],seed_paragraph_id=sp['id'],seed_mention_id=sm['id'],head_chapter_id=c['id'],head_paragraph_id=hp['id'],head_mention_id=head['id'])and head['person_id']==sm['person_id']and head['surface']==seed['ming']
        info=spec['name_seed_context'];assert info['chapter_id']==sc['id']and info['paragraph_id']==sp['id']and info['source_id']==sc['source_id']and info['work_id']==sc['work_id']and info['book_id']==sc['book_id']and info['source_revision']==sc['source']['revision_id']and info['quote']==sp['text']and info['paragraph_sha256']==hashlib.sha256(sp['text'].encode()).hexdigest()
        root=Path(root).resolve();rel=Path(info['raw_file']);path=root/rel;assert not rel.is_absolute()and'..'not in rel.parts and rel.parts[0]=='source-evidence'and path.resolve()==path
        rb=path.read_bytes();assert hashlib.sha256(rb).hexdigest()==info['raw_sha256']==sc['source']['raw_sha256'];lo=sp['source_position']['first_line'];assert lo==sp['source_position']['last_line']and rb.decode().splitlines()[lo-1].strip()==sp['text']
        e=dict(work_id=sc['work_id'],book_id=sc['book_id'],source_id=sc['source_id'],chapter_id=sc['id'],paragraph_id=sp['id'],quote=sp['text'],person_mention_id=sm['id']);assert b['seed_evidence']==e
        if b['traversal']=='child_to_father':assert(a['subject_person_id'],a['object_person_id'])==(seed['person_id'],name['person_id'])and tm['id']==roles['father'][1]['id']
        elif b['traversal']=='father_to_child':assert(a['object_person_id'],a['subject_person_id'])==(seed['person_id'],name['person_id'])and tm['id']==roles['child'][1]['id']
        else:raise ValueError('No spouse/mother/adoptive/collateral or identity-ID inference')
    except(KeyError,TypeError,ValueError,AssertionError,IndexError,StopIteration,OSError,AttributeError):
        raise ValueError('跨篇復姓須有原全名seed、同canonical原名橋、固定raw自然段親屬與逐詞父子角色；不得由label/ID/婚配補姓')
