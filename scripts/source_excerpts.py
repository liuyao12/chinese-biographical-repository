"""固定Git版本古注節錄的原行、Unicode位置與層次檢查；不判定人物身份。"""
import re
from urllib.parse import urlparse
LAYERS={'witness_duyu_annotation_excerpt':'duyu_annotation','witness_received_text_and_duyu_annotation_excerpt':'received_text_and_duyu_annotation'}
def year_number(term):
 digits='一二三四五六七八九'
 if term in digits and len(term)==1:return digits.index(term)+1
 if re.fullmatch('[一二三四五六七八九]?十[一二三四五六七八九]?',term):
  tens,ones=term.split('十');return (digits.index(tens)+1 if tens else 1)*10+(digits.index(ones)+1 if ones else 0)
 return None

def excerpt_errors(chapter):
 errors=[]
 for paragraph in chapter.get('paragraphs',[]):
  e=paragraph.get('source_excerpt');layer=paragraph.get('text_layer')
  if e is None and layer not in LAYERS:continue
  def check(ok,message):
   if not ok:errors.append(message)
  if not isinstance(e,dict):errors.append('missing literal excerpt metadata');continue
  try:
   source=chapter['source'];raw=e['raw_line'];start=e['start'];end=e['end'];line=e['raw_line_number'];book=e['book_number'];commit=e['source_commit'];url=urlparse(e['source_url']);heading=e['year_section_heading'];contexts=e['attribution_context_lines']
   check(e['kind']=='fixed_git_literal_span','unknown excerpt kind')
   check(layer in LAYERS and e['attribution_layer']==LAYERS.get(layer),'text and attribution layer mismatch')
   check(isinstance(raw,str)and type(start)is int and type(end)is int and 0<=start<end<=len(raw)and raw[start:end]==paragraph['text'],'excerpt differs from literal Unicode source span')
   check(type(line)is int and line>0 and type(book)is int and book>0 and chapter['book_id'].endswith(f'-{book:03}'),'invalid source book or line')
   check(isinstance(commit,str)and bool(re.fullmatch('[0-9a-f]{40}',commit))and source['revision_id']==source['source_commit']==commit,'source revision mismatch')
   check(bool(re.fullmatch('[0-9a-f]{40}',e['source_blob']))and e['source_blob']==source['source_blob']and bool(re.fullmatch('[0-9a-f]{64}',e['raw_file_sha256']))and e['raw_file_sha256']==source['raw_file_sha256'],'source digest mismatch')
   check(url.scheme=='https'and url.hostname=='github.com'and not url.username and not url.password and '/blob/'+commit+'/'in url.path and url.path.endswith(f'_{book:03}.txt')and url.fragment==f'L{line}-L{line}'and source['permalink']==e['source_url'],'source link is not exact fixed revision and line')
   match=re.search(r'(?:經|傳)([一二三四五六七八九十]+)年',heading['raw_line']);check(type(heading['line_number'])is int and 0<heading['line_number']<=line and type(heading['year_number'])is int and bool(match)and year_number(match.group(1))==heading['year_number'],'source year heading mismatch')
   check(isinstance(contexts,list)and contexts and all(type(v['line_number'])is int and isinstance(v['raw_line'],str)for v in contexts)and contexts[-1]=={'line_number':line,'raw_line':raw},'attribution context does not end at excerpt line')
   check(all(a['line_number']+1==b['line_number']for a,b in zip(contexts,contexts[1:])),'nonconsecutive attribution context')
   if e['attribution_layer']=='duyu_annotation':
    prefix='\n'.join(v['raw_line']for v in contexts[:-1])+raw[:start]
    check('注'in prefix,'pure commentary lacks original attribution marker')
   else:check('注'in paragraph['text'],'mixed text excerpt lacks original annotation marker')
   check(source['text_scope']=='partial_chapter'and bool(source['extent'])and source['image_verified']is False and chapter['annotation']['human_reviewed']is False,'excerpt scope or review state overclaimed')
  except(KeyError,TypeError,ValueError,AttributeError):errors.append('malformed excerpt metadata')
 return errors
