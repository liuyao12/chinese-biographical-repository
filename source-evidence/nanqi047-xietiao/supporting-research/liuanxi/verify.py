from pathlib import Path
import hashlib,json
p=Path(__file__).parent
d=json.loads((p/'context.json').read_text());b=(p/d['source']['raw_file']).read_bytes();assert hashlib.sha256(b).hexdigest()==d['source']['sha256'];t=b.decode()
for k in ('full_context','target'):
 x=d[k];assert t[x['start']:x['end']]==x.get('raw_quote',x.get('surface'))
r=json.loads((p/'registry-capture.json').read_text());assert r['sha256_before']==r['sha256_after'];assert r['exact_liuanxi_label_or_alias_matches']==[]
a=json.loads((p/'decision.json').read_text());assert a['status']=='unresolved' and a['preferred_person_id'] is None and a['create_person_id'] is False
print('PASS fixed raw/context/target, stable registry capture, unresolved qualification')
