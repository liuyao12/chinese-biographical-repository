import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const f=p=>readFileSync(new URL('../'+p,import.meta.url)),r=p=>JSON.parse(f(p));
const h=b=>createHash('sha256').update(b).digest('hex'), proof=r('source-evidence/jin076-wang-biaozhi/reading.json');
test('本紀、劉注及武英殿書影各據原字核年、官、建宮異載',()=>{
 for(const c of proof.comparisons)for(const q of c.sources){
  const s=proof.external_witnesses[q.witness],b=f(s.raw_path);assert.equal(h(b),s.raw_sha256);
  assert.equal(Array.from(b.toString()).slice(q.raw_start,q.raw_end).join(''),q.quote);
 }
 for(const w of proof.print_witness)assert.equal(h(f(w.path)),w.sha256);
 const ann=Array.from(f(proof.external_witnesses.ann.raw_path).toString());
 for(const a of proof.annals){for(const q of [a.year_anchor,a.date_and_event])assert.equal(ann.slice(q.raw_start,q.raw_end).join(''),q.quote);assert.ok(a.year_anchor.raw_end<a.date_and_event.raw_start);}
 assert.match(proof.annals[0].month.quote,/冬十月.*壬寅。散騎常侍、左光祿大夫、尚書令王彪之卒。/);
});
test('王彪之十八段，省官議、張陳兩姓、彪之與周家的兩組輩稱各有原據',()=>{
 const c=r('corpus/jinshu/076-wangbiaozhi.json'),a=r('corpus/jinshu/076-wangbiaozhi-assertions.json');
 assert.equal(c.paragraphs.length,18);assert.equal(c.annotation.embedded_writings.find(x=>x.genre==='議').scope,'quoted_text');
 const y=a.assertions.find(x=>x.id==='a-w076-jiao-qiu');assert.equal(y.subject_person_id,'rdl_pp9_ce4');
 assert.equal(a.assertions.find(x=>x.id==='a-w076-biaodao').object_person_id,'7r6_k52_qji_ABAA');
 assert.deepEqual(c.paragraphs.find(p=>p.id.endsWith('line071')).mentions.filter(m=>m.kind==='unresolved').map(m=>m.surface),['張','陳']);
});
