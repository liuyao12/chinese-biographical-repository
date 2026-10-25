"""Trusted complete received quotation, never an independently witnessed whole work."""
def validate_container(ch,pin,raw,projected,excluded,root):
 try:
  e=pin['embedded_document'];assert set(e)=={'raw_open_start','raw_close_start','paragraph_ids','author_anchor','work_anchor','intro_paragraph_id','intro_quote','kind','work_id','subject_anchor','subject_resolution_seed'}
  assert e['kind'] in ('complete_received_quotation','complete_received_work_preface')
  opens=[c for c in excluded if c['kind']=='quoted_document_template_open'];closes=[c for c in excluded if c['kind']=='quoted_document_template_close']
  assert len(opens)==len(closes)==1 and opens[0]['start']==e['raw_open_start'] and closes[0]['start']==e['raw_close_start']
  assert raw[e['raw_open_start']:e['raw_open_start']+8]=='{{quote|' and raw[e['raw_close_start']:e['raw_close_start']+2]=='}}'
  assert len(ch['paragraphs'])==len(projected)
  paragraphs={x['id']:x for x in ch['paragraphs']};assert len(paragraphs)==len(ch['paragraphs'])
  quoted=[x['id']for x,w in zip(ch['paragraphs'],projected)if w.get('source_layer')=='received_quoted_document'];assert quoted==e['paragraph_ids']
  documents=ch['annotation']['embedded_documents'];assert documents==[e]
  intro=paragraphs[e['intro_paragraph_id']];assert intro['text']==e['intro_quote'] and intro['id'] not in quoted
  def anchor(a,kind,intro_only=True):
   assert set(a)=={'paragraph_id','mention_id','start','end','surface'}
   q=paragraphs[a['paragraph_id']];assert (not intro_only or q['id']==intro['id']) and q['text'][a['start']:a['end']]==a['surface']
   matches=[m for m in q['mentions']if m['id']==a['mention_id']];assert len(matches)==1
   m=matches[0];assert m['kind']==kind and all(m[k]==a[k]for k in ('start','end','surface'))
   return m
  author=anchor(e['author_anchor'],'person');work=anchor(e['work_anchor'],'work')
  assert author.get('person_id') and work.get('work_id')==e['work_id'] and author['end']<=work['start']
  if e['kind']=='complete_received_quotation':
   assert '乃著' in intro['text'][author['end']:work['start']] and not any(t in intro['text'][author['end']:work['start']]for t in ('不著','未著','非'))
  else:
   assert pin.get('selection_mode')=='main_to_attached_subsection'
   between=intro['text'][author['end']:work['start']]
   assert between.endswith('作《') and not any(t in between for t in ('不作','未作','非'))
   assert intro['text'][work['end']:].startswith('》十八篇，奏之，藏于秘府。其序曰：')
   assert intro['text'][work['end']:]=='》十八篇，奏之，藏于秘府。其序曰：'

  # Resumed biographical subject is anchored in first paragraph, not nearest named philosopher.
  subject=anchor(e['subject_anchor'],'person',False);assert e['subject_anchor']['paragraph_id']==ch['paragraphs'][0]['id'] and subject['person_id']==author['person_id']
  import json
  from pathlib import Path
  seed=e['subject_resolution_seed'];assert set(seed)=={'chapter_id','paragraph_id','mention_id','surface','quote','chapter_path'}
  rel=Path(seed['chapter_path']);assert not rel.is_absolute() and '..'not in rel.parts and rel.parts[0]=='corpus'
  f=Path(root)/rel;assert f.resolve()==f and f.is_file();source=json.loads(f.read_text());assert source['id']==seed['chapter_id']
  p=next(x for x in source['paragraphs']if x['id']==seed['paragraph_id']);assert p['text']==seed['quote']
  matches=[m for m in p['mentions']if m['id']==seed['mention_id']];assert len(matches)==1
  assert matches[0]['kind']=='person' and matches[0]['surface']==seed['surface'] and matches[0]['person_id']==subject['person_id']
  assert all(paragraphs[k]['source_position']['source_layer']=='received_quoted_document'for k in quoted)
  return True
 except (AssertionError,KeyError,TypeError,IndexError,ValueError,OSError,StopIteration):return False
