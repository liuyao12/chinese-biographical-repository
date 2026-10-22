"""Check recorded quote correspondences, not literary identity through NLU."""
from pathlib import Path
import json,hashlib,re
PREFIX='source-evidence/sanguozhi022-classics-title-identification'
def validate(root):
 r=Path(root);read=lambda p:json.loads((r/p).read_text());digest=lambda p:hashlib.sha256((r/p).read_bytes()).hexdigest();norm=lambda s:re.sub(r'[，。；：！？、\s]','',s)
 ws={w['id']:w for w in read(PREFIX+'/witnesses.json')};cs=read(PREFIX+'/quote-comparisons.json');proposal=read(PREFIX+'/proposal.json');works={w['id']:w for w in read('registry/works.json')['works']};md=read('registry/work-provenance.json');by={c['id']:c for c in cs}
 assert len(by)==len(cs),'duplicate comparison'
 for w in ws.values():
  assert w['capture_type']=='rendered_page_text_extraction' and w['fixed_raw_revision'] is None and w['fixed_revision_raw_downloaded'] is False,'page extraction is not fixed raw'
  assert digest(w['complete_unit_extraction_path'])==w['complete_unit_extraction_sha256'],'witness hash'
 for c in cs:
  a=c['source'];d=read(a['chapter_path']);assert all(d[k]==a[k]for k in ('work_id','book_id','source_id')) and d['id']==a['chapter_id'],'source identity'
  p=next(p for p in d['paragraphs']if p['id']==a['paragraph_id']);m=next(m for m in p['mentions']if m['id']==a['mention_id'])
  assert p['text'][a['start']:a['end']]==a['quote'] and hashlib.sha256(p['text'].encode()).hexdigest()==a['full_paragraph_sha256'],'source quote'
  assert p['text_layer']==a['text_layer'] and p['source_position']==a['source_position'],'source layer/location'
  assert m['kind']=='work' and m['work_id']==a['referenced_work_id'] and m['surface']==a['surface'] and a['start']<=m['start']<m['end']<=a['end'],'source title anchor'
  for t in c['targets']:
   assert t['witness_id']in ws and t['path']==ws[t['witness_id']]['complete_unit_extraction_path'],'target witness'
   assert digest(t['path'])==t['sha256'] and (r/t['path']).read_text()[t['start']:t['end']]==t['quote'],'target quote'
   assert t['textual_layer']=='received_classic_text_not_editorial_note','comparison layer'
  corr=c['correspondences'];assert corr
  for pair in corr:
   left=pair['source_fragment'];assert left in a['quote'];target=c['targets'][pair['target_index']];assert pair['target_fragment']in target['quote']
   for change in pair['character_differences']:left=left.replace(change['source'],change['comparison'])
   assert norm(left)==norm(pair['target_fragment']),'recorded phrase correspondence'
  if c['match_type']=='explicit_title_with_two_discontinuous_received_text_phrases':
   assert len({p['target_index']for p in corr})>1 and len(c['targets'])>1,'discontinuous reference needs separate loci'
  else:
   assert len(corr)==1 and len(c['targets'])==1 and corr[0]['target_fragment']==c['targets'][0]['quote'],'full quoted phrase'
 for change in proposal['changes']:
  wid=change['work_id'];w=works[wid];mw=md['works'][wid]
  assert all(w[k]==change[k]==mw[k]for k in ('citation_title','citation_qualification')),'public/meta title sync'
  assert mw['citation_identification']['quote_comparison_ids']==change['quote_comparison_ids'] and mw['citation_identification']['reference_ids']==change['reference_ids'],'metadata pointers'
  for cid in change['quote_comparison_ids']:assert by[cid]['source']['referenced_work_id']==wid,'book identity endpoint'
  for rid in change['reference_ids']:
   ref=md['references'][rid];assert ref['witness_id']in ws and ref['local_evidence_path']==PREFIX+'/witnesses.json' and ref['capture_type']=='rendered_page_text_extraction','primary reference'
 return {'comparisons':len(cs),'witnesses':len(ws),'identified_titles':len(proposal['changes'])}
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('root',type=Path);print(validate(p.parse_args().root))
