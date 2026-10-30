"""Test-only explicit MID normalization of historical pre-pronoun captures."""
import copy,json
from pathlib import Path
ROWS=json.loads((Path(__file__).resolve().parents[1]/'tests/fixtures/standalone-zhi-current-anchors.json').read_text())
def current_snapshot(value):
 value=copy.deepcopy(value)
 def walk(x):
  if isinstance(x,dict):
   if x.get('id') in ROWS and x.get('surface')=='之' and x.get('kind')=='person':
    expected=ROWS[x['id']]['mention']
    assert all(x.get(k)==expected[k] for k in ('start','end','surface'))
    x['kind']='pronoun'
   for v in x.values():walk(v)
  elif isinstance(x,list):
   for v in x:walk(v)
 walk(value)
 return value

def historical_snapshot(value):
 value=copy.deepcopy(value)
 def walk(x):
  if isinstance(x,dict):
   if x.get('id') in ROWS and x.get('kind')=='pronoun':
    assert x==ROWS[x['id']]['mention']
    x['kind']='person'
   for v in x.values():walk(v)
  elif isinstance(x,list):
   for v in x:walk(v)
 walk(value)
 return value
