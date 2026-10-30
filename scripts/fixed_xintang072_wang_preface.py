"""Only the reviewed 404-character Wang preface, not a generic genealogy parser."""
from pathlib import Path
import json
CID='c-xintangshu-072zhong-wyd1739-wang-preface'
PATH='corpus/xintangshu/072zhong-wyd1739-wang-preface.json'
SURNAME_KIND='contextual_surname_from_fixed_repository_witness'
FULL_NAME_KIND='fixed_repository_witness_unsplit_name'
FAMILY_RULE='fixed_repository_witness_near_parent'
def current(root):return json.loads((Path(root)/PATH).read_bytes())
def validate_surname(name,names,chapters,assertions,root):
 try:
  from scripts.fixed_repository_witness import record_valid
 except ImportError:from fixed_repository_witness import record_valid
 if (name.get('chapter_id')!=CID or name.get('surname_basis',{}).get('kind')!=SURNAME_KIND
     or chapters.get(CID)!=current(root) or sum(n==name for n in names)!=1
     or not record_valid(name,root,'person_name_component_set')):
  raise ValueError('王氏前敘復姓須完整固定本源、始氏後具名位置及精確姓名行；始氏前不冠王，不採遠祖譜為真')
def full_name_valid(name,paragraph,chapter,root):
 try:
  from scripts.fixed_repository_witness import record_valid
 except ImportError:from fixed_repository_witness import record_valid
 try:
  c=current(root)
  return (name.get('chapter_id')==CID and chapter==c and paragraph==next(p for p in c['paragraphs']if p['id']==name['paragraph_id'])
          and name.get('full_name_basis',{}).get('kind')==FULL_NAME_KIND and record_valid(name,root,'person_name_component_set'))
 except(KeyError,ValueError,TypeError,OSError,StopIteration,AttributeError):return False

# These are source anchors and literal relationship clauses, not person-ID lists.
NEAR_PARENT_SLOTS={
 'a-xintang072-wyd-qian_liang-father':('p002:m0195','p002:m0211','儉','騫'),
 'a-xintang072-wyd-gui_liang-father':('p002:m0211','p003:m0004','騫','規'),
 'a-xintang072-wyd-bao_zhou-father':('p003:m0004','p003:m0017','規','褒'),
 'a-xintang072-wyd-zi_sui-father':('p003:m0018','p003:m0033','褒','鼒')}
def near_pair_valid(a,c,root):
 try:
  pmid,cmid,ps,cs=NEAR_PARENT_SLOTS[a['id']]
  markers={m['id']:(p,m)for p in c['paragraphs']for m in p['mentions']}
  pp,pm=markers[CID+':'+pmid];cp,cm=markers[CID+':'+cmid]
  b=a['qualifiers']['source_clause_binding']
  if not(pm['surface']==ps and cm['surface']==cs and pm['kind']==cm['kind']=='person'
         and a['subject_person_id']==cm['person_id'] and a['object_person_id']==pm['person_id']
         and a['subject_person_id']!=a['object_person_id'] and cp['text'][cm['start']-1:cm['end']]=='生'+cs
         and b['parent_mention_id']==pm['id'] and b['child_mention_id']==cm['id']
         and a['qualifiers']['lineage']=='paternal' and 'adopted_for_family_tree'not in a['qualifiers']):return False
  base=Path(root)/'source-evidence/xintang072zhong-wyd1739-wang-preface'
  liang=(base/'liang041-complete-unit.wikitext').read_text();zhou=(base/'zhou041-complete-unit.wikitext').read_text()
  # Read the entire fixed comparison units; preserve their different spellings
  # and source dates, never treat their modern digital revision as composition.
  return ('王規字威明，琅邪臨沂人。祖儉，齊太尉南昌文憲公。父騫' in liang
          and '子褒，字子漢' in liang
          and '王襃字子淵，琅邪臨沂人也。曾祖儉' in zhou
          and '祖騫，梁侍中、金紫光祿大夫、南昌安侯。父規' in zhou
          and '子鼒嗣。' in zhou)
 except(KeyError,ValueError,TypeError,OSError):return False

def family_valid(assertion,paragraphs,chapters,root):
 try:
  from scripts.fixed_repository_witness import record_valid
 except ImportError:from fixed_repository_witness import record_valid
 try:
  c=current(root)
  if (assertion.get('predicate')!='father' or assertion.get('qualifiers',{}).get('source_clause_binding',{}).get('rule')!=FAMILY_RULE
      or (chapters or {}).get(CID)!=c or not record_valid(assertion,root,'person_assertion_set')or not near_pair_valid(assertion,c,root)):return False
  by={p['id']:p for p in c['paragraphs']}
  return all(e['chapter_id']==CID and paragraphs.get(e['paragraph_id'])==(CID,by[e['paragraph_id']])for e in assertion['evidence'])
 except(KeyError,ValueError,TypeError,OSError,StopIteration,AttributeError):return False
