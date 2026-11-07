# coding: utf-8
"""Declarative, offline editorial reference bindings, not automated historical proof.

Only a validated binding's enumerated identity leaves receive a comparison view.
Raw/capture bytes, glyphs, offsets and all other metadata remain owner-checked.
No person ID, personal name, chapter ID, or allusion word is a code whitelist.
"""
import copy,hashlib,json,re,string
from collections import Counter
from html import escape
from pathlib import Path
from urllib.parse import urlsplit,unquote
from xml.etree import ElementTree as ET
ANNOTATION_REF='primary_reference_resolutions_ref'
SEMANTIC_KEYS=('kind','person_id','status','interpretation_note','candidate_person_ids','identity_decision_id')
UNRESOLVED_KEYS={'id','person_id','surfaces','scope','chapter_ids','status','candidate_person_ids','evidence','rationale','human_reviewed','model','record_type','paragraph_ids','unresolved_mention_ids','candidate_list_exhaustive','scope_note'}
def same(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 return a==b
def sha(b):return hashlib.sha256(b).hexdigest()
def raw(root,rel):
 root=Path(root).resolve();p=Path(rel);assert not p.is_absolute()and'..'not in p.parts;q=root/p;assert q.resolve()==q and q.is_file();return q.read_bytes()
def read(root,rel):return json.loads(raw(root,rel))
def public_url(s):
 assert isinstance(s,str)and s and not any(c.isspace()or ord(c)<32 for c in s)
 u=urlsplit(s);assert u.scheme in ('http','https')and u.hostname and u.username is None and u.password is None
 return s
def counts(ch):
 values=[m['kind']for p in ch['paragraphs']for m in p['mentions']];assert all(x in ('person','pronoun','unresolved')for x in values)
 c=Counter(values);return{k:c[k]for k in ('person','pronoun','unresolved')}
def _pointer(record,pointer):
 assert pointer=='/annotation/coverage'or re.fullmatch(r'/annotation/limitations/\d+',pointer)
 parts=pointer.split('/')[1:];at=record
 for key in parts[:-1]:at=at[int(key)]if isinstance(at,list)else at[key]
 key=int(parts[-1])if isinstance(at,list)else parts[-1];return at,key
def _format(template,values):
 assert isinstance(template,str)
 for _,field,fmt,conversion in string.Formatter().parse(template):
  if field is not None:assert field in values and not fmt and conversion is None
 return template.format(**values)
def _target(ch,e):
 t=e['target'];rows=[(p,m)for p in ch['paragraphs']for m in p['mentions']if m['id']==t['mention_id']];assert len(rows)==1;p,m=rows[0]
 assert p['id']==t['paragraph_id']and sha(p['text'].encode())==t['paragraph_sha256']
 assert all(same(m.get(k),t[k])for k in ('start','end','surface'))and m['source_role']==e['role']
 assert type(m['start'])is int and type(m['end'])is int and p['text'][m['start']:m['end']]==m['surface'];return p,m

def resolve(root,chapter_path,people=None):
 """Validate captured evidence and current endpoints of explicit editorial decisions."""
 ch=read(root,chapter_path);assert isinstance(ch,dict)and isinstance(ch.get('annotation'),dict);ref=ch['annotation'].get(ANNOTATION_REF)
 if ref is None:return None
 assert isinstance(ref,str)and ref.startswith('source-evidence/')
 doc=read(root,ref);assert set(doc)=={'format_version','record_type','owner','decision_path','entries','progress_formatters','editorial_notice'}
 assert type(doc['format_version'])is int and doc['format_version']==1 and doc['record_type']=='primary_source_reference_resolution_set'
 owner=doc['owner'];assert set(owner)=={'chapter_path','chapter_id','work_id','book_id','source_id'}and owner['chapter_path']==chapter_path
 assert all(ch[k]==owner['chapter_id'if k=='id'else k]for k in ('id','work_id','book_id','source_id'))
 assert isinstance(doc['editorial_notice'],str)and doc['editorial_notice']
 if people is None:people={p['id']:p for p in read(root,'registry/persons.json')['persons']}
 assert doc['decision_path'].startswith('corpus/');decisions=read(root,doc['decision_path']);assert decisions['record_type']=='identity_decision_set'and decisions['chapter_id']==ch['id']
 entries=doc['entries'];assert isinstance(entries,list)and entries and len({e['id']for e in entries})==len(entries)and len({e['target']['mention_id']for e in entries})==len(entries)
 resolved=[]
 for e in entries:
  assert set(e)=={'id','role','kind','target','canonical_anchor','primary','interpretation'}
  assert isinstance(e['id'],str)and e['id']and isinstance(e['role'],str)and e['role']and e['kind']=='allusive_person'
  assert set(e['target'])=={'paragraph_id','mention_id','start','end','surface','paragraph_sha256'};p,m=_target(ch,e)
  s=e['canonical_anchor'];assert set(s)=={'path','source_dimensions','source_metadata_sha256','paragraph_id','paragraph_text_sha256','marker','reverse'}and s['path'].startswith('corpus/')
  source=read(root,s['path']);assert all(same(source[k],v)for k,v in s['source_dimensions'].items())and set(s['source_dimensions'])=={'id','work_id','book_id','source_id'}
  assert sha((json.dumps(source['source'],ensure_ascii=False,indent=2)+'\n').encode())==s['source_metadata_sha256']
  ps=[p for p in source['paragraphs']if p['id']==s['paragraph_id']];assert len(ps)==1;sp=ps[0];assert sha(sp['text'].encode())==s['paragraph_text_sha256']
  ms=[m for m in sp['mentions']if m['id']==s['marker']['id']];assert len(ms)==1;sm=ms[0]
  assert same({k:v for k,v in sm.items()if k!='person_id'},s['marker'])and sm['kind']=='person'and sp['text'][sm['start']:sm['end']]==sm['surface']
  pid=sm['person_id'];assert pid in people;actor=people[pid]
  assert [v for v in actor['evidence']if v.get('mention_id')==sm['id']]==[s['reverse']]
  assert [(a['surface'],mid)for a in actor['aliases']for mid in a['mention_ids']if mid==sm['id']]==[(sm['surface'],sm['id'])]
  w=e['primary'];assert set(w)=={'acquisition_kind','observation_path','observation_sha256','fixed_attempt_path','fixed_attempt_sha256','read_url','reported_permalink','reported_revision','current_rendered_body_read','fixed_permalink_body_read','original_wikitext_obtained','actual_print_edition','image_verified','human_reviewed','complete_tool_lines','complete_unit','normalized_unit_sha256','normalization','citation_layer_kind','source_layer','identity_quote','context_quote'}
  assert w['acquisition_kind']=='current_rendered_unknown_print'
  for k,v in {'current_rendered_body_read':True,'fixed_permalink_body_read':False,'original_wikitext_obtained':False,'actual_print_edition':None,'image_verified':False,'human_reviewed':False}.items():assert same(w[k],v)
  assert type(w['reported_revision'])is int and w['reported_revision']>0
  for key in ('read_url','reported_permalink'):public_url(w[key])
  assert str(w['reported_revision'])in w['reported_permalink']and w['read_url']!=w['reported_permalink']
  for key in ('observation_path','fixed_attempt_path'):assert w[key].startswith('source-evidence/')
  obsraw=raw(root,w['observation_path']);fixedraw=raw(root,w['fixed_attempt_path']);assert sha(obsraw)==w['observation_sha256']and sha(fixedraw)==w['fixed_attempt_sha256']
  obs=json.loads(obsraw);fixed=json.loads(fixedraw);assert isinstance(obs,str)and isinstance(fixed,str)and unquote(w['read_url'])in unquote(obs)
  assert unquote(w['reported_permalink'])in unquote(fixed)and 'Cache miss'in fixed
  a,z=w['complete_tool_lines'];assert type(a)is int and type(z)is int and 0<=a<=z
  lines=[]
  for n in range(a,z+1):
   prefix=f'L{n}: ';rows=[line[len(prefix):]for line in obs.splitlines()if line.startswith(prefix)];assert len(rows)==1;lines.append(rows[0])
  assert w['complete_unit']=='\n'.join(lines)and w['normalization']=='strip_numbered_link_wrappers_only'
  normalized=re.sub(r'【\d+†([^】]+)】',r'\1',w['complete_unit']);assert sha(normalized.encode())==w['normalized_unit_sha256']
  assert w['citation_layer_kind']in ('ancient_commentary_quotation','received_primary_narrative')and isinstance(w['source_layer'],str)and w['source_layer']
  assert isinstance(w['identity_quote'],str)and w['identity_quote']and w['identity_quote']in normalized and sm['surface']in w['identity_quote']and m['surface']in w['identity_quote']
  assert isinstance(w['context_quote'],str)and w['context_quote']and w['context_quote']in normalized
  i=e['interpretation'];assert set(i)=={'reviewer_kind','automated_historical_identity_proof','human_reviewed','rationale'}and i['reviewer_kind']=='offline_ai_editor'and i['automated_historical_identity_proof']is False and i['human_reviewed']is False and isinstance(i['rationale'],str)and i['rationale']
  marker={'kind':'person','person_id':pid,'status':'contextual_provisional','interpretation_note':i['rationale'],'identity_decision_id':e['id']}
  assert all(same(m.get(k),v)for k,v in marker.items())and'candidate_person_ids'not in m
  rev=dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=ch['id'],paragraph_id=p['id'],mention_id=m['id'],quote=m['surface'])
  assert [(person_id,v)for person_id,person in people.items()for v in person['evidence']if v.get('mention_id')==m['id']]==[(pid,rev)]
  assert [(person_id,a['surface'])for person_id,person in people.items()for a in person['aliases']if m['id']in a['mention_ids']]==[(pid,m['surface'])]
  decision={'id':e['id'],'person_id':pid,'surfaces':[m['surface']],'scope':'cross_chapter','chapter_ids':[ch['id'],source['id']],'status':'contextual_provisional','evidence':[dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=ch['id'],paragraph_id=p['id'],quote=p['text'],mention_ids=[m['id']]),s['reverse']],'rationale':i['rationale'],'primary_reading_ref':ref,'source_reference_binding':{'kind':'offline_ai_editorial_primary_reference','ref':ref,'resolution_id':e['id']},'human_reviewed':False,'model':None}
  assert [v for v in decisions['decisions']if v['id']==e['id']]==[decision]
  assert not any(v.get('id')==e['id']for v in ch['annotation'].get('unresolved_identity_cases',[])+ch['annotation'].get('unresolved_source_reference_readings',[]))
  resolved.append({'entry':e,'pid':pid,'marker':marker,'reverse':rev,'decision':decision})
 assert len({x['pointer']for x in doc['progress_formatters']})==len(doc['progress_formatters'])
 for spec in doc['progress_formatters']:
  assert set(spec)=={'pointer','template'};at,key=_pointer(ch,spec['pointer']);assert at[key]==_format(spec['template'],counts(ch))
 return {'ref':ref,'document':doc,'owner':owner,'resolved':resolved,'current_counts':counts(ch)}

def extend_roles(state,roles):
 if state is None:return
 for r in state['resolved']:
  key='$'+r['entry']['role'];assert key not in roles or roles[key]==r['pid'];roles[key]=r['pid']
def augment_reverse(state,reverse,aliases):
 if state is None:return
 for r in state['resolved']:
  reverse.setdefault(r['pid'],[]).append(copy.deepcopy(r['reverse']));rows=aliases.setdefault(r['pid'],[]);surface=r['entry']['target']['surface'];mid=r['entry']['target']['mention_id'];matches=[a for a in rows if a['surface']==surface]
  assert len(matches)<=1
  if matches:matches[0]['mention_ids'].append(mid)
  else:rows.append({'surface':surface,'mention_ids':[mid]})

def semantic_view(record,state,prior=False):
 """A finite identity view, never a blanket annotation/source-field mask."""
 if state is None or not isinstance(record,dict):return record
 owner=state['owner']
 if not(record.get('record_type')=='identity_decision_set'and record.get('chapter_id')==owner['chapter_id']or record.get('record_type')=='marked_chapter'and record.get('id')==owner['chapter_id']):return record
 out=copy.deepcopy(record)
 if out.get('record_type')=='identity_decision_set'and out.get('chapter_id')==owner['chapter_id']:
  for r in state['resolved']:
   found=[d for d in out['decisions']if d['id']==r['entry']['id']]
   assert len(found)<=1
   if found:assert same(found[0],r['decision']);out['decisions'].remove(found[0])
   elif not prior:raise AssertionError('missing current reference decision')
  return out
 if out.get('record_type')!='marked_chapter'or out.get('id')!=owner['chapter_id']:return out
 assert all(out[k]==owner[k]for k in ('work_id','book_id','source_id'))and isinstance(out.get('annotation'),dict)
 # The owner may already project other validated extensions to an older AI
 # template. Count the true current chapter, then undo only this binding's
 # own target-kind delta for a prior view; never count that artificial phase.
 current_counts=copy.deepcopy(state['current_counts'])
 for r in state['resolved']:
  e=r['entry'];paragraph,m=_target(out,e)
  if prior:
   assert m['kind']in ('person','unresolved')
   if m['kind']=='unresolved':
    assert m.get('person_id')is None and m['status']=='unresolved'
    current_counts['person']-=1;current_counts['unresolved']+=1
  else:assert all(same(m.get(k),v)for k,v in r['marker'].items())and'candidate_person_ids'not in m
  for k in SEMANTIC_KEYS:m.pop(k,None)
  for key in ('unresolved_identity_cases','unresolved_source_reference_readings'):
   values=out['annotation'].get(key,[]);found=[v for v in values if v['id']==e['id']];assert len(found)<=1
   if found:
    v=found[0];assert prior and key=='unresolved_source_reference_readings'and set(v)==UNRESOLVED_KEYS
    assert v['record_type']=='unresolved_source_reference_reading'and v['person_id']is None and v['unresolved_mention_ids']==[e['target']['mention_id']]and v['chapter_ids']==[owner['chapter_id']]and v['paragraph_ids']==[e['target']['paragraph_id']]and v['surfaces']==[e['target']['surface']]
    evidence=dict(work_id=out['work_id'],book_id=out['book_id'],source_id=out['source_id'],chapter_id=out['id'],paragraph_id=paragraph['id'],quote=paragraph['text'],mention_ids=[m['id']])
    assert same(v['evidence'],[evidence])and v['scope']=='chapter'and v['status']=='unresolved'and v['human_reviewed']is False
    values.remove(v)
 ref=out['annotation'].pop(ANNOTATION_REF,None);assert ref==state['ref']or prior and ref is None
 for spec in state['document']['progress_formatters']:
  at,key=_pointer(out,spec['pointer']);assert at[key]==_format(spec['template'],current_counts);at[key]=spec['template']
 return out

def xml_view(text,state,prior=False):
 """Normalize only approved reference elements, preserving every other XML byte."""
 if state is None:return text
 if ET.fromstring(text).attrib.get('chapter-id')!=state['owner']['chapter_id']:return text
 for r in state['resolved']:
  e=r['entry'];mid=e['target']['mention_id'];surface=e['target']['surface'];matches=[]
  for m in re.finditer(r'<(persName|rs)\b[^>]*>[^<]*</\1>',text):
   element=ET.fromstring(m[0])
   if element.attrib.get('id')==mid:matches.append((m,element))
  assert len(matches)==1;m,element=matches[0];assert element.text==surface
  if element.tag=='rs':assert prior and element.attrib=={'id':mid,'type':'unresolved'}
  else:
   assert set(element.attrib)=={'id','ref'}and element.attrib['ref']
   if not prior:assert element.attrib['ref']==r['pid']
  neutral='<sourceReference id="'+escape(mid,quote=True)+'">'+escape(surface)+'</sourceReference>';text=text[:m.start()]+neutral+text[m.end():]
 return text
