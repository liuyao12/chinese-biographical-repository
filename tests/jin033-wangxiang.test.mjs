import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
import test from 'node:test';
const file=p=>readFileSync(new URL('../'+p,import.meta.url)),read=p=>JSON.parse(file(p)),sha=b=>createHash('sha256').update(b).digest('hex');
const proof=read('source-evidence/jin033-wangxiang/reading.json'),chapter=read('corpus/jinshu/033.json'),id=proof.person_id;
test('王祥傳十一段、殿本四面與對讀各可按原位核驗',()=>{
 assert.equal(proof.source_scopes.length,11);
 for(const s of proof.source_scopes) {const p=chapter.paragraphs.find(p=>p.id===s.paragraph_id);assert.equal(p.annotation_status,'reviewed');assert.ok(p.text.startsWith(s.first)&&p.text.endsWith(s.last));}
 assert.deepEqual(proof.print_witness.map(fig=>fig.pdf_page),[39,40,41,42]);
 for(const fig of proof.print_witness){
  assert.match(fig.source_url,new RegExp(`^https://upload\\.wikimedia\\.org/.+%E7%AC%AC10%E5%86%8A\\.pdf#page=${fig.pdf_page}$`));
  assert.match(fig.capture_sha256,/^[0-9a-f]{64}$/);
 }
 for(const r of proof.comparisons) {const a=r.anchor,p=chapter.paragraphs.find(p=>p.id===a.paragraph_id);assert.equal(Array.from(p.text).slice(a.start,a.end).join(''),a.surface);for(const s of r.sources){const w=proof.witnesses[s.witness],b=file(w.raw_path);assert.equal(sha(b),w.raw_sha256);assert.equal(Array.from(b.toString()).slice(s.raw_start,s.raw_end).join(''),s.quote);}}
});
test('兩司馬、三件卒時原證及兩次報齡各有實際原生人物與時點',()=>{
 const sg=read('corpus/sanguozhi/018-jin033-wangxiang.json'),k=proof.library_role;
 assert.ok(chapter.paragraphs.flatMap(p=>p.mentions).some(m=>m.surface==='武帝'&&m.person_id===k.received_king));
 assert.ok(sg.paragraphs.flatMap(p=>p.mentions).some(m=>m.surface==='司馬文王'&&m.person_id===k.wang_yin_king));assert.notEqual(k.received_king,k.wang_yin_king);
 const original=chapter.annotation.age_assertions.find(a=>a.id==='age-w033-xiang-will');const role=chapter.annotation.person_reference_occurrences.find(r=>r.id===original.evidence[0].person_reference_id);
 assert.equal(role.person_id,id);assert.equal(role.surface,'吾');assert.equal(role.referent_role,'speaker_self');assert.equal(original.value,85);assert.equal(original.age_context.kind,'during_life');
 const closing=sg.annotation.age_assertions.find(a=>a.person_id===id);assert.equal(closing.value,89);assert.equal(closing.age_context.kind,'at_death');
 for(const [i,p]of ['jinshu/033','jinshu/003-jin033-wangxiang','sanguozhi/018-jin033-wangxiang'].entries()){const key=proof.conflicting_dates[i];const e=read('corpus/'+p+'-life-events.json').events.find(e=>e.id===key.life_event_id);assert.equal(e.person_id,id);assert.equal(e.date_expression,key.term);if(i===2)assert.equal(e.id,closing.age_context.life_event_id);}
 const q=proof.collateral_relative;assert.equal(q.source_term,'族孫');assert.equal(q.common_ancestor_id,null);const row=chapter.annotation.unresolved_identity_cases.find(r=>r.id===proof.han_candidates.case_id);assert.deepEqual(row.candidate_person_ids,proof.han_candidates.candidates);
});
