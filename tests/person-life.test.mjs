import test from 'node:test';
import assert from 'node:assert/strict';
import {summarizeLife} from '../assets/person-life.js';
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
