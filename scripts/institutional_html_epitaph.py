"""One reviewed complete institutional inscription, with mutable source-role IDs.

No HTML is executed or fetched at validation time. The complete response remains
private; its exact capture hash, extraction ledger and text are public evidence.
This proves the preserved text capture, never image collation.
"""
from pathlib import Path
import json,hashlib,copy
KIND='fixed_institutional_html_epitaph'
WITNESS='institutional_html_epitaph_transcription'
CID='c-epitaph-yuanzhan-nmh-full'
SID='s-epitaph-yuanzhan-nmh-8900208'
URL='https://content.teldap.tw/main/dc_detail.php?dc_id=2389779'
TEXT_SHA='ff0421fb3960c1893f4789b06d9c7db2f544361cbc877ff1c3fe5741db6d1490'
HTTP_SHA='8564e672458672cf7581904ea73160d020af4411dcf303cadc647ecc24fdfb6c'
BASE='source-evidence/yuanzhan-epitaph-nmh'
SPANS={'grandfather':(30,31,'嘉'),'grandmother':(53,55,'穆氏'),'mu_shou':(59,60,'壽'),'mu_liang':(65,66,'亮'),'father':(70,71,'淵'),'mother':(93,95,'王氏'),'maternal_grandfather':(97,98,'肅'),'head':(109,110,'湛'),'zi':(112,114,'士深')}
def strict(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys()and all(strict(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(strict(x,y)for x,y in zip(a,b))
 return a==b
def roles(ch):
 assert isinstance(ch,dict)and ch['id']==CID and ch['source_id']==SID
 assert ch['work_id']=='w-epitaph-yuanzhan'and ch['book_id']=='b-epitaph-yuanzhan-full'
 p,=ch['paragraphs'];t=p['text'];assert p['id']==CID+':p001'and len(t)==1474 and hashlib.sha256(t.encode()).hexdigest()==TEXT_SHA==ch['text_sha256']
 assert p['text_layer']=='epitaph_as_modernly_transcribed'and ch['annotation']['human_reviewed']is False
 s=ch['source'];w=s['transcription_witness'];assert w['kind']==WITNESS and s['revision_id']is None and s['url']==s['permalink']==URL and s['image_verified']is False
 assert all(w[k]is False for k in ('transcription_page_visually_checked','original_stone_or_rubbing_image_verified','underlying_rubbing_personally_accessed'))
 assert not any(k in layer for layer in (p,p['source_position'],s,ch)for k in ('annotator','attached_note_to_paragraph_id'))
 assert not s.get('source_commit')and not s.get('source_blob')
 ms={m['id']:m for m in p['mentions']};r={}
 b=ch['annotation']['epitaph_fact_binding'];assert b==dict(kind=KIND,paragraph_id=p['id'],paragraph_sha256=TEXT_SHA,roles={k:p['id']+':m'+str(a).zfill(4)for k,(a,z,v)in SPANS.items()},source_id=SID)
 for k,(a,z,v)in SPANS.items():
  m=ms[b['roles'][k]];assert type(m['start'])is int and type(m['end'])is int and (m['start'],m['end'],m['surface'],m['kind'])==(a,z,v,'person')and t[a:z]==v and isinstance(m['person_id'],str)and m['person_id'];r[k]=m['person_id']
 assert r.pop('zi')==r['head']and len(set(r.values()))==len(r)
 # Original role syntax, not a nearest-name recognizer or permanent person-ID list.
 assert t[28:122]=='祖諱嘉。太保尚書令司徒公冀州刺史廣陽懿烈王祖母河南穆氏。宜都王壽孫女。司空亮從妹父諱淵。侍中吏部尚書司徒公雍州刺史廣陽忠武王母瑯邪王氏。父肅。尚書令司空宣簡公公諱湛。字士深。河南洛陽人也。'
 if 'allusion_binding'in ch['annotation']:
  try:from scripts.yuanzhan_allusion_roles import augment
  except ImportError:from yuanzhan_allusion_roles import augment
  r=augment(ch,r)
 return r
def expand(v,r):
 if isinstance(v,dict):
  if set(v)=={'$person'}:return r[v['$person']]
  return{k:expand(x,r)for k,x in v.items()}
 if isinstance(v,list):return[expand(x,r)for x in v]
 return copy.deepcopy(v)
def templates():return json.loads(Path(__file__).with_name('institutional_html_epitaph_facts.json').read_text())
def expected(ch):return expand(templates(),roles(ch))
def valid(ch,rs,b):
 roles(ch);want=expected(ch);got={}
 for row in rs:
  typ=row['record_type'];assert typ not in got;got[typ]=row
 assert len(got)==len(want)
 for row in want.values():assert strict(got.pop(row['record_type']),row)
 assert not got
 age,=ch['annotation']['age_assertions'];assert strict(age,expand(json.loads(Path(__file__).with_name('institutional_html_epitaph_age.json').read_text()),roles(ch)))
 return True
def relation_valid(a,paragraphs):
 try:
  if not isinstance(a,dict)or a.get('institution_epitaph_binding',{}).get('kind')!=KIND:return False
  p=paragraphs[CID+':p001'][1]
  # Paragraph-only consumers cannot validate a different witness or make IDs immutable.
  assert p['id']==CID+':p001'and hashlib.sha256(p['text'].encode()).hexdigest()==TEXT_SHA and p['text_layer']=='epitaph_as_modernly_transcribed'
  ms={m['id']:m for m in p['mentions']};rr={}
  for k,(x,y,s)in SPANS.items():
   m=ms[p['id']+':m'+str(x).zfill(4)];assert (m['start'],m['end'],m['surface'],m['kind'])==(x,y,s,'person');rr[k]=m['person_id']
  assert rr.pop('zi')==rr['head']and len(set(rr.values()))==len(rr)
  aa=expand(templates()['full-assertions.json']['assertions'],rr)
  return any(strict(a,x)for x in aa)
 except (KeyError,ValueError,TypeError,IndexError,AssertionError,AttributeError,OSError):return False
def age_valid(age,ch):
 try:return isinstance(age,dict)and strict(age,expand(json.loads(Path(__file__).with_name('institutional_html_epitaph_age.json').read_text()),roles(ch)))
 except (KeyError,ValueError,TypeError,IndexError,AssertionError,AttributeError,OSError):return False
def source_errors(ch,root,works,books):
 try:
  r=roles(ch);assert strict(ch,expand(json.loads(Path(__file__).with_name('institutional_html_epitaph_chapter.json').read_text()),r));s=ch['source'];w=s['transcription_witness'];root=Path(root).resolve()
  if 'allusion_binding'in ch['annotation']:
   try:from scripts.yuanzhan_allusion_roles import context_errors
   except ImportError:from yuanzhan_allusion_roles import context_errors
   assert not context_errors(ch,root,r)
  def read(rel):
   assert rel.startswith(BASE+'/')and rel.endswith('.json');p=root/rel;assert p.resolve()==p and p.is_file();return json.loads(p.read_text())
  cap=read(w['capture_path']);tx=read(w['transcription_path']);meta=read(w['metadata_path']);retention=read(w['capture_retention_qualification_path'])
  assert retention['original_response_replay_available']is False and retention['recapture_performed']is False and retention['transcription_retained']is True and retention['transcription_sha256']==TEXT_SHA
  assert retention['recorded_http_capture']['raw_response_sha256']==HTTP_SHA and retention['recorded_http_capture']['sha256']==hashlib.sha256((root/w['capture_path']).read_bytes()).hexdigest()
  assert cap['source_url']==URL and cap['http_status']==200 and cap['revision_id']is None
  assert cap['response_sha256']==HTTP_SHA and type(cap['response_bytes'])is int and cap['response_bytes']==11762
  assert cap['encoding']=='big5'and cap['encoding_errors']=='strict'and cap['source_decoded_codepoint_span']==[4034,5508]and cap['source_original_byte_span']==[5734,8677]
  assert cap['transcription_sha256']==TEXT_SHA and cap['transcription_codepoints']==1474 and cap['question_mark_count']==5 and cap['missing_square_count']==2
  assert cap['html_committed']is False and cap['images_downloaded']is False and cap['character_conversion']=='none'and cap['punctuation_changes']=='none'
  assert cap['transformations']==[dict(operation='strict_decode',encoding='big5'),dict(operation='select_literal_td_field',opening='<td>銘刻內容：',closing='</td>',codepoint_span=[4034,5509]),dict(operation='remove_exact_trailing_layout_space',source='　',count=1)]
  p,=ch['paragraphs'];assert tx==dict(text=p['text'],length=1474,text_sha256=TEXT_SHA,normalization='none',original_stone_or_rubbing_image_verified=False,human_reviewed=False)
  assert meta['institution']=='國立歷史博物館'and meta['accession']=='89-00208'and meta['rubbing']['catalogue_period_literal']=='清'and meta['rubbing']['numeric_date']is None
  assert all(meta['original_stone'][k]is None for k in ('composition_date','engraving_date','excavation_date','excavation_place'))and meta['original_stone']['image_verified']is False
  assert s['text_scope']=='complete_work'and s['license_scope']=='classical_inscription_text_only'and w['scope']=='complete_single_inscription_not_modern_article'
  assert works[ch['work_id']]['work_type']=='single_epitaph';book=books[ch['book_id']];assert book['unit_kind']=='editorial_single_text_container'and book['number']is None and book['original_volume_number']is None
  assert p['source_position']==dict(kind=WITNESS,source_text_start=0,source_text_end=1474,editorial_single_paragraph=True,physical_line_divisions_inferred=False)
  return []
 except (AssertionError,KeyError,ValueError,TypeError,IndexError,AttributeError,OSError):return ['固定機構HTML墓誌：完整錄文、實際捕獲或來源資格不符']
def ancestor_valid(member,rows,assertions,chapters):
 try:
  b=member['parent_connection'];assert b['type']=='parent_between_consecutive_ancestors'and b['interpretation_basis']=='institutional_epitaph_named_consecutive_ancestors'and b['status']=='contextual_provisional'and b['human_reviewed']is False and b['rationale']and member['source_assertion_id']is None
  ch=chapters[CID];r=roles(ch);aa=expected(ch)['full-assertions.json']['assertions'];by={a['id']:a for a in aa}
  near=assertions[b['nearer_ancestor_assertion_id']];far=assertions[b['farther_ancestor_assertion_id']]
  assert strict(near,by['a-yuanzhan-nmh-father'])and strict(far,by['a-yuanzhan-nmh-grandfather'])
  assert member['person_id']==r['father']and member['parent_person_id']==r['grandfather']and b['chain_subject_person_id']==r['head']
  assert r['head']in rows[b['chain_subject_person_id']]['source_person_ids']and r['grandfather']in rows[member['parent_person_id']]['source_person_ids']and r['father']in member['source_person_ids']
  assert b['references']==[dict(assertion_id=a['id'],**{k:ch[k]for k in ('work_id','book_id','source_id')},chapter_id=CID,paragraph_id=CID+':p001',quote=ch['paragraphs'][0]['text'],url=URL,scope='同一完整銘文之明父／祖父；中間父子僅編輯推導，不冒原文明父')for a in (near,far)]
  assert not any(a.get('predicate')=='father'and a.get('subject_person_id')==r['father']and a.get('object_person_id')!=r['grandfather']for a in assertions.values())
  return True
 except (AssertionError,KeyError,ValueError,TypeError,IndexError,AttributeError,OSError):return False
