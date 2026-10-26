"""Exact Song045 Liu Cui AI transcription receipt; does not certify glyph truth or human review."""
import hashlib,json
from pathlib import Path
try:
 from scripts.witness_projection import repository_positions
except ImportError:
 from witness_projection import repository_positions
CID='c-songshu-045-wyd1739-liucui'
SID='s-songshu-045-wyd1739-liucui'
BASE='source-evidence/song045-wyd1739-liucui/'
PINS={'image-column-locations.json': '7f50f2b03e8177a5600a1d59834c63feee9ae53683ced0281e2b679d0c2c8b66', 'acquisition-provenance.json': 'fad1cc0e61613f321b08afe8a6066065cd535cd2a07dcffd3d86da3ab2983a5c', 'glyph-review-qualification.json': '4dce2a01ca7fe2d2cd3751b117bd1a7aa0cd21b5979daec6c6ea4f6492a6c459', 'transcription-projection.json': '1c44f8ec3e3d45300754c4a020514db4bbf93547a3a205ce7ad8bf9034f532eb', 'transcription-witness-contract.json': 'b9a60d83aaa69f279e707275bf4cbf493af43f963a1c02f723f1a31151f1c3db', 'transcription-columns.txt': 'ad4c7d261c6ab397efdbf2933f34c491be371368986212d7854860bc96e514e2'}
def need(ok,msg):
 if not ok:raise ValueError('武英殿宋045轉錄：'+msg)
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
 if not isinstance(chapter,dict):return ['武英殿宋045轉錄：章須為物件']
 a=chapter.get('annotation');binding=a.get('fixed_transcription_contract')if isinstance(a,dict)else None
 if chapter.get('id')!=CID and chapter.get('source_id')!=SID and binding!='wuyingdian_song045_liucui_transcription':return []
 try:validate_source(chapter,root);return []
 except (ValueError,TypeError,KeyError,OSError,UnicodeError,StopIteration)as e:return ['武英殿宋045轉錄：'+str(e)]
