from pathlib import Path
import json
HERE=Path(__file__).parent
OLD="def valid(member,rows,assertions,chapters,root):\n"
NEW=OLD+" if member.get('parent_connection',{}).get('interpretation_basis') in ('fixed_complete_witness_zu_fu_sequence','shared_father_with_estate'):\n  try:from .fixed_witness_assembly_roles import valid as fixed_assembly_valid\n  except ImportError:from fixed_witness_assembly_roles import valid as fixed_assembly_valid\n  return fixed_assembly_valid(member,rows,assertions,chapters,root)\n"
ENUM="('fixed_received_zu_fu_sequence','fixed_received_shared_father','fixed_complete_witness_shared_father')"
ENUMNEW="('fixed_received_zu_fu_sequence','fixed_received_shared_father','fixed_complete_witness_shared_father','fixed_complete_witness_zu_fu_sequence','shared_father_with_estate')"
def plan(root):
 root=Path(root);out={}
 for name,old,new in [('received_kin_assembly.py',OLD,NEW),('family_assemblies.py',ENUM,ENUMNEW)]:
  path='scripts/'+name;s=(root/path).read_text()
  if new not in s:
   assert s.count(old)==1,(name,'unexpected hook');s=s.replace(old,new,1)
  b=s.encode()
  if b!=(root/path).read_bytes():out[path]=b
 rel='scripts/fixed_witness_assembly_roles.py';b=(HERE/'payload'/rel).read_bytes()
 if not(root/rel).exists()or(root/rel).read_bytes()!=b:out[rel]=b
 rel='scripts/fixed_witness_assembly_roles.json';new=json.loads((HERE/'payload'/rel).read_text());p=root/rel
 current=json.loads(p.read_text())if p.exists()else {'format_version':'0.1','bindings':{}}
 assert current['format_version']=='0.1'
 for k,v in new['bindings'].items():
  assert k not in current['bindings']or current['bindings'][k]==v,'trusted binding collision';current['bindings'][k]=v
 b=(json.dumps(current,ensure_ascii=False,indent=2)+'\n').encode()
 if not p.exists()or p.read_bytes()!=b:out[rel]=b
 return out
