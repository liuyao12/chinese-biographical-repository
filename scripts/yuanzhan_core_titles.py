"""Finite source-bound core titles, with no permanent person identifier."""
from pathlib import Path
import hashlib,json,copy
KIND='institutional_epitaph_core_titles'
def _load(n):return json.loads((Path(__file__).parent/n).read_text(encoding='utf-8'))
def render(ch,root):
 pin=_load('yuanzhan_core_title_source_pin.json');p,=ch['paragraphs'];assert ch['id']==pin['chapter_id']and ch['source_id']==pin['source_id']and p['id']==pin['paragraph_id']
 assert hashlib.sha256(p['text'].encode()).hexdigest()==pin['paragraph_sha256']
 assert hashlib.sha256(json.dumps(ch['source'],sort_keys=True,ensure_ascii=False).encode()).hexdigest()==pin['source_sha256']
 assert root is not None and hashlib.sha256((Path(root)/pin['transcription_path']).read_bytes()).hexdigest()==pin['transcription_sha256']
 m,=[m for m in p['mentions']if m['id']==pin['head_mid']];assert m['kind']=='person'and m['surface']=='湛'and m['start']==109 and m['end']==110 and isinstance(m['person_id'],str)and m['person_id']
 out=copy.deepcopy(_load('yuanzhan_core_title_templates.json'))
 for h in out:h['person_id']=m['person_id']
 return out

def valid(h,ch,root=None):
 try:
  assert isinstance(h,dict)and isinstance(h.get('source_career_role'),dict)and h['source_career_role']['kind']==KIND
  expected,=[x for x in render(ch,root)if x['id']==h['id']];return h==expected
 except(AssertionError,KeyError,TypeError,ValueError,OSError,StopIteration,IndexError):return False
