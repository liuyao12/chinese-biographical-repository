"""Received catalogue/Pei-quotation authority, not original-edition or date inference."""
from pathlib import Path,PurePosixPath
import hashlib,json,re
PATH='source-evidence/pei-work-authorities/authorities.json'
def file(root,path):
 p=PurePosixPath(path)if isinstance(path,str)else None
 assert p and not p.is_absolute()and '..'not in p.parts and p.parts[:2]==('source-evidence','pei-work-authorities'),'authority path'
 f=Path(root)/path
 assert not f.is_symlink()and f.resolve()==Path(root).resolve()/path,'authority symlink'
 return f.read_bytes()
def text(raw):
 s=re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]',r'\2',raw)
 s=re.sub(r'\[\[([^\]]+)\]\]',r'\1',s)
 return re.sub(r'</?p>','',s)
def number(s):
 z='一二三四五六七八九'
 if s in z:return z.index(s)+1
 if re.fullmatch('[一二三四五六七八九]?十[一二三四五六七八九]?',s):
  a,b=s.split('十');return(z.index(a)+1 if a else 1)*10+(z.index(b)+1 if b else 0)
 return None
def note_containing(raw,position):
 # Bracket templates nest; nearest unrelated prose in the same line is not enough.
 stack=[];spans=[]
 for m in re.finditer(r'\{\{|\}\}',raw):
  if m.group()=='{{':stack.append(m.start())
  elif stack:
   start=stack.pop()
   if raw.startswith('{{*|',start)and start<=position<m.end():spans.append((start,m.end()))
 assert spans,'author bridge must be in an actual Pei note template'
 a,b=min(spans,key=lambda pair:pair[1]-pair[0]);return raw[a:b]
def validate(data,root):
 works=json.loads((Path(root)/'registry/works.json').read_text())['works'];linked=[w for w in works if w.get('bibliographic_authority_id','').startswith('authority-pei-')]
 if not(Path(root)/PATH).exists():
  assert not linked,'missing authority proof set';return
 p=json.loads(file(root,PATH));assert p['schema_version']==1 and p['record_type']=='pei_cited_work_bibliographic_authorities'and p['human_reviewed']is False
 archives={a['raw_path']:a for a in p['archives']};assert len(archives)==len(p['archives'])
 for a in archives.values():
  raw=file(root,a['raw_path']);meta=json.loads(file(root,a['metadata_path']));assert hashlib.sha256(raw).hexdigest()==a['raw_sha256']==meta['raw_sha256']and a['revision_id']==meta['revision_id']and a['url']==meta['url']and a['title']==meta['title']and meta['image_verified']is False,'fixed archive inventory mismatch'
 ev={x['id']:x for x in p['evidence']};assert len(ev)==len(p['evidence']);raws={}
 for eid,e in ev.items():
  archive=archives[e['raw_path']];assert all(e[k]==archive[k]for k in ('raw_path','metadata_path','raw_sha256','revision_id','url','title')),'evidence archive must resolve'
  raw=file(root,e['raw_path']);meta=json.loads(file(root,e['metadata_path']));digest=hashlib.sha256(raw).hexdigest();s=raw.decode('utf-8');a,b=e['raw_start'],e['raw_end']
  assert e['raw_sha256']==meta['raw_sha256']==digest and e['revision_id']==meta['revision_id']and e['url']==meta['url']and e['title']==meta['title'],'fixed revision/raw metadata mismatch'
  assert type(a)is int and type(b)is int and 0<=a<b<=len(s)and s[a:b]==e['exact_raw_quote'],'exact bibliographic proof span'
  assert e['image_verified']is False and meta['image_verified']is False and e['read_scope'],'no image claim / reading scope'
  ref=data['references']['ref-pei-authority-'+eid]
  assert ref['url']==e['url']and ref['archived_authority']=={'path':PATH,'evidence_id':eid},'unresolved authority reference'
  raws[eid]=s
 authorities={a['id']:a for a in p['authorities']};assert len(authorities)==len(p['authorities'])and {w['bibliographic_authority_id']for w in linked}==set(authorities),'unreferenced or missing authority'
 for aid,a in authorities.items():
  row=next(w for w in works if w['id']==a['work_id']);side=data['works'][row['id']]
  assert row['bibliographic_authority_id']==side['bibliographic_authority_id']==aid
  assert row['citation_title']==side['citation_title']==a['citation_title']and row['author']==side['author']==a['author']and row['citation_qualification']==side['citation_qualification']==a['citation_qualification']
  assert a['catalogue_attestations'][0]['title_as_received']==a['citation_title']and a['citation_qualification']
  for c in a['catalogue_attestations']:
   q=text(ev[c['evidence_id']]['exact_raw_quote']);title=c['title_as_received'];n=c['source_number'];author=a['author'];assert type(c['volumes'])is int and number(n)==c['volumes']
   if c['format']=='author_title_extent':expected=author+title+n+'卷'
   elif c['format']in('title_extent_author','title_extent_office_author'):expected='《'+title+'》'+n+'卷'+c.get('author_qualification','')+author+'撰。'
   else:raise AssertionError('unrecognized catalogue syntax')
   assert q==expected,'catalogue must actually name this title, extent and author'
  b=a['internal_author_bridge'];e=ev[b['evidence_id']];note=text(note_containing(raws[e['id']],e['raw_start']))
  if b['rule']=='same_pei_note_title_then_named_author_then_title_criticism':
   assert note.startswith('{{*|《'+a['citation_title']+'》曰：')and '而'+a['author']+'-{云}-'in note and '此則《'+a['citation_title']+'》之妄說'in note,'Pei title/author bridge'
  elif b['rule']=='pei_explicit_author_abbreviated_title':
   assert '及'+a['author']+'《'+b['abbreviated_title']+'》並云'in note and b['abbreviated_title']in a['citation_title'],'Pei explicit author/short title bridge'
  else:raise AssertionError('unknown authority bridge')
  assert side['composition']['status']=='unknown'and side['composition']['assertions']==[]and side['composition']['note']==a['composition_note'],'authorship is not a numeric completion date'
  assert side['earliest_extant_edition']['status']=='unknown'and side['earliest_extant_edition']['assertions']==[],'no earliest original/base edition established'
  modern=a['composition_reference_id']
  if modern is not None:
   ref=data['references'][modern];assert any(m['url']==ref['url']and m['exact_short_quote']==ref['quote']for m in p['modern_references']),'modern reference must resolve'
 return True
