import test from'node:test';import assert from'node:assert/strict';import fs from'node:fs';
import {personCard}from'../assets/cbr-person.js';
const native=JSON.parse(fs.readFileSync(new URL('../corpus/sanguozhi/009-caoren-caochun-titles.json',import.meta.url),'utf8')).holdings;
const profile=h=>({id:h.person_id,label:'來源人物',names:[],titles:[h],addresses:[],occurrences:[],relations:[],related_people:{},sources:[],dates:[]});
test('each of five native acting appointments has a readable acting badge',()=>{
 const hs=native.filter(h=>h.source_career_role?.role_category==='acting_appointment');assert.equal(hs.length,5);
 for(const h of hs){assert.equal(h.appointment_role,'acting');assert.match(personCard(profile(h),true),/person-acting-office/);}
});
test('four real inherited ranks display the source 嗣 rather than invent a full source title',()=>{
 const hs=native.filter(h=>h.inherited_title_binding?.kind==='fixed_kanripo_named_father_rank_succession');assert.equal(hs.length,4);
 for(const h of hs){const html=personCard(profile(h),true);assert.equal(h.inherited_title_binding.raw_surface,'嗣');assert.match(html,/原文：嗣/);assert(!html.includes('原文：'+h.title));assert.equal(h.effective_period.start.date_expression,null);}
});
test('raw source wording stays escaped and absent bindings retain the old fallback',()=>{
 const h=native.find(h=>h.inherited_title_binding);const raw={...h,inherited_title_binding:{...h.inherited_title_binding,raw_surface:'<script>bad()</script>'}};const html=personCard(profile(raw),true);assert(!html.includes('<script>bad()</script>'));assert(html.includes('&lt;script&gt;'));
 const fallback={...h};delete fallback.inherited_title_binding;assert(personCard(profile(fallback),true).includes('原文：'+h.title));
});
