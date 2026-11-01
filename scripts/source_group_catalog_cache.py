"""Context-only, content-checked prototype for closed source-group validation.

No validation is skipped on a novel/mutated caller or nonstandard reader. A
successful physical proof is reused only for identical ordered, typed contents
and fresh exact dependency bytes. Only selected results leave the private index.
"""
import builtins,copy,hashlib,io,json,marshal,os,sys,sysconfig,time
from contextvars import ContextVar
from pathlib import Path
try:from scripts.validation_context import _ACTIVE,_json_tree,scope,DEPENDENCIES
except ImportError:from validation_context import _ACTIVE,_json_tree,scope,DEPENDENCIES

_NAMESPACE='source_group_catalog_cache_prototype_v1'
_REVIEWED_GUARD_CODE_SHA256='e513b93c63e28ee3e45fd729c4441b252952df771f3dce02a1ad8b25adfb6298'
_OBSERVER=ContextVar('source_group_proof_read_observer',default=None)
_METHODS=('read_bytes','read_text','open','stat','exists','is_file','is_dir','resolve','glob','rglob')
_PATH_BASE={n:getattr(Path,n)for n in _METHODS}
_IO_BASE=(io.open,builtins.open,os.stat,os.scandir,os.listdir)
_RUNTIME_ROOTS=tuple({Path(sys.base_prefix).resolve(),Path(sys.prefix).resolve()})
_PATH_MRO=Path.__mro__
_PATH_MRO_BASE=tuple((owner,name,owner.__dict__[name])for owner in _PATH_MRO for name in _METHODS if name in owner.__dict__)
_STDLIB_ROOT=os.path.normcase(os.path.realpath(sysconfig.get_path('stdlib')))


def _stdlib_path_definition(owner,value):
 # Python 3.13 moves concrete/inherited methods to two private stdlib modules.
 # A module-name string alone must not authenticate an external reader wrapper.
 try:
  name=value.__module__
  if name not in('pathlib','pathlib._local','pathlib._abc'):return False
  module=sys.modules.get(name)
  if module is None or getattr(module,owner.__name__,None)is not owner:return False
  origin=os.path.normcase(os.path.realpath(module.__spec__.origin))
  filename=os.path.normcase(os.path.realpath(value.__code__.co_filename))
  return os.path.commonpath((_STDLIB_ROOT,origin))==_STDLIB_ROOT and filename==origin
 except(AttributeError,OSError,TypeError,ValueError):return False


_BASE_VALID=all(_stdlib_path_definition(owner,value)for owner,name,value in _PATH_MRO_BASE)


def _standard_io():
 return _BASE_VALID and Path.__mro__==_PATH_MRO and all(getattr(Path,n)is v for n,v in _PATH_BASE.items())and all(owner.__dict__.get(name)is value for owner,name,value in _PATH_MRO_BASE)and all(a is b for a,b in zip((io.open,builtins.open,os.stat,os.scandir,os.listdir),_IO_BASE))


def _reviewed_code_ok(root):
 # Conservative prototype boundary: new proof code requires a fresh closure review.
 code={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted((root/'scripts').rglob('*.py'))if '__pycache__'not in p.parts and p.name!='source_group_catalog_cache.py'}
 digest=hashlib.sha256(json.dumps(code,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 return digest==_REVIEWED_GUARD_CODE_SHA256


def _closed_code_pins_reviewed(root, code, pins):
 # Approval must bind the exact code bytes about to enter this certificate,
 # not only a pre-build gate or a separately re-read set. Re-enumeration also
 # rejects a new Python file appearing between code enumeration and membership.
 current=[str(p.relative_to(root))for p in sorted((root/'scripts').rglob('*.py'))if '__pycache__'not in p.parts]
 if current!=code:return False
 reviewed={rel:pins[rel].hex()for rel in code if Path(rel).name!='source_group_catalog_cache.py'}
 return hashlib.sha256(json.dumps(reviewed,sort_keys=True,separators=(',',':')).encode()).hexdigest()==_REVIEWED_GUARD_CODE_SHA256


def _attrs(p):
 s=p.stat();return(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns)


def _audit(event,args):
 bucket=_OBSERVER.get()
 if bucket is None or event!='open':return
 name=args[0]
 if not isinstance(name,(str,bytes,os.PathLike)):bucket['unproved']=True;return
 try:
  p=Path(os.fsdecode(name)).absolute()
  if not p.is_relative_to(bucket['root']):
   # Only the interpreter's own installed modules are runtime dependencies.
   if not any(p.is_relative_to(base)for base in _RUNTIME_ROOTS):bucket['outside'].add(str(p))
   return
  if p.suffix in('.pyc','.pyo'):return
  rel=str(p.relative_to(bucket['root']));mode=args[1]
  if isinstance(mode,str)and any(x in mode for x in('w','a','+')):bucket['unproved']=True
  if rel not in bucket['files']:bucket['files'][rel]=_attrs(p)
 except(OSError,ValueError,TypeError):bucket['unproved']=True


sys.addaudithook(_audit)


def _membership(root):
 rows=[]
 for rel in DEPENDENCIES:
  base=root/rel
  if base.is_file():rows.append(rel);continue
  if not base.exists():rows.append(rel+'/[absent]');continue
  for directory,dirs,files in os.walk(base):
   dirs[:]=sorted(d for d in dirs if d not in('__pycache__','.pytest_cache','node_modules','.git'))
   prefix=str(Path(directory).relative_to(root));rows.append(prefix+'/')
   rows.extend(prefix+'/'+f for f in sorted(files)if not f.endswith(('.pyc','.pyo'))and f!='.DS_Store')
 return hashlib.sha256(marshal.dumps(rows,2)).digest(),len(rows)


def _hash_files(root,paths):
 out={}
 for rel in sorted(paths):
  p=root/rel
  if p.is_symlink()or not p.is_file():raise ValueError('source dependency no longer regular')
  a=_attrs(p);digest=hashlib.sha256(p.read_bytes()).digest()
  if a!=_attrs(p):raise ValueError('source dependency changed during read')
  out[rel]=digest
 return out


def _ordered_caller_key(records,people):
 typename=type(records).__module__+'.'+type(records).__qualname__
 blob=marshal.dumps(('ordered-source-group-row-view-v1',typename,list(records),people),2)
 return hashlib.sha256(blob).digest(),len(blob)


def _docs_match_current_rows(docs,records):
 # This is the original validated_sets comprehension, not a reduced schema.
 projection=[row for row in records if row.get('record_type')=='source_person_reference_group_set']
 return type(docs)is list and marshal.dumps(docs,2)==marshal.dumps(projection,2)


def _index(docs):
 groups=[];readings=[];by_group={};by_reading={}
 for d in docs:
  for g in d['groups']:
   pos=len(groups);members={m['person_id']for m in g['members']};groups.append((g,members))
   for pid in members:by_group.setdefault(pid,set()).add(pos)
  for r in d['unresolved_readings']:
   pos=len(readings);ids=set(r.get('candidate_person_ids',[]))
   if isinstance(r.get('subject_person_id'),str):ids.add(r['subject_person_id'])
   ids.update(m['person_id']for m in r.get('resolved_member_refs',[]));readings.append((r,ids))
   for pid in ids:by_reading.setdefault(pid,set()).add(pos)
 return groups,readings,by_group,by_reading


def _select(index,ids):
 groups,readings,by_group,by_reading=index;gp=set();rp=set();related=set()
 for pid in ids:gp.update(by_group.get(pid,()));rp.update(by_reading.get(pid,()))
 gout=[];rout=[]
 for pos in sorted(gp):g,persons=groups[pos];gout.append(copy.deepcopy(g));related.update(persons)
 for pos in sorted(rp):r,persons=readings[pos];rout.append(copy.deepcopy(r));related.update(persons)
 return gout,rout,related


def _fallback(root,build,ids):
 # Old root-only memo entries must not swallow a Path-reader overlay.
 with scope(root,enabled=False):docs=build()
 return docs if ids is None else _select(_index(docs),ids)


def _stats(state,root):
 key=(_NAMESPACE,'statistics',str(root))
 if key not in state['memo']:state['memo'][key]={'cold_proofs':0,'hits':0,'fallbacks':{},'key_seconds':0.0,'closure_seconds':0.0,'proof_seconds':0.0,'max_key_bytes':0,'records_types':{}}
 return state['memo'][key]


def statistics(root):
 state=_ACTIVE.get()
 if state is None:return{}
 return copy.deepcopy(_stats(state,Path(root).resolve()))


def dependencies(root):
 state=_ACTIVE.get()
 if state is None:return{}
 out={}
 for key,entry in state['memo'].items():
  if len(key)!=4 or key[:3]!=(_NAMESPACE,'entry',str(Path(root).resolve())):continue
  out[key[3]]={'physical_files':{k:v.hex()for k,v in entry['files'].items()},'membership_sha256':entry['membership'].hex(),'membership_rows':entry['membership_count'],'key_sha256':entry['key'].hex(),'code_files':entry['code_files'],'private_index_json_bytes':len(json.dumps(entry['docs'],ensure_ascii=False).encode())}
 return out


def run(root,records,people,build,ids=None):
 root=Path(root).resolve();state=_ACTIVE.get()
 if state is None or state['closed']or state['root']!=root:return build()if ids is None else _select(_index(build()),ids)
 stats=_stats(state,root);typename=type(records).__module__+'.'+type(records).__qualname__;stats['records_types'][typename]=stats['records_types'].get(typename,0)+1
 def fallback(reason):
  stats['fallbacks'][reason]=stats['fallbacks'].get(reason,0)+1
  return _fallback(root,build,ids)
 if not _standard_io():return fallback('nonstandard_reader')
 try:
  from scripts.profile_title_preferences import PreferenceCatalog
 except ImportError:from profile_title_preferences import PreferenceCatalog
 if type(records)not in(list,PreferenceCatalog)or type(people)is not dict:return fallback('unsupported_outer_shape')
 # The reviewed internal view has its own typed class key, separate from list.
 # No arbitrary subclass is coerced; nested types and insertion order are exact.
 def current_key():
  start=time.process_time()
  try:
   value,size=_ordered_caller_key(records,people);stats['max_key_bytes']=max(stats['max_key_bytes'],size);return value
  finally:stats['key_seconds']+=time.process_time()-start
 def require_unchanged(expected,phase):
  try:now=current_key()
  except(ValueError,TypeError,RuntimeError)as error:raise ValueError('Source-group caller catalog changed during '+phase+'; reload catalog')from error
  if now!=expected:raise ValueError('Source-group caller catalog changed during '+phase+'; reload catalog')
 try:key=current_key()
 except(ValueError,TypeError):return fallback('unsupported_marshaled_shape')
 cachekey=(_NAMESPACE,'entry',str(root),typename);entry=state['memo'].get(cachekey)
 if entry is not None:
  if key!=entry['key']:return fallback('caller_content_changed')
  start=time.process_time()
  try:
   members,count=_membership(root)
   if members!=entry['membership']or _hash_files(root,entry['files'])!=entry['files']:return fallback('physical_dependency_changed')
  except(OSError,ValueError,TypeError):return fallback('physical_dependency_unproved')
  finally:stats['closure_seconds']+=time.process_time()-start
  require_unchanged(key,'cached dependency check')
  stats['hits']+=1
  return copy.deepcopy(entry['docs'])if ids is None else _select(entry['index'],ids)
 if not _reviewed_code_ok(root):return fallback('guard_code_closure_not_reviewed')
 # Unsupported JSON shapes retain original behaviour, never receive a certificate.
 if not _json_tree([list(records),people]):return fallback('non_json_nested_shape')
 bucket={'root':root,'files':{},'outside':set(),'unproved':False};token=_OBSERVER.set(bucket);start=time.process_time()
 try:
  with scope(root,enabled=False):docs=build()
 finally:_OBSERVER.reset(token);stats['proof_seconds']+=time.process_time()-start;stats['cold_proofs']+=1
 require_unchanged(key,'cold validation')
 if not _docs_match_current_rows(docs,records):raise ValueError('Source-group validation result differs from current caller rows; reload catalog')
 if bucket['outside']or bucket['unproved']:
  stats['fallbacks']['cold_read_closure_unproved']=stats['fallbacks'].get('cold_read_closure_unproved',0)+1;stats['outside_paths']=sorted(bucket['outside'])[:20]
  return docs if ids is None else _select(_index(docs),ids)
 try:
  for rel,a in bucket['files'].items():
   if a!=_attrs(root/rel):return fallback('cold_dependency_drift')
  code=[str(p.relative_to(root))for p in sorted((root/'scripts').rglob('*.py'))if '__pycache__'not in p.parts]
  physical=set(bucket['files'])|set(code);pins=_hash_files(root,physical);members,count=_membership(root)
  closed_code_approved=_closed_code_pins_reviewed(root,code,pins)
  private=copy.deepcopy(docs)
 except(OSError,ValueError,TypeError):return fallback('cold_closure_unproved')
 if not closed_code_approved:return fallback('code_approval_changed_during_cold')
 index=_index(private)
 require_unchanged(key,'cold dependency closure')
 if not _docs_match_current_rows(private,records):raise ValueError('Source-group private result differs from current caller rows; reload catalog')
 entry={'key':key,'files':pins,'membership':members,'membership_count':count,'docs':private,'index':index,'code_files':code};state['memo'][cachekey]=entry
 return copy.deepcopy(private)if ids is None else _select(entry['index'],ids)
