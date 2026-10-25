from pathlib import Path
import importlib.util,json
HERE=Path(__file__).parent
BASE=HERE.parent/'cbr-caoren-assembly-model-successor'
spec=importlib.util.spec_from_file_location('sealed_model_plan',BASE/'model_plan.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
SAFE=old.OLD+" if not isinstance(member,dict) or not isinstance(member.get('parent_connection'),dict):return False\n"+old.NEW[len(old.OLD):]
def plan(root):
 root=Path(root);out={}
 rel='scripts/fixed_witness_assembly_roles.py';b=(BASE/'payload'/rel).read_bytes();p=root/rel
 assert not p.exists()or p.read_bytes()==b,'existing assembly helper differs: review required'
 if not p.exists():out[rel]=b
 rel='scripts/received_kin_assembly.py';p=root/rel;s=p.read_text()
 if SAFE not in s:
  if old.NEW in s:assert s.count(old.NEW)==1;s=s.replace(old.NEW,SAFE,1)
  else:assert s.count(old.OLD)==1;s=s.replace(old.OLD,SAFE,1)
 if s.encode()!=p.read_bytes():out[rel]=s.encode()
 rel='scripts/family_assemblies.py';p=root/rel;s=p.read_text()
 if old.ENUMNEW not in s:assert s.count(old.ENUM)==1;s=s.replace(old.ENUM,old.ENUMNEW,1)
 if s.encode()!=p.read_bytes():out[rel]=s.encode()
 rel='scripts/fixed_witness_assembly_roles.json';p=root/rel;new=json.loads((BASE/'payload'/rel).read_text());current=json.loads(p.read_text())if p.exists()else dict(format_version='0.1',bindings={})
 assert current['format_version']=='0.1'
 for k,v in new['bindings'].items():assert k not in current['bindings']or current['bindings'][k]==v,'trusted binding collision';current['bindings'][k]=v
 b=(json.dumps(current,ensure_ascii=False,indent=2)+'\n').encode()
 if not p.exists()or p.read_bytes()!=b:out[rel]=b
 return out
