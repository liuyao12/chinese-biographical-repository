import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {lifeYearLabel,summarizeLife} from '../assets/person-life.js';
const event=JSON.parse(readFileSync(new URL('./fixtures/chu-wu-chinese-civil-year.json',import.meta.url),'utf8'));

test('a sourced civil-year label is displayed without destroying the Gregorian window',()=>{
  const before=JSON.stringify(event.normalized_date_range);
  assert.equal(lifeYearLabel(event),'西元前154年（中國曆年）');
  assert.equal(JSON.stringify(event.normalized_date_range),before);
});
test('without an explicit civil-year record neither range endpoint is selected',()=>{
  const legacy=structuredClone(event);delete legacy.chinese_civil_year;
  assert.equal(lifeYearLabel(legacy),'西元前155至154年（暫定範圍）');
});
test('invalid or mismatched year numbering does not silently become a civil year',()=>{
  for (const change of [{era_year:0,year:1},{era_year:154,year:154},{calendar:'gregorian'},{precision:'day'}]) {
    const copy=structuredClone(event);Object.assign(copy.chinese_civil_year,change);
    assert.equal(lifeYearLabel(copy),'西元前155至154年（暫定範圍）');
  }
  const bce=structuredClone(event);Object.assign(bce.chinese_civil_year,{era:'BCE',era_year:1,year:0});
  assert.equal(lifeYearLabel(bce),'西元前1年（中國曆年）');
});
test('synthetic conflicting civil-year assertions are not lost in summary grouping',()=>{
  const alternate=structuredClone(event);alternate.id='synthetic-conflicting-event';Object.assign(alternate.chinese_civil_year,{era_year:155,year:-154});
  const summary=summarizeLife({id:event.person_id,life_events:[event,alternate]});
  assert.equal(summary.death.length,2);
});
