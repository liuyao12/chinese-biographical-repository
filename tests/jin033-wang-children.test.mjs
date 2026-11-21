import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import test from 'node:test';
import assert from 'node:assert/strict';
const file=p=>readFileSync(new URL('../'+p,import.meta.url)),read=p=>JSON.parse(file(p)),sha=b=>createHash('sha256').update(b).digest('hex');
const q=read('source-evidence/jin033-wang-family-children/reading.json'),chapter=read('corpus/jinshu/033.json'),rows=read('data/corpus/six-dynasties-biographies.json').biographies.filter(b=>b.book_id==='b-jinshu-033');
test('王祥、覽十二篇子孫短傳復驗各自原字與既有姓名錨',()=>{
 for(const unit of q.reviewed_source_units){const p=chapter.paragraphs.find(p=>p.id===unit.paragraph_id);assert.deepEqual(unit.slices.map(s=>Array.from(p.text).slice(s.start,s.end).join('')),unit.quotes);const row=rows.find(r=>r.title===unit.title);assert.equal(row.item_reviewed,true);}
 assert.equal(q.reviewed_source_units.length,12);const z=rows.find(r=>r.title==='王肇');assert.equal(z.continuation_spans.length,1);assert.equal(rows.some(r=>r.title==='王夏'),false);
 for(const s of q.print_witness)assert.equal(sha(file(s.path)),s.sha256);
});
test('王裁、基、會分別對讀王導、敦、舒傳，兩本官名差異得保留',()=>{
 for(const r of q.branch_links){const e=r.comparandum,w=q.witnesses[e.witness],b=file(w.raw_path);assert.equal(sha(b),w.raw_sha256);assert.equal(Array.from(b.toString()).slice(e.raw_start,e.raw_end).join(''),e.quote);}
 const a=read('corpus/jinshu/098-jin033-wangji-assertions.json').assertions[0];assert.equal(a.object_person_id,'7r6_k52_qji_ABB');assert.equal(a.predicate,'father');
 const jobs=read('corpus/jinshu/033-titles.json').holdings;assert.ok(jobs.some(x=>x.person_id==='7r6_k52_qji_AAA'&&x.title==='始平太守'));
 const deaths=read('corpus/jinshu/033-life-events.json').events.filter(e=>e.source_term==='二子亦同時而亡');assert.deepEqual(deaths.map(x=>x.person_id),['7r6_k52_qji_AAD','7r6_k52_qji_AAE']);
});
