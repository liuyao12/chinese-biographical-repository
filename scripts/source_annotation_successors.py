"""Exact, source-bound additions to preserved annotation snapshots."""
import copy
import hashlib
import json
from pathlib import Path

CASE_PATH='source-evidence/xunsong-elder-brother/c40-seed-shape-successor.json'
CASE_SHA='f1e4bd9522c59e71bfd96d457f755fdd37a434128ba397472990586242e27384'


def _strip_person_ids(value):
    if isinstance(value,dict):
        return{k:_strip_person_ids(v)for k,v in value.items()
               if not(k=='person_id'or k.endswith('_person_id')or k=='person_ids'or k.endswith('_person_ids'))}
    if isinstance(value,list):return[_strip_person_ids(v)for v in value]
    return value


def _shape_sha(value):
    raw=json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
    return hashlib.sha256(raw).hexdigest()


def xunsong_elder_brother_additions(root,path,before,current):
    """Return only the pinned new 兄 marker when projecting the archived Jinshu 075 unit."""
    if path!='corpus/jinshu/075.json':return[]
    root=Path(root).resolve();case_path=(root/CASE_PATH).resolve()
    assert case_path.is_relative_to(root)and case_path.is_file()and not case_path.is_symlink()
    raw=case_path.read_bytes();assert hashlib.sha256(raw).hexdigest()==CASE_SHA
    case=json.loads(raw)
    assert case.get('kind')=='jin075_xunsong_elder_brother_c40_seed_shape_successor'
    assert case.get('human_reviewed')is False and case.get('model')is None
    assert before.get('id')==current.get('id')==case['source_dimensions']['id']
    assert all(before.get(k)==v for k,v in case['source_dimensions'].items())
    assert all(current.get(k)==v for k,v in case['source_dimensions'].items())
    assert all(before.get('source',{}).get(k)==v for k,v in case['source_identity'].items())
    assert all(current.get('source',{}).get(k)==v for k,v in case['source_identity'].items())
    old_p=[p for p in before.get('paragraphs',[])if p.get('id')==case['paragraph_id']]
    new_p=[p for p in current.get('paragraphs',[])if p.get('id')==case['paragraph_id']]
    assert len(old_p)==len(new_p)==1
    old_shape=_strip_person_ids(old_p[0]);new_shape=_strip_person_ids(new_p[0])
    assert _shape_sha(old_shape)==case['before_shape_sha256']
    assert new_p[0].get('text')==case['full_quote']
    assert _shape_sha(new_shape)==case['after_shape_sha256']
    marker=case['added_mention'];matches=[m for m in new_p[0].get('mentions',[])if m.get('id')==marker.get('id')]
    assert len(matches)==1 and _strip_person_ids(matches[0])==marker
    without=copy.deepcopy(new_shape);without['mentions']=[m for m in without['mentions']if m.get('id')!=marker['id']]
    assert without==old_shape
    old_ids={m['id']for p in before.get('paragraphs',[])for m in p.get('mentions',[])}
    new_ids={m['id']for p in current.get('paragraphs',[])for m in p.get('mentions',[])}
    assert new_ids-old_ids=={marker['id']}and not(old_ids-new_ids)
    return matches
