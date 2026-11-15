"""One source-bound explicit-brother namespace; no shared-parent person or cousin shortcut."""
import copy,json,re
from pathlib import Path
TYPE='explicit_received_brothers_parent_unidentified'
def _members(assembly,people,assertions,chapters,root):
 try:
  from scripts.wyd_song045_roles import CID,relation_records,relation_valid,name_records,name_valid,resolve_roles
  from scripts.fixed_wuyingdian_song045_liucui import validate_source
  from scripts.person_ids import valid_person_id
 except ImportError:
  from wyd_song045_roles import CID,relation_records,relation_valid,name_records,name_valid,resolve_roles
  from fixed_wuyingdian_song045_liucui import validate_source
  from person_ids import valid_person_id
 def need(ok,msg):
  if not ok:raise ValueError('明弟兄無名父namespace：'+msg)
 need(root is not None and isinstance(assembly,dict)and isinstance(people,dict)and isinstance(assertions,dict)and isinstance(chapters,dict),'根/參數型別')
 need(set(assembly)=={'id','schema_mode','namespace_id','root_person_id','entry_person_id','status','human_reviewed','collateral_root_group','members'},'組裝欄位')
 g=assembly.get('collateral_root_group');need(isinstance(g,dict)and set(g)=={'id','type','status','human_reviewed','root_person_ids','brother_assertion_id','name_record_ids','source_term','common_parent_person_id','common_parent_name','common_parent_registered','relative_age','biological_verification','references','rationale'},'明弟兄群組欄位')
 ns=assembly['namespace_id'];need(isinstance(ns,str)and re.fullmatch('[a-z0-9]{3}_[a-z0-9]{3}_[a-z0-9]{3}',ns)is not None and ns not in people,'namespace不是人物')
 need(assembly['schema_mode']=='personless_namespace'and assembly['root_person_id']is None and assembly['status']=='editorial_preferred'and assembly['human_reviewed']is False,'不造父/AI資格')
 need(g['type']==TYPE and g['status']=='contextual_provisional'and g['human_reviewed']is False and g['common_parent_person_id']is None and g['common_parent_name']is None and g['common_parent_registered']is False and g['biological_verification']is False and isinstance(g['rationale'],str)and bool(g['rationale'].strip()),'未名父或資格不可提升')
 ch=chapters[CID];validate_source(ch,root);roles=resolve_roles(ch,root);older,younger=roles['chengdaoyang'],roles['daozhu'];need(older!=younger and g['root_person_ids']==[older,younger]and assembly['entry_person_id']==older,'明兄弟角色/入口')
 a=assertions.get(g['brother_assertion_id']);expected=next(a for a in relation_records(ch,root)if a['id']=='a-song045-wyd-daozhu-brother');ps={p['id']:(CID,p)for p in ch['paragraphs']}
 need(a==expected and relation_valid(a,ps,chapters,root),'完整具名明弟typed proof')
 evidence_p=ps[a['evidence'][0]['paragraph_id']][1];pos=evidence_p.get('source_position',{})
 need(evidence_p.get('text_layer')=='received_chapter'and isinstance(pos,dict)and pos.get('source_layer')=='received_chapter'and pos.get('text_layer')in(None,'received_chapter')and evidence_p.get('source_layer')in(None,'received_chapter')and all(k not in d for d in(evidence_p,pos)for k in('annotator','attached_note_to_paragraph_id')),'只有完整received正文，不接受注層/附注冒名')
 need(g['source_term']==a['qualifiers']['source_term']and g['relative_age']==a['qualifiers']['relative_birth_order'],'原詞/相對年序；不推絕對排行')
 need(g['name_record_ids']==['name-song045-wyd-chengdaoyang','name-song045-wyd-daozhu'],'氏名橋')
 names=json.loads((Path(root)/'corpus/songshu/045-wyd1739-liucui-name-components.json').read_bytes())['records'];wanted=[n for n in name_records(ch,root)if n['id']in g['name_record_ids']]
 need(len(wanted)==2 and all(n in names and name_valid(n,names,chapters,list(assertions.values()),root)for n in wanted),'原文程道養全名/道助弟稱的氏名來源橋')
 e=a['evidence'][0];ref={'assertion_id':a['id'],'chapter_id':e['chapter_id'],'source_id':e['source_id'],'paragraph_id':e['paragraph_id'],'quote':e['quote'],'url':ch['source'].get('permalink')or ch['source']['url'],'scope':'原文明弟兄及相對年序；共同父未名，不建立父親profile。'}
 need(g['references']==[ref],'原完整來源引用')
 rows=assembly['members'];need(isinstance(rows,list)and len(rows)==2,'恰兩真人物首節點');out={}
 for row in rows:
  need(isinstance(row,dict)and set(row)=={'person_id','source_person_ids','representative_source_person_id','identity_equivalence_decision_ids','parent_person_id','source_assertion_id','collateral_root_group_id'},'首節點欄位')
  pid=row['person_id'];need(pid in(older,younger)and pid not in out and pid in people and valid_person_id(pid)and pid.startswith(ns+'_')and len(pid)==len(ns)+2,'同代真人物；不准父子/缺代/字母當排行')
  need(row['source_person_ids']==[pid]and row['representative_source_person_id']==pid and row['identity_equivalence_decision_ids']==[] and row['parent_person_id']is None and row['source_assertion_id']is None and row['collateral_root_group_id']==g['id'],'不造共同父、不冒父子來源')
  out[pid]=dict(copy.deepcopy(row),assembly_id=assembly['id'],root_person_id=None,namespace_id=ns,namespace_entry_person_id=assembly['entry_person_id'],collateral_root_group=copy.deepcopy(g),status=assembly['status'],human_reviewed=False)
 need(set(out)=={older,younger},'首節點端點')
 return out

def members(assembly,people,assertions,chapters,root):
 try:return _members(assembly,people,assertions,chapters,root)
 except(KeyError,TypeError,AttributeError,StopIteration,OSError)as error:raise ValueError('明弟兄namespace來源/欄位無效')from error
