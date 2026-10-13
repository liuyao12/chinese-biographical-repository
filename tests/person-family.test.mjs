import test from 'node:test';
import assert from 'node:assert/strict';
import {traceFamily} from '../assets/person-family.js';
const relation = (subject_person_id, predicate, object_person_id) => ({subject_person_id, predicate, object_person_id, evidence: []});
test('an explicitly recorded grandfather leaves the missing father empty', async () => {
  const a={id:'a',relations:[relation('a','grandfather','g')]};
  const g={id:'g',relations:[relation('g','father','h')]};
  const h={id:'h'};
  const family=await traceFamily(a, async id => ({g,h})[id]);
  assert.deepEqual(family.ancestors.map(row=>row.map(x=>x.id)),[[],['g'],['h']]);
});
test('source JSON traversal derives three generations and separate spouses/children', async () => {
  const people = {
    a: {id:'a',label:'synthetic child',relations:[relation('a','father','b'),relation('a','mother','m'),relation('s','spouse','a'),relation('c','father','a')]},
    b: {id:'b',label:'synthetic father',relations:[relation('b','father','d')]},
    d: {id:'d',label:'synthetic grandfather',relations:[relation('d','father','e')]},
    e: {id:'e',label:'synthetic great grandfather'},
    m:{id:'m'},s:{id:'s'},c:{id:'c'},
  };
  const family = await traceFamily(people.a, async id => people[id]);
  assert.deepEqual(family.ancestors.map(row => row.map(x => x.id)), [['b'],['d'],['e']]);
  assert.deepEqual(family.mother.map(x => x.id), ['m']);
  assert.deepEqual(family.spouses.map(x => x.id), ['s']);
  assert.deepEqual(family.children.map(x => x.id), ['c']);
  assert.equal(family.children[0].spouse, undefined);
});
test('cycles stop traversal while competing source fathers remain visible', async () => {
  const a={id:'a',relations:[relation('a','father','b'),relation('a','father','c')]};
  const b={id:'b',relations:[relation('b','father','a')]};
  const c={id:'c',relations:[]};
  const family=await traceFamily(a, async id => ({a,b,c})[id]);
  assert.equal(family.ancestors[0].length,2);
  assert.equal(family.ancestors[1][0].cycle,true);
  assert.deepEqual(family.ancestors[2],[]);
});
