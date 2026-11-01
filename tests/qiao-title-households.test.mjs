import test from 'node:test';
import assert from 'node:assert/strict';
import {nobleHouseholds,declinedNobleOutcomeUnreported} from '../assets/noble-declination.js';
import {personCard} from '../assets/cbr-person.js';
const amount=(prefix='邑',offered=false)=>{
 const surface=prefix+'四千四百戶';
 return {id:'h',kind:'noble_rank',title:'譙王',mode:'grant',evidence:[{paragraph_id:'p',quote:surface}],reported_households:{value:4400,source_number:'四千四百',unit:'戶',actual_revenue:null,scope:offered?'offered_advancement_not_confirmed_held':'actual_enfeoffment_allotment',source_anchor:{paragraph_id:'p',start:0,end:Array.from(surface).length,surface}}};
};
test('both received structured allotment spellings display their original glyphs',()=>{
 for(const prefix of ['邑','食邑']){const h=amount(prefix);const html=nobleHouseholds(h);assert.match(html,new RegExp('<q>'+prefix+'四千四百戶</q>'));assert.equal(h.reported_households.value,4400);assert.equal(h.evidence[0].quote,prefix+'四千四百戶');}
});
test('ordinary text, other record kinds, invalid span and untyped data are not title allotments',()=>{
 assert.equal(nobleHouseholds({quote:'邑四千四百戶'}),'');assert.equal(nobleHouseholds({kind:'noble_rank',evidence:amount().evidence}),'');
 const office=amount();office.kind='office';assert.equal(nobleHouseholds(office),'');
 const wrong=amount();wrong.reported_households.source_anchor.start++;assert.equal(nobleHouseholds(wrong),'');
 const unit=amount();unit.reported_households.unit='人';assert.equal(nobleHouseholds(unit),'');
});
test('offered uncertainty remains separate for both source spellings',()=>{
 for(const prefix of ['邑','食邑']){const proposed=amount(prefix,true);assert.equal(nobleHouseholds(proposed),'');assert.equal(nobleHouseholds(proposed,true),'');assert.equal(declinedNobleOutcomeUnreported(proposed),false);const held=amount(prefix);assert.equal(nobleHouseholds(held,true),'');}
});
test('existing inherited-title renderer shows resolved rank and preserves raw li',()=>{
 const h={id:'inherit',title:'立',kind:'noble_rank',mode:'accession',period:'未定 → 未定',evidence:[],effective_period:{start:{status:'source_event',date_expression:null,evidence:[]},end:{status:'unknown',date_expression:null,evidence:[]}},inheritance:{predecessor_person_id:'prior',predecessor_holding_id:'prior-h',resolved_title:'譙王',source_term:'子某立',rationale:'本源父爵承襲，未補日期或養父。',status:'contextual_provisional',evidence:[]}};
 for(const full of [false,true]){const html=personCard({id:'successor',label:'承繼者',names:[],titles:[h],addresses:[],occurrences:[],relations:[],sources:[],dates:[],related_people:{prior:'前任'}},full);assert.match(html,/譙王/);assert.match(html,/原文：立/);assert.doesNotMatch(html,/<strong>立<\/strong>/);}
 assert.equal(h.title,'立');assert.equal(h.inheritance.resolved_title,'譙王');
});
