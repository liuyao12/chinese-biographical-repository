import test from 'node:test';import assert from 'node:assert/strict';
import {canonicalProfiles,searchPeople,groupWorks,workURL} from '../assets/corpus-discovery.js';
test('canonical registry, not legacy index aliases, determines distinct people',()=>{
 const people={one:{id:'one',label:'謝安',aliases:['安石']},two:{id:'two',label:'謝玄',aliases:['幼度']}};
 const index={profiles:[{id:'one',label:'謝安',names:['謝安','安']},{id:'old-alias',label:'謝安',names:['安石']},{id:'two',label:'謝玄',names:[]}]};
 const result=canonicalProfiles(people,index);assert.equal(result.length,2);assert.deepEqual(new Set(result.map(p=>p.id)),new Set(['one','two']));assert.ok(result.find(p=>p.id==='one').names.includes('安石'));
});
test('name variants, partial names and structural IDs are searched without rewriting source forms',()=>{
 const people=[{id:'abc_def_123_A',label:'謝安',names:['謝安','安石']},{id:'other',label:'王安',names:['王安']},{id:'third',label:'謝玄',names:['謝玄','幼度']}];
 assert.equal(searchPeople(people,'安石')[0].id,'abc_def_123_A');assert.equal(searchPeople(people,'幼')[0].id,'third');assert.equal(searchPeople(people,'DEF_123')[0].id,'abc_def_123_A');assert.equal(searchPeople(people,'謝').length,2);assert.equal(searchPeople(people,'不存在').length,0);assert.equal(searchPeople(people,' ').length,3);
});
test('exact names rank before partial matches and source names are never converted',()=>{
 const rows=[{id:'a',label:'王安',names:['王安']},{id:'b',label:'安',names:['安']},{id:'c',label:'謝𤣥',names:['謝𤣥']}];assert.equal(searchPeople(rows,'安')[0].id,'b');assert.equal(searchPeople(rows,'玄').length,0);assert.equal(rows[2].label,'謝𤣥');
});
test('all catalog works occur once, including new works not hardcoded into the homepage',()=>{
 const rows=[{id:'w-shiji'},{id:'w-jinshu'},{id:'w-epitaph-new'},{id:'w-future-work'}];const groups=groupWorks(rows);assert.deepEqual(groups.flatMap(g=>g.works).map(w=>w.id),rows.map(w=>w.id));assert.equal(groups.at(-1).works.length,2);
});
test('book links use existing readers and safely encode identifiers',()=>{assert.equal(workURL({id:'w-shiji',reader_kind:'shiji'}),'shiji.html');assert.equal(workURL({id:'w-jinshu',reader_kind:'corpus'}),'reader.html#work=w-jinshu');assert.ok(!workURL({id:'w-<bad>&',reader_kind:'corpus'}).includes('<'));});
import fs from 'node:fs';
test('published CBR index exposes every canonical person once and all current works',()=>{
 const people=JSON.parse(fs.readFileSync(new URL('../data/corpus/persons.json',import.meta.url)));const index=JSON.parse(fs.readFileSync(new URL('../data/corpus/profiles/index.json',import.meta.url)));
 const result=canonicalProfiles(people,index);assert.equal(result.length,Object.keys(people).length);assert.equal(new Set(result.map(p=>p.id)).size,result.length);
 const works=JSON.parse(fs.readFileSync(new URL('../data/corpus/works.json',import.meta.url))).works;assert.equal(groupWorks(works).flatMap(g=>g.works).length,works.length);assert.ok(works.some(w=>w.id==='w-sanguozhi'));assert.ok(works.some(w=>w.id==='w-jinshu'));assert.ok(works.some(w=>w.id==='w-epitaph-yangshu'));
});
