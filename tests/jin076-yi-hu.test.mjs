import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const f=p=>readFileSync(new URL('../'+p,import.meta.url));
const r=p=>JSON.parse(f(p)), h=b=>createHash('sha256').update(b).digest('hex');
const file='source-evidence/jin076-wang-yi/reading.json', e=r(file), c=r('corpus/jinshu/076.json');
test('中興賦佚文與上疏、四十三歲自陳的位置分開',()=>{
 const doc=c.annotation.embedded_writings;assert.equal(doc.find(w=>w.genre==='賦').scope,'reported_only');
 assert.equal(doc.find(w=>w.genre==='上疏').scope,'quoted_text');
 const s=e.source_age, ref=c.annotation.person_reference_occurrences.find(v=>v.id===s.reference_id);
 assert.equal(ref.person_id,s.person_id);assert.equal(ref.surface,'臣');assert.equal(s.value,43);
 const p=c.paragraphs.find(p=>p.id===s.paragraph_id);
 assert.equal(Array.from(p.text).slice(s.start,s.end).join(''),s.surface);
 assert.equal(p.text.includes('卒'),false);
});
test('胡之、耆之、和之各據其書的子名與原字，敬弘曾祖有廣／廙異文',()=>{
 for(const x of e.comparisons)for(const q of x.sources){
  const w=e.external_witnesses[q.witness],b=f(w.raw_path);
  assert.equal(h(b),w.raw_sha256);assert.equal(Array.from(b.toString()).slice(q.raw_start,q.raw_end).join(''),q.quote);
 }
 assert.equal(h(f(e.nanshi024_print.path)),e.nanshi024_print.sha256);
 assert.match(e.nanshi024_print.reading,/廣之曾孫/);assert.match(e.song066.surface,/曾祖廙/);
 const s=e.song066,p=r(s.path).paragraphs.find(p=>p.id===s.paragraph_id);
 assert.equal(Array.from(p.text).slice(s.start,s.end).join(''),s.surface);
 for(const v of e.print_witness)assert.equal(h(f(v.path)),v.sha256);
});
