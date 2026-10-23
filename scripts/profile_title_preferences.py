"""Explicit source-holding presentation choices, never an office/rank/date inference."""
from pathlib import Path
import json
TYPE='profile_title_preference_set'
MODES={'grant','transfer','accession','demotion','self_proclamation','posthumous_grant','posthumous_enfeoffment','posthumous_naming'}
KEYS={'id','person_id','selection_kind','holding_id','attestation_id','source_ref','scope','temporal_claim','status','rationale','human_reviewed'}
REF={'work_id','book_id','source_id','chapter_id','paragraph_id','person_mention_id','start','end','surface'}
def resolve(records,people,root):
 """Validate the complete decision set once; callers may then select exact canonical ID."""
 try:
  chs={r['id']:r for r in records if r.get('record_type')=='marked_chapter'}
  hs={};ds=[]
  for r in records:
   if r.get('record_type')=='title_holding_assertion_set':
    for h in r['holdings']:
     assert h['id']not in hs;hs[h['id']]=h
   if r.get('record_type')==TYPE:
    assert set(r)=={'format_version','record_type','decisions'}and r['format_version']=='0.1'and isinstance(r['decisions'],list)and r['decisions'];ds.extend(r['decisions'])
  if not ds:return{}
  try:from scripts.retired_person_ids import retired_person_ids
  except ImportError:from retired_person_ids import retired_person_ids
  retired=retired_person_ids(root);assert not set(people).intersection(retired)
  aliases={a for p in people.values()for a in p.get('id_aliases',[])}
  out={};seen=set()
  try:from scripts.received_career_roles import holding_valid
  except ImportError:from received_career_roles import holding_valid
  for d in ds:
   assert isinstance(d,dict)and set(d)==KEYS and isinstance(d['id'],str)and d['id']and d['id']not in seen;seen.add(d['id'])
   pid=d['person_id'];assert pid in people and pid not in aliases and pid not in out
   assert d['selection_kind']=='default_profile_title'and d['scope']=='timeless_profile_heading'and d['temporal_claim']=='none'and d['status']=='editorial_provisional'and d['human_reviewed']is False and isinstance(d['rationale'],str)and d['rationale'].strip()
   h=hs[d['holding_id']];assert h['person_id']==pid and h['status']=='source_attested'and h['mode']in MODES and h.get('source_qualification',{}).get('kind')!='reported_office_challenged_by_commentary'
   a,=[a for a in h['attestations']if a['id']==d['attestation_id']];ref=d['source_ref'];assert isinstance(ref,dict)and set(ref)==REF
   c=chs[ref['chapter_id']];p,=[p for p in c['paragraphs']if p['id']==ref['paragraph_id']];m,=[m for m in p['mentions']if m['id']==ref['person_mention_id']]
   assert all(ref[k]==c[k]for k in('work_id','book_id','source_id','chapter_id')if k!='chapter_id')and ref['chapter_id']==c['id']
   assert all(ref[k]==a[k]for k in('paragraph_id','person_mention_id','start','end','surface'))
   assert type(ref['start'])is int and type(ref['end'])is int and 0<=ref['start']<ref['end']<=len(p['text'])and p['text'][ref['start']:ref['end']]==ref['surface']==h['title']
   assert m['kind']=='person'and m.get('person_id')==pid and p['text'][m['start']:m['end']]==m['surface']
   assert any(e.get('work_id')==c['work_id']and e.get('book_id')==c['book_id']and e.get('source_id')==c['source_id']and e.get('chapter_id')==c['id']and e.get('paragraph_id')==p['id']and e.get('person_mention_id')==m['id']and e.get('quote')and e['quote']in p['text']for e in h['evidence'])
   # The holding's existing finite grammar, not a preference-supplied title/regex,
   # must attest the actual recipient and mode. Unknown source contracts fail closed.
   assert holding_valid(h,c,root=root)
   for case in c.get('annotation',{}).get('unresolved_identity_cases',[])+c.get('annotation',{}).get('unresolved_title_attestations',[]):
    ids={case.get('person_mention_id'),case.get('source_mention_id'),case.get('mention_id')}
    ids.update(case.get('mention_ids',[]));assert m['id']not in ids
   for proposal in c.get('annotation',{}).get('title_proposals',[]):
    if proposal.get('outcome')in('not_assumed','not_reported'):
     assert d['holding_id']not in(proposal.get('holding_id'),proposal.get('linked_holding_id'))
   out[pid]=dict(decision_id=d['id'],person_id=pid,holding_id=h['id'],attestation_id=a['id'],title=h['title'],kind=h['kind'],mode=h['mode'],status=d['status'],rationale=d['rationale'],source_ref=dict(ref))
  return out
 except(AssertionError,KeyError,TypeError,ValueError,IndexError,StopIteration,AttributeError,OSError)as exc:
  raise ValueError('預設標頭稱號須唯一同人、已證持職及精確來源用稱；不得以未就、爭議主體、拼合官名或任期推選')from exc

def errors(root,records,people):
 try:resolve(records,people,root);return[]
 except ValueError as e:return[str(e)]

class PreferenceCatalog(list):
 """A read-only row-list transaction, root-local, with no global or cross-load cache.
 Source row dictionaries remain the existing catalogue API; selected dependencies
 are snapshotted and checked before use, so mutating them cannot reuse validation.
 Native callers must reload after editorial changes, as for all bundle data.
 """
 def __init__(self,records,people,root):
  import copy
  list.__init__(self,records);self.root=Path(root).resolve();self._profile_title_index=resolve(self,people,self.root)
  self.dependencies={};self.raw_dependencies={}
  for pid,choice in self._profile_title_index.items():
   deps=[r for r in self if r.get('record_type')==TYPE or(r.get('record_type')=='marked_chapter'and r['id']==choice['source_ref']['chapter_id'])or(r.get('record_type')=='title_holding_assertion_set'and any(h['id']==choice['holding_id']for h in r['holdings']))]
   self.dependencies[pid]=[(r,copy.deepcopy(r))for r in deps]
   for row in deps:
    if row.get('record_type')=='marked_chapter'and row.get('source',{}).get('raw_file'):
     import hashlib
     raw=self.root/row['source']['raw_file'];self.raw_dependencies[pid]=(raw,hashlib.sha256(raw.read_bytes()).hexdigest())
 def choice(self,pid,root):
  import copy
  if Path(root).resolve()!=self.root:raise ValueError('預設稱號索引不可跨root重用')
  if pid not in self._profile_title_index:return None
  if any(actual!=snapshot for actual,snapshot in self.dependencies[pid]):raise ValueError('預設稱號來源交易已變，須重新載入並驗證')
  if pid in self.raw_dependencies:
   import hashlib
   raw,sha=self.raw_dependencies[pid]
   if hashlib.sha256(raw.read_bytes()).hexdigest()!=sha:raise ValueError('預設稱號固定來源原檔已變，須重驗')
  return copy.deepcopy(self._profile_title_index[pid])
 def __copy__(self):
  # A copied editable fixture has no validated transaction identity.
  return list(self)
 def __deepcopy__(self,memo):
  import copy
  result=[];memo[id(self)]=result
  result.extend(copy.deepcopy(row,memo)for row in self)
  return result
 def _readonly(self,*a,**k):raise TypeError('Catalogue transaction is read-only; reload after edits')
 append=extend=insert=pop=remove=clear=sort=reverse=__setitem__=__delitem__=__iadd__=__imul__=_readonly

def choice(records,people,person_id,root):
 if isinstance(records,PreferenceCatalog):return records.choice(person_id,root)
 return resolve(records,people,root).get(person_id)
