import test from 'node:test';
import assert from 'node:assert/strict';
import {summarizeLife, ageLabel, lifeYearLabel} from '../assets/person-life.js';
test('bounded or qualified reported ages retain their source wording', () => {
  assert.equal(ageLabel({value:null,source_term:'百有六十餘歲',qualified_source_term:'蓋老子百有六十餘歲'}),'蓋老子百有六十餘歲');
  assert.equal(ageLabel({value:70,source_term:'年七十'}),'70 歲（來源報齡）');
  assert.equal(ageLabel({value:70,reporting_status:'qualified_report',source_term:'或言七十歲'}),'或言七十歲');
});
test('life summary separates source life events from appointments and unrelated ages', () => {
  const p={id:'a',dates:[{event_type:'appointment',era_year:100}],life_events:[{id:'birth',person_id:'a',event_type:'birth'},{id:'other',person_id:'b',event_type:'death'}],age_assertions:[{person_id:'a',value:70},{person_id:'b',value:20}]};
  const life=summarizeLife(p);
  assert.equal(life.birth.length,1);assert.deepEqual(life.death,[]);
  assert.equal(life.ages[0].value,70);assert.equal(life.ages.length,1);
  assert.equal(life.birth[0].normalized_date,undefined);
});
test('provisional date priority preserves the alternative life event', () => {
  const p={id:'a',life_events:[{id:'old',person_id:'a',event_type:'death'},{id:'new',person_id:'a',event_type:'death'}],life_event_date_decisions:[{status:'editorial_provisional',candidate_event_ids:['old','new'],preferred_event_id:'new'}]};
  assert.deepEqual(summarizeLife(p).death.map(e=>e.id),['new','old']);
});

test('year range labels do not select an endpoint or invent a date', () => {
 assert.equal(lifeYearLabel({}), '');
 assert.equal(lifeYearLabel({normalized_date:{era:'CE',era_year:10}}),'西元10年');
 assert.equal(lifeYearLabel({normalized_date_range:{earliest:{era:'BCE',era_year:1},latest:{era:'CE',era_year:1}}}),'西元前1至西元1年（暫定範圍）');
});
