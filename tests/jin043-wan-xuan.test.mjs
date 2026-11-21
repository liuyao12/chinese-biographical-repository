import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import test from 'node:test';
import assert from 'node:assert/strict';
const f=p=>readFileSync(new URL('../'+p,import.meta.url)),r=p=>JSON.parse(f(p)),h=b=>createHash('sha256').update(b).digest('hex');
const e=r('source-evidence/jin043-wan-xuan/reading.json');
test('萬、綏、萬子與眉子的異文和親屬原話都按固定修訂回讀',()=>{
 for(const v of e.print_witness)assert.equal(h(f(v.path)),v.sha256);
 for(const row of e.comparisons)for(const q of row.sources){
  const v=e.external_witnesses[q.witness], b=f(v.raw_path);assert.equal(h(b),v.raw_sha256);
  assert.equal(Array.from(b.toString()).slice(q.raw_start,q.raw_end).join(''),q.quote);
 }
 assert.deepEqual(e.comparisons[0].sources.map(q=>q.quote.slice(0,5)),['戎子萬子，','王綏字萬子','戎子萬，有']);
 assert.match(e.comparisons[1].sources.at(-1).quote,/王夷甫喪子/);
});
test('王衍子玄與未名幼子分號，戎子綏的求婚止於原記欲取',()=>{
 const d=r('corpus/jinshu/043-wangyan-assertions.json').assertions.find(a=>a.id==='a-w043-xuan-yan-main');
 assert.equal(d.subject_person_id,'35b_mo3_adg');assert.equal(d.object_person_id,'b0c_13f_c3a');
 assert.ok(e.distinct_persons.some(x=>x.person_id===d.subject_person_id&&x.other_ids.includes('pw6_mer_j2p')));
 const s=r('corpus/shishuoxinyu/017-jin043-wan-assertions.json').assertions;
 assert.equal(s.some(x=>x.predicate==='spouse'),false);
});
