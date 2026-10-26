"""Exact Song051 AI transcription receipt; does not certify glyph truth or human review."""
import hashlib,json
from pathlib import Path
try:
 from scripts.witness_projection import repository_positions
except ImportError:
 from witness_projection import repository_positions
CID='c-songshu-051-wyd1739-zongshi'
SID='s-songshu-051-wyd1739-zongshi'
BASE='source-evidence/song051-wyd1739-zongshi/'
PINS={'image-column-locations.json': '8a92dba3533b0c7c618fc698d19d21e722aced925969276d874aa18731de4b68', 'acquisition-provenance.json': 'ae78710bee703680e3a49d15fffe5f4ea6f2b4c944fcf7a633c5b368b5592a59', 'glyph-review-qualification.json': '624b20b2e4b6c6c30b90ba1ca5be839ca6f95924034d392c79b5019866f6adef', 'transcription-projection.json': 'a465733697bf6dbef937e76c9e9a2dcc55fb567a90feec8ba4a8f0e559669c83', 'transcription-witness-contract.json': '399bef4d5fbc86e81a9273e22f355fc2b062f78101a050e4ac19a840bc8f0835', 'transcription-columns.txt': '6a1ea58d5207fcd15d7cbc5a71a17082681930a039904ce789c4debbf7a29d9f', 'two-glyph-correction.json': '899feecbd32f57327f1c9c48437c7d48b556f6864ca085435d492175b4824e96'}
def need(ok,msg):
 if not ok:raise ValueError('武英殿宋051轉錄：'+msg)
def fixed(root,name):
 root=Path(root).resolve();p=(root/(BASE+name)).resolve()
 need(p.is_relative_to(root/'source-evidence'),'路徑越界')
 b=p.read_bytes();need(hashlib.sha256(b).hexdigest()==PINS[name],name+' SHA不符');return b
def validate_source(chapter,root):
 need(isinstance(chapter,dict),'章須為物件')
 c=json.loads(fixed(root,'transcription-witness-contract.json'))
 need(all(chapter.get(k)==v for k,v in c['chapter_dimensions'].items()),'來源維度不符')
 need(chapter.get('source')==c['source'],'來源版本/取得/AI資格不符')
 a=chapter.get('annotation');need(isinstance(a,dict)and a==c['required_annotation'],'完整待標註AI階段資格不符')
 raw=fixed(root,'transcription-columns.txt');sha=hashlib.sha256(raw).hexdigest();lines=raw.decode().splitlines()
 loc=json.loads(fixed(root,'image-column-locations.json'));proj=json.loads(fixed(root,'transcription-projection.json'))
 fixed(root,'glyph-review-qualification.json');fixed(root,'acquisition-provenance.json')
 fixed(root,'two-glyph-correction.json')
 need(loc['raw_sha256']==proj['raw_sha256']==sha,'raw版本不符')
 coords=loc['column_coordinates'];need(len(coords)==len(lines)==c['raw_lines'],'原列遺漏')
 need([x['raw_line']for x in coords]==list(range(1,len(lines)+1)),'列序不符')
 ps=chapter.get('paragraphs');need(isinstance(ps,list)and len(ps)==len(c['paragraphs'])==c['native_paragraphs'],'完整段數不符')
 points=[]
 for p,spec in zip(ps,c['paragraphs']):
  need(isinstance(p,dict)and all(p.get(k)==v for k,v in spec.items()),'原文/層/位置不符')
  need(p.get('annotation_status')=='pending'and p.get('mentions')==[],'source-only段須待標註且無提及')
  pts,digest=repository_positions(root,p,lines);need(digest==sha,'投影SHA不符');points.extend(pts)
  for n,i in pts:
   x=coords[n-1];need(x['side']in('right','left')and 1<=x['physical_column_from_right_1based']<=10 and x['raw_character_offsets_0based']==[0,len(lines[n-1])],'實列位置不符')
 need(points==[(n,i)for n,t in enumerate(lines,1)for i in range(len(t))],'非完整唯一順序投影')
 need(chapter.get('text_sha256')==c['text_sha256']==hashlib.sha256('\n\n'.join(p['text']for p in ps).encode()).hexdigest(),'全文SHA不符')
 return True
def source_errors(chapter,root):
 if not isinstance(chapter,dict):return ['武英殿宋051轉錄：章須為物件']
 a=chapter.get('annotation');binding=a.get('fixed_transcription_contract')if isinstance(a,dict)else None
 if chapter.get('id')!=CID and chapter.get('source_id')!=SID and binding!='wuyingdian_song051_transcription':return []
 try:validate_source(chapter,root);return []
 except (ValueError,TypeError,KeyError,OSError,UnicodeError,StopIteration)as e:return ['武英殿宋051轉錄：'+str(e)]
