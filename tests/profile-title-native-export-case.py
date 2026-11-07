"""Actual native bundle -> production target profile, summary and directory.
The target is regenerated from native source. Unchanged current production
profiles and index supply its real family context in the temporary output tree.
"""
import contextlib,io,json,sys,tempfile,hashlib,shutil
from unittest.mock import patch
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(sys.argv[1]).resolve()
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'tests'))
from portable_fixture_copy import fixture_copy2
from scripts.person_bundle import load_catalog,bundle
from scripts.table_person_profiles import build
from scripts.person_directory import outputs
read=lambda p:json.loads(p.read_text())
d,=[d for d in read(ROOT/'corpus/songshu/063-wyd1739-wangtanshou-profile-title.json')['decisions']if d['id']=='ptp-song063-wyd-hong-taibao']
h,=[h for h in read(ROOT/'corpus/songshu/063-wyd1739-wangtanshou-titles.json')['holdings']if h['id']==d['holding_id']]
assert h['person_id']==d['person_id']and h['mode']=='attestation'and h['title']=='太保'
catalog=load_catalog(ROOT);people,records=catalog;b=bundle(d['person_id'],ROOT,include_provisional=True,catalog=catalog)
assert b['default_profile_title']['holding_id']==h['id']
assert next(v for v in b['title_holdings']if v['id']==h['id'])==h
assert not any(g['kind']!='paragraph'for row in b['source_mention_summary']for g in row['occurrence_groups']), 'selected person has table groups; include actual table transport'
works={w['id']:w for w in read(ROOT/'registry/works.json')['works']}
chapters={c['id']:c for c in records if c.get('record_type')=='marked_chapter'}
# Trace the actual source callback in a fresh proof scope, then transport every
# file it read byte-for-byte. This includes complete C51 source/sidecars/seeds,
# not a synthetic abbreviated chapter or a bypass of the production callback.
from scripts.wyd_song051_yixin import source_appellation_fragments
from scripts.validation_context import scope
source_dependencies=set()
original_open=Path.open
def tracked_open(path,*args,**kwargs):
 resolved=path.resolve()
 mode=args[0]if args else kwargs.get('mode','r')
 if 'r'in mode and resolved.is_relative_to(ROOT)and resolved.is_file():source_dependencies.add(resolved.relative_to(ROOT))
 return original_open(path,*args,**kwargs)
with patch.object(Path,'open',tracked_open),scope(ROOT):
 expected_fragments=source_appellation_fragments(ROOT,set(b.get('person_ids',[]))|{d['person_id']},people,records)
assert expected_fragments==b.get('source_appellation_fragments',[])
# load_catalog also consumes this native input despite its data/ location.
if(ROOT/'data/corpus/profile-names.json').is_file():source_dependencies.add(Path('data/corpus/profile-names.json'))
source_dependency_hashes={p.as_posix():hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in sorted(source_dependencies)}
# Bounded transport index from actual registered work/book/chapter dimensions.
# It is reader metadata only; the bundle above was validated against full native ROOT.
with tempfile.TemporaryDirectory(prefix='profile-title-native-export-')as td:
 r=Path(td)
 def write(path,value):
  p=r/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(value,ensure_ascii=False)+'\n')
 pid=d['person_id']
 for rel in sorted(source_dependencies):
  dest=r/rel;dest.parent.mkdir(parents=True,exist_ok=True)
  fixture_copy2(ROOT/rel,dest)
  assert hashlib.sha256(dest.read_bytes()).hexdigest()==source_dependency_hashes[rel.as_posix()]
 # Keep the real registered people; source roles/reverse evidence are validated.
 if not(r/'registry/persons.json').exists():
  (r/'registry').mkdir(parents=True,exist_ok=True)
  fixture_copy2(ROOT/'registry/persons.json',r/'registry/persons.json')
 write('exports/persons/index.json',{'persons':[{'person_id':pid}]});write('exports/persons/'+pid+'.json',b)
 write('data/historical-tables/person-candidates.json',{'persons':[]})
 write('data/corpus/index.json',{'work_id':'w-shiji','title':works['w-shiji']['title'],'chapters':[]})
 manifest=[]
 for wid in sorted({chapters[m['chapter_id']]['work_id']for m in b['mentions']}):
  work=works[wid];books={book['id']:book for book in work['books']};rows=[]
  for cid in sorted({m['chapter_id']for m in b['mentions']if chapters[m['chapter_id']]['work_id']==wid}):
   ch=chapters[cid];book=books[ch['book_id']];rows.append({'chapter_id':cid,'number':book['number'],'title':ch['title'],'category':book.get('category','')})
  path='data/corpus/integration-'+wid+'/index.json';write(path,{'chapters':rows});manifest.append({'id':wid,'title':work['title'],'reader_kind':'corpus','catalog_path':path})
 write('data/corpus/works.json',{'works':manifest})
 (r/'data/corpus/profiles').mkdir(parents=True,exist_ok=True)
 # Transport current production family context unchanged; regenerate the target
 # from the validated native bundle above. Summary export requires every
 # active family endpoint, so a one-profile transport is incomplete.
 for support in sorted((ROOT/'data/corpus/profiles').glob('*.json')):
  if support.name != pid+'.json':
   fixture_copy2(support,r/'data/corpus/profiles'/support.name)
 with contextlib.redirect_stdout(io.StringIO()):build(r,person_ids=[pid])
 profile=read(r/'data/corpus/profiles'/f'{pid}.json')
 directory=outputs(r);row=json.loads(directory[r/'data/corpus/person-directory.json'])['persons'][pid]
 assert profile['default_profile_title']==b['default_profile_title']
 assert row['default_profile_title']==profile['default_profile_title']
 assert next(v for v in row['titles']if v['id']==d['holding_id'])['attestations']
 print(json.dumps({'decision':d,'holding':h,'native_default_profile_title':b['default_profile_title'],'profile':profile,'directory':row,'temporary_production_transform':True,'source_dependency_hashes':source_dependency_hashes},ensure_ascii=False))
