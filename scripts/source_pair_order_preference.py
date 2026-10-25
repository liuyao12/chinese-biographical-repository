"""Fixed source-role pair ordering, independent of mutable person IDs.
Original source constraints stay intact; this is neither identity equivalence nor general ranking.
"""
from pathlib import Path
import json,copy,hashlib,re
KIND='fixed_xie_ju_an_commentary_order_preference'
TYPE='person_relative_birth_order_preference_set'
OLD='a-song052-xie-ju-brother-an';NEW='a-shishuo071-ju-an-brother'
CID='c-shishuoxinyu-yanyu-071';SONG='c-songshu-052-xiejingren'
PIN='source-evidence/shishuo-yanyu071/fixed-order-source-pins.json'
PIN_SHA='464d84df86de1dfcda03b0392c0ec02eff19ecab2b882bf0843a0fb7b21d20e1'
H=lambda b:hashlib.sha256(b).hexdigest()
def _end(s,i):
 depth=0;j=i
 while j<len(s)-1:
  if s[j:j+2]=='{{':depth+=1;j+=2
  elif s[j:j+2]=='}}':
   depth-=1;j+=2
   if depth==0:return j
  else:j+=1
 raise ValueError('Unclosed fixed source template')
def _plain(s):
 s=re.sub(r'-\{([^{}]+)\}-',r'\1',s)
 while '{{ProperNoun|' in s:
  i=s.index('{{ProperNoun|');e=_end(s,i);s=s[:i]+s[i+13:e-2]+s[e:]
 if '{{'in s:raise ValueError('Unsupported fixed source template')
 return s.strip()
def projection(raw):
 out=[];pos=0
 while '{{*|'in raw[pos:]:
  i=raw.index('{{*|',pos);e=_end(raw,i)
  if i>pos:out.append(('received_chapter',_plain(raw[pos:i])))
  out.append(('witness_appended_liu_xiaobiao_note','〈'+_plain(raw[i+4:e-2])+'〉'));pos=e
 if raw[pos:].strip():out.append(('received_chapter',_plain(raw[pos:])))
 return out

def _identity_free(v):
 if isinstance(v,dict):return{k:('@person'if k=='person_id'and isinstance(x,str)else _identity_free(x))for k,x in v.items()}
 if isinstance(v,list):return[_identity_free(x)for x in v]
 return v

def _bind(v,roles):
 if isinstance(v,dict):return{k:_bind(x,roles)for k,x in v.items()}
 if isinstance(v,list):return[_bind(x,roles)for x in v]
 return roles.get(v[1:],v)if isinstance(v,str)and v.startswith('@')else v

def _role(chapters,anchor,people):
 ch=chapters[anchor['chapter_id']];p=next(p for p in ch['paragraphs']if p['id']==anchor['paragraph_id']);m,=[m for m in p['mentions']if m['id']==anchor['mention_id']]
 assert m['kind']=='person'and all(m[k]==anchor[k]for k in('start','end','surface'))and p['text'][m['start']:m['end']]==m['surface']
 pid=m['person_id'];assert isinstance(pid,str)and pid in people
 person=people[pid];assert any(a['surface']==m['surface']and m['id']in a['mention_ids']for a in person['aliases'])
 assert any(e.get('mention_id')==m['id']and e.get('chapter_id')==ch['id']and e.get('paragraph_id')==p['id']and e.get('quote')==m['surface']for e in person['evidence'])
 return pid

def validate(record,root,chapters,assertions,people):
 """True or ValueError. Fixed MIDs resolve current IDs; registry reverse links must agree."""
 try:
  assert isinstance(people,dict)
  assert isinstance(record,dict)and set(record)=={'format_version','record_type','chapter_id','decisions'}
  assert record['format_version']=='0.2'and record['record_type']==TYPE and record['chapter_id']==CID
  assert isinstance(record['decisions'],list)and len(record['decisions'])==1
  d=record['decisions'][0];assert isinstance(d,dict)
  assert set(d)=={'id','kind','person_ids','claim_assertion_ids','preferred_assertion_id','alternative_assertion_id','status','human_reviewed','rationale','display_note','study_references'}
  assert d['kind']==KIND and d['id']=='d-shishuo071-xieju-xiean-relative-order'
  pinbytes=(Path(root)/PIN).read_bytes();assert H(pinbytes)==PIN_SHA;pin=json.loads(pinbytes)
  roles={}
  for role,anchors in pin['source_roles'].items():
   assert role in('ju','an')and len(anchors)==2
   vals=[_role(chapters,a,people)for a in anchors];assert vals[0]==vals[1];roles[role]=vals[0]
  assert set(roles)=={'ju','an'}and len(set(roles.values()))==2
  pair=set(roles.values());assert d['person_ids']==[roles['ju'],roles['an']]
  assert d['claim_assertion_ids']==[OLD,NEW]and d['preferred_assertion_id']==NEW and d['alternative_assertion_id']==OLD
  assert d['status']=='editorial_preferred'and d['human_reviewed']is False
  assert all(isinstance(d[k],str)and d[k].strip()for k in('rationale','display_note'))and isinstance(d['study_references'],list)
  ch=chapters[CID];song=chapters[SONG]
  assert {k:ch[k]for k in pin['source_chapter']}==pin['source_chapter']
  assert {k:song[k]for k in pin['song_chapter_dimensions']}==pin['song_chapter_dimensions']and song['source']==pin['song_source']
  assert _identity_free(song['paragraphs'][0])==pin['song_paragraph']
  assert [{k:p[k]for k in('id','text','text_layer')}for p in ch['paragraphs']]==pin['paragraph_text_layers']
  src=ch['source'];assert src['provider']=='Wikisource'and type(src['revision_id'])is int and src['revision_id']==2567463
  assert src['url']==src['permalink']=='https://zh.wikisource.org/w/index.php?oldid=2567463'
  assert src['raw_path']=='source-evidence/shishuo-yanyu071/raw-entry.wiki'
  raw=(Path(root)/src['raw_path']).read_bytes();assert H(raw)==src['raw_file_sha256']
  assert projection(raw.decode())==[(p['text_layer'],p['text'])for p in ch['paragraphs']]
  old,new=assertions[OLD],assertions[NEW]
  assert old==_bind(pin['song_assertion'],roles)and new==_bind(pin['new_assertion'],roles)
  for a,older,younger in[(old,roles['an'],roles['ju']),(new,roles['ju'],roles['an'])]:
   assert a['predicate']=='brother'and a['status']=='source_attested'and{a['subject_person_id'],a['object_person_id']}==pair and a['human_reviewed']is False
   q=a['qualifiers']['relative_birth_order'];assert q=={'older_person_id':older,'younger_person_id':younger,'operator':'lt','scope':'siblings','older_ordinal':None,'younger_ordinal':None}
   assert len(a['evidence'])==1
   e=a['evidence'][0];c=chapters[e['chapter_id']];p=next(p for p in c['paragraphs']if p['id']==e['paragraph_id'])
   assert e['quote']==p['text']and e['source_id']==c['source_id']and e['work_id']==c['work_id']and e['book_id']==c['book_id']
   for endpoint,midkey in [('subject_person_id','subject_person_mention_id'),('object_person_id','object_person_mention_id')]:
    m=next(m for m in p['mentions']if m['id']==e[midkey]);assert m['kind']=='person'and m['person_id']==a[endpoint]and p['text'][m['start']:m['end']]==m['surface']
  note=ch['paragraphs'][1];assert note['text_layer']=='witness_appended_liu_xiaobiao_note'
  attrib=note['layer_attribution'];assert attrib['attributed_author']=='劉孝標'and attrib['human_reviewed']is False and attrib['image_verified']is False
  assert len(attrib['quotation_dependencies'])==1 and attrib['quotation_dependencies'][0]['work_id']=='w-xujinyangqiu-shishuo071-reference'and attrib['quotation_dependencies'][0]['quoted_work_directly_read']is False
  assert '《續晉陽秋》曰：「朗字長度，安次兄據之長子。'in note['text']
  assert any(m['kind']=='work'and m['surface']=='續晉陽秋'and m['work_id']=='w-xujinyangqiu-shishuo071-reference'for m in note['mentions'])
  q=new['qualifiers'];assert q['source_claim_layer']=='liu_xiaobiao_note_quoting_received_work'and q['reported_source_work_id']=='w-xujinyangqiu-shishuo071-reference'and q['quoted_work_directly_read']is False
  assert old['qualifiers']['source_term']=='太傅安第二弟'and new['qualifiers']['source_term']=='安次兄據'
 except (AssertionError,KeyError,TypeError,IndexError,ValueError,OSError,StopIteration,AttributeError)as e:
  raise ValueError('Fixed source-role sibling order requires intact sources, matching current MID roles and registry reverse evidence')from e
 return True

def errors(root,records,people):
 try:
  selected=[r for r in records if isinstance(r,dict)and(r.get('record_type')==TYPE or r.get('chapter_id')==CID and 'decisions'in r)]
  owned=Path(root)/'corpus/shishuoxinyu/yanyu-071-order-decisions.json'
  active=any(isinstance(r,dict)and r.get('record_type')=='person_assertion_set'and any(isinstance(a,dict)and a.get('id')==NEW for a in r.get('assertions',[]))for r in records)
  if not selected and not owned.exists()and not active:return []
  if len(selected)!=1:raise ValueError('Fixed source-pair decision is missing, mistyped or duplicated')
  chapters={r['id']:r for r in records if isinstance(r,dict)and r.get('record_type')=='marked_chapter'}
  assertions={a['id']:a for r in records if isinstance(r,dict)and r.get('record_type')=='person_assertion_set'for a in r['assertions']}
  validate(selected[0],root,chapters,assertions,people);return []
 except (ValueError,TypeError,KeyError,AttributeError)as e:return[str(e)]

def relevant(root,records,people,ids):
 selected=[r for r in records if isinstance(r,dict)and r.get('record_type')==TYPE]
 if selected and all(isinstance(d.get('person_ids'),list)and all(isinstance(p,str)for p in d['person_ids'])for r in selected for d in r.get('decisions',[]))and not any(set(d['person_ids']).intersection(ids)for r in selected for d in r.get('decisions',[])):return []
 issues=errors(root,records,people)
 if issues:raise ValueError('; '.join(issues))
 return[copy.deepcopy(d)for r in selected for d in r['decisions']if set(d['person_ids']).intersection(ids)]

def preferred_relation(assertion,decisions):
 result=copy.deepcopy(assertion)
 for d in decisions:
  if assertion['id']not in d['claim_assertion_ids']:continue
  if(d['kind']!=KIND or d['preferred_assertion_id']!=NEW or d['alternative_assertion_id']!=OLD or {assertion['subject_person_id'],assertion['object_person_id']}!=set(d['person_ids'])):raise ValueError('Invalid source-role pair selection')
  if assertion['id']==OLD:result['qualifiers'].pop('relative_birth_order',None)
  result['relative_birth_order_preference_id']=d['id']
 return result
