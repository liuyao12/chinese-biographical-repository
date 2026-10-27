import assert from 'node:assert/strict';
import {test} from 'node:test';
import {readFileSync} from 'node:fs';
import {crossChapterTarget} from '../assets/cross-chapter-references.js';
const directory=JSON.parse(readFileSync(new URL('../data/corpus/chapter-directory.json',import.meta.url)));
const targets=[['w-jinshu','b-jinshu-075','c-jinshu-075-taiyuan-wang','line098'],['w-jinshu','b-jinshu-065','c-jinshu-065-wangdao-family','line084'],['w-jinshu','b-jinshu-065','c-jinshu-065-wangdao-family','p001'],['w-jinshu','b-jinshu-093','c-jinshu-093-chupou','line051'],['w-songshu','b-songshu-067','c-songshu-067-xielingyun','p008']].map(([work_id,book_id,chapter_id,p])=>({work_id,book_id,chapter_id,paragraph_id:chapter_id+':'+p,text_status:'imported'}));
test('five imported targets retain exact chapter and passage',()=>{for(const t of targets){const a=crossChapterTarget(t,directory);assert(a);const u=new URL(a.href,'https://example.test/');const q=new URLSearchParams(u.hash.slice(1));assert.equal(q.get('chapter'),t.chapter_id);assert.equal(q.get('passage'),t.paragraph_id);assert.equal(q.get('book'),t.book_id);}});
test('unimported Fan Hongzhi remains book placeholder',()=>{const a=crossChapterTarget({work_id:'w-jinshu',book_id:'b-jinshu-091',text_status:'not_imported',chapter_id:null},directory);assert(a);assert(!a.href.includes('chapter='));});
test('malformed imported target never silently falls back to book',()=>{for(const patch of [{chapter_id:'javascript:bad'},{paragraph_id:null},{paragraph_id:'c-other:p001'},{paragraph_id:'c-jinshu-075-taiyuan-wang:/bad'},{text_status:'not_imported'},{text_status:'unknown'}])assert.equal(crossChapterTarget({...targets[0],...patch},directory),null);});
