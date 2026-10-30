import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {nameSourceFragmentsHTML} from '../assets/name-source-fragments.js';
import {personCard} from '../assets/cbr-person.js';
import {setLocale} from '../assets/i18n.js';
const rows=JSON.parse(fs.readFileSync(new URL('./actual-seven-name-bundles.json',import.meta.url),'utf8'));
const profile=()=>structuredClone(rows.find(x=>x.label==='綽'));
test('actual source fragment group shows complete courtesy and both original MID links',()=>{
 const p=profile(),before=JSON.stringify(p),html=nameSourceFragmentsHTML(p);
 assert.match(html,/子流/);for(const mid of p.source_name_fragments[0].mention_ids)assert.ok(html.includes(encodeURIComponent(mid)));
 assert.equal(JSON.stringify(p),before);const card=personCard(p);assert.match(card,/<h3>劉綽<\/h3>/);assert.match(card.replace(/<[^>]*>/g,''),/字 子流/);assert.match(card,/person-name-fragments/);
});
test('wrong person, name record, field, source, fragment order and qualification do not display',()=>{
 for(const mode of ['person','record','field','source','order','missing','status','review']){
  const p=profile(),g=p.source_name_fragments[0];
  if(mode==='person')g.person_id='wrong';if(mode==='record')g.complete_component.record_id='missing';if(mode==='field')g.complete_component.field='title';if(mode==='source')g.source_id='wrong';if(mode==='order')g.fragments.reverse();if(mode==='missing')g.mention_ids.pop();if(mode==='status')g.status='source_attested';if(mode==='review')g.human_reviewed=true;
  assert.equal(nameSourceFragmentsHTML(p),'',mode);
 }
 assert.equal(nameSourceFragmentsHTML({id:'none'}),'');
});
test('fragment labels are escaped and locale remains independent of source text',()=>{
 const p=profile(),g=p.source_name_fragments[0];g.fragments[0].surface='<script>';g.fragments[1].surface='&';g.complete_component.value='<script>&';p.name_components.find(n=>n.id===g.complete_component.record_id).zi='<script>&';const html=nameSourceFragmentsHTML(p);assert.doesNotMatch(html,/<script>/);assert.match(html,/&lt;script&gt;/);setLocale('en',{persist:false});assert.match(nameSourceFragmentsHTML(profile()),/Name read across source fragments/);setLocale('zh-Hant',{persist:false});
});

test("malformed optional fragment payloads fail closed without affecting legacy profiles",()=>{
 for(const groups of [null,{},"bad",[null],[{kind:"source_bound_name_fragment_group",person_id:"x",status:"contextual_provisional",human_reviewed:false,source_mentions_and_registry_aliases_retained:true,complete_component:null}]])assert.equal(nameSourceFragmentsHTML({id:"x",person_ids:{},name_components:[null],source_name_fragments:groups}),"");
});
