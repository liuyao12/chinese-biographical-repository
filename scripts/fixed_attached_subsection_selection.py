"""Trusted complete attached subsection, using existing raw-visible projection."""
import json,hashlib
from pathlib import Path
KIND='fixed_wikisource_attached_subsection_selection'
def pin(root,cid):
 f=Path(root)/'scripts/fixed_attached_subsection_witnesses.json'
 if not f.exists():return None
 d=json.loads(f.read_text());assert d['format_version']=='0.1'and isinstance(d['chapters'],dict)
 return d['chapters'].get(cid)
def required_ref_error(ch,root):
 try:
  b=pin(root,ch.get('id'))
  if b is not None:
   assert set(b)==({'selection_mode'}if b.get('selection_mode')=='next_sibling_subsection'else set())|{'source_revision','raw_sha256','raw_file','source_id','opening_heading','following_heading','raw_start','raw_end','projection_ref'}
   assert ch.get('annotation',{}).get('fixed_wikisource_unit_ref')==b['projection_ref']
   f=Path(root)/b['projection_ref'];assert f.resolve()==f and f.is_file();d=json.loads(f.read_text());assert d.get('record_type')==KIND and d.get('chapter_id')==ch['id']
  return []
 except(AssertionError,KeyError,TypeError,ValueError,OSError):return ['受信附傳選錄須保來源projection ref，不能刪除或改指降級']
def errors(ch,root,b):
 try:
  try:from scripts.fixed_biography_subsections import project
  except ImportError:from fixed_biography_subsections import project
  root=Path(root).resolve();p=pin(root,ch['id']);assert p is not None and not required_ref_error(ch,root)
  assert b['record_type']==KIND and b['chapter_id']==ch['id']and b['source_revision']==p['source_revision']and b['raw_sha256']==p['raw_sha256']and b['raw_file']==p['raw_file']
  rel=Path(p['raw_file']);assert not rel.is_absolute()and '..'not in rel.parts and rel.parts[0]in (('source-evidence','sources')if p.get('selection_mode')=='next_sibling_subsection'else ('source-evidence',))
  f=root/rel;assert f.resolve()==f and f.is_file();data=f.read_bytes();assert hashlib.sha256(data).hexdigest()==p['raw_sha256'];raw=data.decode('utf8');s=ch['source']
  assert ch['source_id']==p['source_id']and s['revision_id']==p['source_revision']and s['raw_file']==s['raw_path']==p['raw_file']and s['raw_file_sha256']==s['wikitext_sha256']==p['raw_sha256']
  a,z,ps,excluded=project(raw,ch['title'],p['opening_heading'],p['following_heading']if p.get('selection_mode')=='next_sibling_subsection'else None);assert (a,z)==(p['raw_start'],p['raw_end'])and raw[z:raw.index('\n',z)]==p['following_heading']
  assert b['selection']==dict(start=a,end=z,opening_heading=p['opening_heading'],following_heading=p['following_heading'],raw=raw[a:z])and b['excluded']==excluded
  assert ch['annotation']['preserved_source_headings']==[dict(raw_start=x['start'],raw_end=x['end']-1,raw_text=x['text'])for x in excluded if x['kind']=='editorial_heading']
  assert len(ps)==len(ch['paragraphs'])and len({x['id']for x in ch['paragraphs']})==len(ps)
  for x,w in zip(ch['paragraphs'],ps):
   assert x['text_layer']=='received_chapter'and x['text']==w['text']
   assert x['source_position']==dict(**{k:v for k,v in w.items()if k!='text'},revision_id=p['source_revision'],projection_sha256=hashlib.sha256((json.dumps(w['raw_character_offsets'],ensure_ascii=False,indent=2)+'\n').encode()).hexdigest(),source_layer='received_biography')
  return []
 except(AssertionError,KeyError,TypeError,ValueError,OSError,IndexError,StopIteration):return ['受信三級附傳選錄原版SHA、開閉題頭/字位、完整原字投影不符；不得共移或刪末段']
