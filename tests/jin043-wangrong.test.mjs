import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import test from 'node:test';
import assert from 'node:assert/strict';
const file=p=>readFileSync(new URL('../'+p,import.meta.url)),read=p=>JSON.parse(file(p)),digest=b=>createHash('sha256').update(b).digest('hex');
const proof=read('source-evidence/jin043-wangrong-main/reading.json'),main=read('corpus/jinshu/043-wangrong.json');
test('王戎觀虎約齡、與阮籍年差、長女及妻的原證各自成立',()=>{
 const ag=main.annotation.age_assertions.find(a=>a.source_term==='年六七歲');assert.deepEqual(ag.approximation.numbers,[6,7]);assert.equal(ag.value,null);assert.equal(ag.bounds,undefined);
 const diff=main.annotation.age_difference_assertions.find(a=>a.source_term==='少籍二十歲');assert.equal(diff.reference_person_id,'6d5_075_29b');assert.equal(diff.value,20);
 for(const row of proof.comparisons){const a=row.anchor,p=main.paragraphs.find(p=>p.id===a.paragraph_id);assert.equal(Array.from(p.text).slice(a.start,a.end).join(''),a.surface);
  for(const q of row.sources){const v=proof.witnesses[q.witness],b=file(v.raw_path);assert.equal(digest(b),v.raw_sha256);assert.equal(Array.from(b.toString()).slice(q.raw_start,q.raw_end).join(''),q.quote);}}
 for (const page of proof.print_witness) {
  const source = new URL(page.source_url);
  assert.equal(source.origin, 'https://upload.wikimedia.org');
  assert.match(decodeURI(source.pathname), /第12冊\.pdf$/u);
  assert.equal(source.hash, '#page=' + page.pdf_page);
  assert.match(page.capture_sha256, /^[a-f0-9]{64}$/);
 }
 assert.equal(proof.kinship_source_terms[1].term,'長女');assert.equal(proof.kinship_source_terms[1].person_id,'cxf_421_onp');
 const wife=read('corpus/shishuoxinyu/035-jin043-wangrong-assertions.json').assertions[0];assert.equal(wife.predicate,'spouse');assert.equal(wife.subject_person_id,'c46_7o5_azx');
 const note=read('corpus/shishuoxinyu/017-jin043-wangrong.json').paragraphs.find(p=>p.id.endsWith(':zhulin'));assert.match(note.text,/中朝所不聞/);
});
test('殿本孫秀錄戎與數位孫秀祿戎位於同句',()=>{
 const a=proof.selected_collations.find(x=>x.printed==='孫秀錄戎於城内');assert.equal(a.anchor.surface,'孫秀祿戎於城內');assert.equal(a.pdf_page,51);
 assert.equal(main.annotation.person_reference_occurrences.some(r=>r.id==='c-jinshu-043-wangrong:p010:m0058'&&r.surface==='少年'),true);
});
