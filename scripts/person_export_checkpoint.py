"""Optional core-person export checkpoints. No source interpretation or shared cache."""
import hashlib,json,locale,os,re,stat,sys,tempfile,uuid
from pathlib import Path
try:
 from .validation_context import DEPENDENCIES,DRIFT_ERROR
 from .person_ids import valid_person_id
except ImportError:
 from validation_context import DEPENDENCIES,DRIFT_ERROR
 from person_ids import valid_person_id

EXTRA_DEPENDENCIES=('data/works',)
MAX_BATCH_SIZE=64
FORMAT_VERSION=1
HEX64=re.compile(r'[0-9a-f]{64}')
BATCH_FILE=re.compile(r'batch-[0-9a-f]{32}\.json')

def _canonical(value):return json.dumps(value,ensure_ascii=True,sort_keys=True,separators=(',',':')).encode('ascii')
def _digest(value):return hashlib.sha256(_canonical(value)).hexdigest()
def _attrs(s):return(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
def _need(ok,message):
 if not ok:raise ValueError('Person export checkpoint: '+message)
def _pairs(values):
 out={}
 for k,v in values:
  _need(k not in out,'duplicate JSON key');out[k]=v
 return out
def _json(raw):
 try:return json.loads(raw,object_pairs_hook=_pairs)
 except (ValueError,UnicodeError)as exc:raise ValueError('Person export checkpoint: malformed/truncated JSON')from exc

def _paths(root,dependencies):
 for rel in dependencies:
  base=root/rel
  for p in ([base]if base.is_file()else sorted(base.rglob('*'))if base.exists()else[]):
   s=p.stat()
   if not stat.S_ISREG(s.st_mode):continue
   if rel=='scripts'and('__pycache__'in p.relative_to(base).parts or p.suffix in('.pyc','.pyo')):continue
   yield p,s

def metadata_snapshot(root,dependencies=DEPENDENCIES+EXTRA_DEPENDENCIES):
 root=Path(root).resolve()
 return {str(p.relative_to(root)):_attrs(s)for p,s in _paths(root,dependencies)}

def _code_snapshot(directories,content):
 result={}
 for i,directory in enumerate(sorted({Path(p).resolve()for p in directories})):
  for path in sorted(directory.rglob('*.py')):
   if '__pycache__'in path.parts or not path.is_file():continue
   a=path.stat();key=str(i)+'/'+str(path.relative_to(directory))
   if content:
    raw=path.read_bytes();_need(_attrs(a)==_attrs(path.stat()),DRIFT_ERROR)
    result[key]=(hashlib.sha256(raw).hexdigest(),_attrs(a))
   else:result[key]=_attrs(a)
 return result

class SourceSnapshot:
 """Content for durable identity, metadata+membership for in-run batch safety."""
 def __init__(self,root,owner_before,code_directories):
  self.root=Path(root).resolve();self.code_directories=tuple(code_directories)
  self.inputs={str(p):(v[0],tuple(v[1]))for p,v in owner_before.items()}
  for p,a in _paths(self.root,EXTRA_DEPENDENCIES):
   raw=p.read_bytes();_need(_attrs(a)==_attrs(p.stat()),DRIFT_ERROR)
   self.inputs[str(p.relative_to(self.root))]=(hashlib.sha256(raw).hexdigest(),_attrs(a))
  self.expected_metadata={p:v[1]for p,v in self.inputs.items()}
  code=_code_snapshot(self.code_directories,True);self.expected_code_metadata={p:v[1]for p,v in code.items()}
  self.source_digest=_digest({p:v[0]for p,v in self.inputs.items()})
  runtime={'python':sys.version,'implementation':sys.implementation.name,'platform':sys.platform,'optimize':sys.flags.optimize,'encoding':locale.getpreferredencoding(False),'line_separator':os.linesep}
  self.code_digest=_digest({'files':{p:v[0]for p,v in code.items()},'runtime':runtime})
 def assert_current(self):
  _need(metadata_snapshot(self.root)==self.expected_metadata,DRIFT_ERROR)
  _need(_code_snapshot(self.code_directories,False)==self.expected_code_metadata,DRIFT_ERROR)

def validate_options(root,directory,resume,batch_size):
 _need(type(resume)is bool,'resume must be boolean')
 _need(type(batch_size)is int and 1<=batch_size<=MAX_BATCH_SIZE,'batch size must be 1..64')
 _need(directory is not None or not resume,'resume requires checkpoint directory')
 if directory is None:return None
 raw=Path(directory).expanduser();_need(not raw.is_symlink(),'checkpoint directory cannot be symlink')
 path=raw.resolve();_need(not path.is_relative_to(Path(root).resolve()),'checkpoint directory must be outside source root')
 return path

def _check_regular(path):
 _need(not path.is_symlink(),'symlink file refused: '+str(path))
 if path.exists():_need(path.is_file(),'expected regular file: '+str(path))

def atomic_text(path,text):
 """Same text encoding/newline semantics as Path.write_text, with durable replace."""
 path=Path(path);_need(path.parent.is_dir()and not path.parent.is_symlink(),'unsafe atomic parent')
 _check_regular(path);temporary=None
 try:
  with tempfile.NamedTemporaryFile(mode='w',dir=path.parent,prefix='.cbr-atomic-',suffix='.tmp',delete=False)as stream:
   temporary=Path(stream.name);stream.write(text);stream.flush();os.fsync(stream.fileno())
  os.replace(temporary,path);temporary=None
  descriptor=os.open(path.parent,os.O_RDONLY)
  try:os.fsync(descriptor)
  finally:os.close(descriptor)
 except BaseException:
  if temporary is not None:
   try:temporary.unlink()
   except FileNotFoundError:pass
  raise

class PersonExportCheckpoint:
 def __init__(self,root,directory,source,person_ids,output_ids,*,resume=False,batch_size=32):
  self.root=Path(root).resolve();self.directory=validate_options(self.root,directory,resume,batch_size);_need(self.directory is not None,'directory required')
  _need(isinstance(source,SourceSnapshot) and source.root==self.root,'source snapshot belongs to another root')
  self.source=source;self.batch_size=batch_size;self.pending={};self.completed={};self.reused=0;self.recomputed=0
  people=sorted(person_ids);allowed=sorted(output_ids)
  _need(len(people)==len(set(people))and all(type(p)is str and valid_person_id(p)for p in people),'invalid person membership')
  _need(len(allowed)==len(set(allowed))and all(type(p)is str and valid_person_id(p)for p in allowed)and set(people)<=set(allowed),'invalid output membership')
  self.people=set(people);self.allowed=set(allowed);self.destination=self.root/'exports/persons'
  for path in [self.root/'exports',self.destination]:_need(not path.is_symlink(),'symlink export destination refused')
  _need(self.destination.is_dir(),'normal export destination must already exist')
  self.source.assert_current()
  fixed={'schema_version':FORMAT_VERSION,'record_type':'cbr_person_export_checkpoint','phase':'canonical_person_core_loop_only','source_root':str(self.root),'output_directory':str(self.destination),'source_content_digest':source.source_digest,'runtime_code_digest':source.code_digest,'expected_person_ids':people,'allowed_output_ids':allowed,'batch_size':batch_size}
  fixed['input_digest']=_digest(fixed);self.input_digest=fixed['input_digest'];header=self.directory/'header.json'
  if resume:
   _need(self.directory.is_dir()and header.is_file(),'resume needs an existing owned checkpoint; old outputs are not a checkpoint');_check_regular(header);data=_json(header.read_bytes())
   _need(type(data)is dict and set(data)==set(fixed)|{'owner_token'},'unknown checkpoint header')
   _need(all(_canonical(data[k])==_canonical(v)for k,v in fixed.items()),'source/code/membership/options digest changed; use a new checkpoint')
   self.owner=data['owner_token'];_need(type(self.owner)is str and re.fullmatch('[0-9a-f]{32}',self.owner)is not None,'bad owner token')
  else:
   _need(not self.directory.exists()or(self.directory.is_dir()and not any(self.directory.iterdir())),'existing checkpoint requires explicit resume or a new empty directory')
   self.directory.mkdir(parents=True,exist_ok=True);self.owner=uuid.uuid4().hex;atomic_text(header,json.dumps(dict(fixed,owner_token=self.owner),sort_keys=True,indent=2)+'\n')
  self.batch_directory=self.directory/'batches';_need(not self.batch_directory.is_symlink(),'symlink batch directory refused');self.batch_directory.mkdir(exist_ok=True)
  for path in sorted(self.batch_directory.iterdir()):
   if path.name.startswith('.cbr-atomic-')and path.name.endswith('.tmp'):
    _check_regular(path);continue # An uncommitted temporary is never reused.
   _need(BATCH_FILE.fullmatch(path.name)is not None,'unknown batch path');_check_regular(path);data=_json(path.read_bytes())
   _need(type(data)is dict and set(data)=={'schema_version','record_type','owner_token','input_digest','completed'},'unknown completion record')
   _need(type(data['schema_version'])is int and data['schema_version']==FORMAT_VERSION and data['record_type']=='cbr_person_export_completed_batch'and data['owner_token']==self.owner and data['input_digest']==self.input_digest,'completion owner/digest mismatch')
   entries=data['completed'];_need(type(entries)is dict and 1<=len(entries)<=batch_size,'bad completion batch size')
   for pid,digest in entries.items():
    _need(pid in self.people and type(digest)is str and HEX64.fullmatch(digest)is not None,'unknown completed PID or SHA')
    _need(pid not in self.completed or self.completed[pid]==digest,'conflicting completion SHA')
    self.completed[pid]=digest
 def output_path(self,pid):
  _need(type(pid)is str and pid in self.allowed and valid_person_id(pid),'output PID not in expected membership')
  path=self.destination/(pid+'.json');_check_regular(path);return path
 @staticmethod
 def _bundle(raw,pid):
  try:data=_json(raw)
  except ValueError:return None
  if(type(data)is not dict or data.get('record_type')!='person_source_bundle'or data.get('requested_person_id')!=pid or type(data.get('person_ids'))is not list or pid not in data['person_ids']):return None
  return data
 def reuse(self,pid):
  _need(pid in self.people,'unknown source PID');digest=self.completed.get(pid)
  if digest is None:return None
  path=self.output_path(pid)
  if not path.is_file():return None
  raw=path.read_bytes()
  if hashlib.sha256(raw).hexdigest()!=digest:return None
  result=self._bundle(raw,pid)
  if result is not None:self.reused+=1
  return result
 def write_output(self,pid,text):atomic_text(self.output_path(pid),text)
 def mark(self,pid):
  _need(pid in self.people,'unknown completed PID');path=self.output_path(pid);raw=path.read_bytes();_need(self._bundle(raw,pid)is not None,'output PID/header mismatch')
  digest=hashlib.sha256(raw).hexdigest();_need(pid not in self.completed or self.completed[pid]==digest,'recomputed bytes differ under same digest')
  self.pending[pid]=digest;self.recomputed+=1
  if len(self.pending)>=self.batch_size:self.flush()
 def flush(self):
  if not self.pending:return
  self.source.assert_current()
  for pid,digest in self.pending.items():
   raw=self.output_path(pid).read_bytes();_need(hashlib.sha256(raw).hexdigest()==digest and self._bundle(raw,pid)is not None,'pending output changed before commit')
  data={'schema_version':FORMAT_VERSION,'record_type':'cbr_person_export_completed_batch','owner_token':self.owner,'input_digest':self.input_digest,'completed':dict(self.pending)}
  atomic_text(self.batch_directory/('batch-'+uuid.uuid4().hex+'.json'),json.dumps(data,sort_keys=True,indent=2)+'\n')
  self.completed.update(self.pending);self.pending.clear()
 def finish(self):
  self.flush();self.source.assert_current()
