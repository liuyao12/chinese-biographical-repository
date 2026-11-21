import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import test from 'node:test';
import assert from 'node:assert/strict';
const file=p=>readFileSync(new URL('../'+p,import.meta.url)),read=p=>JSON.parse(file(p)),digest=b=>createHash('sha256').update(b).digest('hex');
const proof=read('source-evidence/jin043-guoshu-main/reading.json'),main=read('corpus/jinshu/043-guoshu.json');
test('郭舒本傳三葉及劉弘、周訪、左傳引用均可回讀',()=>{
 for (const page of proof.print_witness) {
  const source = new URL(page.source_url);
  assert.equal(source.origin, 'https://upload.wikimedia.org');
  assert.match(decodeURI(source.pathname), /第12冊\.pdf$/u);
  assert.equal(source.hash, '#page=' + page.pdf_page);
  assert.match(page.capture_sha256, /^[a-f0-9]{64}$/);
 }
 for(const row of proof.comparisons)for(const q of row.sources){
  const v=proof.witnesses[q.witness],b=file(v.raw_path);assert.equal(digest(b),v.raw_sha256);assert.equal(Array.from(b.toString()).slice(q.raw_start,q.raw_end).join(''),q.quote);}
 const relatives=read('corpus/jinshu/043-guoshu-assertions.json').assertions;assert.ok(relatives.some(a=>a.predicate==='mother'&&a.subject_person_id==='nyu_drp_roe'));
 assert.ok(proof.name_collations.some(v=>v.original==='宗庾廞'&&v.printed==='宗廞'));
});
test('郭舒不是王澄之親，兩寫王暠各指廙，未以暠作名',()=>{
 const chapter=main.paragraphs.at(-1);assert.deepEqual(chapter.mentions.filter(m=>proof.excluded_name_aliases.includes(m.id)).map(m=>[m.surface,m.person_id]),[['王暠','7r6_k52_qji_ABDA'],['暠','7r6_k52_qji_ABDA']]);
 const per=read('registry/persons.json').persons.find(p=>p.id==='7r6_k52_qji_ABDA');
 assert.equal(per.aliases.some(a=>a.mention_ids.some(m=>proof.excluded_name_aliases.includes(m))),false);
 const pub=read('corpus/jinshu/043-guoshu-titles.json').holdings;assert.equal(pub.some(h=>['右丞','梁州刺史'].includes(h.title)),false);
 assert.ok(main.paragraphs[0].mentions.some(m=>m.kind==='unresolved'&&m.surface==='司馬彪'));
});
