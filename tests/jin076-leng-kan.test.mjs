import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
const f=p=>readFileSync(new URL('../'+p,import.meta.url));
const r=p=>JSON.parse(f(p));
const proof=r('source-evidence/jin076-wang-leng-kan/reading.json');
test('棱與稜分別按固定文字和殿本卷葉回讀',()=>{
 for(const s of proof.evidence){const b=f(s.raw_path);assert.equal(createHash('sha256').update(b).digest('hex'),s.raw_sha256);assert.equal(Array.from(b.toString('utf8')).slice(s.raw_start,s.raw_end).join(''),s.quote);}
 for(const s of proof.wuying)assert.equal(createHash('sha256').update(f(s.filename)).digest('hex'),s.sha256);
 for(const s of proof.parallel_paragraphs){const p=r(s.path).paragraphs.find(p=>p.id===s.paragraph_id);assert.equal(Array.from(p.text).slice(s.start,s.end).join(''),s.quote);}
});
test('季父的主體是彬，侃是棱弟，兩個從兄分別有本名',()=>{
 const a=r('corpus/jinshu/076-wangleng-assertions.json').assertions;
 const father=a.find(q=>q.id==='a-jinshu076-leng-father'),uncle=a.find(q=>q.id==='a-w076-bin-uncle-chen');
 assert.equal(uncle.object_person_id,father.object_person_id);assert.notEqual(uncle.subject_person_id,father.subject_person_id);
 assert.equal(a.find(q=>q.id==='a-jinshu076-kan-leng-brother').object_person_id,father.subject_person_id);
 assert.equal(new Set(a.filter(x=>x.predicate==='agnatic_cousin').map(x=>x.object_person_id)).size,2);
 const c=r('corpus/jinshu/076-wangleng.json');assert.equal(c.paragraphs.length,2);
 assert.equal(c.annotation.person_reference_occurrences.find(x=>x.surface==='之').person_id,father.subject_person_id);
});
