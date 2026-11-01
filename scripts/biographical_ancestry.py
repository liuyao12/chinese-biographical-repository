# coding: utf-8
"""Editorial paternal assembly from an explicit biography-opening 祖/父 list.
Raw unspecified 祖 lineage remains unspecified; no father assertion is added.
"""
def biographical_zu_fu_parent_valid(member, rows, assertions, chapters):
 if member.get('parent_connection',{}).get('interpretation_basis')=='bound_unpunctuated_biography_zu_fu_sequence':
  try:from .unpunctuated_zu_fu_assembly import valid as unpunctuated_valid
  except ImportError:from unpunctuated_zu_fu_assembly import valid as unpunctuated_valid
  return unpunctuated_valid(member,rows,assertions,chapters)
 c=member.get('parent_connection',{})
 near=assertions.get(c.get('nearer_ancestor_assertion_id'),{})
 far=assertions.get(c.get('farther_ancestor_assertion_id'),{})
 witness=rows.get(c.get('chain_subject_person_id'),{})
 parent=rows.get(member.get('parent_person_id'),{})
 if not (c.get('type')=='parent_between_consecutive_ancestors'
  and c.get('interpretation_basis')=='biographical_zu_fu_sequence'
  and c.get('status')=='contextual_provisional' and c.get('human_reviewed') is False
  and isinstance(c.get('rationale'),str) and c['rationale'].strip()
  and member.get('source_assertion_id') is None
  and near.get('status')==far.get('status')=='source_attested'
  and near.get('predicate')=='father' and far.get('predicate')=='grandfather'
  and near.get('subject_person_id')==far.get('subject_person_id')
  and near.get('subject_person_id') in witness.get('source_person_ids',[])
  and near.get('object_person_id') in member.get('source_person_ids',[])
  and far.get('object_person_id') in parent.get('source_person_ids',[])
  and near.get('qualifiers',{}).get('lineage') in (None,'unspecified','paternal')
  and far.get('qualifiers',{}).get('lineage') in ('unspecified','paternal')):return False
 people=[near['subject_person_id'],far['object_person_id'],near['object_person_id']]
 if len(set(people))!=3:return False
 refs=c.get('references')
 if not isinstance(refs,list) or len(refs)!=2 or any(not isinstance(x,dict) for x in refs):return False
 if {x.get('assertion_id') for x in refs}!={near['id'],far['id']}:return False
 common={(e.get('chapter_id'),e.get('paragraph_id'),e.get('source_id'),e.get('quote')) for e in near.get('evidence',[])}&{(e.get('chapter_id'),e.get('paragraph_id'),e.get('source_id'),e.get('quote')) for e in far.get('evidence',[])}
 for cid,pid,sid,quote in common:
  chapter=chapters.get(cid,{});p=next((p for p in chapter.get('paragraphs',[]) if p.get('id')==pid),None)
  if not p or p.get('text_layer')!='received_chapter' or p.get('text')!=quote or chapter.get('source_id')!=sid:continue
  if not all(x.get('scope') and (x.get('chapter_id'),x.get('paragraph_id'),x.get('source_id'),x.get('quote'))==(cid,pid,sid,quote) and x.get('url') in [chapter.get('source',{}).get('url'),chapter.get('source',{}).get('permalink')] for x in refs):continue
  mentions=[m for m in p.get('mentions',[]) if m.get('kind')=='person' and quote[m.get('start',0):m.get('end',0)]==m.get('surface')]
  if not any(m.get('person_id')==people[0] and m.get('start')==0 for m in mentions):continue
  bound=[]
  for a,role in [(far,'祖'),(near,'父')]:
   choices=[m for m in mentions if m.get('person_id')==a['object_person_id'] and m.get('start',0)>0 and quote[m['start']-1:m['start']]==role and a.get('qualifiers',{}).get('source_term','').startswith(role+m['surface']) and m['surface'] not in ['祖','父','其','之']]
   if len(choices)!=1:break
   bound.append(choices[0])
  if len(bound)!=2:continue
  g,f=bound
  if not (g['start']<f['start'] and quote[g['start']-2:g['start']]!='外祖'):continue
  # The opening ancestry list may contain 字/office text, never another named person or a transfer/alternative.
  segment=quote[:f['end']]
  if any(x in segment for x in ['外祖','母父','曰','云','非','未','不','或','「','」','『','』','。','；','！','？']):continue
  if any(m.get('person_id') not in people and m.get('start',-1)<f['end'] for m in mentions):continue
  if any(a.get('predicate')=='father' and a.get('subject_person_id') in member.get('source_person_ids',[]) and a.get('object_person_id') not in parent.get('source_person_ids',[]) for a in assertions.values()):continue
  return True
 return False


PUNCTUATED_PATERNAL_PAIR = 'punctuated_biography_explicit_paternal_zu_fu_pair'

def punctuated_paternal_pair_valid(member, rows, assertions, chapters, root, *, people):
 """An opt-in editorial edge; two literal source claims remain independent.
 The current rendered observation is NOT a fixed-revision/raw capture.
 """
 import json, hashlib, re
 from pathlib import Path
 try:
  c=member['parent_connection'];f=c['paternal_pair_frame']
  if (c['interpretation_basis']!=PUNCTUATED_PATERNAL_PAIR or c['type']!='parent_between_consecutive_ancestors'
      or c['status']!='contextual_provisional' or c.get('human_reviewed') is not False
      or not isinstance(c.get('rationale'),str) or not c['rationale'].strip()
      or member.get('source_assertion_id') is not None):return False
  if set(f)!={'chapter_path','assertions_path','observation_path','observation_sha256','chapter_id','paragraph_id','head_mention_id','grandfather_mention_id','father_mention_id'}:return False
  base=Path(root).resolve()
  def read(rel):
   p=Path(rel)
   if p.is_absolute() or '..' in p.parts or not p.parts or p.parts[0] not in ('corpus','source-evidence'):raise ValueError('unowned source path')
   at=base
   for bit in p.parts:
    at=at/bit
    if at.is_symlink():raise ValueError('symlink source')
   if not at.resolve().is_relative_to(base):raise ValueError('outside source')
   return at.read_bytes()
  def same(a,b):
   return type(a) is type(b) and (set(a)==set(b) and all(same(a[k],b[k]) for k in a) if isinstance(a,dict) else len(a)==len(b) and all(same(x,y) for x,y in zip(a,b)) if isinstance(a,list) else a==b)
  chapter=chapters[f['chapter_id']];physical=json.loads(read(f['chapter_path']))
  if not same(physical,chapter):return False
  if any(not isinstance(chapter.get(k),str) or not chapter[k] for k in ('work_id','book_id','source_id')):return False
  p=next(p for p in chapter['paragraphs'] if p['id']==f['paragraph_id']);t=p['text'];src=chapter['source']
  if p.get('text_layer')!='received_chapter':return False
  ob=read(f['observation_path'])
  if hashlib.sha256(ob).hexdigest()!=f['observation_sha256']:return False
  o=json.loads(ob)
  if (o.get('kind')!='current_rendered_observation' or o.get('fixed_body_obtained') is not False
      or o.get('raw_capture_obtained') is not False or o.get('image_checked') is not False
      or o.get('human_reviewed') is not False or any(not same(o.get(k),chapter[k]) for k in ('work_id','book_id','source_id'))
      or not same(o.get('reported_revision'),src.get('revision_id'))
      or o.get('url')!=src.get('url') or o.get('paragraph_sha256')!=hashlib.sha256(t.encode()).hexdigest()
      or src.get('observation_kind')!='current_rendered_observation'
      or src.get('fixed_body_obtained') is not False or src.get('raw_capture_obtained') is not False
      or src.get('image_verified') is not False or src.get('human_reviewed') is not False):return False
  observed=o['observed_text'];mapping=o['character_map']
  if not isinstance(observed,str) or not isinstance(mapping,list) or len(mapping)!=len(t):return False
  if any(type(i) is not int or not 0<=i<len(observed) for i in mapping) or mapping!=sorted(set(mapping)):return False
  if ''.join(observed[i] for i in mapping)!=t:return False
  # Only indentation and numeric editorial callouts may be omitted, never words.
  kept=set(mapping);i=0
  while i<len(observed):
   if i in kept:i+=1;continue
   end=i+1
   while end<len(observed) and end not in kept:end+=1
   # Validate each contiguous omitted run in its original position. Never
   # concatenate punctuation/digits across retained source characters.
   if not re.fullmatch(r'(?:\s+|\[[0-9]+\])+',observed[i:end]):return False
   i=end
  ms={m['id']:m for m in p['mentions']}
  if len(ms)!=len(p['mentions']):return False
  h,g,n=[ms[f[k]] for k in ('head_mention_id','grandfather_mention_id','father_mention_id')]
  ids=[h['person_id'],n['person_id'],g['person_id']]
  if len(set(ids))!=3 or h['start']!=0:return False
  if any(m.get('kind')!='person' or m.get('status') in ('unresolved','ambiguous','rejected')
         or type(m.get('start')) is not int or type(m.get('end')) is not int
         or not 0<=m['start']<m['end']<=len(t) or t[m['start']:m['end']]!=m['surface']
         or m['surface'] in ('其','之','父','祖') for m in (h,g,n)):return False
  # Exactly one complete opening head, then the complete two-role office list.
  pattern=(re.escape(h['surface'])+r'(?:字[\u3400-\u9fff]{1,6})?，[\u3400-\u9fff]{1,12}人也。祖'
           +re.escape(g['surface'])+r'，([^，。；！？]+)，父'+re.escape(n['surface'])+r'，([^，。；！？]+)。')
  match=re.fullmatch(pattern,t)
  if not match:return False
  if g['start']!=t.index('。祖')+2 or n['start']!=t.index('，父')+2:return False
  for career in match.groups():
   if any(x in career for x in ('祖','父','母','子','妻','妾','兄','弟','嗣','繼','養','出','非','未','不','無','或','曰','云','「','」','『','』')):return False
   if not re.fullmatch(r'[\u3400-\u9fff]+',career) or not career.endswith(('太守','刺史','卿','將軍','尚書','侍郎','令','相')):return False
  if {m['id'] for m in p['mentions']}!={h['id'],g['id'],n['id']}:return False
  aa={a['id']:a for a in json.loads(read(f['assertions_path']))['assertions']}
  near=assertions[c['nearer_ancestor_assertion_id']];far=assertions[c['farther_ancestor_assertion_id']]
  if not same(aa.get(near['id']),near) or not same(aa.get(far['id']),far) or near['id']==far['id'] or any(not same(assertions.get(k),v) for k,v in aa.items()):return False
  if c['chain_subject_person_id'] not in rows or h['person_id'] not in rows[c['chain_subject_person_id']]['source_person_ids']:return False
  if n['person_id'] not in member['source_person_ids'] or g['person_id'] not in rows[member['parent_person_id']]['source_person_ids']:return False
  def evidence(e,a,m):
   return (e.get('chapter_id')==chapter['id'] and e.get('paragraph_id')==p['id']
           and all(same(e.get(k),chapter[k]) for k in ('work_id','book_id','source_id')) and e.get('quote')==t
           and e.get('subject_person_mention_id')==h['id'] and e.get('object_person_mention_id')==m['id'])
  for a,pred,m,term in ((near,'father',n,'父'),(far,'grandfather',g,'祖')):
   q=a.get('qualifiers',{})
   if (a.get('status')!='source_attested' or a.get('human_reviewed') is not False
       or a.get('predicate')!=pred or a.get('subject_person_id')!=h['person_id'] or a.get('object_person_id')!=m['person_id']
       or q.get('lineage')!='paternal' or q.get('source_term')!=term+m['surface']
       or set(q)-{'lineage','source_term','generation_difference'}
       or ('generation_difference' in q and (type(q['generation_difference']) is not int or q['generation_difference']!=(-1 if pred=='father' else -2)))
       or not any(evidence(e,a,m) for e in a.get('evidence',[]))):return False
  registry=base/'registry'/'persons.json'
  if (base/'registry').is_symlink() or registry.is_symlink():return False
  physical_people={r['id']:r for r in json.loads(registry.read_bytes())['persons']}
  for m in (h,g,n):
   for catalog in (physical_people,people):
    person=catalog[m['person_id']]
    if not any(a.get('surface')==m['surface'] and m['id'] in a.get('mention_ids',[]) for a in person['aliases']):return False
    if not any(e.get('mention_id')==m['id'] and e.get('chapter_id')==chapter['id'] and e.get('paragraph_id')==p['id'] and e.get('quote')==m['surface'] for e in person['evidence']):return False
  # All relevant competing edges stay visible and prevent silent preference.
  for a in assertions.values():
   s,o2,pred=a.get('subject_person_id'),a.get('object_person_id'),a.get('predicate')
   if s==n['person_id'] and pred=='father' and o2!=g['person_id']:return False
   if s==h['person_id'] and ((pred=='father' and o2!=n['person_id']) or (pred=='grandfather' and o2!=g['person_id'])):return False
  refs=c['references']
  return (len(refs)==2 and {r.get('assertion_id') for r in refs}=={near['id'],far['id']}
          and all(r.get('chapter_id')==chapter['id'] and r.get('paragraph_id')==p['id'] and all(same(r.get(k),chapter[k]) for k in ('work_id','book_id','source_id'))
                  and r.get('quote')==t and isinstance(r.get('scope'),str) and r['scope'].strip()
                  and r.get('url')==src['url'] for r in refs))
 except (KeyError,TypeError,ValueError,IndexError,StopIteration,AttributeError,OSError):return False
