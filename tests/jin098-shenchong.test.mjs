import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
import test from 'node:test';
const file=p=>readFileSync(new URL('../'+p,import.meta.url)),read=p=>JSON.parse(file(p)),sha=b=>createHash('sha256').update(b).digest('hex');
const q=read('source-evidence/jin098-shenchong/reading.json'),main=read('corpus/jinshu/098-shenchong.json');
test('沈充、錢鳳、熊甫原文及本紀、忠義傳各有定位',()=>{
 const titles=q.units.map(u=>u.title);assert.deepEqual(titles,['沈充','錢鳳','熊甫']); const ledger=read('data/corpus/six-dynasties-biographies.json').biographies;for(const title of titles)assert.equal(ledger.find(r=>r.book_id==='b-jinshu-098'&&r.title===title).item_reviewed,true);
 for(const r of q.external_clauses){const w=q.witnesses[r.witness],b=file(w.raw_path);assert.equal(sha(b),w.raw_sha256);assert.equal(Array.from(b.toString()).slice(r.raw_start,r.raw_end).join(''),r.quote);}
 const holdings=read('corpus/jinshu/098-shenchong-titles.json').holdings;assert.equal(holdings.some(x=>x.title==='司空'),false);assert.ok(q.comparisons.some(x=>x.office==='司空'&&x.actual_office===false&&x.decision.surface==='充不納'));
 assert.ok(q.comparisons.find(x=>x.kind==='歌').quote.startsWith('徂風飆起'));assert.ok(main.paragraphs.every(p=>p.annotation_status==='reviewed'));
});
test('父充與子勁雙傳交叉，周光殺鳳、吳儒殺充明分',()=>{
 const a=read('corpus/jinshu/098-shenchong-assertions.json').assertions[0],b=read('corpus/jinshu/089-jin098-shenchong-assertions.json').assertions[0];
 assert.deepEqual([a.subject_person_id,a.object_person_id],[b.subject_person_id,b.object_person_id]);assert.equal(a.predicate,'father');assert.equal(b.predicate,'father');
 const d=read('corpus/jinshu/098-jin033-wangji-life-events.json').events;for(const v of q.victims)assert.equal(d.find(e=>e.id===v.source_event).person_id,v.person_id);
 assert.equal(new Set(q.victims.map(v=>v.killer_person_id)).size,2);
});
