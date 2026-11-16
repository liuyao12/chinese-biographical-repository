# coding: utf-8
"""Validate an explicitly selected complete Kanripo line unit, not historical truth."""
from pathlib import Path
import json,hashlib

def errors(chapter,root):
 ref=chapter.get('annotation',{}).get('fixed_kanripo_projection_ref')
 try:
  root=Path(root).resolve()
  required_pinpath=root/'scripts/fixed_kanripo_witness_pins.json'
  if required_pinpath.exists():
   assert required_pinpath.resolve()==required_pinpath and required_pinpath.is_file()
   required_catalog=json.loads(required_pinpath.read_text(encoding='utf-8'))
   assert isinstance(required_catalog,dict) and required_catalog.get('format_version')=='0.1'
   required_witnesses=required_catalog['witnesses'];required_bindings=required_catalog.get('chapter_bindings',{})
   assert isinstance(required_witnesses,dict) and isinstance(required_bindings,dict)
   assert all(isinstance(cid,str) and cid and isinstance(key,str) and key in required_witnesses for cid,key in required_bindings.items())
   if chapter.get('id') in required_bindings:assert isinstance(ref,str) and ref
  if ref is None:return []
  def path(name):
   p=Path(name)
   assert not p.is_absolute()and p.parts and p.parts[0]=='source-evidence'and'..'not in p.parts
   dest=root/p;assert dest.resolve()==dest and dest.is_file();return dest
  d=json.loads(path(ref).read_text(encoding='utf-8'));b=path(d['raw_file']).read_bytes();raw=b.decode('utf-8',errors='strict');digest=hashlib.sha256(b).hexdigest()
  assert d['record_type']=='fixed_kanripo_complete_unit_projection'and d['source_revision']==chapter['source']['revision_id']==chapter['source']['source_commit']
  assert digest==d['raw_file_sha256']==chapter['source']['response_sha256']
  pinpath=root/'scripts/fixed_kanripo_witness_pins.json';pincatalog=None
  if pinpath.exists():
   assert pinpath.resolve()==pinpath and pinpath.is_file()
   pincatalog=json.loads(pinpath.read_text(encoding='utf-8'))
   assert isinstance(pincatalog,dict) and pincatalog.get('format_version')=='0.1'
   witnesses=pincatalog['witnesses'];bindings=pincatalog.get('chapter_bindings',{})
   assert isinstance(witnesses,dict) and isinstance(bindings,dict)
   assert all(isinstance(cid,str) and cid and isinstance(key,str) and key in witnesses for cid,key in bindings.items())
   if chapter.get('id') in bindings:assert d.get('witness_key')==bindings[chapter['id']]
  if 'witness_key' in d:
   assert pincatalog is not None
   pin=pincatalog['witnesses'][d['witness_key']]
   assert set(pin)=={'revision_id','raw_sha256','raw_file','url','first_line','last_line','next_line'}
   assert pin['revision_id']==d['source_revision'] and pin['raw_sha256']==digest and pin['raw_file']==d['raw_file']
   assert pin['url']==chapter['source']['permalink'] and pin['url']==chapter['source']['url']
   assert all(pin[k]==d['unit'][k]for k in ('first_line','last_line','next_line'))
  u=d['unit'];lines=raw.splitlines(keepends=True);first,last=u['first_line'],u['last_line'];assert type(first)is int and type(last)is int and 1<=first<=last<len(lines)
  start=sum(map(len,lines[:first-1]));end=sum(map(len,lines[:last]));assert u['start']==start and u['end']==end and u['raw']==raw[start:end]and lines[last].rstrip('\r\n')==u['next_line']
  # Full selected unit, not a retained fragment: only presentation wrappers may disappear.
  projected={'body':[],'note':[]};i=start;note=False
  while i<end:
   if raw.startswith('<pb:',i):
    close=raw.index('>',i);assert close<end;i=close+1;continue
   c=raw[i]
   if c=='(':assert not note;note=True
   elif c==')':assert note;note=False
   elif c not in '\n\r¶':projected['note'if note else'body'].append(i)
   i+=1
  assert not note
  seen={'body':[],'note':[]};ps=chapter['paragraphs'];assert len(ps)==len(d['paragraphs'])
  for p,q in zip(ps,d['paragraphs']):
   assert not any(key in layer for layer in (chapter,chapter['source'],d,q,p,p['source_position'])for key in ('annotator','attached_note_to_paragraph_id'))
   assert p['id']==q['paragraph_id']and p['text']==q['text']
   pos=q['raw_positions'];assert pos and all(type(v)is int for v in pos)and pos==sorted(set(pos))and all(start<=v<end for v in pos)
   assert ''.join(raw[v]for v in pos)==p['text'];layer=q['source_layer'];assert layer in seen
   expected={'body':('received_chapter','received_body'),'note':('witness_appended_pei_songzhi_note','pei_annotation')}[layer]
   assert (p['text_layer'],p['source_position']['source_layer'])==expected
   fl,ll=raw.count('\n',0,pos[0])+1,raw.count('\n',0,pos[-1])+1
   assert (q['first_line'],q['last_line'])==(fl,ll)==(p['source_position']['first_line'],p['source_position']['last_line'])
   assert p['source_position']['raw_projection_ref']==ref
   seen[layer]+=pos
  assert seen==projected
  return []
 except(AssertionError,ValueError,TypeError,KeyError,OSError,IndexError):return ['固定Kanripo完整單元原檔、層次、逐字投影或實際行界不符']
