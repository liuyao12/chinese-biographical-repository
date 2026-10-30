"""Finite typed continuation of the complete 031 comparison unit; no new text parser."""
from pathlib import Path
import json,hashlib,copy
try:
 from scripts import fixed_jin031_jia_comparison as core
except ImportError:
 import fixed_jin031_jia_comparison as core
EP='source-evidence/jin031-jia-comparison/typed-phase-proof.json'
PROOF_SHA='6487c1ce4f48bf53fb96dff69ede69c2b4ef2d970dd1dee0847068b4f215150c'
KIND='fixed_jin031_complete_unit_typed'
def proof(root):
 data=core.path(root,EP).read_bytes();core.need(core.H(data)==PROOF_SHA,'typed證照漂移')
 try:from scripts.fixed_jin031_jia_remaining_titles import effective as title_effective
 except ImportError:from fixed_jin031_jia_remaining_titles import effective as title_effective
 return title_effective(json.loads(data),root)
def effective(parent,root):
 if not (Path(root)/EP).is_file():return parent
 b=proof(root);core.need(core.H(core.path(root,'source-evidence/jin031-jia-comparison/full-ner-proof.json').read_bytes())==b['parent_ner_sha256'],'typed原NER證照');out=copy.deepcopy(parent)
 for k,v in b['annotation_additions'].items():core.need(k not in out['chapter_template']['annotation'],'typed不得覆舊annotation');out['chapter_template']['annotation'][k]=v
 try:from scripts.fixed_jin031_jia_remaining_titles import additional_mentions
 except ImportError:from fixed_jin031_jia_remaining_titles import additional_mentions
 return additional_mentions(out,b)

def validate_documents(root,roles):
 b=proof(root);core.need(core.H(core.path(root,core.fixed(root)['raw_path']).read_bytes())==b['source_sha256'],'typed原raw漂移')
 cal=b['calendar_reference'];cb=core.path(root,cal['path']).read_bytes();core.need(core.H(cb)==cal['sha256'] and cal['complete_row'] in cb.decode() and "<tr id='av474'>"in cal['complete_row'] and '西晉'in cal['complete_row'] and '>265<'in cal['complete_row'] and '>274<'in cal['complete_row'],'typed西晉泰始官方列')
 for path,value in b['expected_documents'].items():core.need(core.read(root,path)==core.expand(value,roles),'typed sidecar缺失/額外或單端漂移 '+path)
 return b

def state(ch,root):
 core.need(root is not None and ch is not None,'typed須完整章及root')
 try:from scripts import fixed_jin031_jia_full_ner as ner
 except ImportError:import fixed_jin031_jia_full_ner as ner
 r,parent=ner.prepared(ch,root);b=validate_documents(root,r)
 return b,r

def family_applies(a):return a.get('qualifiers',{}).get('source_clause_binding',{}).get('rule')=='fixed_jin031_typed_complete_unit'
def family_valid(a,paragraphs,root):
 try:
  b,r=state(core.read(root,core.CH),root);want=core.expand(b['expected_documents']['corpus/jinshu/031-jia-comparison-assertions.json'],r)['assertions'];core.need(a in want,'typed親屬完整記錄')
  for e in a['evidence']:core.need(paragraphs[e['paragraph_id']][0]==core.CID and paragraphs[e['paragraph_id']][1]==next(p for p in core.read(root,core.CH)['paragraphs']if p['id']==e['paragraph_id']),'typed caller全段')
  return True
 except (ValueError,KeyError,TypeError,OSError,IndexError,StopIteration,AttributeError):return False

def holding_valid(h,ch,root):
 try:
  b,r=state(ch,root);return h in core.expand(b['expected_documents']['corpus/jinshu/031-jia-comparison-titles.json'],r)['holdings']
 except (ValueError,KeyError,TypeError,OSError,IndexError,StopIteration,AttributeError):return False

def age_valid(age,p,root,chapter):
 try:
  b,r=state(chapter,root);want=core.expand(b['annotation_additions']['age_assertions'],r);core.need(age in want and age.get('subject_scope',{}).get('kind')=='quoted_appearance_estimate','typed外貌估齡完整記錄')
  full=next(x for x in chapter['paragraphs']if x['id']==p['id']);core.need(full==p and p['text_layer']=='received_chapter','typed估齡全段')
  # Common approximate-age qualifications remain mandatory; source expression is not a bound.
  core.need(age['value']is None and age['birth_year']is None and 'bounds'not in age and 'normalized_date'not in age and age['approximation']=={'kind':'adjacent_age_numbers','numbers':[35,36]} and age['reporting_status']=='approximate_report'and age['unit']=='source_age_years'and age['counting']=='unspecified_source_age'and age['status']=='source_attested'and age['human_reviewed']is False and bool(age['reviewer']),'typed估齡不可變確歲/享年/生年')
  return True
 except (ValueError,KeyError,TypeError,OSError,IndexError,StopIteration,AttributeError):return False

def difference_valid(age,chapter,root):
 try:
  b,r=state(chapter,root);return age in core.expand(b['annotation_additions']['age_difference_assertions'],r)
 except (ValueError,KeyError,TypeError,OSError,IndexError,StopIteration,AttributeError):return False

def fixture_paths(root):
 """Exact finite phase inputs for portable isolated negative tests, not a validation bypass."""
 try:from scripts import fixed_jin031_jia_full_ner as ner
 except ImportError:import fixed_jin031_jia_full_ner as ner
 parent=core.fixed(root);b=ner.fixed(root)
 paths={core.CH,core.EP,core.NS,core.AD,ner.EP,ner.IP,ner.NSN,EP,'registry/persons.json','data/corpus/chapter-directory.json',b['raw_path'],parent['father_assertion']['native_path'],parent['father_name']['native_path']}
 paths.update(s['native_path']for s in parent['seeds']+b['external_roles'])
 if(Path(root)/EP).is_file():
  t=proof(root);paths.update(t['expected_documents']);paths.add(t['calendar_reference']['path'])
 if(Path(root)/'source-evidence/jin031-jia-comparison/remaining-titles-phase-proof.json').is_file():
  try:from scripts.fixed_jin031_jia_remaining_titles import fixture_paths as remaining_paths
  except ImportError:from fixed_jin031_jia_remaining_titles import fixture_paths as remaining_paths
  paths.update(remaining_paths(root))
 return paths
