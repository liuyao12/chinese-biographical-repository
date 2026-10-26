"""Bounded same-source surname reading, no inferred relationship generation.
Every edge is an existing named-brother or explicit father record. Sibling
steps preserve generation; parent-to-child steps add one. Full-name seed and
all raw-role/evidence spans are checked independently of structural IDs.
"""
import re,hashlib
KIND='contextual_surname_from_bounded_named_family_path'
MAX_STEPS=5

def validate(name,names,chapters,assertions):
 try:
  b=name['surname_basis'];assert set(b)=={'kind','status','human_reviewed','rationale','source_name_record_id','source_full_quote','seed_frame','steps'}
  assert b['kind']==KIND and b['status']=='contextual_provisional'and b['human_reviewed']is False and b['rationale'].strip()and name['status']=='contextual_provisional'and name['human_reviewed']is False
  seeds=[x for x in names if x.get('id')==b['source_name_record_id']];assert len(seeds)==1;seed=seeds[0];assert not seed.get('surname_basis')and seed['surname']and seed['ming']and seed['surname']==name['surname']and seed['chapter_id']==name['chapter_id']
  ch=chapters[name['chapter_id']];ps={p['id']:p for p in ch['paragraphs']};assert len(ps)==len(ch['paragraphs']);order={p['id']:n for n,p in enumerate(ch['paragraphs'])};aa={a['id']:a for a in assertions};assert len(aa)==len(assertions)
  def mark(p,mid,pid):
   hit=[m for m in p['mentions']if m['id']==mid];assert len(hit)==1;m=hit[0];assert m['kind']=='person'and m['person_id']==pid and type(m['start'])is int and type(m['end'])is int and 0<=m['start']<m['end']<=len(p['text'])and p['text'][m['start']:m['end']]==m['surface'];return m
  def frame(f):
   assert set(f)=={'paragraph_id','paragraph_sha256','source_revision','raw_sha256'};p=ps[f['paragraph_id']];raw=ch['source'].get('raw_file_sha256',ch['source'].get('raw_sha256',ch['source'].get('wikitext_sha256')));assert re.fullmatch('[0-9a-f]{64}',f['raw_sha256'])and f['raw_sha256']==raw and f['source_revision']==ch['source']['revision_id']==p['source_position']['revision_id']and f['paragraph_sha256']==hashlib.sha256(p['text'].encode()).hexdigest()and p['text_layer']=='received_chapter';return p
  sp=frame(b['seed_frame']);assert seed['paragraph_id']==sp['id']and seed['quote']==sp['text']==b['source_full_quote'];sm=mark(sp,seed['person_mention_id'],seed['person_id']);assert sm['surface']==seed['surname']+seed['ming']
  targetp=ps[name['paragraph_id']];tm=mark(targetp,name['person_mention_id'],name['person_id']);assert tm['surface']==name['ming']and name['quote']==targetp['text']
  steps=b['steps'];assert isinstance(steps,list)and 1<=len(steps)<=MAX_STEPS;current=seed['person_id'];seen={current};used=set();generation=0
  for step in steps:
   assert set(step)=={'assertion_id','from_person_id','to_person_id','traversal','generation_before','generation_after','evidence','source_frames'}and step['assertion_id']not in used and step['from_person_id']==current
   a=aa[step['assertion_id']];q=a['qualifiers'];assert a['status']=='source_attested'and not q.get('adoptive')and not q.get('sworn')and not q.get('same_mother_only')and q.get('shared_father')is not False and q.get('lineage')not in('maternal','non_paternal')
   assert type(step['generation_before'])is int and type(step['generation_after'])is int and step['generation_before']==generation and step['evidence']==a['evidence']
   frames=step['source_frames'];assert len(frames)==len({e['paragraph_id']for e in a['evidence']})and {f['paragraph_id']for f in frames}=={e['paragraph_id']for e in a['evidence']}
   for f in frames:frame(f)
   for e in a['evidence']:
    assert(e['chapter_id'],e['work_id'],e['book_id'],e['source_id'])==(ch['id'],ch['work_id'],ch['book_id'],ch['source_id'])and e['quote']==ps[e['paragraph_id']]['text']
   if step['traversal']=='older_to_younger':
    if q.get('source_clause_binding',{}).get('kind')=='biography_family_clause':
     assert a['predicate']=='brother'and a['object_person_id']==current and a['subject_person_id']==step['to_person_id']and step['generation_after']==generation
     try:from .surname_biography_family_steps import valid as source_family_valid
     except ImportError:from surname_biography_family_steps import valid as source_family_valid
     assert source_family_valid(a,ch,assertions)
     e,=a['evidence'];p=ps[e['paragraph_id']];old=mark(p,e['object_person_mention_id'],current);young=mark(p,e['subject_person_mention_id'],step['to_person_id'])
     assert q['relative_birth_order']['older_person_id']==current and q['relative_birth_order']['younger_person_id']==step['to_person_id']and q['relative_birth_order']['operator']=='lt'
    else:
     assert a['predicate']=='brother'and a['object_person_id']==current and a['subject_person_id']==step['to_person_id'];e,=a['evidence'];p=ps[e['paragraph_id']];bind=q['source_clause_binding'];assert bind['kind']=='named_older_di_younger'and bind['source_anchor']['start']==0
     try:from .named_family_offices import sibling_order_valid
     except ImportError:from named_family_offices import sibling_order_valid
     assert sibling_order_valid(a,{p['id']:(ch['id'],p)});old=mark(p,bind['older_mention_id'],current);young=mark(p,bind['younger_mention_id'],step['to_person_id']);assert e['subject_person_mention_id']==young['id']and e['object_person_mention_id']==old['id']and step['generation_after']==generation
   elif step['traversal']=='father_to_child':
    assert a['predicate']=='father'and a['object_person_id']==current and a['subject_person_id']==step['to_person_id']and q.get('lineage','paternal')=='paternal'and step['generation_after']==generation+1
    es=a['evidence']
    if q.get('source_clause_binding',{}).get('kind')=='biography_family_clause':
     try:from .surname_biography_family_steps import valid as source_family_valid
     except ImportError:from surname_biography_family_steps import valid as source_family_valid
     assert source_family_valid(a,ch,assertions)
    elif len(es)==1:
     e=es[0];p=ps[e['paragraph_id']];child=mark(p,e['subject_person_mention_id'],step['to_person_id']);parent=mark(p,e['object_person_mention_id'],current);t=p['text'];assert parent['end']<child['start']and q['source_term']==t[parent['start']:child['end']]
     bridge=t[parent['end']:child['start']];assert re.fullmatch(r'子(?:[^父母兄弟曰云「」『』非不無，。]{1,12}(?:將軍|太守|尚書|侍郎|侍中|參軍|令|卿))?',bridge)
    else:
     assert len(es)==2;ctx=a['context'];assert ctx['kind']=='adjacent_paragraphs'and ctx['status']=='contextual_provisional'and ctx['human_reviewed']is False and ctx['paragraph_ids']==[e['paragraph_id']for e in es]
     pe,ce=es;pp=ps[pe['paragraph_id']];cp=ps[ce['paragraph_id']];assert order[cp['id']]==order[pp['id']]+1
     parent=mark(pp,pe['object_person_mention_id'],current);child=mark(cp,ce['subject_person_mention_id'],step['to_person_id']);assert child['start']==1 and cp['text'].startswith('子'+child['surface']+'，')and q['source_term']=='子'+child['surface']
     # The parent is either a named younger-brother biography head, or the
     # explicit resumed subject after a named person's death in that unit.
     named_head=any(m.get('kind')=='person'and m['start']==0 and pp['text'][:parent['end']]==m['surface']+'弟'+parent['surface']and parent['end']<len(pp['text'])and pp['text'][parent['end']:].startswith('，字')for m in pp['mentions'])
     resumed=pp['text'][max(0,parent['start']-4):parent['start']]=='之死也，'and pp['text'][parent['end']:].startswith('為')and any(m.get('kind')=='person'and m['end']==parent['start']-4 for m in pp['mentions'])
     assert named_head or resumed
    generation+=1
   else:raise AssertionError('No spouse, mother, adoptive, uncle, unknown-parent or inferred edge')
   assert step['to_person_id']not in seen;current=step['to_person_id'];seen.add(current);used.add(step['assertion_id'])
  assert current==name['person_id']
 except(AssertionError,KeyError,ValueError,TypeError,IndexError,StopIteration,AttributeError):
  raise ValueError('Named-family surname needs a bounded acyclic same-source path of exact named brothers and explicit fathers, full-name seed, source-role evidence and generation checks; never generates parentage')
