"""Exact Jin043 Shantao AI transcription receipt; does not certify glyph truth or human review."""
import hashlib,json
from pathlib import Path
try:
 from scripts.witness_projection import repository_positions
except ImportError:
 from witness_projection import repository_positions
CID='c-jinshu-043-wyd1739-shantao'
SID='s-jinshu-043-wyd1739-shantao'
BASE='source-evidence/jin043-wyd1739-shantao/'
PINS={'image-column-locations.json': 'd3115194e09466ac246467f368deac65a96b7a2d7b134cee45f6479abfb48950', 'acquisition-provenance.json': '2110154f0f8f8ff9a6ee2ee943a7cd3a5390710a5574ae280f243e644008c298', 'glyph-review-qualification.json': '8a9d049f632f7d8a574e7b3c2fbeff81886b86323a11d4a507ec15e91edaeb69', 'transcription-projection.json': '9d705661ec0bba6a7292aa03d6eface01bd62e57287f2a957448519cbf65f0d6', 'transcription-witness-contract.json': 'fc73ed0c04a564b577e3152067750b857074abdd12760fde8bb1e8abacd67a45', 'transcription-columns.txt': 'ef5c37602549867433d9829f259bdfa01a66bdd0ab8c1344b6f5c98d5be4c437'}
def need(ok,msg):
 if not ok:raise ValueError('武英殿晉043山濤轉錄：'+msg)
def fixed(root,name):
 root=Path(root).resolve();p=(root/(BASE+name)).resolve()
 need(p.is_relative_to(root/'source-evidence'),'路徑越界')
 b=p.read_bytes();need(hashlib.sha256(b).hexdigest()==PINS[name],name+' SHA不符');return b
def validate_source(chapter,root):
 if isinstance(chapter,dict)and isinstance(chapter.get('annotation'),dict)and chapter['annotation'].get('phase')=='jin043_shantao_complete_unit_ner_v1':
  formal_state(chapter,root);return True
 need(isinstance(chapter,dict),'章須為物件')
 c=json.loads(fixed(root,'transcription-witness-contract.json'))
 need(all(chapter.get(k)==v for k,v in c['chapter_dimensions'].items()),'來源維度不符')
 need(chapter.get('source')==c['source'],'來源版本/取得/AI資格不符')
 a=chapter.get('annotation');need(isinstance(a,dict)and a==c['required_annotation'],'完整待標註AI階段資格不符')
 raw=fixed(root,'transcription-columns.txt');sha=hashlib.sha256(raw).hexdigest();lines=raw.decode().splitlines()
 loc=json.loads(fixed(root,'image-column-locations.json'));proj=json.loads(fixed(root,'transcription-projection.json'))
 fixed(root,'glyph-review-qualification.json');fixed(root,'acquisition-provenance.json')
 need(loc['raw_sha256']==proj['raw_sha256']==sha,'raw版本不符')
 coords=loc['column_coordinates'];need(len(coords)==len(lines)==c['raw_lines'],'原列遺漏')
 need([x['raw_line']for x in coords]==list(range(1,len(lines)+1)),'列序不符')
 ps=chapter.get('paragraphs');need(isinstance(ps,list)and len(ps)==len(c['paragraphs'])==c['native_paragraphs'],'完整段數不符')
 points=[]
 for p,spec in zip(ps,c['paragraphs']):
  need(isinstance(p,dict)and all(p.get(k)==v for k,v in spec.items()),'原文/層/位置不符')
  need(p.get('annotation_status')=='pending'and p.get('mentions')==[],'source-only段須待標註且無提及')
  pts,digest=repository_positions(root,p,lines);need(digest==sha,'投影SHA不符');points.extend(pts)
  for n,i in pts:
   x=coords[n-1];need(x['side']in('right','left')and 1<=x['physical_column_from_right_1based']<=10 and x['raw_character_offsets_0based']==[0,len(lines[n-1])],'實列位置不符')
 need(points==[(n,i)for n,t in enumerate(lines,1)for i in range(len(t))],'非完整唯一順序投影')
 need(chapter.get('text_sha256')==c['text_sha256']==hashlib.sha256('\n\n'.join(p['text']for p in ps).encode()).hexdigest(),'全文SHA不符')
 return True
def source_errors(chapter,root):
 if not isinstance(chapter,dict):return ['武英殿晉043山濤轉錄：章須為物件']
 a=chapter.get('annotation');binding=a.get('fixed_transcription_contract')if isinstance(a,dict)else None
 if chapter.get('id')!=CID and chapter.get('source_id')!=SID and binding!='wuyingdian_jin043_shantao_transcription':return []
 try:validate_source(chapter,root);return []
 except (ValueError,TypeError,KeyError,OSError,UnicodeError,StopIteration)as e:return ['武英殿晉043山濤轉錄：'+str(e)]

# Named complete-unit NER successor; the source-only branch above remains intact.
FORMAL_KIND='jin043_shantao_complete_unit_ner_v1'
FORMAL_CONTRACT_SHA='1e14f8e28e3d9f80f2a435339c901d017e4e45ee307dd8056ab5053b4c878429'
FORMAL_PATH=BASE+'ner-family-contract.json'
def same(a,b):
 import math
 if type(a)is not type(b):return False
 if a is None or type(a)in(str,bool,int):return a==b
 if type(a)is float:return math.isfinite(a)and math.isfinite(b)and a==b
 if type(a)is list:return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 if type(a)is dict:return all(type(k)is str for k in a)and all(type(k)is str for k in b)and a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
 return False
def substitute(value,roles):
 if isinstance(value,str)and value.startswith('$'):
  need(value[1:]in roles,'未知來源角色');return roles[value[1:]]
 if isinstance(value,list):return [substitute(v,roles)for v in value]
 if isinstance(value,dict):return {k:substitute(v,roles)for k,v in value.items()}
 return value
def formal_contract(root):
 b=(Path(root)/FORMAL_PATH).read_bytes();need(hashlib.sha256(b).hexdigest()==FORMAL_CONTRACT_SHA,'NER完整契約SHA不符');return json.loads(b)
def reverse_valid(pid,mid,surface,people,c,p,legacy_expected=None):
 need(pid in people,'人物未登記')
 person=people[pid]
 need(any(a.get('surface')==surface and mid in a.get('mention_ids',[])for a in person.get('aliases',[])),'alias反查不符')
 observed=[e for e in person.get('evidence',[])if e.get('mention_id')==mid]
 if legacy_expected is not None:
  need(same(observed,legacy_expected)and all(e.get('paragraph_id')==p['id']and e.get('chapter_id')==c['id']and e.get('quote')==surface for e in observed),'精確既存seed反查不符')
 else:
  need(any(e.get('mention_id')==mid and e.get('paragraph_id')==p['id'] and e.get('chapter_id')==c['id'] and e.get('work_id')==c['work_id'] and e.get('book_id')==c['book_id'] and e.get('source_id')==c['source_id'] and e.get('quote')==surface for e in observed),'evidence反查不符')
def _formal_state_before_department(chapter,root,people=None,records=None,check_sidecars=True):
 import copy
 need(isinstance(chapter,dict),'正式章須物件');contract=formal_contract(root);root=Path(root)
 if people is None:people={p['id']:p for p in json.loads((root/'registry/persons.json').read_text())['persons']}
 def read(rel):return json.loads((root/rel).read_text())
 def mark(c,mid):
  return next((p,m)for p in c['paragraphs']for m in p.get('mentions',[])if m.get('id')==mid)
 if records is not None:
  need(same(read('corpus/jinshu/043-wyd1739-shantao.json'),chapter),'catalog與現役完整章不一致')
 roles={};cache={}
 for role,spec in contract['known_seeds'].items():
  c=cache.setdefault(spec['path'],None)
  if c is None:c=read(spec['path']);cache[spec['path']]=c
  dimensions=all(c.get(k)==v for k,v in spec['dimensions'].items())
  proposed=spec.get('corrected_source_id_candidate')
  corrected=(isinstance(proposed,str)and c.get('source_id')==proposed and all(c.get(k)==v for k,v in spec['dimensions'].items()if k!='source_id'))
  need((dimensions or corrected)and same(c.get('source'),spec['source']),'跨篇來源版本／限定不符')
  if records is not None:
   supplied=next((r for r in records if r.get('record_type')=='marked_chapter'and r.get('id')==c['id']),None)
   need(same(supplied,c),'catalog跨篇證據與現役檔不一致')
  p,m=mark(c,spec['seed_mention_id']);projected=copy.deepcopy(p)
  for n in projected['mentions']:n.pop('person_id',None)
  need(same(projected,spec['paragraph']),'完整跨篇證據段／MID／位置不符')
  need(m.get('kind')=='person'and isinstance(m.get('person_id'),str),'seed不是人物')
  roles[role]=m['person_id'];observed=[e for e in people[m['person_id']].get('evidence',[])if e.get('mention_id')==m['id']]
  normalized=copy.deepcopy(spec['reverse_evidence'])
  for e in normalized:
   for k in ('work_id','book_id','source_id'):e[k]=c[k]
  legacy=spec.get('legacy_reverse_exception')is True and same(observed,spec['reverse_evidence'])
  need(same(observed,spec['reverse_evidence'])or(spec.get('legacy_reverse_exception')is True and same(observed,normalized)),'既存seed反查整值漂移')
  reverse_valid(m['person_id'],m['id'],m['surface'],people,c,p,spec['reverse_evidence']if legacy else None)
 for role,mid in contract['new_role_first_mentions'].items():
  p,m=mark(chapter,mid);need(m.get('kind')=='person'and isinstance(m.get('person_id'),str),'新角色無人物端點');roles[role]=m['person_id']
 need(len(set(roles.values()))==len(roles),'獨立來源角色被無據同指')
 expected=substitute(contract['chapter_template'],roles);need(same(chapter,expected),'正式章全值／角色／資格不符')
 for p in chapter['paragraphs']:
  for m in p['mentions']:
   if m['kind']=='person':reverse_valid(m['person_id'],m['id'],m['surface'],people,chapter,p)
 if check_sidecars:
  for path,t in contract['sidecars'].items():
   expected_record=substitute(t,roles);need(same(read(path),expected_record),'正式姓名／近系／身份側檔不符：'+path)
   if records is not None:need(any(same(expected_record,r)for r in records),'catalog正式側檔不一致：'+path)
 # Projection is permitted only after full current equality; never accept a stale 251-anchor chapter.
 pending=copy.deepcopy(chapter);base=json.loads(fixed(root,'transcription-witness-contract.json'))
 pending['annotation']=base['required_annotation']
 for p in pending['paragraphs']:p['annotation_status']='pending';p['mentions']=[]
 validate_source(pending,root)
 return roles,contract

def guard_bundle(root,person_id,people,records):
 # No work for unrelated persons; no permanent ID whitelist.
 c=next((r for r in records if r.get('record_type')=='marked_chapter'and r.get('id')==CID),None)
 registry_relevant=any(e.get('chapter_id')==CID for e in people.get(person_id,{}).get('evidence',[]))
 if c is None:
  need(not registry_relevant,'來源人物catalog缺現役完整章');return
 ids={m.get('person_id')for p in c.get('paragraphs',[])for m in p.get('mentions',[])if m.get('kind')=='person'}
 if person_id not in ids and not registry_relevant:return
 need(c.get('annotation',{}).get('phase')==FORMAL_KIND,'來源人物不得使用未完整正式階段')
 formal_state(c,root,people,records)

def family_applies(a):return isinstance(a,dict)and isinstance(a.get('qualifiers'),dict)and isinstance(a['qualifiers'].get('fixed_source_kinship'),dict)and a['qualifiers']['fixed_source_kinship'].get('kind')=='wyd_jin043_shantao'
def family_valid(a,paragraphs,chapters,root):
 if not family_applies(a):return False
 try:
  ch=chapters[CID];roles,ct=formal_state(ch,root)
  rows=substitute(ct['sidecars']['corpus/jinshu/043-wyd1739-shantao-assertions.json']['assertions'],roles)
  need(any(same(a,r)for r in rows),'近系整值非明列來源陳述');return True
 except (ValueError,KeyError,TypeError,OSError,StopIteration):return False

def validate_surname(name,names,chapters,assertions,root):
 roles,ct=formal_state(chapters[CID],root)
 expected=substitute(ct['sidecars']['corpus/jinshu/043-wyd1739-shantao-names.json']['records'],roles)
 need(any(same(name,r)for r in expected) and name.get('surname_basis',{}).get('kind')=='contextual_surname_from_wyd_jin043_shantao','本源山姓復原行不符')
 need(all(any(same(n,x)for x in names)for n in expected),'完整字／單名／復原姓名行缺失')
 required=substitute(ct['sidecars']['corpus/jinshu/043-wyd1739-shantao-assertions.json']['assertions'],roles)
 need(all(any(same(a,x)for x in assertions)for a in required),'明父來源鏈不符')
 return True
# Named source-title interpretation correction, never a person-retirement rule.
try:from scripts.validation_context import memoized
except ImportError:from validation_context import memoized

def _department_correction_receipt(root,contract):
 spec=contract.get('source_record_correction_ref');need(isinstance(spec,dict)and set(spec)=={'path','sha256'},'職掌修正收據缺失')
 need(spec['path']==BASE+'concurrent-department-correction.json','職掌修正收據路徑不符')
 root=Path(root).resolve();path=(root/spec['path']).resolve();need(path.is_relative_to(root/'source-evidence'),'職掌收據越界');raw=path.read_bytes();need(hashlib.sha256(raw).hexdigest()==spec['sha256'],'職掌收據SHA不符');r=json.loads(raw)
 need(r.get('record_type')=='source_title_interpretation_correction'and r.get('source_id')==SID and r.get('chapter_id')==CID and r.get('reuse_policy')=='not_reusable_as_current_source_record_ids'and r.get('human_reviewed')is False and r.get('model')is None,'非人物職掌修正資格不符')
 ids=r.get('retired_source_record_ids');need(isinstance(ids,list)and len(ids)==len(set(ids))and all(isinstance(x,str)and x for x in ids),'舊source record ID清單不符');return r

def _no_retired_source_values(value,retired):
 if isinstance(value,str):return value not in retired
 if isinstance(value,list):return all(_no_retired_source_values(x,retired)for x in value)
 if isinstance(value,dict):return all(_no_retired_source_values(x,retired)for x in value.values())
 return True

@memoized(0)
def _source_record_reservations_valid(root,retired):
 # Same native corpus scope as the loader; no historical evidence directory exemption.
 root=Path(root).resolve()
 for file in (root/'corpus').glob('*/*.json'):
  doc=json.loads(file.read_bytes())
  if isinstance(doc,dict)and(doc.get('chapter_id')==CID or doc.get('id')==CID):need(_no_retired_source_values(doc,set(retired)),'已修正舊holding ID不得在本源current records/refs重用')
 return True

def formal_state(chapter,root,people=None,records=None,check_sidecars=True):
 roles,contract=_formal_state_before_department(chapter,root,people,records,check_sidecars)
 receipt=_department_correction_receipt(root,contract);retired=receipt['retired_source_record_ids'];_source_record_reservations_valid(str(Path(root).resolve()),retired)
 if records is not None:
  for record in records:
   if isinstance(record,dict)and(record.get('chapter_id')==CID or record.get('id')==CID):need(_no_retired_source_values(record,set(retired)),'catalog本源不得復活舊holding ID/refs')
 return roles,contract

def concurrent_department_function_valid(d,ch,holdings,root):
 if not isinstance(d,dict)or not isinstance(ch,dict)or not isinstance(holdings,dict)or root is None:return False
 try:
  need(set(d)=={'id','person_id','kind','status','source_term','source_anchor','source_revision','paragraph_sha256','values','date_expression','evidence','source_detail_pattern','interpretation_note','reviewer','human_reviewed','model'}and d.get('kind')=='official_duty','兼領職掌不得夾帶獨立官秩/任期欄位');roles,ct=formal_state(ch,root);slot,=[s for s in ct['concurrent_department_functions']if s['detail_id']==d.get('id')];expected=substitute(ct['sidecars']['corpus/jinshu/043-wyd1739-shantao-source-details.json'],roles);row,=[x for x in expected['records']if x['id']==d['id']];need(same(d,row),'兼領職掌非受信本源明列資料')
  b=d['source_detail_pattern'];need(set(b)==({'kind','rule','subject_role','subject_mention_id','scope_anchor','fields','later_service_context'}if b.get('rule')=='main_additional_department'else{'kind','rule','subject_role','subject_mention_id','scope_anchor','fields'}),'兼領frame字段不符');need(b['kind']=='concurrent_department_function'and b['rule']==slot['rule']and b['subject_role']==slot['subject_role'],'兼領職掌rule/主體不符');pid=roles[slot['subject_role']];need(d['person_id']==pid and d['status']=='source_attested'and d['human_reviewed']is False and d['model']is None and d['date_expression']is None,'兼領職掌主體/日期/AI資格不符')
  e=d['evidence'][0];p,=[p for p in ch['paragraphs']if p['id']==e['paragraph_id']];t=p['text'];m,=[m for m in p['mentions']if m['id']==b['subject_mention_id']];need(m.get('kind')=='person'and m['person_id']==pid and e['person_mention_id']==m['id'],'兼領職掌非同人MID')
  def exact(a,paragraph=p):
   need(isinstance(a,dict)and set(a)=={'paragraph_id','start','end','surface'}and a['paragraph_id']==paragraph['id']and type(a['start'])is int and type(a['end'])is int and 0<=a['start']<a['end']<=len(paragraph['text'])and paragraph['text'][a['start']:a['end']]==a['surface'],'兼領原位不符');return a
  scope=exact(b['scope_anchor']);f={k:exact(v)for k,v in b['fields'].items()};a=exact(d['source_anchor']);need(d['source_revision']==ch['source']['revision_id']and d['paragraph_sha256']==hashlib.sha256(t.encode()).hexdigest(),'兼領全段/見證不符')
  need(all(e[k]==ch[k]for k in ('work_id','book_id','source_id'))and e['chapter_id']==CID and e['quote']==t,'兼領完整原句範圍不符')
  v=d['values'];need(v=={'duty_code':'personnel_selection','appointment_role':'concurrent','organ_source_name':f['department']['surface'],'office_title':None,'linked_holding_id':slot['linked_holding_id']},'領部不是另造完整官名/品秩')
  need(f['verb']['surface']=='領'and f['department']['surface']=='吏部'and f['verb']['end']==f['department']['start']and a['start']==f['verb']['start']and a['end']==f['department']['end']and a['surface']==d['source_term']=='領吏部','領動作與部門字位不符')
  h=holdings[v['linked_holding_id']];need(h['person_id']==pid and h['title']==f['main_office']['surface']and h['kind']=='office'and h['mode']=='grant'and h['status']=='source_attested','兼領須連同人已驗主職，不借別人/前職')
  need(any(x['paragraph_id']==p['id']and x['start']==f['main_office']['start']and x['end']==f['main_office']['end']and x['surface']==f['main_office']['surface']and x['person_mention_id']==m['id']for x in h['attestations']),'主職原位/持有人與兼領不同')
  need(any(x['paragraph_id']==p['id']and x['person_mention_id']==m['id']and x['quote']==t for x in h['evidence']),'主職不是同一完整段證據')
  if b['rule']=='main_additional_department':tokens=[('L','除'),('F','main_office'),('L','加'),('F','additional_office'),('F','verb'),('F','department')];need(set(f)=={'main_office','additional_office','verb','department'}and t.startswith('固辭',scope['end']),'兼領前後授任/固辭scope不符')
  elif b['rule']=='main_department':tokens=[('L','徵為'),('F','main_office'),('F','verb'),('F','department')];need(set(f)=={'main_office','verb','department'}and m['start']==scope['end']and t.startswith(m['surface']+'欲令朝臣',scope['end']),'兼領後續主語/職掌scope不符')
  else:raise ValueError('未知兼領形狀')
  cursor=scope['start']
  for typ,key in tokens:
   if typ=='L':need(t.startswith(key,cursor),'兼領局部句法不符');cursor+=len(key)
   else:need(f[key]['start']==cursor,'兼領字段不連續');cursor=f[key]['end']
  need(cursor==scope['end'],'兼領scope不完整')
  if b['rule']=='main_additional_department':
   late=b['later_service_context'];q,=[p for p in ch['paragraphs']if p['id']==late['paragraph_id']];qm,=[m for m in q['mentions']if m['id']==late['subject_mention_id']];la=exact(late['source_anchor'],q);order=[p['id']for p in ch['paragraphs']]
   need(order.index(q['id'])==order.index(p['id'])+1 and qm['person_id']==pid and qm['start']==la['start']and la['surface']==qm['surface']+'辭不獲已乃起視事'and late['paragraph_sha256']==hashlib.sha256(q['text'].encode()).hexdigest()and late['interpretation_scope']=='later_return_to_service_not_date_or_individual_duration','後起視事不可借前次自力就職/累計任年')
   need(len(d['evidence'])==2,'後起視事完整證據缺失');le=d['evidence'][1];need(all(le[k]==ch[k]for k in ('work_id','book_id','source_id'))and le['chapter_id']==CID and le['paragraph_id']==q['id']and le['quote']==q['text']and le['person_mention_id']==qm['id'],'後起視事證據不符')
  else:need(len(d['evidence'])==1 and'later_service_context'not in b,'不得借另人後起視事')
  return True
 except(ValueError,KeyError,TypeError,OSError,StopIteration,AssertionError,IndexError):return False
