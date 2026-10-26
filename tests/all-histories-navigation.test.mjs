import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {volumeModel,volumeNavigation,volumeLanding} from '../assets/volume-directory.js';
import {groupWorks} from '../assets/corpus-discovery.js';
const directory=JSON.parse(fs.readFileSync(new URL('../data/corpus/chapter-directory.json',import.meta.url)));
const additions=['chenshu','beiqishu','zhoushu','suishu','jiutangshu','jiuwudaishi','xinwudaishi','songshi','liaoshi','jinshi','yuanshi','mingshi'];
test('all new volume parts are navigable but zero imported text',()=>{for(const slug of additions){const model=volumeModel(directory,'w-'+slug,{chapters:[]});assert(model);assert.equal(model.imported_count,0);assert(model.volume_count>0);const html=volumeNavigation(model);for(const book of model.books){assert(html.includes('book='+book.book_id));const l=volumeLanding(model,book.book_id);assert.equal(l.imported_count,0);assert(l.html.includes('正文尚未收錄'));assert(!l.html.includes('data-source-text'));assert(!l.html.includes('data/corpus/'+slug+'/'));}}});
test('later histories and medieval missing works keep distinct collection scope',()=>{const works=additions.map(s=>({id:'w-'+s}));const groups=groupWorks(works);assert.deepEqual(groups.find(g=>g.key==='medieval').works.map(w=>w.id),['w-chenshu','w-beiqishu','w-zhoushu']);assert(groups.find(g=>g.key==='later').works.every(w=>!['w-chenshu','w-beiqishu','w-zhoushu'].includes(w.id)));});
