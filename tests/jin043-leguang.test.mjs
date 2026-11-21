import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import test from 'node:test';
import assert from 'node:assert/strict';
const file=p=>readFileSync(new URL('../'+p,import.meta.url));
const read=p=>JSON.parse(file(p));
const digest=b=>createHash('sha256').update(b).digest('hex');
const proof=read('source-evidence/jin043-leguang-main/reading.json');
const main=read('corpus/jinshu/043-leguang.json');
const kids=['樂凱','樂肇','樂謨'];
test('樂廣十一段、三名子各自短傳和四幅書影皆可從來源復驗',()=>{
 const rows=read('data/corpus/six-dynasties-biographies.json').biographies.filter(x=>x.book_id==='b-jinshu-043');
 const src=proof.witnesses.j, raw=file(src.raw_path).toString(),points=Array.from(raw);
 assert.equal(main.paragraphs.length,11);
 for(const p of main.paragraphs){const s=p.source_position;assert.equal(points.slice(s.raw_start,s.raw_end).join('').trim(),p.text);assert.equal(p.annotation_status,'reviewed');}
 for(const title of ['樂廣',...kids])assert.equal(rows.find(x=>x.title===title).item_reviewed,true);
 for(const title of kids){const row=rows.find(x=>x.title===title),p=main.paragraphs.at(-1),cut=row.paragraph_slices[p.id];assert.equal(row.unit_kind,'embedded_account');assert.equal(Array.from(raw.split('\n')[159]).slice(row.start_codepoint,row.end_codepoint).join(''),Array.from(p.text).slice(cut.start,cut.end).join(''));}
 for(const fig of proof.print_witness)assert.equal(digest(file(fig.path)),fig.sha256);
});
test('樂廣各說保留各自原句、的確引用色層及既有楊氏三號',()=>{
 for(const item of proof.comparisons)for(const q of item.sources){const w=proof.witnesses[q.witness],b=file(w.raw_path);assert.equal(digest(b),w.raw_sha256);assert.equal(Array.from(b.toString()).slice(q.raw_start,q.raw_end).join(''),q.quote);}
 const p=read('corpus/shishuoxinyu/002-jin043-leguang.json').paragraphs;
 assert.match(p.find(x=>x.id.endsWith(':ending')).text,/無復疑慮/);assert.match(p.find(x=>x.attribution?.quoted_work==='晉陽秋').text,/猶疑之，遂以憂卒/);
 const dy=read('corpus/jinshu/004-jin043-leguang-life-events.json').events;assert.equal(dy[0].date_expression,'正月丙午');
 assert.ok(proof.comparisons.some(x=>x.sources.some(s=>s.witness==='kao'&&s.quote.includes('八月樂廣自裁'))));
 const a=read('corpus/jinshu/043-leguang-assertions.json').assertions;
 for(const son of ['0c1_b9d_9c2_AAAA','0c1_b9d_9c2_AAAB'])assert.ok(a.some(x=>x.subject_person_id===son&&x.object_person_id==='0c1_b9d_9c2_AAA'));
 const y=proof.yang_family,parallel=read('corpus/sanguozhi/019-yangxiu.json').paragraphs.find(x=>x.id===y.paragraph_id);assert.equal(y.quote,parallel.text);
});
test('成都王妃及衛玠妻按婚配原句分錄，武昌太守同名另列',()=>{
 const men=read('registry/persons.json').persons,c=proof.children_count.children_defined_by_marriage;
 assert.equal(new Set(c).size,2);for(const id of c)assert.equal(men.find(x=>x.id===id).family_path.parent_person_id,'591_360_8ca');
 const a=read('corpus/jinshu/036-jin043-leguang-assertions.json').assertions;assert.ok(a.some(x=>x.subject_person_id===c[1]&&x.object_person_id==='412_2d3_654'&&x.predicate==='spouse'));
 assert.ok(main.paragraphs.at(-2).mentions.some(m=>m.surface==='五男'&&m.kind==='unresolved'));
 assert.ok(proof.homonyms.some(h=>h.this_id!==h.other_id&&h.status==='unresolved_same_person'));
});
