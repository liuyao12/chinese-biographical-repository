import test from 'node:test';
import assert from 'node:assert/strict';
import {summarizeLife, ageLabel, lifeYearLabel, civilYearLabelData, studyReferencesHTML} from '../assets/person-life.js';
test('an era window remains a Chinese civil-year range without choosing either endpoint',()=>{
 const event={normalized_date_range:{basis:'within_named_era',calendar:'chinese_civil',earliest:{era:'CE',era_year:100,year:100},latest:{era:'CE',era_year:108,year:108}}};
 assert.equal(lifeYearLabel(event),'西元100至108年（中國曆年範圍）');
 assert.equal(civilYearLabelData(event),null);
});
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

test('identical resolved life dates share a summary row but retain both source quotations',()=>{
 const range={earliest:{era:'BCE',era_year:191,year:-190},latest:{era:'BCE',era_year:190,year:-189},precision:'year_range'};
 const p={id:'a',life_events:[{id:'one',person_id:'a',event_type:'death',date_expression:'孝惠五年',normalized_date_range:{...range,references:[{quote:'甲'}]},evidence:[{quote:'甲書卒'}]},{id:'two',person_id:'a',event_type:'death',date_expression:'孝惠五年',normalized_date_range:{...range,references:[{quote:'乙'}]},evidence:[{quote:'乙書薨'}]}]};
 const life=summarizeLife(p);assert.equal(life.death.length,1);assert.equal(life.death[0].evidence.length,2);
 assert.equal(p.life_events.length,2);assert.equal(p.life_events[0].evidence.length,1);
});
test('date precision, original date expressions and unresolved alternatives prevent life-date merging',()=>{
 const event={person_id:'a',event_type:'death',date_expression:'五年',normalized_date:{era:'CE',era_year:10}};
 const p={id:'a',life_events:[{...event,id:'year'},{...event,id:'day',normalized_date:{era:'CE',era_year:10,month:3,day:2}},{...event,id:'other-term',date_expression:'六年'},{id:'unknown-one',person_id:'a',event_type:'death'},{id:'unknown-two',person_id:'a',event_type:'death'}]};
 assert.equal(summarizeLife(p).death.length,5);
});

test('research references expose scope and unverified status without inventing publication year',()=>{
 const html=studyReferencesHTML([{display_title:'改訂紀年表',author:'辛德勇',publication_year:null,url:'https://example.org/paper',reviewed_scope:'第六頁腳注',opinion_validation:'not_attempted'}]);
 assert.match(html,/辛德勇/);assert.match(html,/第六頁腳注/);assert.match(html,/研究意見未獨立驗證/);assert.doesNotMatch(html,/null|undefined|2020/);
});
test('research bibliography escapes text and rejects executable links',()=>{
 const html=studyReferencesHTML([{display_title:'<img src=x>',author:'<b>',url:'javascript:alert(1)',reference_note:'<script>'}]);
 assert.doesNotMatch(html,/<a|<img|<script>/);assert.match(html,/&lt;img/);assert.match(html,/&lt;b/);
});
test('missing research references produce no empty profile field',()=>{
 assert.equal(studyReferencesHTML(), '');assert.equal(studyReferencesHTML([]),'');assert.equal(studyReferencesHTML([null,{}]),'');
});

test('adjacent-number source ages remain approximations without a fabricated lifespan',()=>{
 const age={person_id:'synthetic-person',value:null,source_number:'七八',source_term:'皆七八歲',approximation:{kind:'adjacent_age_numbers',numbers:[7,8]}};
 assert.equal(ageLabel(age),'七八歲');
 const life=summarizeLife({id:'synthetic-person',age_assertions:[age]});assert.deepEqual(life.birth,[]);assert.deepEqual(life.death,[]);assert.equal(life.ages[0].value,null);assert.equal(life.ages[0].bounds,undefined);
});


test('explicitly normalized Chinese civil years retain calendar meaning without an exact day',()=>{
 const event={normalized_date:{era:'CE',era_year:149,year:149,year_numbering:'astronomical',precision:'year',calendar:'chinese_civil'}};
 assert.deepEqual(civilYearLabelData(event),{key:'{year} CE (Chinese civil year)',params:{year:149}});
 assert.match(lifeYearLabel(event),/149/);
 assert.equal(civilYearLabelData({normalized_date:{...event.normalized_date,calendar:'gregorian'}}),null);
 assert.equal(civilYearLabelData({normalized_date:{...event.normalized_date,precision:'day'}}),null);
 assert.equal(event.normalized_date.day,undefined);
});
test('an explicitly Chinese projection window still cannot supply a single event year',()=>{
 const range={calendar:'chinese_civil',earliest:{era:'CE',era_year:149,year:149},latest:{era:'CE',era_year:150,year:150}};
 assert.equal(civilYearLabelData({normalized_date_range:range}),null);
 assert.match(lifeYearLabel({normalized_date_range:range}),/149.*150/);
});
