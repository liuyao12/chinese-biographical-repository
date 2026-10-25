import json,hashlib
from pathlib import Path
p=Path(__file__).parent
a=json.loads((p/'source-context.json').read_text());b=(p/a['raw_file']).read_bytes();assert hashlib.sha256(b).hexdigest()==a['sha256'];t=b.decode()
for k in ['context','target']:
 x=a[k];assert t[x['start']:x['end']]==x.get('raw_quote',x.get('surface'))
a=json.loads((p/'shiji-capture.json').read_text());assert a['hashes_before']==a['hashes_after'];q=a['paragraph'];m=next(x for x in q['mentions'] if x['surface']=='少正卯');assert q['text'][m['start']:m['end']]=='少正卯';assert m['person_id']==a['person']['id'];assert any(x.get('mention_id')==m['id'] for x in a['person']['evidence'])
r=json.loads((p/'identity-proposal.json').read_text());assert r['person_id']==m['person_id'] and r['create_id'] is False
print('PASS raw spans, stable capture, source MID and reverse evidence')
