import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
const file = path => readFileSync(new URL('../'+path,import.meta.url));
const read=path=>JSON.parse(file(path));
const inv=read('data/corpus/six-dynasties-biographies.json');
const rows=inv.biographies.filter(x=>x.book_id==='b-jinshu-076');
const proof=read('source-evidence/jin076-wang-family/survey.json');
const raw=file(proof.raw_path);
const lines=raw.toString('utf8').split('\n');
test('卷七十六所有數位傳題、井然可分的無題短傳及固定原文',()=>{
  assert.equal(createHash('sha256').update(raw).digest('hex'),proof.sha256);
  for(const p of rows){
    if(p.heading_line) assert.equal(lines[p.heading_line-1],p.heading_raw);
    if(p.unit_kind==='embedded_account'){
      const q=Array.from(lines[p.first_line-1]).slice(p.start_codepoint,p.end_codepoint).join('');
      const c=read(p.chapter_path), para=c.paragraphs.find(x=>x.id===p.paragraph_ids[0]),s=p.paragraph_slices[para.id];
      assert.equal(q,Array.from(para.text).slice(s.start,s.end).join(''));
    }
  }
  assert.equal(new Set(rows.filter(p=>p.heading_line).map(p=>p.heading_line)).size,11);
  for(const x of proof.lineage_and_title_notices)assert.ok(lines[x.line-1].includes(x.raw_quote));
});
test('王廙中興賦疏五段與四個既有段號順接，舊姓名錨以原字回讀',()=>{
  const ps=read('corpus/jinshu/076.json').paragraphs;
  assert.deepEqual(ps.map(p=>p.source_position.first_line),[27,29,31,33,35,37,39,41,43]);
  assert.deepEqual(ps.filter(p=>/:p\d+$/.test(p.id)).map(p=>p.id.split(':')[1]),['p001','p002','p003','p004']);
  for(const p of ps)for(const m of p.mentions)assert.equal(Array.from(p.text).slice(m.start,m.end).join(''),m.surface);
  for(const page of proof.print_witness.pages)assert.equal(createHash('sha256').update(file(page.path)).digest('hex'),page.sha256);
});
