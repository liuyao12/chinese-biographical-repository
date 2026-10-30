"""Exact Jin040 JiaChong AI transcription receipt; does not certify glyph truth or human review."""
import hashlib,json
from pathlib import Path
try:
 from scripts.witness_projection import repository_positions
except ImportError:
 from witness_projection import repository_positions
CID='c-jinshu-040-wyd1739-jiachong'
SID='s-jinshu-040-wyd1739-jiachong'
BASE='source-evidence/jin040-wyd1739-jiachong/'
PINS={'image-column-locations.json': '7e20be06fda6c822340f1da6a3d59a595f6f93519072221a5437eecb4ec2f16c', 'acquisition-provenance.json': '4e2f170f19fd0c9134093b859f7ad8299f288204fa94460cb2420abfebf2b5b5', 'glyph-review-qualification.json': '49593e5e9e88d16ae81555aea4309bf75c20e92309da58e22d4022476ade088c', 'transcription-projection.json': 'dc0810a31b2daaa16b5ee4477770b37b4058db9f21ab272958fc8dba9b2b34f4', 'transcription-witness-contract.json': '7deeb2d4f004a5b6cdbe907fc2ec5d0f3706cd2cc18611a183d9ee12090a94c8', 'transcription-columns.txt': '209d9b8a8a2f183a7ad3ed749da0273d85e177f9ff7feaf3ceea7edc3ffeabd0', 'ai-transcription-correction-pdf92-r3.json': '3c368d3dee16b6764b87234c19879be0c9499697a6c896e9e0d16e641fd86437', 'historical/transcription-columns-before-4b1ca3bc.txt': '4b1ca3bcdb60bc3edf861894d5947902f920ee074a97efe2a24e8fdf2ccb8c40'}
def same(a,b):
 if type(a)is not type(b):return False
 if type(a)is dict:return all(type(k)is str for k in a)and a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
 if type(a)is list:return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 if type(a)in(str,int,bool,type(None)):return a==b
 return False

def need(ok,msg):
 if not ok:raise ValueError('武英殿晉040賈充轉錄：'+msg)
def fixed(root,name):
 root=Path(root).resolve();p=(root/(BASE+name)).resolve()
 need(p.is_relative_to(root/'source-evidence'),'路徑越界')
 b=p.read_bytes();need(hashlib.sha256(b).hexdigest()==PINS[name],name+' SHA不符');return b
def validate_source(chapter,root):
 need(isinstance(chapter,dict),'章須為物件')
 c=json.loads(fixed(root,'transcription-witness-contract.json'))
 need(all(same(chapter.get(k),v) for k,v in c['chapter_dimensions'].items()),'來源維度不符')
 need(same(chapter.get('source'),c['source']),'來源版本/取得/AI資格不符')
 a=chapter.get('annotation');need(isinstance(a,dict)and same(a,c['required_annotation']),'完整待標註AI階段資格不符')
 raw=fixed(root,'transcription-columns.txt');sha=hashlib.sha256(raw).hexdigest();lines=raw.decode().splitlines()
 loc=json.loads(fixed(root,'image-column-locations.json'));proj=json.loads(fixed(root,'transcription-projection.json'))
 fixed(root,'glyph-review-qualification.json');fixed(root,'acquisition-provenance.json')
 fixed(root,'ai-transcription-correction-pdf92-r3.json');fixed(root,'historical/transcription-columns-before-4b1ca3bc.txt')
 need(loc['raw_sha256']==proj['raw_sha256']==sha,'raw版本不符')
 coords=loc['column_coordinates'];need(len(coords)==len(lines)==c['raw_lines'],'原列遺漏')
 need([x['raw_line']for x in coords]==list(range(1,len(lines)+1)),'列序不符')
 ps=chapter.get('paragraphs');need(isinstance(ps,list)and len(ps)==len(c['paragraphs'])==c['native_paragraphs'],'完整段數不符')
 points=[]
 for p,spec in zip(ps,c['paragraphs']):
  need(isinstance(p,dict)and same(p,spec),'原文/層/位置不符')
  need(p.get('annotation_status')=='pending'and p.get('mentions')==[],'source-only段須待標註且無提及')
  pts,digest=repository_positions(root,p,lines);need(digest==sha,'投影SHA不符');points.extend(pts)
  for n,i in pts:
   x=coords[n-1];need(x['side']in('right','left')and 1<=x['physical_column_from_right_1based']<=10 and x['raw_character_offsets_0based']==[0,len(lines[n-1])],'實列位置不符')
 need(points==[(n,i)for n,t in enumerate(lines,1)for i in range(len(t))],'非完整唯一順序投影')
 need(chapter.get('text_sha256')==c['text_sha256']==hashlib.sha256('\n\n'.join(p['text']for p in ps).encode()).hexdigest(),'全文SHA不符')
 return True
def source_errors(chapter,root):
 if not isinstance(chapter,dict):return ['武英殿晉040賈充轉錄：章須為物件']
 a=chapter.get('annotation');binding=a.get('fixed_transcription_contract')if isinstance(a,dict)else None
 if chapter.get('id')!=CID and chapter.get('source_id')!=SID and binding!='wuyingdian_jin040_jiachong_transcription':return []
 try:validate_source(chapter,root);return []
 except (ValueError,TypeError,KeyError,OSError,UnicodeError,StopIteration)as e:return ['武英殿晉040賈充轉錄：'+str(e)]

# Named complete-unit phase; the original pending transcription validator is preserved above.
import copy
C40_PHASE='jin040_jiachong_complete_unit_ner_v1'
C40_CONTRACT='complete-unit-ner-contract.json'
# Replaced with the exact contract digest when the final payload is composed.
C40_CONTRACT_SHA='7d2a3a3c10bc5b30e2a4c9b060c13a9420e8bf866d478b6fb57303ca7ba85e98'

def _c40_read(root,rel):
 root=Path(root).resolve();p=(root/rel).resolve()
 need(p.is_relative_to(root),'formal依賴路徑越界')
 return json.loads(p.read_text())
def _c40_strip_ids(x):
 if type(x)is dict:return{k:_c40_strip_ids(v)for k,v in x.items()if not(k=='person_id'or k.endswith('_person_id')or k=='person_ids'or k.endswith('_person_ids'))}
 if type(x)is list:return[_c40_strip_ids(v)for v in x]
 return x
def _c40_sub(x,roles):
 if type(x)is str and x.startswith('$'):
  need(x[1:]in roles,'未知角色token');return roles[x[1:]]
 if type(x)is dict:return{k:_c40_sub(v,roles)for k,v in x.items()}
 if type(x)is list:return[_c40_sub(v,roles)for v in x]
 return x
def _c40_contract(root):
 p=Path(root)/(BASE+C40_CONTRACT);b=p.read_bytes()
 need(hashlib.sha256(b).hexdigest()==C40_CONTRACT_SHA,'完整NER契約SHA不符')
 c=json.loads(b);need(c.get('phase')==C40_PHASE,'formal階段不符');return c

def _c40_seed_role(root,spec,people):
 values=[]
 for s in spec['seeds']:
  ch=_c40_read(root,s['path'])
  need(all(same(ch.get(k),v)for k,v in s['chapter_dimensions'].items()),'known seed章維度漂移')
  need(same(ch.get('source'),s['source']),'known seed來源metadata漂移')
  p=next(p for p in ch['paragraphs']if p['id']==s['paragraph']['id'])
  need(same(_c40_strip_ids(p),s['paragraph']),'known seed完整段/錨漂移')
  for mid in s['person_mention_ids']:
   m=next(m for m in p['mentions']if m['id']==mid)
   pid=m.get('person_id');need(pid in people,'known seed人物未登記');person=people[pid]
   need(m.get('kind')=='pronoun' or any(a.get('surface')==m['surface']and mid in a.get('mention_ids',[])for a in person.get('aliases',[])if type(a)is dict),'known seed alias逆引缺')
   actual=[e for e in person.get('evidence',[])if e.get('mention_id')==mid]
   expected=[e for e in s['reverse_evidence_shapes']if e.get('mention_id')==mid]
   dims={k:ch[k]for k in('work_id','book_id','source_id')};dims.update(chapter_id=ch['id'],paragraph_id=p['id'],mention_id=mid)
   normalized=[dict(dims,quote=q)for q in(m['surface'],p['text'])]
   need(actual and all(any(same(e,z)for z in expected+normalized)for e in actual),'known seed逆引維度/quote漂移')
   values.append(pid)
 need(values and len(set(values))==1,'known seed多端點不一致');return values[0]

try:from scripts.validation_context import memoized as _c40_memoized
except ImportError:from validation_context import memoized as _c40_memoized
@_c40_memoized(1)
def complete_unit_state(chapter,root,people=None,records=None):
 c=_c40_contract(root);reg=_c40_read(root,'registry/persons.json')['persons'];by={p['id']:p for p in reg}
 need(len(by)==len(reg),'registry人物重複')
 if people is not None:
  supplied=people if type(people)is dict else{p['id']:p for p in people}
  need(same(supplied,by),'傳入registry不是current完整值')
 mids={m['id']:m for p in chapter.get('paragraphs',[])for m in p.get('mentions',[])}
 roles={}
 for role,spec in c['role_specs'].items():
  if spec['kind']=='known_source_roles':roles[role]=_c40_seed_role(root,spec,by)
  else:
   m=mids[spec['first_mention_id']];need(m.get('kind')=='person','新角色firstMID非person');roles[role]=m.get('person_id');need(roles[role]in by,'新角色未登記')
 need(len(set(roles.values()))==len(roles),'本契約不同角色不得無判斷合端')
 for comparison in c.get('identity_comparisons',[]):
  candidate=_c40_seed_role(root,comparison['supporting_seed'],by)
  need(comparison['disposition']=='unresolved_cross_source_identity_no_preferred_merge'and comparison['permanent_not_same_asserted']is False and comparison['human_reviewed']is False,'比較判讀資格漂移')
  need(roles[comparison['role']]!=candidate,'本scope未有來源支持把同名兩事件角色逕接；須另更新有據身份判讀')
 expected=_c40_sub(c['chapter_template'],roles)
 need(same(chapter,expected),'完整formal章不符：未知改動/舊錨/新錨/資格漂移')
 if records is not None:need(sum(same(r,chapter)for r in records if r.get('record_type')=='marked_chapter'and r.get('id')==CID)==1,'current catalog須唯一完整本章')
 # Every actual forward occurrence has a precise registry alias and six-dimensional reverse.
 wanted={pid:[]for pid in roles.values()}
 for p in chapter['paragraphs']:
  for m in p['mentions']:
   if m.get('kind')not in('person','pronoun'):continue
   pid=m['person_id'];person=by[pid]
   need(m.get('kind')=='pronoun' or any(a.get('surface')==m['surface']and m['id']in a.get('mention_ids',[])for a in person.get('aliases',[])if type(a)is dict),'本源alias缺反查')
   e={k:chapter[k]for k in('work_id','book_id','source_id')};e.update(chapter_id=CID,paragraph_id=p['id'],mention_id=m['id'],quote=m['surface']);wanted[pid].append(e)
 for pid,es in wanted.items():
  actual=[e for e in by[pid].get('evidence',[])if e.get('chapter_id')==CID]
  need(same(sorted(actual,key=lambda e:e['mention_id']),sorted(es,key=lambda e:e['mention_id'])),'本源registry逆引非完整精確聯集')
 for key,rel in [('assertions','corpus/jinshu/040-wyd1739-jiachong-assertions.json'),('names','corpus/jinshu/040-wyd1739-jiachong-names.json'),('addresses','corpus/jinshu/040-wyd1739-jiachong-addresses.json')]:
  doc=_c40_read(root,rel);need(same(doc,_c40_sub(c['sidecar_templates'][key],roles)),key+'正式資料漂移')
  if records is not None:need(any(same(doc,r)for r in records),'傳入catalog漏/改正式資料')
 pending=copy.deepcopy(chapter);pc=json.loads(fixed(root,'transcription-witness-contract.json'));pending['annotation']=copy.deepcopy(pc['required_annotation']);pending['paragraphs']=copy.deepcopy(pc['paragraphs']);_pending_validate_source(pending,root)
 return {'contract':c,'roles':roles,'chapter':chapter,'people':by}

_pending_validate_source=validate_source
def validate_source(chapter,root):
 if type(chapter)is dict and isinstance(chapter.get('annotation'),dict) and chapter['annotation'].get('formal_phase')==C40_PHASE:
  st=complete_unit_state(chapter,root);c=json.loads(fixed(root,'transcription-witness-contract.json'));pending=copy.deepcopy(chapter)
  pending['annotation']=copy.deepcopy(c['required_annotation']);pending['paragraphs']=copy.deepcopy(c['paragraphs'])
  return _pending_validate_source(pending,root)
 return _pending_validate_source(chapter,root)

def _c40_chapter(root):return _c40_read(root,'corpus/jinshu/040-wyd1739-jiachong.json')
def _c40_relevant(person,records=None):
 return any(e.get('chapter_id')==CID for e in person.get('evidence',[]))
def guard_bundle(root,person_id,people,records):
 p=people.get(person_id,{})
 if not _c40_relevant(p):return
 chs=[r for r in records if r.get('record_type')=='marked_chapter'and r.get('id')==CID]
 need(len(chs)==1 and isinstance(chs[0].get('annotation'),dict) and chs[0]['annotation'].get('formal_phase')==C40_PHASE,'關聯人物須完整formal來源，不得缺章/退pending')
 return complete_unit_state(chs[0],root,people,records)
def family_applies(a):return isinstance(a,dict)and isinstance(a.get('qualifiers'),dict)and isinstance(a['qualifiers'].get('fixed_source_kinship'),dict)and a['qualifiers']['fixed_source_kinship'].get('kind')=='wyd_jin040_jiachong'
@_c40_memoized(0)
def _c40_local_docs(root):
 ch=_c40_chapter(root);st=complete_unit_state(ch,root);c=st['contract'];roles=st['roles']
 return ch,roles,{k:_c40_sub(v,roles)for k,v in c['sidecar_templates'].items()}
def family_valid(a,paragraphs,chapters,root):
 try:
  ch,roles,docs=_c40_local_docs(root);need(same(chapters.get(CID),ch),'親屬catalog章漂移')
  return family_applies(a)and any(same(a,x)for x in docs['assertions']['assertions'])
 except (ValueError,TypeError,KeyError,OSError,StopIteration):return False
def name_record_valid(name,root):
 try:
  ch,roles,docs=_c40_local_docs(root)
  return any(same(name,x)for x in docs['names']['records'])
 except (ValueError,TypeError,KeyError,OSError,StopIteration):return False
def validate_surname(name,names,chapters,assertions,root):
 need(name_record_valid(name,root),'固定近系補姓row不符')
 ch,roles,docs=_c40_local_docs(root);need(same(chapters.get(CID),ch),'補姓current章缺失/漂移')
 need(all(any(same(a,x)for x in assertions)for a in docs['assertions']['assertions']),'補姓完整親屬來源未入catalog')
 need(all(any(same(n,x)for x in names)for n in docs['names']['records']),'補姓完整姓名資料缺失')
 return True
def address_fragment_valid(address,root):
 try:
  ch,roles,docs=_c40_local_docs(root);row=next(a for a in docs['addresses']['assertions']if a['id']=='pa-jin040-wyd-hanshou')
  need(same(address,row),'跨頁籍貫不是完整固定row')
  b=row['qualifiers']['source_address_fragments'];ps={p['id']:p for p in ch['paragraphs']};fs=b['fragments'];order=[p['id']for p in ch['paragraphs']]
  p,q=[ps[f['paragraph_id']]for f in fs];need(order.index(q['id'])==order.index(p['id'])+1,'跨頁籍貫非真相鄰')
  need(fs[0]['end']==len(p['text'])and fs[1]['start']==0,'跨頁籍貫不是尾首')
  need(''.join(ps[f['paragraph_id']]['text'][f['start']:f['end']]for f in fs)==row['source_term']==row['place']['source_name'],'跨頁籍貫漏字/錯位')
  m=next(m for m in p['mentions']if m['id']==b['person_mention_id']);need(m['person_id']==row['person_id']==roles['hanshou']and m['surface']=='韓壽','跨頁籍貫主體非韓壽')
  return True
 except (ValueError,TypeError,KeyError,OSError,StopIteration):return False

def source_name_fragments(root,person_ids,people,records):
 if not any(_c40_relevant(people.get(pid,{}))for pid in person_ids):return []
 ch=_c40_chapter(root)
 if not isinstance(ch.get('annotation'),dict)or ch['annotation'].get('formal_phase')!=C40_PHASE:return []
 st=complete_unit_state(ch,root,people,records);result=[]
 for group in _c40_sub(st['contract']['name_fragment_groups'],st['roles']):
  if group['person_id']not in person_ids:continue
  group=copy.deepcopy(group);group.pop('role',None);fs=group['fragments'];ps={p['id']:p for p in ch['paragraphs']};order=[p['id']for p in ch['paragraphs']]
  need(len(fs)==2 and order.index(fs[1]['paragraph_id'])==order.index(fs[0]['paragraph_id'])+1,'姓名非相鄰兩片')
  need(fs[0]['end']==len(ps[fs[0]['paragraph_id']]['text'])and fs[1]['start']==0,'姓名片段非真尾首')
  need(''.join(f['surface']for f in fs)==group['complete_component']['value']=='王粹','完整姓名片段不符')
  for f in fs:need(any(same(m,{k:v for k,v in f.items()if k!='paragraph_id'})for m in ps[f['paragraph_id']]['mentions']),'姓名片段非current全錨')
  result.append(group)
 return result

# Named successor of the original full-unit owner: no base contract duplication.
WQ_BOUNDARY_PATH=BASE+'p014-boundary-and-narrative-successor.json'
WQ_BOUNDARY_SHA='8152c701a25dc869c1723b8ab0719183fed916f3ae2f19a945b56a88d0631a25'
WQ_NOTE='斷為建議諡曰武／帝乃從之；武屬賈充諡字，本人物錨僅帝。此已回外層敘事，非前段詔文；本marker不另建諡號事件。'

def _wq_pinned(data,digest,label):
 need(isinstance(data,bytes)and hashlib.sha256(data).hexdigest()==digest,label+' SHA不符')
 obj=json.loads(data);need(type(obj)is dict,label+'須JSON物件');return obj

def apply_wq_boundary_contract(contract,patch):
 need(patch.get('kind')=='jin040_posthumous_name_boundary_patch'and patch.get('base_contract_sha256')==C40_CONTRACT_SHA,'界線繼承親本不符')
 need(patch.get('human_reviewed')is False and patch.get('source_text_changed')is False and patch.get('opaque_MIDs_changed')is False and patch.get('new_posthumous_title_fact_created')is False,'界線資格不可提升')
 need(patch.get('chapter_id')==CID and patch.get('paragraph_id')==CID+':p014','界線篇段不符')
 p=next(p for p in contract['chapter_template']['paragraphs']if p['id']==patch['paragraph_id'])
 need(p['text']==patch['full_text']and same(p['source_position'],patch['source_position']),'界線完整段/原頁位漂移')
 required={CID+':p014:'+x for x in('m0067','m0071','m0077','m0082','m0090')};changes=patch.get('changes');need(type(changes)is list and len(changes)==5 and{v.get('mention_id')for v in changes}==required,'僅准明列五個外敘事錨')
 boundary=p['text'].index('及下禮官議充諡');edict=next(m for m in p['mentions']if m['id']==CID+':p014:m0022');true=next(m for m in p['mentions']if m['id']==CID+':p014:m0193')
 need(edict['end']<=boundary and edict.get('narrative_qualification',{}).get('kind')=='imperial_edict_continues','真詔中錨不得改層')
 need(true['start']==193 and true['end']==195 and true['surface']=='武帝'and p['text'][193:].startswith('武帝踐祚'),'真武帝稱謂不得改')
 for row in changes:
  index=next(i for i,m in enumerate(p['mentions'])if m['id']==row['mention_id']);before=p['mentions'][index];need(same(before,row['before_marker']),'before marker未知差異')
  need(before['start']>=boundary and before.get('narrative_qualification',{}).get('kind')=='imperial_edict_continues','此錨須位於回敘事轉折後')
  after=copy.deepcopy(before);after['narrative_qualification']['kind']='narrator_posthumous_name_deliberation'
  if row['mention_id']==CID+':p014:m0090':
   need(before['start']==90 and before['end']==92 and before['surface']=='武帝'and p['text'][90:95]=='武帝乃從之','諡字與帝的原始字位不符')
   after.update(start=91,surface='帝');after['resolution_note']=WQ_NOTE
  need(same(after,row['after_marker']),'只准換五個敘事層及一個span，不得換PID/MID/其他欄')
  p['mentions'][index]=after
 return contract

_wq_original_c40_contract=_c40_contract
def _c40_contract(root):
 c=_wq_original_c40_contract(root);p=Path(root)/WQ_BOUNDARY_PATH
 if p.exists():c=apply_wq_boundary_contract(c,_wq_pinned(p.read_bytes(),WQ_BOUNDARY_SHA,'界線patch'))
 return c

WQ_CASE_PATH=BASE+'p015-wangqian-maternal-uncle-case.json'
WQ_CASE_SHA='6a054d826f638477d4cdb7a0c7355088d5c0159c360186c38220a3406db88722'
WQ_RECORD_PATH='corpus/jinshu/040-wyd1739-wangqian-maternal-uncle-assertions.json'
WQ_KIND='jin040_named_maternal_uncle_with_intervening_office'

def wangqian_relation_applies(a):
 return(type(a)is dict and type(a.get('qualifiers'))is dict and type(a['qualifiers'].get('source_clause_binding'))is dict and a['qualifiers']['source_clause_binding'].get('kind')==WQ_KIND)

def _wangqian_case_with_state(a,record,paragraphs,state,case):
 need(case.get('kind')==WQ_KIND and case.get('base_complete_contract_sha256')==C40_CONTRACT_SHA,'母舅case親本不符')
 need(case.get('human_reviewed')is False and case.get('image_verified')is False and case.get('model')is None,'母舅資格不可提升')
 ch=state['chapter'];roles=state['roles'];need(all(same(ch.get(k),v)for k,v in case['chapter_dimensions'].items())and same(ch['source'],case['source']),'母舅來源維度/版本不符')
 ps={p['id']:p for p in ch['paragraphs']}
 for cp in case['context_paragraphs']:
  p=ps[cp['id']];need(all(same(p.get(k),v)for k,v in cp.items()),'母舅完整上下文/頁位不符')
 p=ps[CID+':p015'];need(type(paragraphs.get(p['id'])) is tuple and len(paragraphs[p['id']])==2 and paragraphs[p['id']][0]==CID and same(paragraphs[p['id']][1],p),'母舅caller段落不是完整current值')
 anchors=case['anchors'];s=anchors['subject'];o=anchors['object'];marks={m['id']:m for m in p['mentions']};sm=marks[s['id']];om=marks[o['id']]
 for spec,m,role in[(s,sm,'simayan'),(o,om,'wangqian')]:
  need(all(m[k]==spec[k]for k in('id','start','end','surface'))and m['kind']=='person'and m['person_id']==roles[role]and spec['person_role']==role,'母舅雙MID/角色/字位不符')
 need(s['start']==80 and s['end']==81 and s['surface']=='帝'and o['start']==85 and o['end']==87 and o['surface']=='王虔','母舅固定原錨不符')
 need(p['text'][sm['end']:om['start']]=='舅羽林監'and p['text'][om['end']:om['end']+2]=='前妻','舅字/官稱/前妻界線不符')
 need(anchors['kinship']=={'start':81,'end':82,'surface':'舅'}and anchors['office']=={'start':82,'end':85,'surface':'羽林監','lexical_role':'office_title_not_place'},'插入者必為完整官稱，不是假地名或泛空隙')
 bm=anchors['explicit_emperor_context'];bp=ps[bm['paragraph_id']];b=next(m for m in bp['mentions']if m['id']==bm['mention_id'])
 need(bm['mention_id']==CID+':p014:m0193'and b['start']==193 and b['end']==195 and b['surface']=='武帝'and b['person_id']==roles['simayan']and bp['text'][193:].startswith('武帝踐祚'),'不能借錯m0090/最近帝號作時層橋')
 expected=_c40_sub(case['record_template'],roles);need(same(record,expected)and len(record.get('assertions',[]))==1 and same(a,expected['assertions'][0]),'只准受owner驗證的一行母舅sidecar，不能同章泛加')
 need(a['subject_person_id']==roles['simayan']and a['object_person_id']==roles['wangqian']and a['qualifiers']['mother_person_id']is None,'甥→舅方向及本句未名母限制不符')
 return True

def validate_wangqian_candidate_bytes(a,record,paragraphs,root,case_bytes):
 # Private/pre-adoption candidate interface: real unchanged source owner first,
 # then the exact proposed sidecar. This does not claim root file adoption.
 case=_wq_pinned(case_bytes,WQ_CASE_SHA,'母舅case');ch=_c40_chapter(root);state=complete_unit_state(ch,root)
 return _wangqian_case_with_state(a,record,paragraphs,state,case)

def wangqian_maternal_uncle_valid(a,record,paragraphs,root):
 if not wangqian_relation_applies(a):return False
 try:
  need((Path(root)/WQ_BOUNDARY_PATH).is_file(),'母舅後繼要求已採界線phase')
  actual=_c40_read(root,WQ_RECORD_PATH);need(same(record,actual),'sidecar須為受owner驗證的實際current檔')
  return validate_wangqian_candidate_bytes(a,record,paragraphs,root,(Path(root)/WQ_CASE_PATH).read_bytes())
 except (ValueError,KeyError,TypeError,OSError,UnicodeError,StopIteration):return False

# This named optional phase validates the entire source owner before the new row.
_wangqian_parent_complete_unit_state=complete_unit_state
def complete_unit_state(chapter,root,people=None,records=None):
 state=_wangqian_parent_complete_unit_state(chapter,root,people,records)
 path=Path(root)/WQ_RECORD_PATH
 if path.exists():
  need((Path(root)/WQ_BOUNDARY_PATH).is_file(),'母舅階段缺boundary前置')
  case=_wq_pinned((Path(root)/WQ_CASE_PATH).read_bytes(),WQ_CASE_SHA,'母舅case')
  record=_c40_read(root,WQ_RECORD_PATH)
  paragraphs={p['id']:(CID,p)for p in chapter['paragraphs']}
  need(type(record.get('assertions'))is list and len(record['assertions'])==1,'母舅sidecar只准一行')
  _wangqian_case_with_state(record['assertions'][0],record,paragraphs,state,case)
  if records is not None:need(sum(same(record,r)for r in records)==1,'catalog漏/改母舅sidecar')
 return state

# Optional named C40 death/age phase; prior boundary and maternal-uncle owners stay intact.
DEATH_CASE=BASE+'death282-age66-contract.json'
DEATH_SHA='5d91469894c96833e7947663827fdc752e1875f9980f3e1663564a3740188fa7'
DEATH_LIFE='corpus/jinshu/040-wyd1739-jiachong-life-events.json'
DEATH_GROUP='corpus/jinshu/040-wyd1739-jiachong-life-event-groups.json'
DEATH_KIND='fixed_jin039_jin040_jiachong_same_death'
def death_stage_present(root):return(Path(root)/DEATH_CASE).is_file()
def _death_case(root):return _wq_pinned((Path(root)/DEATH_CASE).read_bytes(),DEATH_SHA,'賈充死亡報齡契約')
def _death_pid(root):
 ch=_c40_chapter(root);p=next(p for p in ch['paragraphs']if p['id']==CID+':p001');m=next(m for m in p['mentions']if m['id']==CID+':p001:m0000')
 need(m.get('kind')=='person','賈充death首MID非人物');return m['person_id']
def _death_expanded(root):return _c40_sub(_death_case(root),{'chong':_death_pid(root)})
_death_parent_contract=_c40_contract
def _c40_contract(root):
 contract=_death_parent_contract(root)
 if death_stage_present(root):
  case=_death_case(root);need(case['kind']=='fixed_jin040_death282_age66'and case['prior_complete_contract_sha256']==C40_CONTRACT_SHA,'死亡親本不符')
  a=contract['chapter_template']['annotation'];need(same(a,case['old_annotation']),'死亡phase前annotation不符')
  need(all(k not in a for k in case['annotation_delta']),'不可覆未知生命annotation')
  a.update(copy.deepcopy(case['annotation_delta']))
 return contract
_death_parent_state=complete_unit_state
def complete_unit_state(chapter,root,people=None,records=None):
 st=_death_parent_state(chapter,root,people,records)
 if death_stage_present(root):
  t=_death_expanded(root);need(same(chapter['source'],t['source']),'死亡原始來源變動')
  ps={p['id']:p for p in chapter['paragraphs']}
  for q in t['context_paragraphs']:need(all(same(ps[q['id']].get(k),v)for k,v in q.items()),'死亡連續完整上下文變動')
  for path,key in((DEATH_LIFE,'life_record'),(DEATH_GROUP,'group_record')):
   actual=_c40_read(root,path);need(same(actual,t[key]),'死亡/分組sidecar漂移')
   if records is not None:need(sum(same(actual,r)for r in records)==1,'catalog漏/改死亡sidecar')
  cal=t['calendar_proof'];need(hashlib.sha256((Path(root)/cal['existing_capture_path']).read_bytes()).hexdigest()==cal['existing_capture_sha256'],'太康官方capture改變')
  need(hashlib.sha256(cal['exact_row'].encode()).hexdigest()==cal['row_sha256']and cal['row_id']=='av476'and cal['columns']=={'dynasty':'西晉','era_name':'太康','first_year':280,'last_year':289},'太康官方完整row不符')
 return st
def death_month_valid(event,chapters,root):
 try:
  st=complete_unit_state(_c40_chapter(root),root);t=_death_expanded(root);expected=t['life_record']['events'][0]
  need(same(chapters.get(CID),st['chapter'])and same(event,expected),'明月不是完整current死亡')
  try:from scripts.source_date_parts import explicit_month_parts_valid
  except ImportError:from source_date_parts import explicit_month_parts_valid
  parts=event['source_date_parts'];p=next(p for p in st['chapter']['paragraphs']if p['id']==CID+':p012')
  return explicit_month_parts_valid(parts,p['text'],{'paragraph_id':p['id'],'start':14,'end':20,'surface':'太康三年四月'},lambda n:4 if n=='四'else None)
 except(ValueError,KeyError,TypeError,OSError,StopIteration):return False
def death_group_valid(g,events,chapters,people,root):
 try:
  st=complete_unit_state(_c40_chapter(root),root);t=_death_expanded(root);expected=t['group_record']['groups'][0]
  need(same(g,expected)and same(chapters.get(CID),st['chapter']),'賈充同死亡group/current章不符')
  pid=st['roles']['chong'];need(pid in people and same(people[pid],st['people'][pid]),'賈充current完整metadata不符')
  old=t['prior_039_event'];new=t['life_record']['events'][0]
  need(same(events.get(old['id']),old)and same(events.get(new['id']),new),'原039或040事件漂移')
  actualold=next(e for e in _c40_read(root,'corpus/jinshu/039-life-events.json')['events']if e['id']==old['id']);need(same(actualold,old),'039原event不可改')
  ch39=_c40_read(root,'corpus/jinshu/039.json');need(same(chapters.get(ch39['id']),ch39),'039 caller章非實際current')
  need(all(same(ch39['source'].get(k),v)for k,v in t['prior_039_source'].items()),'039來源版本漂移')
  p=next(p for p in ch39['paragraphs']if p['id']==t['prior_039_paragraph']['id']);need(same({k:v for k,v in p.items()if k!='mentions'},t['prior_039_paragraph']),'039完整段落漂移')
  sm=next(m for m in p['mentions']if m['id']==old['evidence'][0]['person_mention_id']);need(same(sm,t['prior_039_subject_marker'])and sm['person_id']==pid,'039同人MID不符')
  person=st['people'][pid];reverse={k:ch39[k]for k in('work_id','book_id','source_id')};reverse.update(chapter_id=ch39['id'],paragraph_id=p['id'],mention_id=sm['id'],quote=sm['surface']);need(any(same(e,reverse)for e in person['evidence']),'039完整逆引缺失');need(any(a.get('surface')==sm['surface']and sm['id']in a.get('mention_ids',[])for a in person.get('aliases',[])),'039別名逆引缺失')
  return True
 except(ValueError,KeyError,TypeError,OSError,StopIteration):return False
def death_group_required(root,person_ids=None):
 return death_stage_present(root)and(person_ids is None or _death_pid(root)in person_ids)

# Named external-source annotation successor; original C40 contract and 3 case pins stay exact.
EW_SEED_CASE_PATH='source-evidence/eight-wang-contextual-identity/c40-external-seed-shape-successor.json'
EW_SEED_CASE_SHA='11fb8db31d334d92256ac8bc463f067ef6b800dd10540127d949026793c2f346'
_ew_seed_base_c40_contract=_c40_contract
def _c40_contract(root):
 c=_ew_seed_base_c40_contract(root);path=Path(root)/EW_SEED_CASE_PATH
 if not path.exists():return c
 case=_wq_pinned(path.read_bytes(),EW_SEED_CASE_SHA,'外部035八王seed-shape後繼')
 need(case.get('kind')=='jin035_eight_wang_source_seed_shape_successor'and case.get('base_complete_contract_sha256')==C40_CONTRACT_SHA,'外部seed親本/類型漂移')
 need(case.get('human_reviewed')is False and case.get('model')is None,'外部seed資格漂移')
 ch=_c40_read(root,case['source_path']);need(same(ch.get('source'),case['source_metadata'])and all(ch.get(k)==v for k,v in case['source_dimensions'].items()),'外部seed來源/章維度漂移')
 p=next(p for p in ch['paragraphs']if p['id']==case['paragraph_id']);need(p['text']==case['full_quote']and same(_c40_strip_ids(p),case['after_shape']),'外部seed完整原文/after錨形漂移')
 by={p['id']:p for p in _c40_read(root,'registry/persons.json')['persons']};roles={r:_c40_seed_role(root,s,by)for r,s in case['role_seeds'].items()}
 need(set(roles)=={'sui','cheng','xuan'}and len(set(roles.values()))==3,'外部seed角色缺失/誤合')
 decisions=_c40_read(root,case['identity_decisions_path'])['decisions'];mids={m['id']:m for m in p['mentions']}
 for binding in case['target_bindings']:
  r=binding['role'];m=mids[binding['mention_id']];need(m.get('kind')=='person'and m.get('person_id')==roles[r],'外部seed單端/錯角色')
  person=by[roles[r]];need(any(a.get('surface')==m['surface']and m['id']in a.get('mention_ids',[])for a in person.get('aliases',[])),'外部seed alias逆引缺')
  dims={k:ch[k]for k in('work_id','book_id','source_id')};dims.update(chapter_id=ch['id'],paragraph_id=p['id'],mention_id=m['id'],quote=m['surface'])
  need(any(same(e,dims)for e in person.get('evidence',[])),'外部seed精確reverse缺')
  found=[d for d in decisions if d.get('id')==binding['decision_id']];need(len(found)==1,'外部seed身份判讀缺/重')
  decision=found[0];need(decision.get('person_id')==roles[r]and hashlib.sha256(json.dumps(_c40_strip_ids(decision),ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()==binding['decision_shape_sha256'],'外部seed判讀角色/資格/參考漂移')
 for pin in case['reference_payloads']:
  need(hashlib.sha256((Path(root)/pin['path']).read_bytes()).hexdigest()==pin['sha256'],'外部seed平行引用payload漂移')
 c=copy.deepcopy(c)
 for row in case['seed_pointers']:
  current=c
  for part in row['pointer'].split('/')[1:-1]:current=current[int(part)]if isinstance(current,list)else current[part]
  key=row['pointer'].split('/')[-1];need(same(current[key],case['before_shape']),'C40兩seed原shape/位置漂移');current[key]=copy.deepcopy(case['after_shape'])
 return c
