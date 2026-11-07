"""Test-only successor pin propagation: do not short-circuit any production validator."""
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
@contextmanager
def synchronized_minimal_parent_pins(fixture_root):
 root=Path(fixture_root).resolve()
 if root==ROOT.resolve():raise ValueError('Only an independent temporary fixture may be mutated')
 from scripts import fixed_jin034_yanghu_ner as core
 rel=core.BASE+'minimal-life-phase.json';target=root/rel
 if not target.is_file():
  yield
  return
 from scripts import fixed_jin034_minimal_life as minimal
 before=target.read_bytes();assert hashlib.sha256(before).hexdigest()==minimal.PROOF_SHA,'fixture minimal proof was already changed'
 value=json.loads(before);after=json.loads(before)
 after['parent_ner_sha256']=hashlib.sha256((root/core.EP).read_bytes()).hexdigest()
 after['parent_close_kin_sha256']=hashlib.sha256((root/(core.BASE+'close-kin-phase.json')).read_bytes()).hexdigest()
 assert {k:v for k,v in after.items()if k not in('parent_ner_sha256','parent_close_kin_sha256')}=={k:v for k,v in value.items()if k not in('parent_ner_sha256','parent_close_kin_sha256')}
 payload=(json.dumps(after,ensure_ascii=False,indent=2)+'\n').encode()
 try:
  target.write_bytes(payload)
  with patch.object(minimal,'PROOF_SHA',hashlib.sha256(payload).hexdigest()):yield
 finally:target.write_bytes(before)
