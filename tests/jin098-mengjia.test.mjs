import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
import test from 'node:test';
const file=p=>readFileSync(new URL('../'+p,import.meta.url)),read=p=>JSON.parse(file(p)),sha=b=>createHash('sha256').update(b).digest('hex');
const q=read('source-evidence/jin098-mengjia/reading.json');
test('孟嘉三段、吳國官稱三異文與各引文原字',()=>{
 for(const s of q.references){const w=q.witnesses[s.witness],b=file(w.raw_path);assert.equal(sha(b),w.raw_sha256);assert.equal(Array.from(b.toString()).slice(s.raw_start,s.raw_end).join(''),s.quote);}
 assert.deepEqual([...new Set(q.wu_offices.map(a=>a.term))].sort(),['司徒','司空','司馬'].sort());
 assert.deepEqual(q.origins.map(o=>o.name),['江夏鄳','江夏鄂']);assert.equal(q.three_paragraphs.length,3);
 const sg=read('corpus/sanguozhi/048-jin098-mengjia.json').paragraphs.find(p=>p.id.endsWith(':name'));assert.equal(sg.attribution.quoted_work,'吳錄');assert.equal(new Set(sg.mentions.map(m=>m.person_id)).size,1);
});
