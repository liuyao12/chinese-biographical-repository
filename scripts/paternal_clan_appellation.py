"""Finite source-first clan style, retaining an unnamed woman's unknown ming."""
from pathlib import Path
import json,hashlib
PROOF_SHA='cdf313175baa2e4a9a690b9802d91b60c523ead486dfa807c97e3c5d0f776778'
def valid(n,p,relations):
 if isinstance(n,dict)and isinstance(n.get('clan_style_basis'),dict)and n['clan_style_basis'].get('kind')=='fixed_comparison_jin080_paternal_role':
  try:from scripts.fixed_jin080_wangxizhi_comparison import clan_valid
  except ImportError:from fixed_jin080_wangxizhi_comparison import clan_valid
  return clan_valid(n,p,relations)
 try:
  root=Path(__file__).resolve().parents[1];raw=(root/'source-evidence/name-context/xie-women-paternal-clans.json').read_bytes();assert hashlib.sha256(raw).hexdigest()==PROOF_SHA
  cases=json.loads(raw);basis=n['clan_style_basis'];assert set(basis)=={'kind','case_id','parent_full_name_source','father_assertion_id','local_father_mention_id'}and basis['kind']=='fixed_explicit_father_and_literal_parent_name';case,=[c for c in cases if c['case_id']==basis['case_id']];assert basis['local_father_mention_id']==case['father_mention_id']
  def frame(f):
   rel=Path(f['native_path']);assert not rel.is_absolute()and rel.parts[0]=='corpus'and '..'not in rel.parts
   c=json.loads((root/rel).read_bytes());assert all(c[k]==f[k]for k in('work_id','book_id','source_id'))and c['id']==f['chapter_id']and all(c['source'][k]==v for k,v in f['source_fingerprints'].items())
   q,=[q for q in c['paragraphs']if q['id']==f['paragraph_id']];assert q['text']==f['quote']and q['text_layer']=='received_chapter'and[{k:m[k]for k in('id','start','end','surface','kind')}for m in q['mentions']]==f['mentions'];return c,q,{m['id']:m for m in q['mentions']}
  ch,q,ms=frame(case['source']);sc,sp,sms=frame(case['seed']);assert p==q and n['chapter_id']==ch['id']and n['paragraph_id']==p['id']and n['quote']==p['text']and n['person_mention_id']==case['woman_mention_id']
  woman=ms[case['woman_mention_id']];father=ms[case['father_mention_id']];seed=sms[case['seed_mention_id']];assert all(m['kind']=='person'for m in(woman,father,seed))and woman['person_id']==n['person_id']and father['person_id']==seed['person_id']and father['person_id']!=woman['person_id']and seed['surface']==case['surname']+case['father_ming']
  st=n['clan_style'];assert set(st)=={'kind','value','source_term','assertion_ids','status','rationale','human_reviewed'}and st['kind']=='paternal_clan_appellation'and st['value']==case['surname']+'氏'and st['source_term']==case['source_term']and st['assertion_ids']==[case['assertion_id']]and st['status']=='editorial_provisional'and st['human_reviewed']is False and st['rationale'].strip()
  assert n['surname']==case['surname']and n['ming']is None and 'full_name'not in n and n['status']=='contextual_provisional'and n['human_reviewed']is False
  ref={k:v for k,v in case['seed'].items()if k!='mentions'};ref.update(person_mention_id=seed['id'],parent_person_id=father['person_id'],surface=seed['surface']);assert basis['parent_full_name_source']==ref and basis['father_assertion_id']==case['assertion_id']
  a,=[a for a in relations if a['id']==case['assertion_id']];assert a['predicate']=='father'and a['status']=='source_attested'and a['subject_person_id']==woman['person_id']and a['object_person_id']==father['person_id']and a['qualifiers']['lineage']=='paternal'and not a['qualifiers'].get('adoptive')and a['qualifiers']['source_term']==case['source_term'];e,=a['evidence'];assert e['quote']==p['text']and e['paragraph_id']==p['id']and e['chapter_id']==ch['id']and all(e[k]==ch[k]for k in('work_id','book_id','source_id'))
  if case['mode']=='adjacent_daughter':assert woman['surface']=='女'and father['end']==woman['start']and p['text'][father['start']:woman['end']]==father['surface']+'女'and e['subject_person_mention_id']==woman['id']
  elif case['mode']=='wife_father':
   try:from .wife_father_clause import wife_father_clause_valid
   except ImportError:from wife_father_clause import wife_father_clause_valid
   assert wife_father_clause_valid(a,{p['id']:(ch['id'],p)},{ch['id']:ch})and a['qualifiers']['wife_father_context']['father_mention_id']==father['id']and a['qualifiers']['wife_father_context']['wife_mention_id']==woman['id']
  else:
   assert case['mode']=='father_arranged_marriage'
   try:from .biography_family_clause import valid as family_valid
   except ImportError:from biography_family_clause import valid as family_valid
   assert family_valid(a,{p['id']:(ch['id'],p)},relations,{ch['id']:ch})and a['qualifiers']['source_clause_binding']['roles']['father']==father['id']and a['qualifiers']['source_clause_binding']['roles']['daughter']==woman['id']
  return True
 except (AssertionError,KeyError,ValueError,TypeError,OSError,IndexError,AttributeError):return False
