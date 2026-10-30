"""Bounded comparison Jin098 source/layer acceptance; not a person-ID rule."""
from pathlib import Path
import hashlib,json
try:from scripts.witness_projection import repository_positions
except ImportError:from witness_projection import repository_positions
try:from scripts.validation_context import memoized
except ImportError:from validation_context import memoized
CID='c-jinshu-098-wangdun-comparison';SID='s-jinshu098-wangdun-ws2614273-comparison'
EP='source-evidence/jin098-wangdun-comparison/'
RAW='sources/jinshu/wikisource-2614273-raw.wikitext'
RAW_SHA='019eb1b16d5b12d4fac53fe1c94cb23ef4794434faa88ce8222576f948f4ca36'
PINS={'projection.json': 'c132f7f84af2698de8fe0b43c366e843aaee07aadcc06983a253e6e1ef2a33c0', 'extraction-exclusions.json': 'da956cb2540ad0d330f4556f335680a375de25f3b6cd45917f0d09a106bd57e7', 'source-template.json': '0e1c5d158158ce2aed6eff63d4593db8203ec5ee6259bed704dd049b8e999a39', 'ner-quotation-scopes.json': '2fdeda73b155a656c432db061b98eeb4e081a91158ddfae696760bc0fe6d697f', 'ner-identities-template.json': '54549d6c49575a536fdd0ec77eba21d82bd1c71902a28b28ab78e51de1e59ffd', 'ner-stage-review.json': 'bd49b34c930d876572801563794bd40205e239aa01fab9acf291dd50541d5e0d', 'ner-unresolved.json': 'ade93b073ec9aff80cc00c59f851f5950fde2d5f96e9bd798c6aebe08abf226b', 'ner-names-template.json': 'd30b6c20b2ba3629497f1deba99fcdbf9c80fe8234f1881a2244b77c61746eb2', 'ner-facts-template.json': '57997867e3d336cde93d786a912cc57e49c7dcd2c7bec26b0b520fd2e0e25e6c', 'ner-speech-reading.json': '27f75ba1ca58b6543843163dc6f39fbbb22c6cea91ed67c9a1a9b61f9adb55a7', 'ner-legal-precedent.json': '3645b013ffb973ad744d7565203a96f53a3d7c98e25b4c609941b41f1ada43df', 'ner-existing-reading.json': '836fdfd96f94ff060abfdda30d1e931c69a46c698566e339239966707910365f', 'ner-roles.json': 'f8c031e58449591583e6c2bdd6608333c56c65d5e33271874fc14bc0fe667a7c', 'ner-template.json': 'a6d02334f6c2573d4d70bc5ffe24aa983d1af4fc9ac0aca8ada778c2b5f67ade'}
def need(ok,msg):
 if not ok:raise ValueError('晉098比較來源：'+msg)
def path(root,rel):
 root=Path(root).resolve();p=Path(rel);need(not p.is_absolute()and '..'not in p.parts,'不安全路徑');q=root/p;need(q.resolve()==q and q.is_file(),'來源缺檔或越根');return q
def fixed(root,name):
 b=path(root,EP+name).read_bytes();need(hashlib.sha256(b).hexdigest()==PINS[name],'固定projection/模板漂移');return json.loads(b)
def validate(ch,root):
 need(isinstance(ch,dict),'章不是物件');
 if ch.get('annotation',{}).get('ner_stage')=='complete_selected_41_person_roles':return validate_ner(ch,root)
 expected=fixed(root,'source-template.json');need(ch==expected,'完整來源/層/字位/比較資格不符')
 raw=path(root,RAW).read_bytes();need(hashlib.sha256(raw).hexdigest()==RAW_SHA,'原raw漂移');fixed(root,'projection.json');fixed(root,'extraction-exclusions.json');need(len(ch['paragraphs'])==41,'不完整單元')
 for i,p in enumerate(ch['paragraphs'],1):
  need(p['text_layer']==('received_compiler_appraisal'if i==41 else'received_chapter'),'奏疏與史評不得換層');_,sha=repository_positions(root,p,raw.decode().splitlines());need(sha==RAW_SHA,'raw位置不符')
 need(ch['paragraphs'][40]['text'].startswith('史臣曰：'),'缺史評原題');return True
def source_errors(ch,root):
 if not isinstance(ch,dict):return ['晉098比較來源：章不是物件']
 ann=ch.get('annotation',{})
 if ch.get('id')!=CID and ch.get('source_id')!=SID and not(isinstance(ann,dict)and ann.get('fixed_comparison_contract')=='jin098_wangdun_ws2614273'):return []
 try:validate(ch,root);return []
 except(ValueError,KeyError,TypeError,OSError,UnicodeError,IndexError,AttributeError)as e:return[str(e)]

RULE='fixed_comparison_jin098_received_roles'
NAME_KIND='contextual_surname_from_fixed_jin098_received_family'
def same(a,b):return json.dumps(a,ensure_ascii=False,sort_keys=True,separators=(',',':'))==json.dumps(b,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def expand(x,roles):
 if isinstance(x,dict):return{k:expand(v,roles)for k,v in x.items()}
 if isinstance(x,list):return[expand(v,roles)for v in x]
 if isinstance(x,str)and x.startswith('$'):return roles[x[1:]]
 return x
def seed_role(root,s,people):
 c=json.loads(path(root,s['native_path']).read_bytes());need(all(c[k]==s[k]for k in('work_id','book_id','source_id'))and c['id']==s['chapter_id']and same(c['source'].get('revision_id'),s['source_revision']),'外源作品/卷/見證漂移');ps=[p for p in c['paragraphs']if p['id']==s['paragraph_id']];need(len(ps)==1,'外源段不唯一');p=ps[0]
 need(p['text']==s['complete_paragraph']and hashlib.sha256(p['text'].encode()).hexdigest()==s['paragraph_sha256'],'外源完整段漂移');ms=[m for m in p['mentions']if m['id']==s['mention_id']];need(len(ms)==1,'外源MID不唯一');m=ms[0]
 need(m.get('kind')=='person'and same({k:m[k]for k in('start','end','surface')},{k:s[k]for k in('start','end','surface')})and p['text'][m['start']:m['end']]==m['surface'],'外源字位/角色不符');pid=m['person_id'];person=people.get(pid,{})
 need(any(e.get('mention_id')==m['id']and e.get('chapter_id')==c['id']and e.get('paragraph_id')==p['id']for e in person.get('evidence',[]))and any(a.get('surface')==m['surface']and m['id']in a.get('mention_ids',[])for a in person.get('aliases',[])),'外源缺registry反向證據');return pid

@memoized(0)
def resolve(root,ch):
 spec=fixed(root,'ner-roles.json');registry=json.loads(path(root,'registry/persons.json').read_bytes())['persons'];people={p['id']:p for p in registry};need(len(people)==len(registry),'重複登記');roles={r:seed_role(root,s,people)for r,s in spec['existing_seeds'].items()};own={m['id']:(p,m)for p in ch['paragraphs']for m in p['mentions']};need(len(own)==sum(len(p['mentions'])for p in ch['paragraphs']),'本源MID重複')
 for r,mid in spec['new_role_first_mids'].items():
  need(mid in own,'新來源角色缺首MID');p,m=own[mid];need(m.get('kind')=='person'and p['text'][m['start']:m['end']]==m['surface'],'新來源角色錯字位');roles[r]=m['person_id']
 for role,s in spec.get('comparison_seeds',{}).items():roles[role]=seed_role(root,s,people)
 for item in spec.get('negative_identity_seeds',[]):need(seed_role(root,item['seed'],people)!=roles[item['role']],'已核同名反例不得混入本源人物')
 for item in spec.get('support_seeds',[]):need(seed_role(root,item['seed'],people)==roles[item['role']],'跨篇官稱/父系補證不同人')
 rev={}
 for person in registry:
  for a in person.get('aliases',[]):
   for mid in a.get('mention_ids',[]):rev.setdefault((mid,a.get('surface')),set()).add(person['id'])
 for mid,r in spec['role_by_mid'].items():
  need(mid in own,'漏本源MID');p,m=own[mid];need(m.get('kind')=='person'and m.get('person_id')==roles[r],'本源角色/單端改號不符');person=people.get(roles[r],{})
  need(any(e.get('mention_id')==mid and e.get('chapter_id')==CID and e.get('paragraph_id')==p['id']and e.get('source_id')==SID and e.get('quote')==m['surface']for e in person.get('evidence',[])),'本源缺反向evidence');
  if mid in spec.get('source_spelling_not_alias_mids',[]):need(not rev.get((mid,m['surface']),set())and all(a.get('surface')!=m['surface']for a in person.get('aliases',[])),'疑誤字不可變成真正姓名/通用alias')
  else:need(rev.get((mid,m['surface']),set())=={roles[r]},'本源alias反向所有人不唯一')
 return roles

@memoized(1)
def validate_ner(ch,root):
 need(isinstance(ch,dict),'NER章不是物件');roles=resolve(root,ch);expected=expand(fixed(root,'ner-template.json'),roles);need(same(life_aware_chapter(ch,root),expected),'完整NER文字/層/錨/引用範圍不符')
 raw=path(root,RAW).read_bytes();need(hashlib.sha256(raw).hexdigest()==RAW_SHA,'原raw漂移');fixed(root,'projection.json');fixed(root,'extraction-exclusions.json');fixed(root,'source-template.json')
 for p in ch['paragraphs']:
  _,sha=repository_positions(root,p,raw.decode().splitlines());need(sha==RAW_SHA,'本源投影不符')
 for name in('ner-existing-reading.json','ner-unresolved.json','ner-quotation-scopes.json','ner-stage-review.json','ner-speech-reading.json','ner-legal-precedent.json'):fixed(root,name)
 for name,rel in[('ner-facts-template.json','corpus/jinshu/098-wangdun-comparison-assertions.json'),('ner-names-template.json','corpus/jinshu/098-wangdun-comparison-names.json'),('ner-identities-template.json','corpus/jinshu/098-wangdun-comparison-identities.json')]:need(same(json.loads(path(root,rel).read_bytes()),expand(fixed(root,name),roles)),'本源親屬/姓名/身份有限槽漂移')
 legal_binding_valid(root,ch,roles)
 return roles

def family_valid(a,paragraphs=None,root=None):
 try:
  if not isinstance(a,dict)or a.get('qualifiers',{}).get('source_clause_binding',{}).get('rule')!=RULE:return False
  root=Path(root).resolve()if root is not None else Path(__file__).resolve().parents[1];ch=json.loads(path(root,'corpus/jinshu/098-wangdun-comparison.json').read_bytes());roles=validate_ner(ch,root);rows=expand(fixed(root,'ner-facts-template.json'),roles)['assertions'];need(same([x for x in rows if x['id']==a.get('id')],[a]),'親屬非完整受驗槽')
  if paragraphs is not None:
   own={p['id']:p for p in ch['paragraphs']}
   for e in a['evidence']:
    p=paragraphs[e['paragraph_id']];p=p[1]if isinstance(p,tuple)else p;need(same(p,own[e['paragraph_id']]),'傳入段非實際本源完整段')
  return True
 except(ValueError,KeyError,TypeError,OSError,UnicodeError,IndexError,AttributeError):return False

def validate_surname(n,names,chapters,assertions,root=None):
 try:
  root=Path(root).resolve()if root is not None else Path(__file__).resolve().parents[1];ch=json.loads(path(root,'corpus/jinshu/098-wangdun-comparison.json').read_bytes());roles=validate_ner(ch,root);rows=expand(fixed(root,'ner-names-template.json'),roles)['records'];need(isinstance(n,dict)and n.get('surname_basis',{}).get('kind')==NAME_KIND,'復姓kind不符');need(same([x for x in rows if x['id']==n.get('id')],[n]),'復姓有限槽/資格漂移');b=n['surname_basis'];seed,=[x for x in rows if x['id']==b['source_name_record_id']];need(same([x for x in names if isinstance(x,dict)and x.get('id')==seed['id']],[seed]),'父全名proof未帶入');a,=[x for x in expand(fixed(root,'ner-facts-template.json'),roles)['assertions']if x['id']==b['father_assertion_id']];need(any(same(a,x)for x in assertions)and family_valid(a,root=root),'明父proof未帶入')
  need(a['predicate']=='father'and a['subject_person_id']==n['person_id']and a['object_person_id']==seed['person_id']and seed['surname']==n['surname']and seed['ming']and not seed.get('surname_basis'),'復姓父子方向不符');c=chapters[seed['chapter_id']];p=next(p for p in c['paragraphs']if p['id']==seed['paragraph_id']);m,=[m for m in p['mentions']if m['id']==seed['person_mention_id']];need(p['text']==seed['quote']and m['person_id']==seed['person_id']and m['surface']==seed['surname']+seed['ming']and p['text'][m['start']:m['end']]==m['surface'],'父全名非原生來源literal')
 except(ValueError,KeyError,TypeError,OSError,UnicodeError,IndexError,AttributeError,StopIteration):raise ValueError('晉098復姓須076同父全名與098明父子完整proof，不能從ID/label補姓')

def guard_bundle(root,person_id,people,records):
 q=Path(root)/'corpus/jinshu/098-wangdun-comparison.json'
 if not q.exists():return
 ch=json.loads(q.read_bytes())
 referenced=any(e.get('chapter_id')==CID for e in people.get(person_id,{}).get('evidence',[]))or any(m.get('person_id')==person_id for p in ch['paragraphs']for m in p['mentions'])
 if referenced:
  need(ch.get('annotation',{}).get('ner_stage')=='complete_selected_41_person_roles','人物反向源仍在但NER階段被撤');validate_ner(ch,root)

def legal_binding_valid(root,ch,roles):
 b=fixed(root,'ner-legal-precedent.json');local=b['local'];ref=b['parallel'];need(all(ch[k]==local[k]for k in('work_id','book_id','source_id'))and ch['id']==local['chapter_id']and ch['source']['revision_id']==local['revision_id'],'刑例本源維度不符');p,=[p for p in ch['paragraphs']if p['id']==local['paragraph_id']]
 need(p['text']==local['complete_quote']and hashlib.sha256(p['text'].encode()).hexdigest()==local['paragraph_sha256']and p['text_layer']=='received_chapter','刑例完整本源段不符');m,=[m for m in p['mentions']if m['id']==local['received_mention_id']];later,=[m for m in p['mentions']if m['id']==local['later_named_mention_id']];need(m['surface']=='王浚'and later['surface']=='王淩'and m['person_id']==later['person_id']==roles['wangling']and m['end']<later['start'],'刑例前後同指角色/後句淩不得撤')
 c=json.loads(path(root,ref['native_path']).read_bytes());need(all(c[k]==ref[k]for k in('work_id','book_id','source_id'))and c['id']==ref['chapter_id'],'刑例比較作品/卷/篇不符');need(c['source'].get('revision_id')==ref['revision_id']and c['source'].get('source_commit')==ref['source_commit']and c['source'].get('source_blob')==ref['source_blob']and c['source'].get('raw_path')==ref['raw_path']and c['source'].get('raw_file_sha256')==ref['raw_sha256']and c['source'].get('permalink')==ref['url'],'刑例比較原見證/取得維度不符');raw=path(root,ref['raw_path']).read_bytes();need(hashlib.sha256(raw).hexdigest()==ref['raw_sha256'],'刑例比較raw漂移')
 q,=[q for q in c['paragraphs']if q['id']==ref['paragraph_id']];need(q['text']==ref['complete_quote']and hashlib.sha256(q['text'].encode()).hexdigest()==ref['paragraph_sha256']and q.get('text_layer','received_chapter')==ref['source_layer'],'刑例完整比較段/來源層不符');a,=[a for a in q['mentions']if a['id']==ref['person_mention_id']];need(a.get('kind')=='person'and a['surface']=='凌'and a['person_id']==roles['wangling']and q['text'][a['start']:a['end']]=='凌','刑例比較真MID/逆證不符');need('齊崔杼' in q['text']and'剖棺' in q['text']and'親土埋之'in q['text']and'剖棺戮屍'in p['text']and'王淩儭土'in p['text'],'不是同一組刑例線索')
 need(len({roles['wangling'],roles['candidate_youzhou_wangjun'],roles['candidate_conqueror_wangjun']})==3,'不能借兩個真正王浚/濬作首選')

def reading_valid(decision,chapters,people,root):
 try:
  ch=json.loads(path(root,'corpus/jinshu/098-wangdun-comparison.json').read_bytes());roles=validate_ner(ch,root);expected=expand(fixed(root,'ner-identities-template.json'),roles)['decisions'];need(isinstance(decision,dict)and same([x for x in expected if x['id']==decision.get('id')],[decision]),'刑例判讀非完整有限槽');r=decision['parallel_context_reading'];need(r.get('kind')=='fixed_jin098_quoted_legal_precedent'and r.get('source_spelling_is_not_alias')is True and r.get('status')=='editorial_provisional'and decision.get('human_reviewed')is False,'刑例判讀資格不符');need(set(r['candidate_person_ids'])=={roles['wangling'],roles['candidate_youzhou_wangjun'],roles['candidate_conqueror_wangjun']}and len(r['candidate_person_ids'])==3,'刑例候選不能換人');target=people[roles['wangling']];need(all(a['surface']!=r['received_surface']for a in target['aliases'])and any(a['surface']==r['preferred_surface']for a in target['aliases']),'刑例疑誤字不得污染首選姓名/alias');b=fixed(root,'ner-legal-precedent.json')
  for item in[b['local'],b['parallel']]:
   c=chapters[item['chapter_id']];p,=[p for p in c['paragraphs']if p['id']==item['paragraph_id']];actual=json.loads(path(root,'corpus/jinshu/098-wangdun-comparison.json' if item is b['local'] else item['native_path']).read_bytes());actual_p,=[z for z in actual['paragraphs']if z['id']==item['paragraph_id']];need(same(p,actual_p)and p['text']==item['complete_quote'],'傳入刑例完整段含MID/端點須與root相同')
  return True
 except(ValueError,KeyError,TypeError,OSError,UnicodeError,IndexError,AttributeError,StopIteration):return False

def name_record_valid(n,root):
 try:
  need(isinstance(n,dict),'姓名不是物件');ch=json.loads(path(root,'corpus/jinshu/098-wangdun-comparison.json').read_bytes());roles=validate_ner(ch,root);rows=expand(fixed(root,'ner-names-template.json'),roles)['records'];return same([r for r in rows if r['id']==n.get('id')],[n])
 except(ValueError,KeyError,TypeError,OSError,UnicodeError,IndexError,AttributeError):return False

def life_aware_chapter(ch,root):
 ann=ch.get('annotation',{})
 if isinstance(ann,dict)and ('career_stage'in ann or 'title_proposals'in ann):
  try:from scripts.fixed_jin098_wangdun_career import joint_stripped_chapter
  except ImportError:from fixed_jin098_wangdun_career import joint_stripped_chapter
  return joint_stripped_chapter(ch,root)
 if isinstance(ann,dict)and ('life_stage'in ann or 'age_assertions'in ann):
  try:from scripts.fixed_jin098_wangdun_life import stripped_chapter
  except ImportError:from fixed_jin098_wangdun_life import stripped_chapter
  return stripped_chapter(ch,root)
 return ch
