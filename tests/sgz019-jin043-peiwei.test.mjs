import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import test from 'node:test';
import assert from 'node:assert/strict';
const file=p=>readFileSync(new URL('../'+p,import.meta.url)),read=p=>JSON.parse(file(p)),hash=b=>createHash('sha256').update(b).digest('hex');
const q=read('source-evidence/sgz019-jin043-peiwei/review.json'),person=q.canonical_person_id;
test('兩本裴注與樂廣傳、嵇紹傳、裴頠本傳各自核回完整原字',()=>{
 for(const w of Object.values(q.witnesses)){const raw=file(w.path);assert.equal(hash(raw),w.sha256);assert.equal(Array.from(raw.toString()).slice(w.quote.raw_start,w.quote.raw_end).join(''),w.quote.quote);}
 assert.ok(q.witnesses.sgz.quote.quote.includes('裘頠'));assert.ok(q.witnesses.sgz2.quote.quote.includes('裴頠'));assert.equal(hash(file(q.print_witness.path)),q.print_witness.sha256);
 for(const src of q.native_sources){const p=read(src.path).paragraphs.find(x=>x.id===src.paragraph_id);assert.equal(p.text,src.quote);for(const x of src.mentions){const m=p.mentions.find(m=>m.id===x.id);assert.equal(m.surface,x.surface);assert.equal(m.person_id,person);}}
 const per=read('registry/persons.json').persons.find(x=>x.id===person);assert.equal(per.aliases.some(a=>a.surface==='裘頠'),false);assert.equal(per.evidence.some(e=>e.mention_id.endsWith('p006:m0098')),true);
});
test('原始楊氏匯入樣本及固定讀本仍有原指紋，代詞候選及兩份可更新的來源包讀到本次人號',()=>{
 for(const row of q.immutable_captures){assert.equal(hash(file(row.path)),row.sha256);for(const e of row.current_endpoints)assert.equal(e.person_id,person);}
 const p=read('corpus/sanguozhi/019-yangxiu.json').paragraphs.find(p=>p.id.endsWith(':p006')),m=p.mentions.find(x=>x.id.endsWith(':m0106'));assert.equal(m.kind,'unresolved');assert.deepEqual(m.candidate_person_ids,[person,'591_360_8ca']);
 const joined=read('source-evidence/jin043-wangrong-source/identity-review.json').find(x=>x.key==='wei');assert.deepEqual(joined.same_surface_candidates,[]);assert.equal(joined.followup_interpretation.decision_id,q.decision_id);
});
