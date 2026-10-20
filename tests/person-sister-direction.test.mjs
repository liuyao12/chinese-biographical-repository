import test from 'node:test';
import assert from 'node:assert/strict';
import {personCard} from '../assets/cbr-person.js';

const profile = (id, order) => ({id, person_ids:[id], label:id,
  names:[], name_components:[], titles:[], addresses:[], occurrences:[], table_occurrences:[],
  relations:[{subject_person_id:'sister', object_person_id:'brother', predicate:'sister',
    qualifiers:order ? {relative_birth_order:order} : {}, evidence:[]}],
  related_people:{sister:'某女',brother:'某男'}, sources:[], dates:[]});

test('sister statement describes its subject from either person page', () => {
  const order={operator:'lt',older_person_id:'sister',younger_person_id:'brother'};
  for (const id of ['sister','brother']) {
    const html=personCard(profile(id,order),true);
    assert.match(html,/某女<\/a> · 為對方之姊：<a[^>]*>某男<\/a>/);
    assert.ok(!html.includes('為對方之妹'));
  }
});

test('younger sister and unknown order do not guess the other person is female', () => {
  const younger=personCard(profile('sister',{operator:'lt',older_person_id:'brother',younger_person_id:'sister'}),true);
  assert.match(younger,/某女<\/a> · 為對方之妹：<a[^>]*>某男<\/a>/);
  const unknown=personCard(profile('sister'),true);
  assert.match(unknown,/某女<\/a> · 為對方之姊妹：<a[^>]*>某男<\/a>/);
});
