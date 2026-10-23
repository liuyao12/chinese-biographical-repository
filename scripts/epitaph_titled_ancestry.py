"""Editorial parent between a complete epitaph's titled father and grandfather."""
import json,hashlib
from pathlib import Path
BASIS='epitaph_bound_titled_ancestor_sequence'
def valid(member,rows,assertions,chapters,root):
 try:
  assert root is not None
  base=Path(root).resolve()
  def read(rel):
   assert isinstance(rel,str) and rel.startswith('source-evidence/') and rel.endswith('.json')
   q=base/rel;assert q.resolve().is_relative_to(base)
   for p in [q,*q.parents]:
    if p==base:break
    assert not p.is_symlink()
   return json.loads(q.read_bytes())
  b=member['parent_connection'];near=assertions[b['nearer_ancestor_assertion_id']];far=assertions[b['farther_ancestor_assertion_id']]
  assert b['type']=='parent_between_consecutive_ancestors' and b['interpretation_basis']==BASIS and b['status']=='contextual_provisional' and b['human_reviewed']is False and b['rationale'] and member['source_assertion_id']is None
  assert near['predicate']=='father' and far['predicate']=='grandfather' and near['subject_person_id']==far['subject_person_id'] and far['qualifiers']['lineage']=='paternal'
  assert near['subject_person_id']in rows[b['chain_subject_person_id']]['source_person_ids'] and near['object_person_id']in member['source_person_ids'] and far['object_person_id']in rows[member['parent_person_id']]['source_person_ids']
  en,=near['evidence'];ef,=far['evidence'];c=chapters[en['chapter_id']];p,=c['paragraphs'];binding=c['annotation']['epitaph_fact_binding']
  try:from .epitaph_titled_ancestors import valid as facts_valid
  except ImportError:from epitaph_titled_ancestors import valid as facts_valid
  facts_valid(c,[{'record_type':'person_assertion_set','assertions':[near,far]}],binding)
  w=c['source']['transcription_witness'];t=read(w['transcription_path']);cap=read(w['capture_path']);meta=read(w['metadata_path']);text=p['text'];h=hashlib.sha256(text.encode()).hexdigest()
  assert c['source']['text_scope']=='complete_work' and c['source']['revision_id']is None and c['source']['image_verified']is False and w['scope']=='complete_single_inscription_not_modern_article' and w['underlying_rubbing_personally_accessed']is False and w['transcription_page_visually_checked']is False
  assert t['text']==text and t['text_sha256']==h and t['length']==len(text) and t['captured_article_field']=="article: '"+text+"'," and t['fragment_sha256']==hashlib.sha256(t['captured_article_field'].encode()).hexdigest()
  assert t['normalization']=='none' and t['human_reviewed']is False and t['original_stone_or_rubbing_image_verified']is False
  assert cap['article_sha256']==h and cap['article_codepoints']==len(text) and cap['url']==c['source']['url'] and cap['public_http_status']==200
  assert meta['record_key']==w['database_record_id'] and meta['institution']==w['institution'] and meta['reported_transcription_origin']==w['reported_transcription_origin']
  assert p['source_position']['source_text_start']==0 and p['source_position']['source_text_end']==len(text)
  assert not any(a['predicate']=='father'and a['subject_person_id']in member['source_person_ids'] and a['object_person_id']not in rows[member['parent_person_id']]['source_person_ids']for a in assertions.values())
  refs=b['references'];assert len(refs)==2 and {r['assertion_id']for r in refs}=={near['id'],far['id']}
  for a in [near,far]:
   e,=a['evidence'];r,=[r for r in refs if r['assertion_id']==a['id']]
   assert all(r[k]==e[k]for k in ['work_id','book_id','source_id','chapter_id','paragraph_id','quote','subject_person_mention_id','object_person_mention_id']) and r['url']in[c['source']['url'],c['source']['permalink']] and r['scope']
  # The identity is a preferred title-role identification, never a named source ancestor.
  ir=b['ancestor_identity_reference'];review=read(ir['path']);decision,=[d for d in review['decisions']if d['key']==ir['decision_key']]
  assert review['human_reviewed']is False and decision['person_id']==far['object_person_id'] and decision['status']=='contextual_provisional' and decision['selection']=='preferred_source_role_identification' and decision['qualification'] and decision['evidence']
  par=decision.get('current_parallel_source_anchor',decision['parallel_source']);pc=chapters[par['chapter_id']];pp,=[p for p in pc['paragraphs']if p['id']==par['paragraph_id']];mm,=[m for m in pp['mentions']if m['id']==par['mention_id']]
  np=base/par['path'];assert par['path'].startswith('corpus/') and np.resolve().is_relative_to(base) and not np.is_symlink() and json.loads(np.read_bytes())==pc
  assert par['person_id']==far['object_person_id'] and mm['person_id']==far['object_person_id'] and pp['text']==par['quote'] and mm['surface']==par['surface'] and pp['text'][mm['start']:mm['end']]==mm['surface'] and pp['text_layer']=='received_chapter'
  return True
 except (AssertionError,KeyError,TypeError,ValueError,IndexError,OSError,AttributeError):return False
