"""Finite typed cited works over the true current 263-anchor SGZ023 caller.
Legacy NER/source views are exact private proof inputs, never caller replacements.
"""
import copy,json,hashlib
from pathlib import Path
REF='source-evidence/sgz023-peiqian-ws2376966/work-author-contract.json'
SHA='e1a86fbca7de0228f5bc46b391e2d13f2c89f53fb85e5d2adde397ceebf31d26'
CID='c-sanguozhi-023-peiqian-ws2376966'
def need(ok,msg):
 if not ok:raise ValueError('裴潛引書作者層：'+msg)
def same(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 return a==b
def read(root,rel):
 root=Path(root).resolve();p=root/rel;need(not Path(rel).is_absolute()and'..'not in Path(rel).parts and p.resolve()==p and p.is_file(),'實檔路徑');return json.loads(p.read_bytes())
def expand(x,r):
 if isinstance(x,str):return r.get(x,x)
 if isinstance(x,list):return[expand(v,r)for v in x]
 if isinstance(x,dict):return{k:expand(v,r)for k,v in x.items()}
 return x
def state(root):
 root=Path(root).resolve();b=(root/REF).read_bytes();need(hashlib.sha256(b).hexdigest()==SHA,'契約SHA');c=json.loads(b);
 for report in c.get('catalogue_identity_reports',[]):
  rawb=(root/report['raw_file']).read_bytes();need(hashlib.sha256(rawb).hexdigest()==report['raw_sha256'],'固定目錄原文SHA');need(rawb.decode('utf8')[report['start']:report['end']]==report['quote'],'目錄原字位/署名層');need(report['layer']=='received_bibliographical_catalogue_report'and report['human_reviewed']is False and report['image_verified']is False,'目錄資格不得冒親見原書')
 need(hashlib.sha256((root/c['parent_contract_path']).read_bytes()).hexdigest()==c['parent_contract_sha256'],'NER父契約SHA');parent=read(root,c['parent_contract_path']);ch=read(root,c['chapter_path']);ms={m['id']:m for p in ch['paragraphs']for m in p['mentions']};r={}
 for key,s in parent['source_seeds'].items():
  if s['kind']=='new_source_local':m=ms[s['first_mid']]
  else:
   source=read(root,s['path']);p=next(p for p in source['paragraphs']if p['id']==s['paragraph_id']);m=next(m for m in p['mentions']if m['id']==s['marker']['id'])
  need(m.get('kind')=='person','來源角色仍為人物');r['$'+key]=m['person_id']
 need(same(ch,expand(c['chapter_template'],r)),'真實caller章的263錨/書名/作者層/章目資格')
 works={w['id']:w for w in read(root,'registry/works.json')['works']};expected=expand(c['expected_affected_works'],r)
 for wid,w in expected.items():need(same(works.get(wid),w),'引書/作者/同書未決登記')
 prov=read(root,'registry/work-provenance.json')
 for wid,p in c['expected_new_provenance'].items():need(same(prov['works'].get(wid),p),'未知作品履歷不得補年/底本')
 directory=read(root,'data/corpus/chapter-directory.json');bookrows={(w['work_id'],b['book_id']):b for w in directory['works']for b in w['books']}
 for ref in ch['cross_chapter_references']:
  t=ref['target'];need((t['work_id'],t['book_id'])in bookrows and t['chapter_id']is None and t['paragraph_id']is None and t['text_status']=='not_imported','已有目錄導航/未虛構原生章')
 # Semantic back-reference excludes a nearest-book fallback and preserves quoted spans.
 p=next(p for p in ch['paragraphs']if p['id'].endswith(':p011'));mm={m['id'].split(':')[-1]:m for m in p['mentions']};need(mm['m0501']['surface']=='《春秋公羊》'and mm['m0514']['surface']=='《公羊》'and mm['m0501']['work_id']==mm['m0514']['work_id'],'有書名號簡稱回指')
 old=expand(c['parent_chapter_template'],r)
 need(ch['source']==old['source']and ch['text_sha256']==old['text_sha256'],'原文來源不變')
 actual={m['id']:m for p in ch['paragraphs']for m in p['mentions']};prior={m['id']:m for p in old['paragraphs']for m in p['mentions']};need(set(actual)==set(prior)and len(actual)==263,'不新增或棄MID')
 for mid,m in prior.items():
  now=actual[mid];need(all(now[k]==m[k]for k in('id','start','end','surface','person_id')),'字位/人物端點不變')
  if mid in c['promoted_original_markers']:need(m['kind']=='unresolved'and now['kind']=='work','僅精確未決書題升解')
  else:need(same(m,now),'非書題原錨全值保存')
 try:from scripts.two_hui_identity import validate as validate_hui
 except ImportError:from two_hui_identity import validate as validate_hui
 validate_hui(root,ch)
 return c,ch,old,r,expected

def proof(root):
 c,ch,old,r,works=state(root)
 try:from scripts.fixed_sgz023_four_biographies import _base_proof
 except ImportError:from fixed_sgz023_four_biographies import _base_proof
 # Exact former NER chapter is validated only after the true current caller/works.
 original=_base_proof(root,chapter_override=old)
 try:from scripts.fixed_sgz023_peiqian import _base_validate
 except ImportError:from fixed_sgz023_peiqian import _base_validate
 _base_validate(original['parent_chapter'],root,original['parent_people'],original['parent_sidecars'])
 original['chapter']=ch;original['typed_work_case']=c
 return original

def author_valid(ev,work,ch,root):
 try:
  c,current,old,r,works=state(root);need(same(ch,current),'作者必真caller，不收父view');wid=ev['referenced_work_id'];need(same(work,works[wid])and any(same(ev,x)for x in works[wid].get('source_author_attributions',[])),'固定原署作者行')
  p=next(p for p in ch['paragraphs']if p['id']==ev['paragraph_id']);mm={m['id']:m for m in p['mentions']};a=mm[ev['author_mention_id']];w=mm[ev['work_mention_id']];need(a['kind']=='person'and a['person_id']==ev['author_person_id']and w['kind']=='work'and w['work_id']==wid,'書/作者雙端')
  if w['surface']in('崇有','貴無'):
   end=p['text'].index('二論',w['end'])+2;need(a['surface']=='頠'and p['text'][a['start']:end]=='頠理具淵博，贍於論難，著崇有、貴無二論','具名著二論，不取最近作者')
  else:need(a['surface']=='謝鯤'and w['surface']=='樂廣傳'and p['text'][a['end']:w['start']]=='爲'and p['text'][w['end']:].startswith('，稱楷'),'原文謝鯤為傳，不冒題前緊接')
  return True
 except (AssertionError,ValueError,KeyError,TypeError,OSError,StopIteration):return False
