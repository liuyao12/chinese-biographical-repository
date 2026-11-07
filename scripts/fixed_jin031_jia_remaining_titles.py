"""Named bounded continuation of the original 031 NER/typed proof, not a source layer."""
from pathlib import Path
import json,copy
try:from scripts import fixed_jin031_jia_comparison as core
except ImportError:import fixed_jin031_jia_comparison as core
EP='source-evidence/jin031-jia-comparison/remaining-titles-phase-proof.json'
PROOF_SHA='ff46261d73b03ca266778c124af67ff247390e5135afa1621d9f6beb33cc74d2'

def proof(root):
 data=core.path(root,EP).read_bytes();core.need(core.H(data)==PROOF_SHA,'remaining-title證照漂移');b=json.loads(data)
 for key in ['parent_typed','parent_ner','comparison','group']:
  core.need(core.H(core.path(root,b[key+'_path']).read_bytes())==b[key+'_sha256'],'remaining-title依據漂移 '+key)
 return b

def effective(parent,root):
 if not(Path(root)/EP).is_file():return parent
 b=proof(root);out=copy.deepcopy(parent);path='corpus/jinshu/031-jia-comparison-titles.json';old=out['expected_documents'][path]['holdings'];new=b['holdings']
 core.need(len(old)==11 and len(new)==19 and len({h['id']for h in old+new})==30,'remaining-title槽位不得蓋舊或重複')
 out['expected_documents'][path]['holdings']=old+copy.deepcopy(new)
 out['annotation_additions']['fixed_jin031_remaining_titles_ref']=EP
 out['annotation_additions']['remaining_titles_scope']='新增19個人持號/稱職及楚王漏錨；三兄亭侯群體待source_group介面，不宣稱全篇事實完成。'
 out['additional_mentions']=[copy.deepcopy(b['new_mention'])]
 return out

def additional_mentions(parent,context):
 out=copy.deepcopy(parent)
 for item in context.get('additional_mentions',[]):
  p,=[p for p in out['chapter_template']['paragraphs']if p['id']==item['paragraph_id']];m=item['mention'];core.need(m['surface']=='楚王'and(m['start'],m['end'])==(92,94)and p['text'][92:94]=='楚王'and not any(x['id']==m['id']or x['start']<m['end']and m['start']<x['end']for x in p['mentions']),'楚王補錨位置/舊MID不得覆蓋')
  p['mentions'].append(copy.deepcopy(m));p['mentions'].sort(key=lambda x:(x['start'],x['end']))
 return out

def fixture_paths(root):
 b=proof(root);return{EP,b['comparison_path'],b['group_path']}

def transfer_valid(holding,holdings,paragraphs,mentions,chapters,root):
 try:
  core.need(root is not None and isinstance(chapters,dict)and core.CID in chapters,'031改封須完整root/章')
  try:from scripts.fixed_jin031_jia_typed import state
  except ImportError:from fixed_jin031_jia_typed import state
  b,r=state(chapters[core.CID],root);expected=core.expand(b['expected_documents']['corpus/jinshu/031-jia-comparison-titles.json'],r)['holdings'];by={h['id']:h for h in expected};basis=holding['transfer_basis']
  core.need(holding in expected and basis['kind']=='fixed_jin031_title_change'and holding['source_career_role']['slot']in ('remaining:guo-yicheng','remaining:linhai-renamed'),'031僅兩同人改封槽')
  previous=holdings.get(basis['previous_holding_id']);core.need(previous==by.get(basis['previous_holding_id'])and previous['person_id']==holding['person_id']and previous['mode']=='attestation'if holding['source_career_role']['slot']=='remaining:guo-yicheng'else previous==by.get(basis['previous_holding_id'])and previous['person_id']==holding['person_id']and previous['mode']=='grant','031前爵須本源實際同人資料')
  start=holding['effective_period']['start'];end=previous['effective_period']['end'];core.need(end['status']=='source_event'and end['event_type']=='explicit_end'and end['evidence']==start['evidence']==basis['evidence']and end['date_expression']==start['date_expression']and end.get('normalized_date')==start.get('normalized_date'),'031同次改封終始須同證，不借死亡')
  for e in basis['evidence']:
   pid=e['paragraph_id'];p=next(p for p in chapters[core.CID]['paragraphs']if p['id']==pid);core.need(paragraphs[pid]==(core.CID,p)and e['quote']==p['text']and basis['source_term']in p['text'],'031改封caller整段')
  anchor=mentions[basis['actor_mention_id']];expected=next(m for m in p['mentions']if m['id']==basis['actor_mention_id']);core.need(anchor==(core.CID,p['id'],expected)and expected['kind']=='person'and expected['person_id']==holding['person_id'],'031改封caller完整本人MID/字位/body')
  return True
 except(ValueError,KeyError,TypeError,OSError,IndexError,StopIteration,AttributeError):return False
