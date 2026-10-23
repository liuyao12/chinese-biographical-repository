"""Complete ancient inscription as published by a public institutional database."""
import hashlib,json,re
from pathlib import Path
KIND='institutional_database_epitaph_transcription'
LAYER='epitaph_as_modernly_transcribed'
def errors(chapter,root,works,books):
 failures=[]
 def require(ok,msg):
  if not ok:failures.append('機構墓誌錄文見證：'+msg)
 def read(rel):
  assert isinstance(rel,str) and rel.startswith('source-evidence/') and rel.endswith('.json')
  base=Path(root).resolve();p=(base/rel).resolve();assert p.is_relative_to(base) and p.is_file()
  return json.loads(p.read_text())
 try:
  source=chapter['source'];w=source['transcription_witness']
  require(w['kind']==KIND,'類型不符')
  require(source.get('revision_id') is None and not source.get('source_commit') and not source.get('source_blob'),'不得偽造網站修訂或Git版本')
  require(source['image_verified'] is False and w['original_stone_or_rubbing_image_verified'] is False and w['underlying_rubbing_personally_accessed'] is False,'錄文不得升為原物影校')
  require(chapter['annotation']['human_reviewed'] is False and w['transcription_page_visually_checked'] is False,'本契約為文字HTTP覆核，不冒圖像或人工覆核')
  require(source['text_scope']=='complete_work' and w['scope']=='complete_single_inscription_not_modern_article','須為單方全文')
  require(source['license_scope']=='classical_inscription_text_only' and bool(source['rights']),'古文與現代影像權利分層')
  require(bool(w['institution']) and bool(w['database_record_id']) and bool(w['reported_transcription_origin']),'責任機構及來源缺失')
  require(re.match(r'^https?://[^/]+/',source['url']) is not None and source['url']==source['permalink'],'實際公開單件URL缺失')
  work=works[chapter['work_id']];book=books[chapter['book_id']]
  require(work['work_type']=='single_epitaph' and len(work['books'])==1,'作品須單方墓誌')
  require(book['unit_kind']=='editorial_single_text_container' and book['number'] is None and book['original_volume_number'] is None and work['numbering_note'],'不可偽造卷一')
  t=read(w['transcription_path']);cap=read(w['capture_path']);meta=read(w['metadata_path'])
  text=t['text'];require(isinstance(text,str) and bool(text),'古文全文缺失')
  require(t['length']==len(text) and t['text_sha256']==hashlib.sha256(text.encode()).hexdigest(),'全文指紋/長度')
  fragment=t['captured_article_field'];require(fragment=="article: '"+text+"',",'原article字串須完整一欄，不混現代論述')
  require(t['fragment_sha256']==hashlib.sha256(fragment.encode()).hexdigest(),'原欄片段指紋')
  require(cap['article_sha256']==t['text_sha256'] and cap['article_codepoints']==len(text),'HTTP捕獲與全文不符')
  require(cap['url']==source['url'] and cap['public_http_status']==200,'捕獲URL/HTTP狀態不符')
  require(re.fullmatch('[0-9a-f]{64}',cap['raw_response_sha256']) is not None and type(cap['raw_response_bytes']) is int and cap['raw_response_bytes']>len(fragment.encode()),'完整捕獲指紋/界線缺失')
  a,b=cap['source_codepoint_span'];u,v=cap['source_utf8_byte_span']
  require(type(a)is int and 0<=a<b and b-a==len(text) and type(u)is int and 0<=u<v<=cap['raw_response_bytes'] and v-u==len(text.encode()),'原捕獲絕對碼位/byte位不符')
  require(meta['record_key']==w['database_record_id'] and meta['institution']==w['institution'] and meta['reported_transcription_origin']==w['reported_transcription_origin'],'機構書目/種次資格不符')
  require(t['original_stone_or_rubbing_image_verified'] is False and t['human_reviewed'] is False and t['normalization']=='none','不得改原數位字或冒校原物')
  ps=chapter['paragraphs'];require(len(ps)==1,'首版只支援全文一編輯段')
  for p in ps:
   pos=p['source_position'];require(p['text']==text and p['text_layer']==LAYER,'正文必須是完整見證原字')
   require(pos['kind']==KIND and pos['source_text_start']==0 and pos['source_text_end']==len(text) and pos['editorial_single_paragraph'] is True and pos['physical_line_divisions_inferred'] is False,'邏輯分段不得冒原石行界')
 except (AssertionError,KeyError,TypeError,ValueError,IndexError,OSError,AttributeError):failures.append('機構墓誌錄文見證：格式/證據不可讀')
 return failures
