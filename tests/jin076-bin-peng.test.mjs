import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const f=p=>readFileSync(new URL('../'+p,import.meta.url));
const r=p=>JSON.parse(f(p));
const proof=r('source-evidence/jin076-wang-bin-peng/reading.json');
test('彬與彭之據殿本、劉注引書、碑誌各核原字',()=>{
 const refs=proof.external_witnesses;
 for(const q of proof.comparisons.flatMap(x=>x.sources)){
  const w=refs[q.witness], b=f(w.raw_path);
  assert.equal(createHash('sha256').update(b).digest('hex'),w.raw_sha256);
  assert.equal(Array.from(b.toString()).slice(q.raw_start,q.raw_end).join(''),q.quote);
 }
 for(const q of proof.print_witness)assert.equal(createHash('sha256').update(f(q.path)).digest('hex'),q.sha256);
 const e=proof.comparisons.find(q=>q.collateral_epitaph).collateral_epitaph;
 const p=r(e.path).paragraphs.find(p=>p.id===e.paragraph_id);
 assert.equal(Array.from(p.text).slice(e.start,e.end).join(''),e.surface);
 assert.match(e.surface,/左僕射.*彬之孫/);
});
test('兄子籍之所指之叔、彭之第三弟各按來源保留方向與用詞',()=>{
 const a=r('corpus/jinshu/076-wangbin-assertions.json').assertions.find(x=>x.id==='a-w076-jizhi-bin');
 assert.equal(a.subject_person_id,'57l_v07_8z9');assert.equal(a.object_person_id,'7r6_k52_qji_ABDB');
 const b=r('corpus/shishuoxinyu/026-jin076-wangpeng-assertions.json').assertions.find(x=>x.id==='a-w076-biao-peng-pu');
 assert.equal(b.qualifiers.source_term,'彭之第三弟');assert.notEqual(b.subject_person_id,b.object_person_id);
 const p=r('corpus/shishuoxinyu/026-jin076-wangpeng.json').paragraphs;
 assert.equal(p[0].attribution.quoted_work,null);assert.equal(p[1].attribution.quoted_work,'王氏譜');
});
