import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
import test from 'node:test';
const file=p=>readFileSync(new URL('../'+p,import.meta.url)),read=p=>JSON.parse(file(p)),sha=b=>createHash('sha256').update(b).digest('hex');
const q=read('source-evidence/jin098-huan-four-children/reading.json'),ledger=read('data/corpus/six-dynasties-biographies.json').biographies,vol=b=>ledger.filter(r=>r.book_id===b);
test('桓氏四短傳逐一從清冊讀回，玄另有傳，禕存家傳評語',()=>{
 const four=['桓熙','桓濟','桓歆','桓偉'];assert.deepEqual(q.source_ranges.map(s=>s.title),four);
 for(const t of four)assert.equal(vol('b-jinshu-098').find(r=>r.title===t).item_reviewed,true);
 assert.equal(vol('b-jinshu-098').some(r=>r.title==='桓禕'||r.title==='桓玄'),false);assert.equal(vol('b-jinshu-098').find(r=>r.title==='桓溫').first_pass,true);
 for(const s of [...q.comparisons.map(c=>c.source),q.variant.transmitted,q.variant.later]){const w=q.witnesses[s.witness],b=file(w.raw_path);assert.equal(sha(b),w.raw_sha256);assert.equal(Array.from(b.toString()).slice(s.raw_start,s.raw_end).join(''),s.quote);}
});
test('偉生前官與二贈有別，桓欽原疑錨與桓歆對讀',()=>{
 const titles=read('corpus/jinshu/098-huanwen-titles.json').holdings,deaths=read('corpus/jinshu/099-jin098-huan-children-life-events.json').events;
 assert.equal(q.kin_link.grants.length,2);for(const tid of q.kin_link.grants){const h=titles.find(h=>h.id===tid);assert.equal(h.mode,'posthumous_grant');assert.ok(deaths.some(e=>e.id===h.posthumous_basis.death_event_id&&e.person_id===h.person_id));}
 const x=read('corpus/jinshu/074-huan-family.json').paragraphs.flatMap(p=>p.mentions).find(m=>m.id===q.variant.prior_mention_id);assert.equal(x.surface,'桓欽');assert.equal(x.kind,q.variant.prior_status);
});
