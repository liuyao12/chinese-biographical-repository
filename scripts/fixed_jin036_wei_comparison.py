"""Complete fixed-revision rendered Wei unit; unknown print, comparison only."""
from pathlib import Path
import hashlib,json
CID='c-jinshu-036-wei-comparison'
SID='s-jinshu036-wei-ws2108231-rendered-comparison'
CH='corpus/jinshu/036-wei-comparison.json'
BASE='source-evidence/jin036-wei-comparison/'
PINS={'rendered-extract.txt': '6db27cbd14cb251ba7ab4e58e9064b02d808cd893b02c044e359c7ccedd73659', 'projection.json': '28e2542d54d18654527a0cc681747bf0139dd5fdf12702091e7a5ad89ab313a1', 'acquisition-qualification.json': '187f26a7ec5bb2ee7360cb7d3f58943ee000916b6ea8dea1a40702a9f5a9ef37', 'contract.json': 'e8e27d35c69585f272f25da06a5aad7d4337f8b5e65f42288daddb2acd15164c'}
def validate_source(ch,root):
 root=Path(root).resolve()
 def fixed(name):
  rel=BASE+name;p=(root/rel).resolve()
  if not p.is_relative_to(root/'source-evidence')or p!=root/rel:raise ValueError('本源來源路徑越界或symlink')
  data=p.read_bytes()
  if hashlib.sha256(data).hexdigest()!=PINS[name]:raise ValueError('固定比較見證SHA不同：'+name)
  return data
 contract=json.loads(fixed('contract.json'));projection=json.loads(fixed('projection.json'));qual=json.loads(fixed('acquisition-qualification.json'));capture=fixed('rendered-extract.txt').decode()
 if ch!=contract['chapter_template']:raise ValueError('完整21段/原字/層/空mentions/pending/比較資格/現代註不符')
 if projection['capture_sha256']!=hashlib.sha256(capture.encode()).hexdigest()or projection['source_response_sha256']!=qual['acquisition']['response_sha256']:raise ValueError('rendered extract與私有HTML回應不得混用hash')
 if len(projection['blocks'])!=25 or sum(len(x['text'])for x in projection['blocks'])!=7145 or len(projection['headings_not_body'])!=4:raise ValueError('完整25數位blocks/4題頭範圍')
 for b in projection['blocks']:
  if capture[b['capture_start']:b['capture_end']]!=b['text']:raise ValueError('原rendered block切片不符')
 ps=ch['paragraphs'];units=projection['units']
 if len(ps)!=21 or len(units)!=21 or sum(len(p['text'])for p in ps)!=7129:raise ValueError('完整21正文段/7129字範圍')
 for p,u in zip(ps,units):
  ix=u['capture_character_offsets']
  if not all(type(i)is int and u['capture_start']<=i<u['capture_end']for i in ix)or ix!=sorted(set(ix)):raise ValueError('投影字位無效')
  if ''.join(capture[i]for i in ix)!=p['text']or hashlib.sha256(p['text'].encode()).hexdigest()!=u['text_sha256']or p['id']!=u['paragraph_id']:raise ValueError('原字投影/段落不符')
 note=projection['modern_note']
 if capture[note['capture_marker_start']:note['capture_marker_end']]!='[1]'or capture[note['capture_note_start']:note['capture_note_end']]!=note['raw_text']or ch['annotation']['modern_collation_reports']!=[note]:raise ValueError('現代數位footnote與正文分層不符')
 if qual['edition']is not None or qual['human_reviewed']is not False or qual['image_verified']is not False or qual['preferred_text_base']is not False:raise ValueError('未知印本/AI比較資格不可升格')
 return True
def source_errors(ch,root,source_path=None):
 if not isinstance(ch,dict):return ['晉036章不是物件']
 a=ch.get('annotation');owned=source_path is not None and Path(source_path).resolve()==(Path(root)/CH).resolve()
 if not owned and ch.get('id')!=CID and ch.get('source_id')!=SID and not(isinstance(a,dict)and a.get('fixed_rendered_capture_contract')=='jin036_complete_wei_source_only_v1'):return []
 try:validate_source(ch,root);return []
 except(ValueError,KeyError,TypeError,OSError,UnicodeError,IndexError)as exc:return ['晉036完整比較單元：'+str(exc)]

# This phase validates the complete actual chapter before delegating to the unchanged source-only witness.
_source_only_validate_source=validate_source
def validate_source(ch,root):
 if 'fixed_jin036_full_ner_ref'in ch.get('annotation',{})or(Path(root)/(BASE+'ner-phase.json')).is_file():
  try:from scripts.fixed_jin036_wei_ner import validate_source as ner_source
  except ImportError:from fixed_jin036_wei_ner import validate_source as ner_source
  return ner_source(ch,root)
 return _source_only_validate_source(ch,root)
