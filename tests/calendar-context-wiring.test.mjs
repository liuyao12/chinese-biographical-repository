import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,readdirSync} from 'node:fs';
import {personCard} from '../assets/cbr-person.js';
import {civilYearLabelData} from '../assets/person-life.js';
const load=p=>JSON.parse(readFileSync(new URL(p,import.meta.url),'utf8'));
const files=readdirSync(new URL('../exports/persons/',import.meta.url)).filter(x=>x.endsWith('.json')&&x!=='index.json');
test('export and runtime API expose numeric year without NLU',()=>{
 let seen=0;
 for(const fn of files){
  const b=load('../exports/persons/'+fn);
  const dates=(b.date_normalizations||[]).filter(x=>x.calendar_context);
  if(!dates.length)continue;
  const p=load('../data/corpus/profiles/'+fn);
  assert.ok(p.dates.some(x=>x.calendar_context&&Number.isSafeInteger(x.year)));
  assert.ok(b.calendar_context_assertions.length);
  for(const d of dates){assert.ok([277,329].includes(d.year));assert.equal(civilYearLabelData({normalized_date:d}).params.year,d.year);assert.ok(d.original_quote);seen++;}
  if(p.life_events?.some(e=>e.normalized_date?.calendar_context))assert.match(personCard(p,true),/329/);
  if(p.titles.some(t=>t.effective_period?.start?.normalized_date?.calendar_context))assert.match(personCard(p,true),/277/);
 }
 assert.ok(seen>=21);
});
test('later 277 offices remain undated and amnesty is no death',()=>{
 const h=load('../corpus/jinshu/059-titles.json').holdings;
 for(const x of h.filter(x=>/^th-phase4-j-02[4-9]$/.test(x.id)))assert.equal(x.effective_period.start.normalized_date,undefined);
 const e=load('../corpus/zizhitongjian/094-life-events.json').events;
 assert.ok(e.every(x=>x.event_type==='death'&&x.date_expression==='二月，丙戌'));
 assert.ok(e.every(x=>x.normalized_date.calendar_context.context_id!=='cal-context-phase5-003'));
});
test('independent calendar API preserves Dinghai amnesty without a person event',()=>{
 const api=load('../exports/calendar-contexts.json');assert.equal(api.runtime_ai_required,false);assert.equal(api.records.length,3);
 const d=api.records.find(x=>x.anchor.surface==='丁亥');assert.equal(d.normalized_date.year,329);assert.equal(d.scope.quote,'丁亥，大赦。');assert.equal(d.event_type,undefined);
});
