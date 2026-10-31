"""Opt-in editorial surname through received source roles, never new parentage.

Capture bytes and actual current MIDs authorize source consistency, not automatic
historical identity. No person/book whitelist, ID ancestry or raw-fiction bridge.
"""
import hashlib,json,re
from pathlib import Path
KIND='contextual_surname_from_observed_named_near_kin'

def same(a,b):
 if type(a)is not type(b):return False
 if type(a)is dict:return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
 if type(a)is list:return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 return a==b

def read(root,rel):
 root=Path(root).resolve();p=Path(rel);assert not p.is_absolute()and'..'not in p.parts
 q=root/p;assert q.is_file()and not q.is_symlink()and q.resolve().is_relative_to(root)
 return q.read_bytes()

def at(value,pointer):
 for token in pointer.split('/')[1:]:
  token=token.replace('~1','/').replace('~0','~');value=value[int(token)]if type(value)is list else value[token]
 return value

def validate(name,names,chapters,assertions,root):
 try:
  b=name['surname_basis'];assert type(b)is dict and set(b)=={'kind','status','human_reviewed','rationale','frames','seed','edge'}
  assert b['kind']==KIND and b['status']==name['status']=='contextual_provisional'and b['human_reviewed']is False and name['human_reviewed']is False and type(b['rationale'])is str and b['rationale'].strip()
  try:from scripts.surname_source_frames import source_view
  except ImportError:from surname_source_frames import source_view
  ps,cs,people,marker,anchor,existing_assertion=source_view(b['frames'],chapters,assertions,root)
  seed=b['seed'];sc,sp,sm=marker(seed['paragraph_id'],seed['person_mention_id']);assert seed['surname']==name['surname']and seed['ming']
  if seed['kind']=='literal_full_name':assert set(seed)=={'kind','paragraph_id','person_mention_id','surname','ming'}and sm['surface']==seed['surname']+seed['ming']
  elif seed['kind']=='explicit_surname_named_head':
   assert set(seed)=={'kind','paragraph_id','person_mention_id','surname','ming','surname_anchor','head_anchor'};anchor(seed['surname_anchor']);anchor(seed['head_anchor']);head=seed['head_anchor'];sa=seed['surname_anchor'];assert sm['surface']==seed['ming']and sa['surface']=='姓'+seed['surname']+'氏'and sp['text'][sm['start']-1:sm['start']]=='諱'
   assert head['paragraph_id']==sa['paragraph_id']==sp['id']and sp['text'][:head['start']].strip()=='' and head['end']==max(sm['end'],sa['end']) and head['end']<=sp['text'].index('。') and sp['text'][head['end']]in'，。' and head['start']<=min(sm['start'],sa['start'])and max(sm['end'],sa['end'])<=head['end']and not any(q in head['surface']for q in'「」『』')
   assert all(m.get('person_id')==sm['person_id']for m in sp['mentions']if m.get('kind')=='person'and head['start']<=m['start']<head['end'])
  elif seed['kind']=='declared_clan_near_member':
   assert set(seed)=={'kind','paragraph_id','person_mention_id','surname','ming','clan_anchor','near_family_anchor','near_parent_mid','father_assertion_id','father_assertions_path','interpretation','not_full_name_literal'}
   assert seed['not_full_name_literal']is True and seed['interpretation']=='editorial_near_member_of_declared_clan' and sm['surface']==seed['ming']
   clan=seed['clan_anchor'];near=seed['near_family_anchor'];anchor(clan);anchor(near)
   assert clan['paragraph_id']==near['paragraph_id']==sp['id']and clan['start']==0 and clan['surface']==seed['surname']+'氏'and sp['text'][clan['end']:].startswith('出自')
   _,_,parent=marker(sp['id'],seed['near_parent_mid']);assert near['start']==parent['start']and near['start']>clan['end']and near['end']==len(sp['text'].rstrip('。'))
   assert re.fullmatch(re.escape(parent['surface'])+'[一二三四五六七八九十]+子：[\u3400-\u9fff、]+',near['surface']) and sm['start']>parent['end']and sm['end']<=near['end']
   fa=existing_assertion(seed['father_assertions_path'],seed['father_assertion_id']);assert fa['predicate']=='father'and fa['status']=='source_attested'and fa['subject_person_id']==sm['person_id']and fa['object_person_id']==parent['person_id']
   fe,=fa['evidence'];assert fe['paragraph_id']==sp['id']and fe['chapter_id']==sc['id']and fe['source_id']==sc['source_id']and fe['quote']==sp['text']and fe['subject_person_mention_id']==sm['id']and fe['object_person_mention_id']==parent['id']
  else:raise AssertionError('Unsupported named seed')
  tc,tp,tm=marker(name['paragraph_id'],name['person_mention_id']);assert tc['id']==name['chapter_id']and name['quote']==tp['text']and tm['person_id']==name['person_id']
  na=name['source_anchor'];anchor(na);assert na.get('paragraph_id',tp['id'])==tp['id'] and na['surface']==name['ming']and tm['start']<=na['start']<na['end']<=tm['end']and na['end']==tm['end']
  edge=b['edge'];assert set(edge)==({'assertion_id','traversal','clause_anchor','rule','seed_role_mid','target_role_mid','assertions_path'}|({'resumed_target_mid'}if edge['rule']=='named_emperor_father_huangkao'else set()))
  a=existing_assertion(edge['assertions_path'],edge['assertion_id']);q=a['qualifiers'];assert a['status']=='source_attested'and not q.get('adoptive')and not q.get('sworn')and not q.get('same_mother_only')and q.get('shared_father')is not False and q.get('lineage')not in('maternal','non_paternal')
  e,=a['evidence'];ec,ep=ps[e['paragraph_id']];assert e['chapter_id']==ec['id']and e['work_id']==ec['work_id']and e['book_id']==ec['book_id']and e['source_id']==ec['source_id']and e['quote']==ep['text']
  _,_,srole=marker(ep['id'],edge['seed_role_mid']);_,_,trole=marker(ep['id'],edge['target_role_mid']);assert srole['person_id']==sm['person_id']and trole['person_id']==tm['person_id']and srole['person_id']!=trole['person_id']
  assert e['subject_person_mention_id']in(srole['id'],trole['id'])and e['object_person_mention_id']in(srole['id'],trole['id'])and e['subject_person_mention_id']!=e['object_person_mention_id'];assert a['subject_person_id']==next(m['person_id']for m in ep['mentions']if m['id']==e['subject_person_mention_id'])and a['object_person_id']==next(m['person_id']for m in ep['mentions']if m['id']==e['object_person_mention_id'])
  ca=edge['clause_anchor'];anchor(ca);assert ca['paragraph_id']==ep['id']and q['source_term']in ca['surface'];pre=ep['text'][:ca['start']];assert pre.count('「')==pre.count('」')and pre.count('『')==pre.count('』')and not any(x in ca['surface']for x in'「」『』')
  pair=(sm['person_id'],tm['person_id']);rule=edge['rule']
  if rule=='head_named_paternal_grandfather':
   assert a['predicate']=='grandfather'and edge['traversal']=='child_to_paternal_grandfather'and(a['subject_person_id'],a['object_person_id'])==pair and ep['id']==sp['id']and srole['id']==sm['id']and ca['surface']=='祖'+trole['surface']and ca['start']+1==trole['start']and ca['end']==trole['end']
   assert sm['start']==len(sp['text'])-len(sp['text'].lstrip())and re.match('[，,]?字',sp['text'][sm['end']:])
  elif rule=='named_brother_clause':
   assert a['predicate']=='brother'and edge['traversal']=='named_person_to_brother'and(a['subject_person_id'],a['object_person_id'])==(pair[1],pair[0])
   assert ca['start']==srole['start']and ca['end']==trole['end']and ep['text'][srole['end']:trole['start']]=='兄'and ca['surface']==srole['surface']+'兄'+trole['surface']
  elif rule=='topic_di_enumeration':
   assert a['predicate']=='brother'and edge['traversal']=='named_person_to_brother'and(a['subject_person_id'],a['object_person_id'])==(pair[1],pair[0])and ca['start']==srole['start']and ca['end']==trole['end']
   bridge=ep['text'][srole['end']:trole['start']];assert bridge.endswith(('及弟','，弟'))and not any(x in bridge for x in'。；：「」『』')
   # Other named roles in this finite clause are finite ally/older-brother roles,
   # never a new topic: no family relation is inferred from their membership.
   for m in ep['mentions']:
    if srole['end']<=m['start']<trole['start']:assert m.get('kind')not in('pronoun','unresolved')
    if srole['end']<=m['start']<trole['start']and m.get('kind')=='person':assert ep['text'][max(srole['end'],m['start']-2):m['start']].endswith(('其將','兄'))
  elif rule=='named_head_numbered_son':
   assert a['predicate']=='father'and edge['traversal']=='father_to_child'and(a['object_person_id'],a['subject_person_id'])==pair and (trole['id']==tm['id']or trole['end']<tm['start']and ep['text'][trole['end']:tm['start']]=='諱')and ca['surface']==srole['surface']+q['source_term'][len(srole['surface']):]and re.fullmatch(re.escape(srole['surface'])+'(?:第[一二三四五六七八九十]+|長)子',ca['surface'])
   head=next(m for m in ep['mentions']if m['kind']=='person');assert head['person_id']==tm['person_id']and ep['text'][:head['start']].strip()==''
   assert ca['start']==srole['start']and ca['end']==srole['end']+len(ca['surface'])-len(srole['surface'])and tm['end']<srole['start']and re.fullmatch('[，、]?字[^。]+，?',ep['text'][tm['end']:srole['start']])
  elif rule=='named_emperor_father_huangkao':
   assert a['predicate']=='father'and edge['traversal']=='child_to_father'and(a['subject_person_id'],a['object_person_id'])==pair and ep['id']==sp['id']
   _,_,resume=marker(ep['id'],edge['resumed_target_mid']);assert resume['person_id']==trole['person_id']and resume['surface']==trole['surface']==name['ming']and ep['text'][trole['end']:resume['start']]=='，'and ca['surface']==resume['surface']+'即皇考'and ca['start']==resume['start']and ca['end']==resume['end']+3
  else:raise AssertionError('Unsupported finite received kin-role grammar')
 except(AssertionError,KeyError,ValueError,TypeError,IndexError,StopIteration,OSError,AttributeError)as error:
  raise ValueError('Observed surname needs honest captured complete paragraphs, explicit named seed, exact existing kin roles and reciprocal current MIDs; no ID/label/unknown-parent inference')from error
