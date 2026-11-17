"""Finite original-source allusions; no person-ID or ownership allowlist."""
from pathlib import Path
import json,hashlib,copy
KIND='fixed_yuanzhan_allusion_identifications';CID='c-epitaph-yuanzhan-nmh-full';TEXT_SHA='ff0421fb3960c1893f4789b06d9c7db2f544361cbc877ff1c3fe5741db6d1490';BASE='source-evidence/yuanzhan-allusion-identities'
D=lambda v:(json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode();H=lambda b:hashlib.sha256(b).hexdigest()
def config():return json.loads(Path(__file__).with_name('yuanzhan_allusion_identity_specs.json').read_text())
def augment(ch,base):
 cfg=config();p,=ch['paragraphs'];assert ch['id']==CID and H(p['text'].encode())==TEXT_SHA and p['text_layer']=='epitaph_as_modernly_transcribed'
 assert ch['annotation']['allusion_binding']==dict(kind=KIND,roles={r:x['mention_id']for r,x in cfg['roles'].items()})
 ms={m['id']:m for m in p['mentions']};r=copy.deepcopy(base);assert set(r)=={'grandfather','grandmother','mu_shou','mu_liang','father','mother','maternal_grandfather','head'}
 for role,x in cfg['roles'].items():
  m=ms[x['mention_id']];assert type(m['start'])is int and type(m['end'])is int and (m['start'],m['end'],m['surface'],m['kind'],m['status'])==(x['start'],x['end'],x['surface'],'person','contextual_provisional')and p['text'][m['start']:m['end']]==m['surface']
  assert m['reference_role']==('contemporaneous_sovereign'if role=='xiaojing'else'historical_allusion')and m['interpretation_note']==x['rationale']and isinstance(m['person_id'],str)and m['person_id'];r[role]=m['person_id']
 assert len(set(r.values()))==len(r)==15
 return r

def seed(root,spec,people):
 root=Path(root).resolve();rel=Path(spec['chapter_path']);assert not rel.is_absolute()and'..'not in rel.parts and rel.parts[0]=='corpus';path=root/rel;assert path.resolve()==path and path.is_file();c=json.loads(path.read_bytes())
 assert c['id']==spec['chapter_id']and all(c[k]==spec[k]for k in ('work_id','book_id','source_id'))
 source=c['source'];assert H(D(source))==spec['source_metadata_sha256']and all(type(source[k])is type(v)and source[k]==v for k,v in spec['source_fields'].items());assert source['provider']and source['url']and source['permalink']and source['revision_id']is not None
 raw=Path(spec['raw_path']);q=root/raw;assert not raw.is_absolute()and'..'not in raw.parts and q.resolve()==q and q.is_file()and H(q.read_bytes())==spec['raw_sha256']
 p,=[p for p in c['paragraphs']if p['id']==spec['paragraph_id']];assert H(p['text'].encode())==spec['paragraph_sha256'];m,=[m for m in p['mentions']if m['id']==spec['mention_id']]
 assert m['kind']=='person'and (m['start'],m['end'],m['surface'])==(spec['start'],spec['end'],spec['surface'])and p['text'][m['start']:m['end']]==m['surface']
 row=people[m['person_id']];assert any(m['id']in a.get('mention_ids',[])for a in row['aliases'])and any(e.get('mention_id')==m['id']and e['source_id']==c['source_id']and e['paragraph_id']==p['id']for e in row['evidence'])
 return m['person_id']

def context_errors(ch,root,r):
 try:
  cfg=config();root=Path(root).resolve();people={p['id']:p for p in json.loads((root/'registry/persons.json').read_bytes())['persons']}
  for role,spec in cfg['seed_specs'].items():assert seed(root,spec,people)==r[role]
  for row in cfg['primary_raw_pins'].values():
   p=root/row['path'];assert p.resolve()==p and p.is_file();raw=p.read_bytes();assert len(raw)==row['bytes']and H(raw)==row['sha256']and hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==row['git_blob']
  # Every current allusion endpoint has both forward and reverse source references.
  for role,x in cfg['roles'].items():
   row=people[r[role]];assert any(x['mention_id']in a.get('mention_ids',[])for a in row['aliases'])and any(e.get('mention_id')==x['mention_id']and e['chapter_id']==CID and e['source_id']==ch['source_id']for e in row['evidence'])
  return []
 except (AssertionError,KeyError,ValueError,TypeError,IndexError,StopIteration,AttributeError,OSError):return ['元湛七稱謂須保固定原典/來源角色與全部現役正反向引用；不得單端換人或靠人物號白名單']
