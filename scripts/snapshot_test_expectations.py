"""Test-only explicit MID normalization of historical pre-pronoun captures."""
import copy,json
from pathlib import Path
from scripts.sima_snapshot_source_roles import STANDALONE_SLOTS,standalone_expected
ROOT=Path(__file__).resolve().parents[1]
ROWS=json.loads((Path(__file__).resolve().parents[1]/'tests/fixtures/standalone-zhi-current-anchors.json').read_text())
def current_snapshot(value,root=ROOT):
 value=copy.deepcopy(value)
 def walk(x):
  if isinstance(x,dict):
   if x.get('id') in ROWS and x.get('surface')=='之' and x.get('kind')=='person':
    expected=ROWS[x['id']]['mention']
    assert all(x.get(k)==expected[k] for k in ('start','end','surface'))
    if x['id']in STANDALONE_SLOTS:
     current=standalone_expected(x['id'],root);assert x.get('person_id')in(expected['person_id'],current['person_id']);x['person_id']=current['person_id']
    x['kind']='pronoun'
   for v in x.values():walk(v)
  elif isinstance(x,list):
   for v in x:walk(v)
 walk(value)
 return value

def historical_snapshot(value,root=ROOT):
 value=copy.deepcopy(value)
 def walk(x):
  if isinstance(x,dict):
   if x.get('id') in ROWS and x.get('kind')=='pronoun':
    expected=standalone_expected(x['id'],root)if x['id']in STANDALONE_SLOTS else ROWS[x['id']]['mention']
    assert x==expected
    if x['id']in STANDALONE_SLOTS:x['person_id']=ROWS[x['id']]['mention']['person_id']
    x['kind']='person'
   for v in x.values():walk(v)
  elif isinstance(x,list):
   for v in x:walk(v)
 walk(value)
 return value
