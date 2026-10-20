import test from 'node:test';
import assert from 'node:assert/strict';
import {personCard} from '../assets/cbr-person.js';
const holding=(id,title='嗣',resolved='東興縣侯')=>({id,title,kind:'noble_rank',mode:'accession',period:'未定 → 未定',evidence:[],effective_period:{start:{status:'source_event',date_expression:null,evidence:[]},end:{status:'unknown',date_expression:null,evidence:[]}},inheritance:{predecessor_person_id:'prior',predecessor_holding_id:'prior-'+id,resolved_title:resolved,source_term:'子某嗣',rationale:'同單元前爵省稱，年月未定',status:'contextual_provisional',evidence:[]}});
const profile=titles=>({id:'successor',label:'承繼者',names:[],titles,addresses:[],occurrences:[],relations:[],sources:[],dates:[],related_people:{prior:'前任姓名'}});
test('inherited title keeps source wording and named predecessor on compact/full cards',()=>{
 const p=profile([holding('h')]);
 for(const full of[false,true]){const html=personCard(p,full);assert.match(html,/東興縣侯/);assert.match(html,/原文：嗣/);assert.match(html,/前任姓名/);assert.match(html,/person.html#prior/);assert.match(html,/爵位承襲依據/);}
});
test('different inherited titles with identical source shorthand do not collapse',()=>{
 const html=personCard(profile([holding('h1'),holding('h2','嗣','另一侯')]),true);
 assert.match(html,/東興縣侯/);assert.match(html,/另一侯/);assert.equal((html.match(/person-holding-succession/g)||[]).length,2);
});
test('compact keeps inherited rank while full retains all offices; explicit reading wins',()=>{
 const office=id=>({id,title:'官'+id,kind:'office',mode:'attestation',period:'西元400年（暫定） → 未定',evidence:[]});
 const p=profile([office('一'),office('二'),holding('h')]);assert.match(personCard(p,false),/東興縣侯/);
 const html=personCard(p,true);assert.match(html,/官一/);assert.match(html,/官二/);
 p.preferred_title_readings=[{holding_id:'h',preferred_title:'既有校讀',source_title:'嗣'}];assert.match(personCard(p,true),/既有校讀/);
});
