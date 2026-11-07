import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {summarizeLife,ageLabel} from '../assets/person-life.js';
const root=new URL('../',import.meta.url),read=path=>JSON.parse(fs.readFileSync(new URL(path,root),'utf8'));
const ch=read('corpus/jinshu/098-wangdun-comparison.json'),old=read('corpus/jinshu/076-wangbin-life-events.json').events.find(x=>x.id==='le-jin076-wangbin-50-3'),now=read('corpus/jinshu/098-wangdun-comparison-life-events.json').events[0],group=read('corpus/jinshu/098-wangdun-comparison-life-event-groups.json').groups[0];
const input=()=>({id:now.person_id,person_ids:[now.person_id],life_events:structuredClone([old,now]),life_event_groups:structuredClone([group]),age_assertions:structuredClone(ch.annotation.age_assertions)});
test('one explicit group retains two exact source witnesses and reported age59',()=>{
 const p=input(),before=JSON.stringify(p),s=summarizeLife(p);assert.equal(s.death.length,1);assert.deepEqual(s.death[0].source_event_ids,group.member_event_ids);assert.deepEqual(s.death[0].evidence,group.evidence);assert.equal(s.death[0].source_event_group.date,null);assert.equal(s.death[0].normalized_date,undefined);assert.equal(s.ages[0].value,59);assert.equal(ageLabel(s.ages[0]),'59 歲（來源報齡）');assert.equal(JSON.stringify(p),before);
});
test('old no-group unknown-date reports remain unchanged',()=>{
 const p=input();delete p.life_event_groups;const s=summarizeLife(p);assert.deepEqual(s.death,p.life_events);assert.equal(s.death.length,2);assert.equal(s.death[0].source_event_group,undefined);
});
test('wrong person or event type cannot merge',()=>{
 for(const key of['person','type']){const p=input();if(key==='person')p.life_events[0].person_id='other';else p.life_events[0].event_type='birth';assert.throws(()=>summarizeLife(p));}
});
test('missing member and fake-death paragraph cannot merge',()=>{
 const p=input();p.life_events.pop();assert.throws(()=>summarizeLife(p));const q=input();q.life_event_groups[0].evidence[1].paragraph_id=ch.id+':p023';assert.throws(()=>summarizeLife(q));
});
test('group cannot supply invented date, human review, or source-attested interpretation',()=>{
 for(const [key,value]of[['date',{year:324}],['human_reviewed',true],['status','source_attested']]){const p=input();p.life_event_groups[0][key]=value;assert.throws(()=>summarizeLife(p));}
 const p=input();p.life_events[1].normalized_date={year:323};assert.throws(()=>summarizeLife(p));
});
test('one end rekey rejects and full typed UID rekey stays valid',()=>{
 const oldId=now.person_id,newId='8jk_w4v_a3t',one=input();one.life_events[1].person_id=newId;assert.throws(()=>summarizeLife(one));
 const replace=x=>Array.isArray(x)?x.map(replace):x&&typeof x==='object'?Object.fromEntries(Object.entries(x).map(([k,v])=>[k,replace(v)])):x===oldId?newId:x;
 const s=summarizeLife(replace(input()));assert.equal(s.death.length,1);assert.equal(s.death[0].person_id,newId);assert.equal(s.death[0].evidence.length,2);
});
test('no automatic inference from two same-person death rows',()=>{
 const p=input();p.life_event_groups=[];assert.equal(summarizeLife(p).death.length,2);p.life_event_groups={};assert.throws(()=>summarizeLife(p));
});
test('a member cannot belong to two groups',()=>{const p=input();p.life_event_groups.push({...structuredClone(group),id:'other-group'});assert.throws(()=>summarizeLife(p));});
