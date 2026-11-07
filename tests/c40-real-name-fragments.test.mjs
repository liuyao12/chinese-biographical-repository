import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {nameSourceFragmentsHTML} from '../assets/name-source-fragments.js';
import {summarizeNameComponents} from '../assets/name-components.js';
import {personCard} from '../assets/cbr-person.js';
import {setLocale} from '../assets/i18n.js';
const rows=JSON.parse(fs.readFileSync(new URL('./fixtures/c40-actual-profiles.json',import.meta.url),'utf8'));
test('actual Wang Cui profile uses full_name and keeps both original links',()=>{
 const p=structuredClone(rows.wangcui),before=JSON.stringify(p),s=summarizeNameComponents(p.name_components);
 assert.equal(s.names.full_name,'王粹');assert.equal(s.names.surname,'王');assert.equal(s.names.ming,'粹');assert.equal(s.coreConflict,false);
 assert.ok(!p.names.includes('王')&&!p.names.includes('粹'));
 for(const full of [false,true]){const html=personCard(p,full);assert.match(html,new RegExp(`<h${full?1:3}>王粹</h${full?1:3}>`));assert.match(html,/person-name-fragments/);for(const mid of p.source_name_fragments[0].mention_ids)assert.ok(html.includes(encodeURIComponent(mid)));}
 assert.equal(JSON.stringify(p),before);
});
test('full_name continuation rejects a forged person, record, field, source or order',()=>{
 for(const mode of ['person','record','field','source','order','review']){const p=structuredClone(rows.wangcui),g=p.source_name_fragments[0];if(mode==='person')g.person_id='wrong';if(mode==='record')g.complete_component.record_id='wrong';if(mode==='field')g.complete_component.field='title';if(mode==='source')g.source_id='wrong';if(mode==='order')g.fragments.reverse();if(mode==='review')g.human_reviewed=true;assert.equal(nameSourceFragmentsHTML(p),'',mode);}
});
test('full_name source fragment text is escaped',()=>{
 const p=structuredClone(rows.wangcui),g=p.source_name_fragments[0];g.fragments[0].surface='<img>';g.fragments[1].surface='&';g.complete_component.value='<img>&';p.name_components.find(n=>n.id===g.complete_component.record_id).full_name='<img>&';const html=nameSourceFragmentsHTML(p);assert.doesNotMatch(html,/<img>/);assert.match(html,/&lt;img&gt;/);
});
test('actual Han Shou geography retains both adjacent source quotations',()=>{
 const p=rows.hanshou,a=p.addresses.find(x=>x.id==='pa-jin040-wyd-hanshou');assert.equal(a.term,'南陽堵陽');assert.equal(a.evidence.length,2);assert.ok(a.evidence[0].quote.endsWith('南'));assert.ok(a.evidence[1].quote.startsWith('陽堵陽人'));
 for(const full of [false,true])assert.match(personCard(p,full),/南陽堵陽/);
});
test('actual Han Mi keeps two literal surnames without inventing a change date',()=>{
 const p=rows.hanmi,ns=p.name_components;assert.ok(ns.some(n=>n.surname==='韓'&&n.ming==='謐'));const j=ns.find(n=>n.surname==='賈'&&n.ming==='謐');assert.equal(j.person_mention_id,'c-jinshu-040-wyd1739-jiachong:p020:m0130');assert.equal(j.source_name_phase.change_date,null);assert.equal(j.source_name_phase.surname_change_event_asserted,false);
 for(const full of [false,true]){const html=personCard(p,full);assert.match(html,/韓謐/);assert.match(html,/賈謐/);}
});
test('unfragmented control and English switch do not invent a fragment group',()=>{
 assert.equal(nameSourceFragmentsHTML(rows.chong),'');setLocale('en',{persist:false});assert.match(nameSourceFragmentsHTML(rows.wangcui),/Name read across source fragments/);setLocale('zh-Hant',{persist:false});
});
