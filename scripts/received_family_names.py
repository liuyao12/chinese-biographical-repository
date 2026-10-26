"""Names read from a fixed received witness and its already validated near kin.
No labels, structural ID ancestry, spouses, invented fathers or global aliases.
"""
from pathlib import Path
import hashlib,json
KIND='contextual_surname_from_fixed_received_kinship'
def witness(c,root,ref):
 root=Path(root).resolve();rel=Path(ref['path']);p=root/rel;assert set(ref)=={'path','sha256'}and not rel.is_absolute()and'..'not in rel.parts and rel.parts[0]=='source-evidence'and p.resolve()==p
 rb=p.read_bytes();assert hashlib.sha256(rb).hexdigest()==ref['sha256'];w=json.loads(rb);s=c['source'];assert w['chapter_id']==c['id']and w['source_commit']==s['source_commit']and w['raw_sha256']==s['raw_file_sha256']and w['raw_file']==s['raw_path'];assert w['units']==[dict(paragraph_id=p['id'],text=p['text'],text_layer=p['text_layer'],source_position=p['source_position'])for p in c['paragraphs']]
 rel=Path(w['raw_file']);p=root/rel;assert not rel.is_absolute()and'..'not in rel.parts and rel.parts[0]=='sources'and p.resolve()==p;rb=p.read_bytes();assert hashlib.sha256(rb).hexdigest()==w['raw_sha256'];ls=rb.decode().splitlines(keepends=True)
 for p in c['paragraphs']:
  fs=p['source_position']['source_fragments'];assert ''.join(f['text']for f in fs)==p['text']
  for f in fs:assert ls[f['line']-1][f['raw_start']:f['raw_end']]==f['text']
def source_component_valid(n,c,root):
 if isinstance(n,dict) and isinstance(n.get('component_source_binding'),dict) and n['component_source_binding'].get('kind')=='fixed_wyd_song044_name_component':
  try:from .wyd_song044_names import component_valid
  except ImportError:from wyd_song044_names import component_valid
  return component_valid(n,c,root)
 try:
  b=n['component_source_binding'];assert b['kind']=='fixed_received_name_component';p=next(p for p in c['paragraphs']if p['id']==n['paragraph_id']);m=next(m for m in p['mentions']if m['id']==n['person_mention_id']);assert m['kind']=='person'and m['person_id']==n['person_id']and n['chapter_id']==c['id']and n['quote']==p['text']and n['human_reviewed']is False and n['status']in('editorial_provisional','contextual_provisional');assert b['source_revision']==c['source']['revision_id']and b['paragraph_sha256']==hashlib.sha256(p['text'].encode()).hexdigest();witness(c,root,b['fixed_witness_reference'])
  form=b['name_form']
  if form=='full_name':assert n['surname']and n['ming']and m['surface']==n['surname']+n['ming']and not n.get('surname_basis')
  elif form=='ming_only':assert n['ming']and m['surface']==n['ming']and n['surname_basis']['kind']==KIND
  elif form=='sister_clan':assert n['ming']is None and m['surface']=='妹'and n['clan_style']['kind']=='bound_named_sister_clan_appellation'and n['clan_style']['value']==n['surname']+'氏'and n['surname_basis']['kind']==KIND
  else:raise AssertionError('unsupported name role')
  if 'zi'in n:
   a=b['courtesy_anchor'];assert a==dict(paragraph_id=p['id'],start=m['end']+1,end=m['end']+1+len(n['zi']),surface=n['zi'])and p['text'][m['end']:a['end']]=='字'+n['zi']
  else:assert 'courtesy_anchor'not in b
  assert set(b)=={'kind','name_form','paragraph_sha256','source_revision','fixed_witness_reference'}|({'courtesy_anchor'}if'zi'in n else set())
  return True
 except(AssertionError,KeyError,ValueError,TypeError,OSError,IndexError,StopIteration):return False

def validate(n,names,chapters,assertions,root):
 try:
  b=n['surname_basis'];assert b['kind']==KIND and set(b)=={'kind','status','human_reviewed','rationale','source_name_record_id','source_full_quote','fixed_witness_reference','steps'}and b['status']=='contextual_provisional'and b['human_reviewed']is False and b['rationale']and n['status']=='contextual_provisional';c=chapters[n['chapter_id']];assert source_component_valid(n,c,root)
  seed,=[x for x in names if x.get('id')==b['source_name_record_id']];assert seed['chapter_id']==c['id']and not seed.get('surname_basis')and seed['surname']==n['surname']and seed['quote']==b['source_full_quote']and source_component_valid(seed,c,root)and b['fixed_witness_reference']==seed['component_source_binding']['fixed_witness_reference'];assert seed['component_source_binding']['name_form']=='full_name'
  aa={a['id']:a for a in assertions};assert len(aa)==len(assertions);paragraphs={p['id']:(c['id'],p)for p in c['paragraphs']};steps=b['steps'];assert 1<=len(steps)<=3;current=seed['person_id'];seen={current};used=set();gen=0
  try:from scripts.received_quoted_family import valid as kin_valid
  except ImportError:from received_quoted_family import valid as kin_valid
  for index,step in enumerate(steps):
   assert set(step)=={'assertion_id','from_person_id','to_person_id','traversal','generation_before','generation_after','evidence'}and step['from_person_id']==current and step['assertion_id']not in used and step['to_person_id']not in seen and step['generation_before']==gen and type(step['generation_before'])is int and type(step['generation_after'])is int
   a=aa[step['assertion_id']];q=a['qualifiers'];assert kin_valid(a,paragraphs,{c['id']:c},root)and step['evidence']==a['evidence']and all(e['chapter_id']==c['id']for e in a['evidence']);assert not any(q.get(k)for k in('adoptive','sworn','same_mother_only'))and q.get('shared_father')is not False and q.get('lineage')not in('maternal','non_paternal')
   direction=step['traversal'];dest=step['to_person_id'];predicate=a['predicate']
   if direction=='father_to_child':assert predicate=='father'and(a['object_person_id'],a['subject_person_id'])==(current,dest);delta=1
   elif direction=='child_to_father':assert predicate=='father'and(a['subject_person_id'],a['object_person_id'])==(current,dest);delta=-1
   elif direction=='child_to_grandfather':assert predicate=='grandfather'and q['lineage']=='paternal'and(a['subject_person_id'],a['object_person_id'])==(current,dest);delta=-2
   elif direction=='older_to_younger':assert predicate=='brother'and(a['object_person_id'],a['subject_person_id'])==(current,dest);delta=0
   elif direction=='older_brother_to_younger_sister_clan':assert predicate=='sister'and(a['object_person_id'],a['subject_person_id'])==(current,dest)and index==len(steps)-1 and n['ming']is None and n['component_source_binding']['name_form']=='sister_clan';delta=0
   else:raise AssertionError('no spouse/adoption/affine/cousin or inferred-parent traversal')
   gen+=delta;assert step['generation_after']==gen;current=dest;seen.add(current);used.add(a['id'])
  assert current==n['person_id']
  if n['ming']is None:assert clan_valid(n,next(p for p in c['paragraphs']if p['id']==n['paragraph_id']),assertions)
 except(AssertionError,KeyError,ValueError,TypeError,OSError,IndexError,StopIteration):raise ValueError('Surname requires a fixed received full-name seed and at most three fully bound source father/grandfather/brother steps; no family-ID or marital surname inference')

def clan_valid(n,p,relations):
 try:
  st=n['clan_style'];assert st['kind']=='bound_named_sister_clan_appellation'and st['status']=='editorial_provisional'and n['surname_basis']['kind']==KIND and n['ming']is None and st['value']==n['surname']+'氏';a,=[a for a in relations if a['id']in st['assertion_ids']];assert st['assertion_ids']==[a['id']]and a['predicate']=='sister'and a['subject_person_id']==n['person_id']and a['qualifiers']['source_kinship_frame']['rule']=='wife_named_brother_sister';e,=a['evidence'];assert e['paragraph_id']==n['paragraph_id']==p['id']and e['quote']==n['quote']==p['text'];ms={m['id']:m for m in p['mentions']};brother=ms[e['object_person_mention_id']];sister=ms[e['subject_person_mention_id']];assert brother['person_id']==a['object_person_id']and sister['person_id']==n['person_id']and brother['surface'].startswith(n['surname'])and sister['surface']=='妹'and p['text'][brother['end']:sister['start']]=='之'and st['source_term']==brother['surface']+'之'+sister['surface']and n['person_mention_id']==sister['id'];return True
 except(AssertionError,KeyError,ValueError,TypeError,IndexError,StopIteration):return False
