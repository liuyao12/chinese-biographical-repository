import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import test from 'node:test';
import assert from 'node:assert/strict';
const file=p=>readFileSync(new URL('../'+p,import.meta.url)),read=p=>JSON.parse(file(p)),digest=b=>createHash('sha256').update(b).digest('hex');
const proof=read('source-evidence/jin043-wangcheng-main/reading.json'),main=read('corpus/jinshu/043-wangcheng.json');
test('王澄子徽與王氏譜微同父同官，排行與同名者分存',()=>{
 const hv='rlk_lzd_86c_B',p=read('corpus/shishuoxinyu/002-jin043-wangcheng.json').paragraphs[0];assert.match(p.text,/祖父乂，平北將軍。父澄，荊州刺史。微歴尚書郎、右軍司馬/);
 assert.equal(p.mentions.find(m=>m.surface==='微').person_id,hv);
 assert.equal(main.paragraphs.at(-1).mentions.find(m=>m.surface==='徽').person_id,hv);
 const alt=read('corpus/shishuoxinyu/008-jin043-wangcheng.json').paragraphs.find(x=>x.id.endsWith(':yongjia'));assert.equal(alt.text,'澄弟四子微。');
 assert.equal(proof.child_identity.status,'editorial_provisional');assert.ok(proof.child_identity.excluded_person_ids.includes('d8d_ced_96e'));
 for(const row of proof.comparisons)for(const q of row.sources){const v=proof.witnesses[q.witness],b=file(v.raw_path);assert.equal(digest(b),v.raw_sha256);assert.equal(Array.from(b.toString()).slice(q.raw_start,q.raw_end).join(''),q.quote);}
 for (const page of proof.print_witness) {
  const source = new URL(page.source_url);
  assert.equal(source.origin, 'https://upload.wikimedia.org');
  assert.match(decodeURI(source.pathname), /第12冊\.pdf$/u);
  assert.equal(source.hash, '#page=' + page.pdf_page);
  assert.match(page.capture_sha256, /^[a-f0-9]{64}$/);
 }
});
test('王澄及詹卒例有不同原句；王沖所稱與澄的荊州任區別',()=>{
 assert.deepEqual(main.annotation.age_assertions.map(e=>e.value),[14,44]);
 const ev=read('corpus/jinshu/043-wangcheng-life-events.json').events;assert.ok(ev.some(e=>e.person_id==='rlk_lzd_86c_A'&&e.source_term==='早卒'));assert.ok(ev.some(e=>e.person_id==='rlk_lzd_86c'&&e.source_term.includes('路戎')));
 const ho=read('corpus/jinshu/043-wangcheng-titles.json').holdings.filter(x=>x.title==='荊州刺史');assert.ok(ho.some(h=>h.self_claimed_term==='自稱'));assert.ok(ho.some(h=>h.person_id==='rlk_lzd_86c'&&!h.self_claimed_term));
});
