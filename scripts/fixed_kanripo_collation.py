"""Exact independent Qing collation unit; never a Pei annotation or body relaxation."""
from pathlib import Path
import json,hashlib,re
CID='c-sanguozhi-023-qing-collation'
SHA='d6f42012810a7643dbf554325f4f653b5ae8758322d9afaa0caf1b385b51d4f3'
REV='214fcafa79894355909c9d8c2c1533089e7791c6'
REF='source-evidence/sgz023-peiqian/qing-collation-projection.json'
RAW='source-evidence/sgz023-peiqian/KR2a0012_023-214fcafa.txt'
URL='https://github.com/kanripo/KR2a0012/blob/'+REV+'/KR2a0012_023.txt'
def errors(chapter,root):
 if chapter.get('id')!=CID:return []
 try:
  root=Path(root).resolve()
  def read(rel):
   p=root/rel;assert p.resolve()==p and p.is_file();return p.read_bytes()
  pin=json.loads(read('scripts/fixed_kanripo_collation_pins.json'))
  assert pin=={'format_version':'0.1','bindings':{CID:{'raw_file':RAW,'raw_sha256':SHA,'revision_id':REV,'projection_ref':REF,'first_line':471,'last_line':520}}}
  assert chapter['annotation']['fixed_kanripo_collation_ref']==REF
  assert chapter['work_id']=='w-sanguozhi'and chapter['book_id']=='b-sanguozhi-023'and chapter['source_id']=='s-sanguozhi-023-qing-collation-kr214fcafa'
  source=chapter['source'];assert source['response_sha256']==SHA and source['revision_id']==source['source_commit']==REV and source['url']==source['permalink']==URL
  b=read(RAW);assert hashlib.sha256(b).hexdigest()==SHA;raw=b.decode('utf-8');lines=raw.splitlines(keepends=True);assert len(lines)==520
  start=sum(map(len,lines[:470]));end=len(raw);positions=[];i=start
  while i<end:
   if raw.startswith('<pb:',i):i=raw.index('>',i)+1;continue
   if raw[i]not in'()\n\r¶':positions.append(i)
   i+=1
  text=''.join(raw[i]for i in positions);d=json.loads(read(REF));assert d=={'record_type':'fixed_kanripo_qing_collation_projection','raw_file':RAW,'raw_sha256':SHA,'source_revision':REV,'first_line':471,'last_line':520,'raw_start':start,'raw_end':end,'raw_positions':positions,'paragraph_id':CID+':p001','text':text,'chapter_id':CID}
  assert len(chapter['paragraphs'])==1;p=chapter['paragraphs'][0]
  assert p['id']==CID+':p001'and p['text']==text and p['text_layer']=='witness_appended_qing_siku_collation'
  assert p['source_position']=={'first_line':471,'last_line':520,'source_layer':'qing_siku_collation_appendix','raw_projection_ref':REF}
  meta=p['layer_attribution'];assert meta['attributed_author']=='四庫館臣'and meta['period']=='清'and meta['scope']=='independent_volume_appendix'and meta['human_reviewed']is False and meta['image_verified']is False
  assert meta['received_authority']and isinstance(meta['quotation_dependencies'],list)and meta['quotation_dependencies']
  return []
 except(AssertionError,ValueError,TypeError,KeyError,OSError,IndexError):return ['固定卷023清考證原檔/完整範圍/獨立層或逐字投影不符']
