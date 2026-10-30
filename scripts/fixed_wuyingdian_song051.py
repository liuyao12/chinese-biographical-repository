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
PINS={'image-column-locations.json': '4bcfcfd76cebf5837b789359bd2f0f5fa245dfc0a2aab33cf15088c2b1070607', 'acquisition-provenance.json': '6a8e194a14637e13a1f51b07f4b0b384a8481a77e3a0d297470c94b86196c92c', 'glyph-review-qualification.json': '57efb3f00f2ddc3397bbb85975a780a7858f3f1d53d49c9f2a4b7aa9cb462d28', 'transcription-projection.json': 'a1dc2720b8c4b0b9e021b12739a7db1dba5617ec5a6283b1b4077ef8ed5449dc', 'transcription-witness-contract.json': '3bf2e5af1897b58d08c4cc34e0a7f2c395ed79b7ef4dc8fbb97f80c642ed2808', 'transcription-columns.txt': '8d2ae0cd97228ef9a252a07a5886f2f0c3d445e305f311e484b38a97f462fcad', 'two-glyph-correction.json': '899feecbd32f57327f1c9c48437c7d48b556f6864ca085435d492175b4824e96', 'yinxiao-glyph-ner-correction.json': '440278deb18fb31a0c37d0f5c19a42d9f608022f86058e6956301af1e7594fb0', 'yirong-son-di-glyph-correction.json': 'f26c307f31abf05e12cb300cd78f477e4c3bcfd3a172cec3c3ba76f843222192', 'yiqing-son-aiwang-ye-glyph-correction.json': 'cfe6b90e34e0531a9246ed05afc92e836fff440a599cae0d4c2ecbd5a6e0b77e', 'zunkao-kunzhi-twelve-glyph-correction.json': '83836934c1a3a0cc54ba39d7172de593513463dc5766fa2194ab1cb3d116105d', 'zihui-name-glyph-correction.json': '5b29f49cfd63c63f8498653544b7553271c7895dc6ef529db7c4dcf480e5aa10', 'seven-glyph-image-correction.json': '607c9122be6f0480a1217121dce572e00718dfe2c1b7e2738f8978f467c4d6fd', 'seven-glyph-historical-qualification.json': '1be725281cafddc57a3470444922f446c39d798d9eb41047f995f74a3107481b', 'six-glyph-image-correction.json': '6402177480f0eb6279d122eaa611d779b5fab386f674eb7805abe3bb7d315357', 'six-glyph-historical-qualification.json': 'c141320eff9a77092992aaefa8707e6e105c44ec8e9eacd49e8b57cacb944177', 'historical-transcriptions/56753db8e4242acd19dd7729cc4ca460d53795449c5d9e336c923be767dd91ed/transcription-columns.txt': '56753db8e4242acd19dd7729cc4ca460d53795449c5d9e336c923be767dd91ed', 'historical-transcriptions/f74728c7bbdcc282b0285671b86bfb8eb3d51b0bef5e5a0b165fde4ee9cd97c4/transcription-columns.txt': 'f74728c7bbdcc282b0285671b86bfb8eb3d51b0bef5e5a0b165fde4ee9cd97c4', 'historical-transcriptions/f74728c7bbdcc282b0285671b86bfb8eb3d51b0bef5e5a0b165fde4ee9cd97c4/glyph-review-qualification.json': '624b20b2e4b6c6c30b90ba1ca5be839ca6f95924034d392c79b5019866f6adef', 'zhi-glyph-image-correction.json': 'cffafe774417f5726c21cf5cb8cc93b73dcec9f0babaec3b886ed587edacc780', 'zhi-glyph-historical-qualification.json': '49ad6a9c18abec91f0179a201508add082811637a0d67f89402db9cadcd0ed2a'}
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
 fixed(root,'yinxiao-glyph-ner-correction.json')
 fixed(root,'yirong-son-di-glyph-correction.json')
 fixed(root,'yiqing-son-aiwang-ye-glyph-correction.json')
 fixed(root,'zunkao-kunzhi-twelve-glyph-correction.json')
 fixed(root,'zihui-name-glyph-correction.json')
 fixed(root,'seven-glyph-image-correction.json')
 historical=json.loads(fixed(root,'seven-glyph-historical-qualification.json'))
 for item in historical['historical_files']:
  path=(Path(root)/item['path']).resolve();need(path.is_relative_to(Path(root).resolve()/'source-evidence'),'歷史snapshot路徑');need(hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256'],'歷史snapshot原bytes不符')
 correction=json.loads(fixed(root,'six-glyph-image-correction.json'))
 historical6=json.loads(fixed(root,'six-glyph-historical-qualification.json'))
 zhi_correction=json.loads(fixed(root,'zhi-glyph-image-correction.json'));zhi_historical=json.loads(fixed(root,'zhi-glyph-historical-qualification.json'))
 need(correction['after_transcription_sha256']==historical6['current_transcription_sha256']==zhi_correction['before_transcription_sha256'] and correction['human_reviewed']is False and correction['image_verified']is False,'六字階段資格')
 for item in historical6['historical_files']:
  path=(Path(root)/item['path']).resolve();need(path.is_relative_to(Path(root).resolve()/'source-evidence'),'六字前版本路徑');need(hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256'],'六字前版本原bytes不符')
 prior_name='historical-transcriptions/'+correction['before_transcription_sha256']+'/transcription-columns.txt'
 prior=fixed(root,prior_name).decode().splitlines(keepends=True)
 need(len(correction['changes'])==6,'六字訂正範圍')
 for change in correction['changes']:
  n=change['raw_line']-1;i=change['raw_character_0based'];need(prior[n][i]==change['before'] and len(change['before'])==len(change['after'])==1,'六字原位置');prior[n]=prior[n][:i]+change['after']+prior[n][i+1:]
 six_raw=fixed(root,'historical-transcriptions/'+zhi_correction['before_transcription_sha256']+'/transcription-columns.txt')
 need(''.join(prior).encode()==six_raw,'六字階段外原轉錄被改')
 need(zhi_correction['after_transcription_sha256']==zhi_historical['current_transcription_sha256']==sha and zhi_correction['human_reviewed']is False and zhi_correction['image_verified']is False,'祗字訂正當前資格')
 for item in zhi_historical['historical_files']:
  path=(Path(root)/item['path']).resolve();need(path.is_relative_to(Path(root).resolve()/'source-evidence'),'祗字前版本路徑');need(hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256'],'祗字前版本原bytes不符')
 changes=zhi_correction['changes'];need(len(changes)==1,'祗字訂正範圍');change=changes[0];need(change['raw_line']==91 and change['raw_character_0based']==19 and change['before']=='〓' and change['after']=='祗','祗字限定位置');stage=six_raw.decode().splitlines(keepends=True);need(stage[90][19]=='〓','祗字原佔位');stage[90]=stage[90][:19]+'祗'+stage[90][20:];need(''.join(stage).encode()==raw,'祗字外原轉錄被改')
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
