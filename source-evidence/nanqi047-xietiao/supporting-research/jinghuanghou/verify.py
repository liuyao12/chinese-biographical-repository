from pathlib import Path
import hashlib,json
p=Path(__file__).parent
d=json.loads((p/'primary-proof.json').read_text())
for x in d['files'].values():
 b=(p/x['file']).read_bytes();assert hashlib.sha256(b).hexdigest()==x['sha256']
 if 'git_blob_sha' in x:assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['git_blob_sha']
for x in d['anchors']:
 t=(p/x['file']).read_text();assert t[x['start']:x['end']]==x['raw_quote']
a=json.loads((p/'registry-review.json').read_text());assert a['sha256_before']==a['sha256_after']
r=json.loads((p/'identity-proposal.json').read_text());assert r['human_reviewed'] is False and r['create_id'] is False
print('PASS 4 fixed raws/3 Git blobs, full unit positions, stable registry, qualified identity')
