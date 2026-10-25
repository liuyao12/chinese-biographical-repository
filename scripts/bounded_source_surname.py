"""Opt-in exact legacy-unit names and a pinned quoted paternal-grandfather reading."""
from pathlib import Path
import json,hashlib
KIND='bounded_source_name_components'
def strict(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys()and all(strict(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(strict(x,y)for x,y in zip(a,b))
 return a==b
def valid(n,names,chapters,assertions,root):
 try:
  assert isinstance(n,dict)and isinstance(names,list)and isinstance(chapters,dict)and isinstance(assertions,list)and root is not None
  root=Path(root).resolve();b=n['bounded_source_name_binding'];assert isinstance(b,dict)and b['kind']==KIND
  p=root/'scripts/bounded_source_surname.json';assert p.resolve()==p;cfg=json.loads(p.read_text());assert cfg['format_version']=='0.1';proof=cfg['proofs'][b['key']];f=proof['frame'];c=chapters[f['dimensions']['id']]
  path=root/f['native_path'];assert path.resolve()==path and json.loads(path.read_bytes())==c
  assert all(c[k]==v for k,v in f['dimensions'].items())and c['source']['revision_id']==f['source_revision']
  assert all(c['source'].get(k)==v for k,v in f['source_metadata'].items())
  rawrel=Path(f['raw_file']);assert not rawrel.is_absolute()and'..'not in rawrel.parts and rawrel.parts[0]in('source-evidence','sources');raw=root/rawrel;assert raw.resolve()==raw and hashlib.sha256(raw.read_bytes()).hexdigest()==f['raw_sha256']
  assert len(c['paragraphs'])==len(f['paragraphs']);mids={}
  for actual,expected in zip(c['paragraphs'],f['paragraphs']):
   assert all(actual[k]==expected[k]for k in('id','text','text_layer','source_position'))
   stripped=[{k:v for k,v in m.items()if k!='person_id'}for m in actual['mentions']];assert stripped==expected['mentions']
   for m in actual['mentions']:
    if m['kind']=='person':assert actual['text'][m['start']:m['end']]==m['surface'];mids[m['id']]=m
  def expand(v):
   if isinstance(v,dict):
    if set(v)=={'$person_mid'}:return mids[v['$person_mid']]['person_id']
    return {k:expand(x)for k,x in v.items()}
   if isinstance(v,list):return [expand(x)for x in v]
   return v
  expected_names=expand(proof['required_name_records']);expected={v['id']:v for v in expected_names};assert n['id']in expected and strict(n,expected[n['id']])
  for rid,value in expected.items():actual,=[x for x in names if x.get('id')==rid];assert strict(actual,value)
  wanted=expand(proof['assertions']);aa={a['id']:a for a in assertions};assert len(aa)==len(assertions);assert all(strict(aa[a['id']],a)for a in wanted)
  seed=expected[proof['seed_name_record_id']];sm=mids[seed['person_mention_id']];assert sm['surface']==seed['surname']+seed['ming']and not seed.get('surname_basis')
  for record in expected_names:
   mark=mids[record['person_mention_id']];assert mark['person_id']==record['person_id']
   if record.get('surname_basis'):
    assert record['status']=='contextual_provisional'and record['human_reviewed']is False and record['surname']==seed['surname']and mark['surface']==record['ming']
   elif record['id']!=seed['id']:assert record['surname']is None and record['ming']==mark['surface']
  if proof['kind']=='legacy_biography':
   assert len(c['paragraphs'])==19
   try:from scripts.biography_family_clause import valid as clause_valid
   except ImportError:from biography_family_clause import valid as clause_valid
   ps={p['id']:(c['id'],p)for p in c['paragraphs']}
   assert all(a['predicate']=='father'and a['status']=='source_attested'and not a['qualifiers'].get('adoptive')and clause_valid(a,ps,assertions,{c['id']:c})for a in wanted)
   for record in expected_names:
    if not record.get('surname_basis'):continue
    current=seed['person_id'];seen={current};generation=0
    for s in record['surname_basis']['steps']:
     a=aa[s['assertion_id']];assert a in wanted and s['from_person_id']==current and s['generation_before']==generation
     if s['traversal']=='object_to_subject':assert a['object_person_id']==current and a['subject_person_id']==s['to_person_id'];generation+=1
     else:assert s['traversal']=='subject_to_object'and a['subject_person_id']==current and a['object_person_id']==s['to_person_id'];generation-=1
     assert s['generation_after']==generation and s['to_person_id']not in seen;current=s['to_person_id'];seen.add(current)
    assert current==record['person_id']
  elif proof['kind']=='note_paternal_ancestor':
   try:from scripts.fixed_kanripo_fact_slots import grammar
   except ImportError:from fixed_kanripo_fact_slots import grammar
   grammar(c,root);g=aa[proof['grandfather_assertion_id']];father=aa[proof['father_assertion_id']]
   assert g['predicate']=='grandfather'and g['qualifiers']['lineage']=='paternal'and g['subject_person_id']==father['subject_person_id']==seed['person_id']and father['predicate']=='father'and len({g['subject_person_id'],g['object_person_id'],father['object_person_id']})==3
   target=next(x for x in expected_names if x.get('surname_basis'));assert g['object_person_id']==target['person_id']and target['surname_basis']['generation_distance']==2
   e,=g['evidence'];para=next(p for p in c['paragraphs']if p['id']==e['paragraph_id']);assert para['text_layer']=='witness_appended_pei_songzhi_note'and para['text'].startswith('魏書曰')
  else:raise AssertionError('Unknown bounded source proof')
  return True
 except(AssertionError,KeyError,TypeError,ValueError,AttributeError,IndexError,StopIteration,OSError):return False

def validate(n,names,chapters,assertions,root):
 if not valid(n,names,chapters,assertions,root):raise ValueError('Bounded source surname requires exact full unit, raw pin, full-name seed and validated source roles; no edited father or label surname')
