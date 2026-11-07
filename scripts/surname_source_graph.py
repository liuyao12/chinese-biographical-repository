"""Current-source surname graph; offline editorial semantics, no runtime NLU.

The ordinary caller constructs one private state through real load_assemblies.
No name validator calls assemblies or validates a fabricated passed-state dict.
There is no persistent memo or certificate and no person/source whitelist.
"""
import copy,hashlib,json,marshal
from pathlib import Path
try:
 from scripts.surname_source_frames import same,read,source_view
 from scripts.source_assertion_endpoints import conditions
except ImportError:
 from surname_source_frames import same,read,source_view
 from source_assertion_endpoints import conditions
KIND='contextual_surname_from_source_bound_kinship_graph'
_AUTHORITY=object()


def _caller_key(catalog):
 people,records=catalog
 return hashlib.sha256(marshal.dumps((people,type(records).__module__+'.'+type(records).__qualname__,list(records)),2)).digest()


class _GraphContext:
 __slots__=('_root','_catalog','_key','_names','_chapters','_assertions','_assemblies','_pins','_sealed')
 def __init__(self,authority,root,catalog,assemblies,pins):
  if authority is not _AUTHORITY:raise TypeError('Use ordinary prepare(root, full_catalog)')
  people,records=catalog
  fields=dict(_root=str(root),_catalog=catalog,_key=_caller_key(catalog),
   _names=marshal.dumps([n for r in records if r.get('record_type')=='person_name_component_set'for n in r['records']],2),
   _chapters=marshal.dumps({r['id']:r for r in records if r.get('record_type')=='marked_chapter'},2),
   _assertions=marshal.dumps([a for r in records if r.get('record_type')=='person_assertion_set'for a in r['assertions']],2),
   _assemblies=marshal.dumps(assemblies,2),_pins=marshal.dumps(pins,2),_sealed=True)
  for k,v in fields.items():object.__setattr__(self,k,v)
 def __setattr__(self,key,value):raise AttributeError('Ordinary graph state is immutable')


def prepare(root,catalog):
 """Called before surname enrichment, never from validate(). No mock state."""
 root=Path(root).resolve();people,records=catalog
 rows=json.loads(read(root,'registry/persons.json'))['persons']
 assert len(rows)==len({p['id']for p in rows}) and same(people,{p['id']:p for p in rows})
 pins={'registry/persons.json':hashlib.sha256(read(root,'registry/persons.json')).digest()}
 assembly_path=root/'registry/family-assemblies.json'
 if assembly_path.exists():pins['registry/family-assemblies.json']=hashlib.sha256(read(root,'registry/family-assemblies.json')).digest()
 else:pins['registry/family-assemblies.json']=None
 before=_caller_key(catalog)
 try:from scripts.family_assemblies import load_assemblies
 except ImportError:from family_assemblies import load_assemblies
 # The complete ordinary assembly owner, with all original checks, is authoritative.
 assemblies=load_assemblies(root,catalog)
 assert _caller_key(catalog)==before
 for path,digest in pins.items():
  assert (hashlib.sha256(read(root,path)).digest()if (root/path).exists()else None)==digest
 return _GraphContext(_AUTHORITY,root,catalog,assemblies,pins)


def _views(context,names,chapters,assertions,root):
 assert type(context)is _GraphContext and context._root==str(Path(root).resolve())
 assert _caller_key(context._catalog)==context._key
 assert marshal.dumps(names,2)==context._names
 assert marshal.dumps(chapters,2)==context._chapters
 assert marshal.dumps(assertions,2)==context._assertions
 for path,digest in marshal.loads(context._pins).items():
  assert (hashlib.sha256(read(root,path)).digest()if (Path(root)/path).exists()else None)==digest
 return marshal.loads(context._assemblies)


def validate(name,names,chapters,assertions,root,context):
 try:
  b=name['surname_basis']
  assert type(b)is dict and set(b)=={'kind','status','human_reviewed','rationale','frames','seed','target','steps','assertion_sources'}
  assert b['kind']==KIND and b['status']==name['status']=='contextual_provisional'
  assert b['human_reviewed']is False and name['human_reviewed']is False and type(b['rationale'])is str and b['rationale'].strip()
  _,assembled=_views(context,names,chapters,assertions,root)
  assert len([n for n in names if n.get('id')==name['id']])==1 and any(same(n,name)for n in names)
  ps,cs,people,marker,anchor,physical_assertion=source_view(b['frames'],chapters,assertions,root)
  by_mid={}
  for par,(ch,p)in ps.items():
   for m in p['mentions']:
    assert m['id']not in by_mid;by_mid[m['id']]=par
  def bound(mid):
   assert mid in by_mid
   return marker(by_mid[mid],mid)
  sources={s['assertion_id']:s['assertions_path']for s in b['assertion_sources']}
  assert len(sources)==len(b['assertion_sources']) and all(set(s)=={'assertion_id','assertions_path'}for s in b['assertion_sources'])
  used=set()
  continuation_roles={}
  def relation(aid,allow_brother=False):
   used.add(aid);a,document=physical_assertion(sources[aid],aid,with_document=True);q=a.get('qualifiers',{})
   assert document['record_type']=='person_assertion_set'and all(e['chapter_id']==document['chapter_id']for e in a['evidence'])
   allowed={'father','grandfather','great_grandfather','paternal_uncle','agnatic_senior_kin'}|({'brother','sister'}if allow_brother else set())
   assert a['predicate']in allowed and a['status']=='source_attested'and a.get('human_reviewed')is False
   assert not q.get('adoptive')and not q.get('sworn')and not q.get('same_mother_only')and q.get('shared_father')is not False
   assert q.get('adopted_for_family_tree')is not False and q.get('lineage')not in('maternal','non_paternal')
   assert not isinstance(q.get('kinship_structure'),dict)or q['kinship_structure'].get('lineage')not in('maternal','non_paternal')
   assert not any(k in q for k in('care_basis','succession_kind','maternal_path'))
   if a['predicate']in('father','grandfather','great_grandfather'):assert q.get('lineage')=='paternal'and '外祖'not in q.get('source_term','')
   if a['predicate']=='agnatic_senior_kin':
    try:from scripts.collateral_kinship import agnatic_senior_kin_valid
    except ImportError:from collateral_kinship import agnatic_senior_kin_valid
    assert agnatic_senior_kin_valid(a,{pid:(ch['id'],p)for pid,(ch,p)in ps.items()})
   ctx=a.get('context');ee=a['evidence'];assert type(ee)is list and ee
   assert type(q.get('source_term'))is str and q['source_term']and any(q['source_term']in e['quote']for e in ee)
   adjacent=None
   if type(ctx)is dict and ctx.get('kind')=='biographical_child_continuation':
    try:from scripts.biographical_kinship import child_continuation_errors
    except ImportError:from biographical_kinship import child_continuation_errors
    c=chapters[document['chapter_id']]
    assert a['predicate']=='father'and not child_continuation_errors(a,c,root)
    adjacent=ctx['paragraph_ids']
    assert type(adjacent)is list and adjacent==[e['paragraph_id']for e in ee]
    continuation_roles[aid]={(ctx['parent_mention_id'],adjacent[0],a['object_person_id']),
                             (ctx['child_mention_id'],adjacent[-1],a['subject_person_id'])}
   elif ctx is not None:
    assert type(ctx)is dict and ctx.get('kind')=='adjacent_paragraphs'and {'kind','paragraph_ids'}<=set(ctx)
    adjacent=ctx['paragraph_ids'];assert type(adjacent)is list and len(adjacent)==2 and adjacent==[e['paragraph_id']for e in ee]
    c=chapters[ee[0]['chapter_id']];order=[p['id']for p in c['paragraphs']]
    assert order.index(adjacent[1])==order.index(adjacent[0])+1
   local=[]
   for e in ee:
    ch,p=ps[e['paragraph_id']];assert e['quote']==p['text'] and e['work_id']==ch['work_id']and e['book_id']==ch['book_id']
    tests=conditions(a,e,{par:(ch0['id'],p0)for par,(ch0,p0)in ps.items()},chapters,document['chapter_id'])
    assert all(ok for ok,_ in tests[:2])and(adjacent is not None or tests[2][0])
    local.append({m['person_id']for m in p['mentions']if m.get('kind')=='person'})
   if adjacent is not None:assert a['object_person_id']in local[0]and a['subject_person_id']in local[-1]
   return a
  seed=b['seed'];target=b['target']
  assert set(seed)=={'kind','name_form','paragraph_id','person_mention_id','surname_anchor'}
  assert seed['kind']=='literal_surname_with_current_named_person_anchor'and seed['name_form']in('surname_given_name','surname_courtesy_appellation')
  _,sp,sm=marker(seed['paragraph_id'],seed['person_mention_id']);sa=seed['surname_anchor']
  assert set(sa)=={'start','end','surface'}and type(sa['start'])is int and type(sa['end'])is int
  assert sm['start']==sa['start']<sa['end']<sm['end']and sp['text'][sa['start']:sa['end']]==sa['surface']==name['surname']
  assert set(target)=={'name_record_id','paragraph_id','person_mention_id','given_name_anchor'}and target['name_record_id']==name['id']
  tc,tp,tm=marker(target['paragraph_id'],target['person_mention_id']);ga=target['given_name_anchor']
  assert tm['person_id']==name['person_id']and target['paragraph_id']==name['paragraph_id']and target['person_mention_id']==name['person_mention_id']and tc['id']==name['chapter_id']and name['quote']==tp['text']
  assert set(ga)=={'start','end','surface'}and type(ga['start'])is int and type(ga['end'])is int
  assert tm['start']<=ga['start']<ga['end']==tm['end']and tp['text'][ga['start']:ga['end']]==ga['surface']==name['ming']
  steps=b['steps'];assert type(steps)is list and len(steps)<=32
  current=sm['person_id'];seen={current}
  for step in steps:
   assert step['from_person_id']==current
   if step['kind']=='validated_source_paternal_relation':
    assert set(step)=={'kind','assertion_id','from_person_id','to_person_id','traversal','from_person_mention_id','to_person_mention_id'}
    a=relation(step['assertion_id']);pair=(a['subject_person_id'],a['object_person_id'])
    if step['traversal']=='object_to_subject':pair=pair[::-1]
    else:assert step['traversal']=='subject_to_object'
    assert pair==(current,step['to_person_id'])
    for key,pid in [('from_person_mention_id',pair[0]),('to_person_mention_id',pair[1])]:
     ch,p,m=bound(step[key]);assert m['person_id']==pid
     assert any(e['paragraph_id']==p['id']and e.get('subject_person_mention_id')==m['id']or e['paragraph_id']==p['id']and e.get('object_person_mention_id')==m['id']for e in a['evidence'])or (m['id'],p['id'],pid)in continuation_roles.get(a['id'],set())
   elif step['kind']=='validated_editorial_assembly_connection':
    assert set(step)=={'kind','assembly_id','member_person_id','parent_connection_type','supporting_assertion_ids','from_person_id','to_person_id','traversal'}
    row=assembled[step['member_person_id']];c=row['parent_connection'];parent=assembled[row['parent_person_id']]
    assert row['assembly_id']==step['assembly_id']and row['source_assertion_id']is None
    # Ordinary row status belongs to the whole assembly; the selected
    # parent_connection below remains independently provisional.
    assert row['status']in('contextual_provisional','editorial_preferred')and row.get('human_reviewed')is False
    assert c['type']==step['parent_connection_type']and c['status']=='contextual_provisional'and c.get('human_reviewed')is False
    assert c['type']in('parent_between_consecutive_ancestors','shared_father_through_sibling')
    support={v for k,v in c.items()if k.endswith('_assertion_id')}|{ref['assertion_id']for ref in c['references']}
    assert type(step['supporting_assertion_ids'])is list and len(step['supporting_assertion_ids'])==len(support)and set(step['supporting_assertion_ids'])==support
    for aid in support:relation(aid,allow_brother=True)
    child_ids=set(row['source_person_ids']);parent_ids=set(parent['source_person_ids'])
    if step['traversal']=='parent_to_child':assert current in parent_ids and step['to_person_id']in child_ids
    else:assert step['traversal']=='child_to_parent'and current in child_ids and step['to_person_id']in parent_ids
   else:raise AssertionError('Unsupported graph step')
   current=step['to_person_id'];assert current not in seen;seen.add(current)
  assert current==tm['person_id']and used==set(sources)
 except (AssertionError,KeyError,TypeError,ValueError,IndexError,OSError,StopIteration)as exc:
  raise ValueError('來源圖復姓須普通assembly狀態、完整current frames、實際反查及有限父系步驟；不得推姓名或偽已驗狀態')from exc
