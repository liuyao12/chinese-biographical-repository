import assert from 'node:assert/strict';
import test from 'node:test';
import {lifeYearLabel,sourceDateLabel} from '../assets/person-life.js';
import {personCard} from '../assets/cbr-person.js';
import {setLocale} from '../assets/i18n.js';
import fs from 'node:fs';

const p=JSON.parse(fs.readFileSync(new URL('./fixtures/song047_single_year_era_profile.json',import.meta.url)));
test('single-year Chinese era shows 465 while received 中 and unknown month/day remain',()=>{
 setLocale('zh-Hant');const event=p.life_events[0];
 assert.equal(sourceDateLabel(event),'景和中');assert.match(lifeYearLabel(event),/465/);assert.doesNotMatch(lifeYearLabel(event),/至|元年/);
 for(const full of [false,true]){const html=personCard(p,full);assert.match(html,/465/);assert.match(html,/景和中/);assert.doesNotMatch(html,/景和元年/);}
 assert.equal(event.normalized_date_range.month,undefined);assert.equal(event.normalized_date_range.day,undefined);
 assert.equal(event.normalized_date_range.year,undefined);
});
test('multi-year outer window remains a range and does not select its last year',()=>{
 const e=structuredClone(p.life_events[0]);e.normalized_date_range.earliest={era:'CE',era_year:424,year:424};e.normalized_date_range.latest={era:'CE',era_year:453,year:453};
 assert.match(lifeYearLabel(e),/424至453/);
});
