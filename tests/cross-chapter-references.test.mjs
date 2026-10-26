import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {boundCrossChapterReferences,crossChapterReferences,crossChapterTarget} from '../assets/cross-chapter-references.js';
import {chapterParagraph} from '../assets/corpus-reader.js';
import {t} from '../assets/i18n.js';
const chapter=JSON.parse(fs.readFileSync(new URL('../corpus/jinshu/079.json',import.meta.url)));
const ref=chapter.cross_chapter_references[0], pid=ref.source.paragraph_id;
const directory={works:[{work_id:'w-jinshu',title:'晉書',books:[{book_id:'b-jinshu-091',number:91,title:'卷091',citation_title:'儒林',category:'列傳'}]}]};
const clone=x=>structuredClone(x);
test('exact 079 reference resolves registered placeholder volume, not invented chapter',()=>{
 const html=crossChapterReferences(chapter,pid,directory);
 assert.match(html,/reader.html#work=w-jinshu&amp;book=b-jinshu-091/);
 assert.match(html,/范弘之/);assert.match(html,/目標段正文尚未收錄/);assert.doesNotMatch(html,/chapter=/);
 assert.match(html,/《晉書・儒林》 · 卷091/);
});
test('unknown directory or unregistered book is explicit and unlinked',()=>{
 for(const d of [null,{works:[]},{works:[{work_id:'w-jinshu',title:'晉書',books:[]}]}]){
  const html=crossChapterReferences(chapter,pid,d);assert.match(html,/目標卷尚未登記/);assert.doesNotMatch(html,/<a /);
 }
});
test('wrong source work/book/chapter/source/revision and paragraph changes fail closed',()=>{
 for(const key of ['work_id','book_id','chapter_id','source_id','revision_id']){
  const c=clone(chapter);c.cross_chapter_references[0].source[key]='wrong';assert.throws(()=>boundCrossChapterReferences(c,pid));
 }
 const c=clone(chapter);c.paragraphs.find(p=>p.id===pid).text+='字';assert.throws(()=>boundCrossChapterReferences(c,pid));
});
test('wrong character range/surface is rejected',()=>{
 for(const change of [{start:104},{end:111},{surface:'別有傳'},{start:-1}]){
  const c=clone(chapter);Object.assign(c.cross_chapter_references[0].source,change);assert.throws(()=>boundCrossChapterReferences(c,pid));
 }
});
test('same chapter other paragraphs get no cross-reference',()=>{
 assert.equal(crossChapterReferences(chapter,chapter.paragraphs[0].id,directory),'');
});
test('absence of data does not scan common phrases or nearest people',()=>{
 const c=clone(chapter);delete c.cross_chapter_references;assert.equal(crossChapterReferences(c,pid,directory),'');
});
test('person markup and source p are unchanged; note sits after source p',()=>{
 const p=chapter.paragraphs.find(p=>p.id===pid),context={work_id:chapter.work_id,book_id:chapter.book_id,chapter_id:chapter.id};
 const old=chapterParagraph(p,{},context),html=chapterParagraph(p,{},context,{},crossChapterReferences(chapter,pid,directory));
 assert.ok(html.includes(old));assert.match(html,/m0107[^>]*class="cbr-person-link"/);
 assert.ok(html.indexOf('</p>')<html.indexOf('cross-chapter-references'));let depth=0;for(const tag of html.matchAll(/<\/?a(?:\s[^>]*)?>/g)){if(tag[0].startsWith('</'))depth--;else{assert.equal(depth,0);depth++;}}assert.equal(depth,0);
});
test('legal person rekey changes no source reference binding',()=>{
 const c=clone(chapter);for(const p of c.paragraphs)for(const m of p.mentions)if(m.person_id)m.person_id='new_mutable_id';
 assert.equal(crossChapterReferences(c,pid,directory),crossChapterReferences(chapter,pid,directory));
});
test('target URL injection/duplicate book registration rejected',()=>{
 assert.equal(crossChapterTarget({work_id:'javascript:alert(1)',book_id:'b-jinshu-091'},directory),null);
 const d=clone(directory);d.works[0].books.push(clone(d.works[0].books[0]));assert.equal(crossChapterTarget(ref.target,d),null);
});
test('labels follow i18n and do not translate source surface',()=>{
 assert.equal(t('Cross-reference',{},'en'),'Cross-reference');assert.equal(t('Cross-reference',{},'zh-Hant'),'互見');
 assert.equal(ref.source.surface,'語在弘之傳');
});
