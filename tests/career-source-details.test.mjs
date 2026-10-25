import test from 'node:test';
import assert from 'node:assert/strict';
import {sourceDetailsHTML} from '../assets/person-source-details.js';
import {setLocale} from '../assets/i18n.js';
const row=(kind,values={})=>({id:kind,person_id:'p',kind,source_term:'原詞',values,evidence:[]});
const p={id:'p',titles:[{id:'h',person_id:'p',title:'原官'}]};
test('all seven classes are readable in both languages without machine codes',()=>{
 const rows=[row('unassumed_appointment',{office_title:'遼東太守',appointment_stage:'recommendation',outcome:'not_assumed'}),row('refused_rank_offer',{named_title:'武陵侯',acceptance:'declined'}),row('declined_collective_nomination',{office_title:'元帥',outcome:'not_assumed'}),row('military_authority',{linked_holding_id:'h',office_title_created:false}),row('office_continuation',{linked_holding_id:'h',new_appointment_created:false}),row('appointment_with_omitted_office',{jurisdiction_source_name:'荊州'}),row('office_disqualification',{not_reinterpreted_as_lifetime_actual_nonservice:true})];
 for(const lang of ['zh-Hant','en']){setLocale(lang);const s=sourceDetailsHTML({...p,source_details:rows});for(const r of rows)assert.ok(s.includes(r.source_term));assert.doesNotMatch(s,/>Source detail<|>unassumed_appointment<|>not_assumed</);assert.match(s,/原官/);if(lang==='zh-Hant')assert.match(s,/受舉未就|辭封不受/);else assert.match(s,/Appointment not assumed/);assert.equal(sourceDetailsHTML({...p,source_details:rows},false),'');}
 setLocale('zh-Hant');
});
test('linked title requires unique exact ID and same person; no textual fallback',()=>{
 const r=row('military_authority',{linked_holding_id:'h',office_title:'不可回退',office_title_created:false});
 for(const titles of [[{id:'h',person_id:'other',title:'外人官'}],[{id:'other',person_id:'p',title:'錯官'}],[...p.titles,...p.titles]]){const s=sourceDetailsHTML({...p,titles,source_details:[r]});assert.doesNotMatch(s,/外人官|錯官|不可回退|原官/);}
 const s=sourceDetailsHTML({...p,source_details:[{...r,person_id:'other'}]});assert.doesNotMatch(s,/原官/);
});
test('qualification flags are not guessed; source escaped and no invented dates',()=>{
 const s=sourceDetailsHTML({...p,source_details:[row('refused_rank_offer',{named_title:'<爵>'}),row('appointment_with_omitted_office',{jurisdiction_source_name:'青州'})]});assert.match(s,/&lt;爵&gt;/);assert.doesNotMatch(s,/原文明言辭封不受|刺史|任職起年/);assert.match(s,/原文省略官名/);
});
