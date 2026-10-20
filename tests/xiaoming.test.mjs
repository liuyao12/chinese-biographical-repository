import test from 'node:test';
import assert from 'node:assert/strict';
import {summarizeNameComponents} from '../assets/name-components.js';
import {personCard} from '../assets/cbr-person.js';
import {setLocale} from '../assets/i18n.js';
const aliases=h=>h.match(/<p class="person-aliases">(.*?)<\/p>/)?.[1].replace(/<[^>]*>/g,'')||'';
const p=names=>({id:'person',label:'張邵',name_components:names});
test('compact and full render xiaoming with exact source and preserve zi separately',()=>{
 for(const full of [false,true]){const html=personCard(p([{surname:'張',ming:'邵',zi:'茂宗',quote:'張邵字茂宗'},{xiaoming:'梨',quote:'敷小名查父邵小名梨'}]),full);assert.equal(aliases(html),'字 茂宗 小名 梨');assert.match(html,/敷小名查父邵小名梨/);assert.match(html.replace(/<[^>]*>/g,''),/小名 梨/);assert.doesNotMatch(html,/小字 梨/);}
});
test('xiaozhi and xiaoming with same spelling preserve two source classifications',()=>{assert.equal(aliases(personCard(p([{zi:'字某',xiaozhi:'某',xiaoming:'某'}]),true)),'字 字某 小字 某 小名 某');});
test('Cao Shuang existing childhood name stays xiaozhi',()=>{assert.equal(aliases(personCard({id:'cao',label:'曹爽',name_components:[{zi:'昭伯',xiaozhi:'黙'}]},true)),'字 昭伯 小字 黙');});
test('untyped fruit does not produce typed xiaoming',()=>{assert.doesNotMatch(personCard(p([{additional_names:[],quote:'梨為百果之宗'}]),true),/小名 梨/);});
test('missing xiaoming is omitted',()=>{assert.doesNotMatch(aliases(personCard(p([{zi:'茂宗'}]),false)),/小名|undefined|null/);});
test('xiaoming conflicts remain visible without choosing a default',()=>{const names=[{xiaoming:'查'},{xiaoming:'梨'}];assert.equal(summarizeNameComponents(names).names.xiaoming,undefined);const html=personCard(p(names),true);assert.match(html.replace(/<[^>]*>/g,''),/小名 查／梨/);assert.equal(aliases(html),'');});
test('typed xiaoming exact prefix deduplicates without mutating records',()=>{const names=[{xiaoming:'梨',additional_names:['小名梨','梨','梨果']}];const before=JSON.stringify(names);assert.equal(aliases(personCard(p(names),false)),'梨果 小名 梨');assert.equal(JSON.stringify(names),before);});
test('English uses separate labels and restores traditional Chinese',()=>{setLocale('en');assert.equal(aliases(personCard(p([{xiaozhi:'甲',xiaoming:'乙'}]),true)),'Childhood name 甲 Childhood name (xiaoming) 乙');setLocale('zh-Hant');assert.equal(aliases(personCard(p([{xiaozhi:'甲',xiaoming:'乙'}]),true)),'小字 甲 小名 乙');});
