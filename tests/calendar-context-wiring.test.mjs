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
  const dates=(b.date_normalizations||[]).filter(x=>x.calendar_context?.context_id.startsWith('cal-context-phase5-'));
  if(!dates.length)continue;
  const p=load('../data/corpus/profiles/'+fn);
  assert.ok(p.dates.some(x=>x.calendar_context&&Number.isSafeInteger(x.year)));
  assert.ok(b.calendar_context_assertions.length);
  for(const d of dates){assert.ok([277,329].includes(d.year));assert.equal(civilYearLabelData({normalized_date:d}).params.year,d.year);assert.ok(d.original_quote);seen++;}
  if(p.life_events?.some(e=>e.normalized_date?.calendar_context?.context_id.startsWith('cal-context-phase5-')))assert.match(personCard(p,true),/329/);
  if(p.titles.some(t=>t.effective_period?.start?.normalized_date?.calendar_context?.context_id.startsWith('cal-context-phase5-')))assert.match(personCard(p,true),/277/);
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
 const api=load('../exports/calendar-contexts.json');assert.equal(api.runtime_ai_required,false);assert.equal(api.records.filter(x=>x.id.startsWith('cal-context-phase5-')).length,3);assert.equal(api.records.length,8);
 const d=api.records.find(x=>x.anchor.surface==='丁亥');assert.equal(d.normalized_date.year,329);assert.equal(d.scope.quote,'丁亥，大赦。');assert.equal(d.event_type,undefined);
});

test('biography contexts expose five exact event years with local event quotes',()=>{
 const api=load('../exports/calendar-contexts.json');
 const expected=new Map([['cal-songwang9-1',432],['cal-songwang9-2',427],['cal-songwang9-3',430],['cal-songwang9-4',432],['cal-songwang9-5',432]]);
 const contexts=api.records.filter(x=>expected.has(x.id));assert.equal(contexts.length,5);
 for(const c of contexts){
  const year=expected.get(c.id);assert.equal(c.normalized_date.year,year);
  const b=load('../exports/persons/'+c.event_binding.person_id+'.json');
  const p=load('../data/corpus/profiles/'+c.event_binding.person_id+'.json');
  const d=b.date_normalizations.find(x=>x.calendar_context?.context_id===c.id);assert.ok(d);assert.equal(d.year,year);
  assert.equal(civilYearLabelData({normalized_date:d}).params.year,year);assert.equal(d.original_quote,c.full_paragraph);
  assert.ok(d.evidence.every(e=>e.paragraph_id===c.anchor.paragraph_id&&e.quote===c.full_paragraph));
  assert.ok(p.dates.some(x=>x.calendar_context?.context_id===c.id&&x.year===year));assert.match(personCard(p,true),new RegExp(String(year)));
  if(c.event_binding.event_type==='posthumous_enfeoffment')assert.equal(b.title_holdings.find(h=>h.id===c.event_binding.record_id).mode,'posthumous_enfeoffment');
  else assert.equal(b.life_events.find(e=>e.id===c.event_binding.record_id).normalized_date.year,year);
 }
});
