import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import test from 'node:test';
import assert from 'node:assert/strict';
const f=p=>readFileSync(new URL('../'+p,import.meta.url)),r=p=>JSON.parse(f(p));
const q=r('source-evidence/jin043-langye-sections/survey.json'),h=b=>createHash('sha256').update(b).digest('hex');
test('王戎題旁印有郭舒，固定轉錄保留自己的題記與郭舒別傳全文',()=>{
 assert.equal(h(f(q.raw_path)),q.sha256);
 for (const page of q.print_witness) {
  const source = new URL(page.source_url);
  assert.equal(source.origin, 'https://upload.wikimedia.org');
  assert.match(decodeURI(source.pathname), /第12冊\.pdf$/u);
  assert.equal(source.hash, '#page=' + page.pdf_page);
  assert.match(page.capture_sha256, /^[a-f0-9]{64}$/);
 }
 const n=q.heading_survey.find(x=>x.title==='郭舒'),p=r(n.chapter_path);assert.equal(p.paragraphs.length,5);assert.match(p.paragraphs[0].text,/郭舒，字稚行/);
 assert.match(p.paragraphs.at(-1).text,/表為梁州刺史。病卒。$/);
});
test('王萬、王玄在父傳各有可逐字重算的附傳邊界',()=>{
 const lines=f(q.raw_path).toString().split('\n');
 for(const t of ['王萬','王玄']){
  const a=q.heading_survey.find(x=>x.title===t), p=r(a.chapter_path).paragraphs.find(p=>p.id===a.paragraph_ids[0]), s=a.paragraph_slices[p.id];
  assert.equal(Array.from(lines[a.first_line-1]).slice(a.start_codepoint,a.end_codepoint).join(''),Array.from(p.text).slice(s.start,s.end).join(''));
 }
});
