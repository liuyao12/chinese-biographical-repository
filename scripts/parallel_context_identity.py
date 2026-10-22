# coding: utf-8
"""Fixed primary-context identity judgments, distinct from reported variants.
This validates machine-readable bindings and editorial boundaries, not NLU truth.
"""
from pathlib import Path
import hashlib,re
NEG=('不','未','非','無','莫','弗','勿')
def affirmative(surface):return bool(surface)and not any(x in surface for x in NEG)
def received_anchor(text,start,end):
 if not 0<=start<end<=len(text):return False
 return not any(start<m.end()and end>m.start()for m in re.finditer(r'<ref\b[^>]*>.*?</ref\s*>|<!--.*?-->',text,re.S|re.I))
def _safe(root,relative,prefix):
 p=Path(relative)
 if p.is_absolute()or '..'in p.parts or not p.parts or p.parts[0]!=prefix:raise ValueError('source path boundary')
 q=Path(root)/p
 if q.resolve()!=Path(root).resolve()/p or not q.is_file():raise ValueError('source symlink/path boundary')
 return q

def valid(decision,chapters,people,root):
 try:
  r=decision['parallel_context_reading'];pid=decision['person_id'];ids=r['candidate_person_ids'];other=r['countercandidate_person_id']
  if set(r)!={'kind','person_mention_id','target_mention_ids','received_surface','preferred_surface','candidate_person_ids','countercandidate_person_id','countercandidate_surface','source_spelling_is_not_alias','status','rationale','local_paragraph_id','local_quote','local_cues','local_binding','parallel_reference'}:return False
  if r['kind']!='two_candidates_same_event_parallel_context'or r['status']!='editorial_provisional'or r['source_spelling_is_not_alias']is not True or decision.get('human_reviewed')is not False or not r['rationale']:return False
  if len(ids)!=2 or len(set(ids))!=2 or set(ids)!={pid,other}or not set(ids)<=set(people):return False
  aliases=lambda p:{x['surface']for x in people[p]['aliases']}
  if r['preferred_surface']not in aliases(pid)or r['countercandidate_surface']not in aliases(other)or r['received_surface']==r['preferred_surface']:return False
  c=chapters[decision['chapter_ids'][0]];p=next(p for p in c['paragraphs']if p['id']==r['local_paragraph_id'])
  if p.get('text_layer')!='received_chapter'or any(k in p for k in ['annotator','attached_note_to_paragraph_id'])or p['text']!=r['local_quote']:return False
  mm={m['id']:m for m in p['mentions']};mid=r['person_mention_id'];target=r['target_mention_ids']
  if len(target)!=len(set(target))or mid not in target or not set(target)<=set(mm):return False
  if any(mm[x]['person_id']!=pid for x in target)or mm[mid]['surface']!=r['received_surface']:return False
  if any(mid in a['mention_ids']for a in people[pid]['aliases']):return False
  if not any(e.get('paragraph_id')==p['id']and e.get('chapter_id')==c['id']and e.get('source_id')==c['source_id']and e['quote']==p['text']for e in decision['evidence']):return False
  # Full local unformatted raw line, not a retained fragment or detached note.
  b=r['local_binding'];rawbytes=_safe(root,b['source_path'],'sources').read_bytes();raw=rawbytes.decode('utf-8')
  if hashlib.sha256(rawbytes).hexdigest()!=b['raw_file_sha256']or c['source']['wikitext_sha256']!=b['raw_file_sha256']or c['source']['raw_file']!=b['source_path']:return False
  a,z=b['start'],b['end'];line_a=raw.rfind('\n',0,a)+1;line_z=raw.find('\n',z);line_z=len(raw)if line_z<0 else line_z
  if not received_anchor(raw,a,z)or raw[a:z]!=p['text']or raw[line_a:line_z].strip()!=p['text']or raw.count('\n',0,a)+1!=p['source_position']['first_line']or p['source_position']['first_line']!=p['source_position']['last_line']:return False
  if len(r['local_cues'])!=2:return False
  for cue in r['local_cues']:
   if p['text'][cue['start']:cue['end']]!=cue['surface']or not affirmative(cue['surface'])or cue['start']<mm[mid]['end']:return False
  ref=r['parallel_reference'];w=chapters[ref['witness_chapter_id']];rb=_safe(root,ref['source_path'],'sources').read_bytes();text=rb.decode('utf-8')
  if hashlib.sha256(rb).hexdigest()!=ref['raw_file_sha256']or w['source']['wikitext_sha256']!=ref['raw_file_sha256']or w['source']['revision_id']!=ref['revision_id']or w['source']['permalink']!=ref['url']:return False
  units=ref['units'];headers=list(re.finditer(r'^==[^=\n].*?==\s*$',text,re.M));bounds={h.start():headers[i+1].start()if i+1<len(headers)else len(text)for i,h in enumerate(headers)}
  if len(units)!=2 or {u['candidate_person_id']for u in units}!=set(ids):return False
  for u in units:
   if bounds.get(u['start'])!=u['end']or text[u['start']:u['end']]!=u['raw']or hashlib.sha256(u['raw'].encode()).hexdigest()!=u['sha256']:return False
   intro=text[u['start']:u['end']].splitlines()[1].strip();name=u['identity_anchor']
   if name['surface']not in aliases(u['candidate_person_id'])or text[name['start']:name['end']]!=name['surface']or not received_anchor(text,name['start'],name['end'])or not u['start']<=name['start']<name['end']<=u['end']:return False
   intro_start=text.index(intro,u['start']);
   if not intro_start<=name['start']<name['end']<=intro_start+len(intro):return False
  if units[0]['end']!=units[1]['start']:return False
  anchors=ref['anchors']
  if set(anchors)!={'preferred_event','bowing_event','counter_distinguishes_preferred'}:return False
  for role,x in anchors.items():
   u=next(u for u in units if u['candidate_person_id']==(other if role=='counter_distinguishes_preferred'else pid))
   if not u['start']<=x['start']<x['end']<=u['end']or text[x['start']:x['end']]!=x['surface']or not affirmative(x['surface'])or not received_anchor(text,x['start'],x['end']):return False
  if r['preferred_surface']not in anchors['counter_distinguishes_preferred']['surface']:return False
  return True
 except (ValueError,KeyError,TypeError,IndexError,StopIteration,UnicodeError,OSError):return False
