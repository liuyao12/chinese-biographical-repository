import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import test from 'node:test';
import assert from 'node:assert/strict';
const file=p=>readFileSync(new URL('../'+p,import.meta.url)),read=p=>JSON.parse(file(p)),digest=b=>createHash('sha256').update(b).digest('hex');
const proof=read('source-evidence/jin043-wangyan-main/reading.json');
const main=read('corpus/jinshu/043-wangyan.json');
test('王衍的兩個年齡、郭泰寧女與同卷齊王冏都有獨立來源',()=>{
 for(const row of proof.comparisons){const a=row.anchor,p=main.paragraphs.find(p=>p.id===a.paragraph_id);assert.equal(Array.from(p.text).slice(a.start,a.end).join(''),a.surface);
  for(const q of row.sources){const v=proof.witnesses[q.witness],b=file(v.raw_path);assert.equal(digest(b),v.raw_sha256);assert.equal(Array.from(b.toString()).slice(q.raw_start,q.raw_end).join(''),q.quote);}}
 for (const page of proof.print_witness) {
  const source = new URL(page.source_url);
  assert.equal(source.origin, 'https://upload.wikimedia.org');
  assert.match(decodeURI(source.pathname), /第12冊\.pdf$/u);
  assert.equal(source.hash, '#page=' + page.pdf_page);
  assert.match(page.capture_sha256, /^[a-f0-9]{64}$/);
 }
 const vr=proof.printed_variant;assert.equal(vr.printed,'齊王冏');assert.equal(vr.received,'齊王乂');assert.equal(vr.image.pdf_page,55);
 const local=main.annotation.age_assertions.find(a=>a.id==='age-w043-yan-young'),other=read('corpus/shishuoxinyu/007-jin043-wangyan.json').annotation.age_assertions[0];assert.equal(local.value,14);assert.equal(other.value,17);
 const rel=read('corpus/shishuoxinyu/010-jin043-wangyan-assertions.json').assertions.find(a=>a.predicate==='father');
 assert.equal(rel.subject_person_id,'4rl_6u1_b3j');assert.equal(rel.object_person_id,'28k_44w_ibb');
});
test('舊指代 ID 沿用，卷43「齊王乂」未歸入冏的別名',()=>{
 const mid='c-jinshu-043-wangyan:p006:m0063',r=main.annotation.person_reference_occurrences.find(r=>r.id===mid);
 assert.equal(r.surface,'之');assert.equal(r.person_id,'ee0_b2a_68e');
 const j=read('registry/persons.json').persons.find(p=>p.id===r.person_id);assert.equal(j.aliases.some(a=>a.mention_ids.includes(mid)||a.mention_ids.includes(proof.printed_variant.mention_id)),false);
 const d=read('corpus/jinshu/043-wangyan-identities.json').decisions.find(d=>d.id===proof.printed_variant.old_parallel_decision_id);assert.deepEqual(d.additional_print_collation,proof.printed_variant);
 const holds=read('corpus/jinshu/043-wangyan-titles.json').holdings;assert.equal(holds.some(h=>['武陵侯','遼東太守','元帥'].includes(h.title)),false);
});
