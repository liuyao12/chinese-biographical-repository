"""Bounded 1739 Song044 AI transcription witness, not a generic image or truth validator."""
import hashlib,json
from pathlib import Path
try:
 from scripts.witness_projection import repository_positions
except ImportError:
 from witness_projection import repository_positions
CID='c-songshu-044-wyd1739-xiehui'
SID='s-songshu-044-wyd1739-xiehui'
BASE='source-evidence/song044-wyd1739-xiehui/'
PINS={'transcription-columns.txt': '8977928c0263cad8f1ab482fbae1e626c9c1f12bed1b45268adbe8f32f112fc2', 'transcription-projection.json': 'f7958f225f5c87809d854888f27c146b8bbe3a19ff52ee375e90131b96d6b016', 'image-column-locations.json': '35afc2ea70f50d917c9895214ce910b2d4be5744aa2d57dc150a1acc62804fef', 'glyph-review-qualification.json': '80f96775b3cb8b4acb095d684f7d9821c3dde1ceed5ecea5aeeeda9d48fc3c0b', 'acquisition-provenance.json': '5dd7898b92f52ea7705f031dc2d1a9bc23e05f7c6aa175bf88d2fcaf086fbb66', 'transcription-witness-contract.json': '960ba887342855e0430808e4ae6eb946fded2d8a7a60419b386e951d17983266'}
def need(ok,message):
 if not ok:raise ValueError('武英殿宋044轉錄：'+message)
def digest(value):return hashlib.sha256(value).hexdigest()
def fixed(root,name):
 root=Path(root).resolve();path=(root/(BASE+name)).resolve()
 need(path.is_relative_to(root)and path.is_relative_to(root/'source-evidence'),'路徑越界')
 raw=path.read_bytes();need(digest(raw)==PINS[name],name+' SHA不符')
 return raw
def validate_source(chapter,root):
 need(isinstance(chapter,dict),'須為物件')
 contract=json.loads(fixed(root,'transcription-witness-contract.json'))
 for key,value in contract['chapter_dimensions'].items():need(chapter.get(key)==value,'來源維度不符')
 need(chapter.get('source')==contract['source'],'來源取得/轉錄/疑缺/版本元資料不符')
 need(isinstance(chapter.get('annotation'),dict)and chapter['annotation'].get('fixed_transcription_contract')==contract['required_annotation_binding'],'來源入口資格缺失')
 raw=fixed(root,'transcription-columns.txt');lines=raw.decode('utf-8').splitlines()
 projection=json.loads(fixed(root,'transcription-projection.json'));locations=json.loads(fixed(root,'image-column-locations.json'))
 fixed(root,'glyph-review-qualification.json');fixed(root,'acquisition-provenance.json')
 need(projection['raw_sha256']==locations['raw_sha256']==digest(raw),'轉錄版本SHA不符')
 ps=chapter.get('paragraphs');need(isinstance(ps,list)and len(ps)==len(contract['paragraphs'])==22,'完整22段須保存')
 coords=locations['column_coordinates'];need(len(coords)==len(lines)==325,'逐行座標缺失')
 need([r['raw_line']for r in coords]==list(range(1,len(lines)+1)),'原行序重複/缺漏')
 allpoints=[]
 for p,spec in zip(ps,contract['paragraphs']):
  need(isinstance(p,dict)and all(p.get(k)==v for k,v in spec.items()),'段落字文/層/位置不符')
  points,sha=repository_positions(root,p,lines);need(sha==digest(raw),'既有投影API來源SHA不符');allpoints.extend(points)
  for n,i in points:
   coordinate=coords[n-1];need(coordinate['raw_line']==n and coordinate['raw_character_offsets_0based']==[0,len(lines[n-1])],'字位座標不符')
   need(coordinate['side']in('right','left')and 1<=coordinate['physical_column_from_right_1based']<=10 and 0<=i<len(lines[n-1]),'頁側/行字位不符')
 need(allpoints==[(n,i)for n,line in enumerate(lines,1)for i in range(len(line))],'完整轉錄字位非唯一順序全覆蓋')
 need(chapter.get('text_sha256')==contract['text_sha256']==digest('\n\n'.join(p['text']for p in ps).encode()),'全文SHA不符')
 norm=chapter['source']['normalization'];eds=norm['editorial_readings'];markers=norm['missing_text_markers']
 need(len(eds)==1 and len(markers)==2,'一疑兩缺不分離')
 e=eds[0];p=next(p for p in ps if p['id']==e['paragraph_id'])
 need(e['kind']=='unresolved_printed_glyph'and e['accepted_reading']is None and e['placeholder']=='〓'and e['placeholder_is_source_glyph']is False and p['text'][e['start']:e['end']]=='〓'and e['end']==e['start']+1,'未識字占位不符')
 need(sum(p['text'].count('〓')for p in ps)==1,'未識字占位數量不符')
 for marker in markers:
  need(marker['printed_notice']=='缺'and marker['notice_in_main_text']is False and marker['estimated_missing_characters']is None and marker['blank_extent_in_characters']is None,'印缺不得補字數/正文')
 tw=chapter['source']['received_transcription_witness']
 need(tw['original_pdf_locally_obtained']is False and tw['reported_pdf_sha1']=='126c34411892f6943a575a15ee46fb0064bd5b7b','PDF取得資格不符')
 return True
def source_errors(chapter,root):
 if not isinstance(chapter,dict):return ['武英殿宋044轉錄：須為物件']
 annotation=chapter.get('annotation');binding=annotation.get('fixed_transcription_contract')if isinstance(annotation,dict)else None
 if chapter.get('id')!=CID and chapter.get('source_id')!=SID and binding!='wuyingdian_song044_transcription':return []
 try:validate_source(chapter,root);return []
 except (ValueError,KeyError,TypeError,OSError,UnicodeError,StopIteration) as error:return ['武英殿宋044轉錄：'+str(error)]
