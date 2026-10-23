"""Ancient inscription quoted by a modern printed witness; never an image-collation claim."""
import json,hashlib,re,unicodedata
from pathlib import Path
LAYER='epitaph_as_modernly_transcribed'

def errors(chapter,root,works,books):
 source=chapter.get('source',{});w=source.get('transcription_witness')
 if isinstance(w,dict) and w.get('kind')=='institutional_database_epitaph_transcription':
  try:
   from .epitaph_database_witness import errors as database_errors
  except ImportError:
   from epitaph_database_witness import errors as database_errors
  return database_errors(chapter,root,works,books)
 if w is None and works.get(chapter.get('work_id'),{}).get('work_type')!='single_epitaph' and not any(p.get('text_layer')==LAYER for p in chapter.get('paragraphs',[])):return []
 failures=[]
 def require(ok,reason):
  if not ok:failures.append('古文校錄見證：'+reason)
 def read(rel):
  if not isinstance(rel,str)or not rel.startswith('source-evidence/')or not rel.endswith('.json'):raise ValueError('證據路徑格式')
  base=Path(root).resolve();path=(base/rel).resolve()
  if not path.is_relative_to(base)or not path.is_file():raise ValueError('證據路徑離開實際root或缺檔')
  return json.loads(path.read_text(encoding='utf-8'))
 try:
  require(isinstance(w,dict)and w.get('kind')=='modern_printed_epitaph_transcription','未知類型')
  if not isinstance(w,dict):return failures
  require(source.get('revision_id')is None and not source.get('source_commit')and not source.get('source_blob'),'不可偽造網站或Git修訂號')
  require(source.get('image_verified')is False and w.get('original_stone_or_rubbing_image_verified')is False and w.get('underlying_rubbing_personally_accessed')is False,'不得將轉錄頁視讀升為原石或原拓校核')
  require(w.get('transcription_page_visually_checked')is True and chapter.get('annotation',{}).get('human_reviewed')is False,'轉錄頁覆核與人工資格')
  require(source.get('text_scope')=='complete_work' and w.get('scope')=='complete_single_inscription_not_modern_article','只支援單方古文全文，不能冒現代文章全文或其他節錄')
  require(source.get('license_scope')=='classical_inscription_text_only'and bool(source.get('rights')),'古文與現代權利須分層')
  require(all(isinstance(w.get(k),str)and bool(w[k])for k in ['publication_author','publication_title','publication']),'現代校錄署名書目缺失')
  require(type(w.get('printed_page'))is int and w['printed_page']>0 and type(w.get('pdf_page'))is int and w['pdf_page']>0,'頁位無效')
  require(isinstance(w.get('pdf_sha256'),str)and re.fullmatch('[0-9a-f]{64}',w['pdf_sha256'])is not None,'固定PDF指紋缺失')
  work=works.get(chapter.get('work_id'),{});book=books.get(chapter.get('book_id'),{})
  require(work.get('work_type')=='single_epitaph' and len(work.get('books',[]))==1,'作品須是單方墓誌，而非虛造史書或文集')
  require(book.get('unit_kind')=='editorial_single_text_container'and book.get('number')is None and book.get('original_volume_number')is None and bool(work.get('numbering_note')),'編輯全文容器不得偽造古代卷一')
  t=read(w.get('transcription_path'));a=read(w.get('span_path'));meta=read(w.get('metadata_path'))
  text=t.get('text');require(isinstance(text,str)and bool(text),'缺古文全文')
  if not isinstance(text,str):return failures
  require(t.get('length')==len(text)and hashlib.sha256(text.encode()).hexdigest()==t.get('text_sha256'),'全文字數或指紋不符')
  columns=t.get('printed_columns',[]);require(isinstance(columns,list)and bool(columns),'缺排印閱讀順序')
  require([x.get('printed_column_number')for x in columns]==list(range(1,len(columns)+1)),'排印欄號須完整含空欄')
  require(all(isinstance(x.get('text'),str)and x.get('length')==len(x['text'])and unicodedata.normalize('NFKC',x.get('pdf_cmap_codepoints',''))==x['text']for x in columns)and ''.join(x.get('text','')for x in columns)==text,'欄全文或相容碼位轉換不符')
  require(t.get('original_stone_or_rubbing_image_verified')is False and t.get('transcription_page_visually_checked')is True and t.get('human_reviewed')is False,'轉錄證據資格不符')
  spans=a.get('upper_transcription_only',[]);anchors=a.get('character_anchors',[])
  require(len(anchors)==len(text),'每一字須有原排印text span錨點')
  covered=set()
  for i,x in enumerate(anchors):
   si=x.get('span_index');offset=x.get('offset_in_span')
   require(type(si)is int and 0<=si<len(spans)and type(offset)is int,'span索引無效')
   if type(si)is not int or not 0<=si<len(spans)or type(offset)is not int:continue
   span=spans[si];raw=span.get('text','')
   ok=(0<=offset<len(raw)and raw[offset]==x.get('raw_codepoint')and unicodedata.normalize('NFKC',raw[offset])==x.get('normalized')==text[i]
       and x.get('linear_start')==i and x.get('linear_end')==i+1 and x.get('pdf_text_matrix_x')==span.get('x')and x.get('pdf_text_matrix_y')==span.get('y'))
   require(ok,'原字／字位／座標不符');covered.add((si,offset))
  visible={(i,j)for i,s in enumerate(spans)for j,c in enumerate(s.get('text',''))if not c.isspace()}
  require(covered==visible,'所選古文排印區有可見字未消費或多領字')
  require(a.get('printed_page')==w['printed_page']and a.get('pdf_page_1_based')==w['pdf_page'],'span頁位不符')
  require(meta.get('publisher_contents_url')==source.get('url') and meta.get('author')==w['publication_author'] and meta.get('title')==w['publication_title'],'出版者入口與校錄書目不符')
  require(meta.get('pdf_sha256')==w['pdf_sha256']and meta.get('pdf_url')+'#page='+str(w['pdf_page'])==source.get('permalink')and meta.get('transcription_page_link')==source.get('permalink'),'書目PDF指紋與頁鏈不符')
  require(meta.get('copied_original_images')is False and meta.get('copied_pdf')is False,'此契約只存文字與外鏈')
  paragraphs=chapter.get('paragraphs',[])
  require(len(paragraphs)==1,'首版只支援單方全文的一個編輯段落')
  for p in paragraphs:
   pos=p.get('source_position',{})
   require(p.get('text_layer')==LAYER and p.get('text')==text,'古文全文不可混現代註號、翻譯或改字')
   require(pos.get('kind')=='modern_printed_transcription'and pos.get('source_text_start')==0 and pos.get('source_text_end')==len(text)and pos.get('printed_page')==w['printed_page']and pos.get('pdf_page')==w['pdf_page']and pos.get('editorial_single_paragraph')is True and pos.get('physical_line_divisions_inferred')is False,'編輯段落範圍或原石行界資格無效')
 except (KeyError,TypeError,ValueError,IndexError,AttributeError,OSError,json.JSONDecodeError)as exc:failures.append('古文校錄見證：格式或原文證據缺失 '+type(exc).__name__)
 return failures
