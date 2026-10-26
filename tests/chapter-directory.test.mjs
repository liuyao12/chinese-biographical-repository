import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {chapterDirectoryMap} from '../assets/source-caption.js';
const read=async path=>JSON.parse(await readFile(new URL('../'+path,import.meta.url),'utf8'));
const directory=await read('data/corpus/chapter-directory.json');
const registry=await read('registry/works.json');
const manifest=await read('data/corpus/works.json');
test('every published work has a directory and every existing book keeps its ID',()=>{
 const map=chapterDirectoryMap(directory);
 assert.deepEqual(Object.keys(map).sort(),manifest.works.map(w=>w.id).sort());
 for(const work of registry.works.filter(w=>Object.hasOwn(map,w.id)))for(const book of work.books)assert.ok(Object.hasOwn(map[work.id].books,book.id),book.id);
});
test('complete numbered extents have no missing volumes',()=>{
 const extents={'w-shiji':130,'w-hanshu':100,'w-zizhitongjian':294,'w-zuozhuan-zhushu':60,'w-sanguozhi':65,'w-houhanshu':90,'w-jinshu':130,'w-songshu':100,'w-nanqishu':59,'w-nanshi':80,'w-weishu-weishou':114,'w-beishi':100,'w-liangshu':56,'w-xintangshu':225};
 for(const [id,max] of Object.entries(extents)){
  const work=directory.works.find(w=>w.work_id===id);
  const books=work.books.filter(b=>b.category!=='志'||id!=='w-houhanshu');
  assert.deepEqual([...new Set(books.map(b=>b.number))].sort((a,b)=>a-b),Array.from({length:max},(_,i)=>i+1),id);
 }
 assert.equal(directory.works.find(w=>w.work_id==='w-houhanshu').books.filter(b=>b.book_id.startsWith('b-houhanshu-zhi-')).length,30);
});
test('subvolumes follow reading order and preserve previously published Tang ID',()=>{
 for(const work of directory.works){
  for(const n of new Set(work.books.map(b=>b.number))){
   const parts=work.books.filter(b=>b.number===n&&b.part).map(b=>b.part);
   const ranks={上:1,中:2,下:3,之一:1,之二:2,之三:3,之四:4};
   assert.deepEqual(parts.map(p=>ranks[p]),parts.map(p=>ranks[p]).sort((a,b)=>a-b),work.work_id+' '+n);
  }
 }
 const parts=directory.works.find(w=>w.work_id==='w-xintangshu').books.filter(b=>b.number===71);
 assert.equal(parts.filter(b=>b.part==='下').length,1);
 assert.equal(parts.find(b=>b.part==='下').book_id,'b-xintangshu-071-xia');
});
test('directory metadata does not pretend to contain or verify source text',()=>{
 for(const work of directory.works){
  if(work.source?.url){assert.equal(work.source.role,'navigation_directory_only');assert.match(work.source.revision_url,/oldid=\d+$/);}
  for(const book of work.books){assert.equal(book.paragraphs,undefined);assert.equal(book.image_verified,undefined);assert.equal(book.path,undefined);}
 }
 const jin=directory.works.find(w=>w.work_id==='w-jinshu');
 assert.equal(jin.books.find(b=>b.number===79).citation_title,'謝尚 謝安');
 assert.ok(jin.books.find(b=>b.number===91).citation_title.startsWith('儒林'));
 assert.ok(directory.works.find(w=>w.work_id==='w-zuozhuan-zhushu').books.every(b=>b.citation_title===null));
});
