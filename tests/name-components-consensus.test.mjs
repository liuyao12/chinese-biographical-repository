import test from 'node:test';
import assert from 'node:assert/strict';
import {summarizeNameComponents} from '../assets/name-components.js';
import {personCard} from '../assets/cbr-person.js';
import {setLocale} from '../assets/i18n.js';
const record=(x={})=>({surname:'曹',ming:'爽',quote:'甲來源原文',additional_names:[],...x});
const person=(records,x={})=>({id:'synthetic',label:'曹爽',name_components:records,...x});
const aliases=html=>html.match(/<p class="person-aliases">(.*?)<\/p>/)?.[1].replace(/<[^>]*>/g,'') || '';
test('consistent multiple sources preserve structured name and each citation in compact and full cards',()=>{
 const records=[record({zi:'昭伯',quote:'甲源爽字昭伯'}),record({zi:'昭伯',quote:'乙源曹爽字昭伯'})];
 for(const full of [false,true]){
  const html=personCard(person(records),full);assert.match(html,new RegExp(`<h${full?1:3}>曹爽<`));assert.equal(aliases(html),'字 昭伯');assert.match(html,/甲源爽字昭伯/);assert.match(html,/乙源曹爽字昭伯/);assert.equal((html.match(/class="person-name-source"/g)||[]).length,2);
 }
});
test('complementary unknowns do not veto non-empty consensus',()=>{
 const got=summarizeNameComponents([record({surname:null,zi:null}),record({ming:'',zi:'昭伯'}),null]);assert.equal(got.names.surname,'曹');assert.equal(got.names.ming,'爽');assert.equal(got.names.zi,'昭伯');assert.deepEqual(got.conflicts,[]);
});
test('conflicting ming never reduces the heading to only the agreed surname',()=>{
 for(const full of [false,true]){const html=personCard(person([record(),record({ming:'甲'})]),full);assert.match(html,new RegExp(`<h${full?1:3}>曹爽<`));assert.doesNotMatch(html,/<h[13]>曹<\//);assert.match(html,/姓名構件有異說/);assert.match(html,/爽／甲/);}
});
test('conflicting surname likewise retains canonical label and explicit alternatives',()=>{
 const html=personCard(person([record(),record({surname:'夏侯'})]),true);assert.match(html,/<h1>曹爽<\/h1>/);assert.match(html,/曹／夏侯/);
});
test('courtesy-name disagreement is not selected or deduplicated away',()=>{
 const records=[record({zi:'昭伯',additional_names:['字昭伯']}),record({zi:'少季',additional_names:['字少季']})];const d=summarizeNameComponents(records);assert.equal(d.names.zi,undefined);assert.deepEqual(d.names.additional_names,['字昭伯','字少季']);const html=personCard(person(records),true);assert.match(html,/昭伯／少季/);assert.match(aliases(html),/字昭伯/);assert.match(aliases(html),/字少季/);
});
test('only exact prefixed duplicate of an explicitly typed zi is removed for display',()=>{
 const records=[record({zi:'少季',additional_names:['字少季','字開頭的其他稱呼','少季']}),record({zi:'少季'})];const before=JSON.stringify(records);const html=personCard(person(records),true);assert.equal(aliases(html),'字開頭的其他稱呼 字 少季');assert.equal(JSON.stringify(records),before);assert.deepEqual(records[0].additional_names,['字少季','字開頭的其他稱呼','少季']);
});
test('without typed zi a raw additional name beginning with 字 is retained',()=>{
 assert.equal(aliases(personCard(person([record({additional_names:['字少季']})]),true)),'字少季');
});
test('different historical titles are not promoted into a generic heading',()=>{
 const p=person([record({title:'某侯'}),record({title:'某公'})],{titles:[{title:'某侯',period:'始於220'},{title:'某公',period:'始於230'}]});
 for(const full of [false,true]){const html=personCard(p,full);assert.match(html,new RegExp(`<h${full?1:3}>曹爽<`));assert.match(html,/某侯/);assert.match(html,/某公/);}
 assert.equal(summarizeNameComponents(p.name_components).names.title,undefined);
});
test('single-source legacy title display and clan appellation remain intact',()=>{
 assert.match(personCard(person([record({title:'某侯'})]),true),/<h1>某侯 曹爽<\/h1>/);assert.match(personCard(person([record({surname:'鍾',ming:null,zi:'琰',clan_style:{value:'鍾氏'}})]),true),/<h1>鍾氏<\/h1>/);
});
test('full-name disagreement with explicitly recorded components cannot silently win',()=>{
 const d=summarizeNameComponents([record({full_name:'曹操'}),record()]);assert.equal(d.coreConflict,true);assert.match(personCard(person([record({full_name:'曹操'}),record()]),true),/<h1>曹爽<\/h1>/);
});
test('missing fields are omitted and records are never mutated',()=>{
 const records=[{surname:null,ming:null,zi:null,additional_names:[],quote:'來源'}];const before=JSON.stringify(records);for(const full of [false,true]){const html=personCard(person(records),full);assert.doesNotMatch(html,/person-aliases|undefined|null|未詳/);}assert.equal(JSON.stringify(records),before);
});
test('conflicting values, evidence and notes are escaped',()=>{
 const html=personCard(person([record({ming:'<script>',quote:'<img src=x>',note:'<danger>'}),record()]),true);assert.match(html,/&lt;script&gt;/);assert.match(html,/&lt;img/);assert.match(html,/&lt;danger&gt;/);assert.doesNotMatch(html,/<script>|<img/);
});
test('multiple records with surname only retain full canonical label in compact and full cards',()=>{
 for(const full of [false,true]){const html=personCard(person([record({ming:null}),record({ming:''})]),full);assert.match(html,new RegExp(`<h${full?1:3}>曹爽<`));assert.doesNotMatch(html,/<h[13]>曹<\//);}
});
test('multiple surname-only sources may head by an explicit full name or clan appellation',()=>{
 assert.match(personCard(person([record({ming:null,full_name:'曹爽'}),record({ming:null})]),true),/<h1>曹爽<\/h1>/);
 assert.match(personCard(person([record({ming:null,clan_style:{value:'曹氏'}}),record({ming:null})]),true),/<h1>曹氏<\/h1>/);
});
test('typed childhood name joins courtesy name without promoting generic source forms',()=>{
 const p=person([record({zi:'昭伯'}),record({xiaozhi:'黙'})],{names:['公','中軍大將軍','黙']});const html=personCard(p,true);assert.equal(aliases(html),'字 昭伯 小字 黙');assert.doesNotMatch(aliases(html),/公|中軍/);assert.match(html,/來源中的其他稱呼/);
});
test('two typed classifications sharing one spelling keep both labels',()=>{
 const html=personCard(person([record({zi:'某',xiaozhi:'某',additional_names:['某']})]),true);assert.equal(aliases(html),'字 某 小字 某');
});
test('conflicting childhood names are not selected or erased',()=>{
 const d=summarizeNameComponents([record({xiaozhi:'甲'}),record({xiaozhi:'乙'})]);assert.equal(d.names.xiaozhi,undefined);const html=personCard(person([record({xiaozhi:'甲'}),record({xiaozhi:'乙'})]),true);assert.match(html,/甲／乙/);assert.equal(aliases(html),'');
});

test('childhood-name label changes language without changing the received name',()=>{
 const p=person([record({zi:'昭伯',xiaozhi:'黙'})]);setLocale('en');assert.equal(aliases(personCard(p,true)),'Courtesy name 昭伯 Childhood name 黙');setLocale('zh-Hant');assert.equal(aliases(personCard(p,false)),'字 昭伯 小字 黙');
});
