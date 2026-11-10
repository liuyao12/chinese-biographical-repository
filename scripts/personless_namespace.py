# coding:utf-8
"""Qualified shared namespace without a fabricated common-parent person."""
import copy,re
try:
 from .person_ids import family_path_errors
 from .biography_congfudi import biography_congfudi_valid
except ImportError:
 from person_ids import family_path_errors
 from biography_congfudi import biography_congfudi_valid

def received(p):
 pos=p.get('source_position',{})
 return (isinstance(pos,dict) and pos.get('source_layer')in(None,'received_text','received_body','received_biography')
  and pos.get('text_layer')in(None,'received_text','received_body','received_biography','received_chapter')
  and p.get('source_layer')in(None,'received_text') and p.get('text_layer')in(None,'received_chapter')
  and all(k not in d for d in(p,pos)for k in('annotator','attached_note_to_paragraph_id')))

def father_bound(a,chapters):
 try:
  if a['predicate']!='father'or a['status']!='source_attested'or a['qualifiers'].get('lineage')!='paternal':return False
  e,=a['evidence'];c=chapters[e['chapter_id']];p=next(p for p in c['paragraphs']if p['id']==e['paragraph_id']);t=p['text'];ms={m['id']:m for m in p['mentions']}
  s=ms[e['subject_person_mention_id']];o=ms[e['object_person_mention_id']]
  head=next((m for m in p['mentions']if m.get('start')==0 and m.get('kind')=='person'and m.get('person_id')==a['subject_person_id']),None)
  if not head or (s['start']!=0 and (head['end']>s['start']or t[head['end']:s['start']]not in('字','，字'))):return False
  return(received(p)and e['source_id']==c['source_id']and e['quote']==t
   and a['subject_person_id']!=a['object_person_id']and s['person_id']==a['subject_person_id']and o['person_id']==a['object_person_id']
   and all(m['kind']=='person'and t[m['start']:m['end']]==m['surface']for m in(s,o))
   and a['qualifiers']['source_term']=='父'and t[o['start']-1:o['start']]=='父'
   and s['end']<=o['start']and not any(v in t[s['end']:o['start']]for v in('非','未','不','或云','曰','「','」')))
 except(KeyError,TypeError,ValueError,StopIteration):return False

def namespace_members(assembly,people,assertions,chapters,root=None):
 # explicit-received-brothers-namespace-dispatch
 if isinstance(assembly,dict)and isinstance(assembly.get('collateral_root_group'),dict)and assembly['collateral_root_group'].get('type')=='explicit_received_brothers_parent_unidentified':
  try:from .explicit_brothers_namespace import members as explicit_members
  except ImportError:from explicit_brothers_namespace import members as explicit_members
  return explicit_members(assembly,people,assertions,chapters,root)
 """Raise on any unaudited multi-root shortcut; return ordinary assembled rows."""
 ns=assembly.get('namespace_id');g=assembly.get('collateral_root_group',{})
 if set(assembly)!={'id','schema_mode','namespace_id','root_person_id','entry_person_id','status','human_reviewed','collateral_root_group','members'}:raise ValueError('Unknown namespace assembly fields')
 if set(g)!={'id','type','status','human_reviewed','root_person_ids','cousin_assertion_id','named_father_assertion_ids','common_parent_person_id','common_parent_name','common_parent_registered','relative_age','biological_verification','references','rationale'}:raise ValueError('Unknown common-parent or collateral metadata')
 if(not isinstance(ns,str)or not re.fullmatch('[a-z0-9]{3}_[a-z0-9]{3}_[a-z0-9]{3}',ns)
    or ns in people or assembly.get('root_person_id')is not None
    or assembly.get('status')not in('contextual_provisional','editorial_preferred')
    or type(assembly.get('human_reviewed'))is not bool):raise ValueError('Personless namespace must never be a person')
 if(g.get('type')!='unknown_shared_father_from_qualified_first_cousins'
    or g.get('status')!='contextual_provisional'or type(g.get('human_reviewed'))is not bool
    or any(g.get(k)is not None for k in('common_parent_person_id','common_parent_name'))
    or g.get('common_parent_registered')is not False or g.get('relative_age')!='unknown'
    or g.get('biological_verification')is not False or not g.get('rationale')):raise ValueError('Unknown parent constraint cannot name a person or paternal age')
 a=assertions.get(g.get('cousin_assertion_id'));ps={p['id']:(c['id'],p)for c in chapters.values()for p in c['paragraphs']}
 if not a or not biography_congfudi_valid(a,ps):raise ValueError('Namespace needs validated precise received congfu clause')
 if not all(received(ps[e['paragraph_id']][1])for e in a['evidence']):raise ValueError('Cousin paragraph has nonreceived nested layer metadata')
 fids=g.get('named_father_assertion_ids',[])
 if not isinstance(fids,list)or len(fids)!=2 or len(set(fids))!=2:raise ValueError('Namespace needs two distinct named fathers')
 fathers=[assertions.get(i)for i in fids]
 if not all(f and father_bound(f,chapters)for f in fathers):raise ValueError('Namespace father evidence is not exact received text')
 if {f['subject_person_id']for f in fathers}!={a['subject_person_id'],a['object_person_id']}:raise ValueError('Cousin and father subjects differ')
 roots={f['object_person_id']for f in fathers};children={f['subject_person_id']for f in fathers}
 if len(roots)!=2 or len(roots|children)!=4 or set(g.get('root_person_ids',[]))!=roots:raise ValueError('Namespace roots must be distinct named father objects')
 for f in fathers:
  if any(b['predicate']=='father'and b['subject_person_id']==f['subject_person_id']and b['object_person_id']!=f['object_person_id']for b in assertions.values()):raise ValueError('Conflicting father must be reviewed before namespace')
 proofs={p['id']:p for p in[a]+fathers};refs=g.get('references',[])
 if not isinstance(refs,list)or len(refs)!=3 or {r.get('assertion_id')for r in refs}!=set(proofs):raise ValueError('Namespace requires all three attributed references')
 for r in refs:
  proof=proofs[r['assertion_id']]
  if(not r.get('scope')or not any(all(r.get(k)==e.get(k)for k in('chapter_id','paragraph_id','source_id','quote'))and r.get('url')in(chapters[e['chapter_id']]['source'].get('url'),chapters[e['chapter_id']]['source'].get('permalink'))for e in proof['evidence'])):raise ValueError('Namespace reference quote/source/layer mismatch')
 rows={r['person_id']:r for r in assembly.get('members',[])}
 if len(rows)!=len(assembly.get('members',[]))or assembly.get('entry_person_id')not in roots or not roots<=set(rows):raise ValueError('Namespace root/member/entry mismatch')
 output={}
 for pid,r in rows.items():
  if set(r)!={'person_id','source_person_ids','representative_source_person_id','identity_equivalence_decision_ids','parent_person_id','source_assertion_id','collateral_root_group_id'}:raise ValueError('Unknown namespace member pedigree fields')
  if pid not in people or not pid.startswith(ns+'_')or r.get('source_person_ids')!=[pid]or r.get('representative_source_person_id')!=pid or r.get('identity_equivalence_decision_ids')!=[]:raise ValueError('Namespace cannot alias or invent members')
  parent=r.get('parent_person_id')
  if pid in roots:
   if parent is not None or r.get('source_assertion_id')is not None or r.get('collateral_root_group_id')!=g['id']or len(pid)!=len(ns)+2:raise ValueError('Two actual roots must be same generation without fictitious parent')
  else:
   f=assertions.get(r.get('source_assertion_id'))
   if(not parent or parent not in rows or not f or f.get('status')!='source_attested'or f.get('qualifiers',{}).get('lineage')!='paternal'or f['predicate']!='father'or f['subject_person_id']!=pid or f['object_person_id']!=parent or family_path_errors(pid,dict(connection='father',parent_person_id=parent))):raise ValueError('Namespace descendant requires actual one-generation father assertion')
   seen={pid};cursor=parent
   while cursor not in roots:
    if cursor in seen or cursor not in rows:raise ValueError('Namespace path cycle/disconnected branch')
    seen.add(cursor);cursor=rows[cursor].get('parent_person_id')
  output[pid]=dict(copy.deepcopy(r),assembly_id=assembly['id'],root_person_id=None,namespace_id=ns,namespace_entry_person_id=assembly['entry_person_id'],collateral_root_group=copy.deepcopy(g),status=assembly['status'],human_reviewed=assembly['human_reviewed'])
 return output

def namespace_index_root(family,members):
 """Select a real heading entry; never require namespace to have a profile."""
 matches=[r for r in members if r.get('assembled_identity',{}).get('namespace_id')==family]
 if matches:
  entries={r['assembled_identity']['namespace_entry_person_id']for r in matches}
  if len(entries)!=1:raise ValueError('Conflicting namespace entries')
  entry=next(iter(entries));row=next((r for r in members if r['person_id']==entry),None)
  if row is None:raise ValueError('Namespace real entry absent')
  group=matches[0]['assembled_identity'].get('collateral_root_group',{})
  if group.get('type')=='explicit_received_brothers_parent_unidentified':return dict(row,label=row['label']+'等弟兄（原文明記；父未名）')
  return dict(row,label=row['label']+'等兩支（共同父未名；編輯接合）')
 return next(r for r in members if r['person_id']==family)

def prune_person_files(destination, expected_ids):
 """Keep the established export cleanup rule; no redirect or alias is retained."""
 removed=[]
 for path in destination.glob('*.json'):
  if path.name!='index.json'and path.stem not in expected_ids:
   path.unlink();removed.append(path.name)
 return removed
