"""Narrow adapter to the existing full received-biography family clause validator.
The independent fixed excerpt pins contain no person IDs; all endpoints follow MIDs.
"""
from pathlib import Path
import hashlib,json
PROOF_SHA='de1a48adfa6dbeaa585d912946c6addb3b49c9c08e2b9f5139a33115be1d2eba'
RULES={'named_children_list','son_heir_childless_younger_brother_supplies_son','younger_brother'}
def valid(a,ch,assertions):
 try:
  raw=(Path(__file__).resolve().parents[1]/'source-evidence/name-context/jin079-xie-family.json').read_bytes()
  assert hashlib.sha256(raw).hexdigest()==PROOF_SHA;pinned=json.loads(raw)
  assert all(ch[k]==pinned[k]for k in('work_id','book_id','source_id'))and ch['id']==pinned['chapter_id']and ch['source']['revision_id']==pinned['source_revision']and ch['source']['wikitext_sha256']==pinned['wikitext_sha256']
  ps={p['id']:p for p in ch['paragraphs']}
  for fixed in pinned['paragraphs']:
   p=ps[fixed['id']];assert p['text']==fixed['text']and p['text_layer']==fixed['text_layer']and p['source_position']['revision_id']==pinned['source_revision']
   assert [{k:m[k]for k in('id','start','end','surface','kind')}for m in p['mentions']]==fixed['mentions']
  q=a['qualifiers'];b=q['source_clause_binding'];assert b['kind']=='biography_family_clause'and b['rule']in RULES and a['predicate']in('father','brother')and not q.get('adoptive')and not q.get('same_mother_only')and q.get('lineage')not in('maternal','non_paternal')
  try:from .biography_family_clause import valid as family_valid
  except ImportError:from biography_family_clause import valid as family_valid
  return family_valid(a,{p['id']:(ch['id'],p)for p in ch['paragraphs']},assertions,{ch['id']:ch})
 except (AssertionError,KeyError,TypeError,ValueError,OSError,IndexError,AttributeError):return False
