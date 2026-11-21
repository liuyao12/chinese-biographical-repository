import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import test from 'node:test';
import assert from 'node:assert/strict';
const f=p=>readFileSync(new URL('../'+p,import.meta.url)),r=p=>JSON.parse(f(p)),sha=b=>createHash('sha256').update(b).digest('hex');
const e=r('source-evidence/jin039-043-wangyi/review.json');
test('二荀問答與郭舒受譖各有本卷直接書影，同人保留四個原字舊錨',()=>{
 const files=['corpus/jinshu/039.json','corpus/jinshu/043-guoshu.json'];
 const people=r('registry/persons.json').persons,target=people.find(p=>p.id===e.canonical_person_id);
 const rec=r('source-evidence/jin039-043-wangyi/annotation-chain.json');assert.equal(rec.identity_decision_id,e.decision_id);
 assert.equal(people.some(p=>rec.retired_person_ids.includes(p.id)),false);
 const decision=r('corpus/jinshu/039-identities.json').decisions.find(d=>d.id===e.decision_id);
 assert.equal(decision.person_id,e.canonical_person_id);
 e.collations.forEach((x,i)=>{
   const b=f(x.digital_quote.raw_path),q=x.digital_quote,printed=x.printed;assert.equal(sha(b),q.raw_sha256);assert.equal(Array.from(b.toString()).slice(q.raw_start,q.raw_end).join(''),q.quote);
   assert.equal(sha(f(printed.path)),printed.sha256);assert.match(printed.transcription,/王廙/);assert.match(q.quote,/王暠/);
   const p=r(files[i]).paragraphs.find(p=>p.id===x.paragraph_id);
   for(const a of x.received_name_mentions){const m=p.mentions.find(m=>m.id===a.mention_id);assert.equal(m.surface,a.surface);assert.equal(m.person_id,target.id);
     assert.ok(target.evidence.some(ev=>ev.mention_id===m.id));assert.equal(target.aliases.some(alias=>alias.mention_ids.includes(m.id)),false);}
 });
 const bucket=r('source-evidence/jin059-jiong-yi-source/identity-reading-notes.json').additional_complete_paragraphs.find(o=>o.paragraph.id===e.collations[0].paragraph_id);
 assert.equal(bucket.current_identity_projection.canonical_person_id,target.id);assert.ok(bucket.paragraph.mentions.filter(m=>bucket.current_identity_projection.mention_ids.includes(m.id)).every(m=>m.person_id===target.id));
});
