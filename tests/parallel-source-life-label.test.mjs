import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {sourceDateLabel,lifeYearLabel} from '../assets/person-life.js';
import {t} from '../assets/i18n.js';
const chapter=JSON.parse(readFileSync(new URL('../corpus/jinshu/034-yanghu.json',import.meta.url),'utf8'));
const personID=chapter.paragraphs.flatMap(p=>p.mentions).find(m=>m.id==='c-jinshu-034-yanghu:p001:m0000').person_id;
const profile=JSON.parse(readFileSync(new URL(`../exports/persons/${personID}.json`,import.meta.url),'utf8'));
const death=profile.life_events.find(e=>e.id==='le-jin034-yanghu-hu-death');
test('received death report displays its independently mapped reign year without rewriting the source',()=>{
 const before=JSON.stringify(death);
 assert.equal(death.normalized_date.year,278);
 assert.equal(sourceDateLabel(death),'咸寧四年（平行史料暫定對讀）');
 assert.match(lifeYearLabel(death),/278/);
 assert.equal(death.date_expression,null);
 assert.equal(death.source_term,'尋卒');
 assert.equal(JSON.stringify(death),before);
 assert.equal(t('{date} (provisional parallel-source reading)',{date:'咸寧四年'},'en'),'咸寧四年 (provisional parallel-source reading)');
});
test('inconsistent, unknown or non-year mappings never invent a reign-year label',()=>{
 for(const change of [d=>d.regnal_year_mapping.regnal_year=5,d=>d.year=279,d=>d.era_year=279,d=>d.calendar='gregorian',d=>d.precision='day',d=>d.regnal_year_mapping.kind='unreviewed',d=>d.regnal_year_mapping.end_ce_year=277]){
  const row=structuredClone(death);row.date_expression='未詳';change(row.normalized_date);
  assert.equal(sourceDateLabel(row),'未詳');
 }
});
