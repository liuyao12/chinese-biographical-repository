import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const f=p=>readFileSync(new URL('../'+p,import.meta.url));
const r=p=>JSON.parse(f(p));
const base='corpus/jinshu/076-wangshu-family', c=r(base+'.json');
const proof=r('source-evidence/jin076-wang-shu-yun/reading.json');
const digest=b=>createHash('sha256').update(b).digest('hex');
test('本紀用所屬年目回讀卒日，傳末三代各按父子次序',()=>{
 for(const a of proof.annal_dates){
  const raw=Array.from(f(proof.external_witnesses.ann.raw_path).toString());
  for(const q of [a.heading,a.passage])assert.equal(raw.slice(q.raw_start,q.raw_end).join(''),q.quote);
  assert.ok(a.heading.raw_end < a.passage.raw_start);
 }
 const as=r(base+'-assertions.json').assertions;
 for(const [a,b] of [['xi-yun','zhao-xi'],['kun-yan','lou-kun']]){
  const first=as.find(x=>x.id==='a-w076-'+a),second=as.find(x=>x.id==='a-w076-'+b);
  assert.equal(first.subject_person_id,second.object_person_id);
 }
 assert.equal(c.paragraphs[2].text.includes('吳王師虞𩦎'),true);
 assert.equal(c.paragraphs[1].mentions.filter(m=>m.kind==='unresolved'&&['裒','褚裒'].includes(m.surface)).length,4);
 assert.equal(c.paragraphs[2].mentions.filter(m=>m.kind==='person'&&m.surface==='敦').length,0);
});
test('四庫本所傳婚書、御覽所引晉中興書及殿本各守原字',()=>{
 const sources=proof.external_witnesses;
 for(const x of proof.comparisons){
  const p=c.paragraphs.find(p=>p.id===x.anchor.paragraph_id),a=x.anchor;
  assert.equal(Array.from(p.text).slice(a.start,a.end).join(''),a.surface);
  for(const q of x.sources){const w=sources[q.witness],raw=f(w.raw_path);
   assert.equal(digest(raw),w.raw_sha256);assert.equal(Array.from(raw.toString()).slice(q.raw_start,q.raw_end).join(''),q.quote);}
 }
 for(const q of proof.print_witness)assert.equal(digest(f(q.path)),q.sha256);
 const y=proof.comparisons.find(q=>q.anchor.surface==='允之字深猷');
 assert.ok(y.sources.slice(0,2).every(s=>s.quote.includes('淵猷')));
});
