import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {traceFamily} from '../assets/person-family.js';

const read = path => JSON.parse(fs.readFileSync(new URL(`../${path}`, import.meta.url)));
const chapter = read('corpus/sanguozhi/023-peiqian.json');
const assertions = read('corpus/sanguozhi/023-peiqian-assertions.json').assertions;
const mention = id => chapter.paragraphs.flatMap(p => p.mentions).find(m => m.id === id);
const childId = mention('c-sanguozhi-023-peiqian:p009:m0053').person_id;
const families = read('registry/family-assemblies.json').assemblies;
const family = families.find(f => f.members.some(m => m.person_id === childId));
const member = family.members.find(m => m.person_id === childId);
const profiles = Object.fromEntries(family.members.map(m => [m.person_id, {
  id:m.person_id, relations:assertions,
  assembled_identity:{...m, assembly_id:family.id, status:family.status},
}]));

test('the actual qualified cousin assembly shows the named grandfather while leaving the father absent', async () => {
  const loaded=[];
  const result=await traceFamily(profiles[childId],async id=>{loaded.push(id);return profiles[id];});
  assert.deepEqual(result.ancestors[0],[]);
  assert.deepEqual(result.ancestors[1].map(p=>p.id),[member.ancestor_person_id]);
  assert.equal(result.ancestors[1][0].role,'assembly_inferred');
  assert(result.ancestors[1][0].evidence.some(e=>e.assertion_id===member.ancestor_connection.qualified_cousin_assertion_id));
  assert.deepEqual(result.ancestors[2].map(p=>p.id),[family.root_person_id]);
  assert.equal(result.ancestors[2][0].role,'assembly_inferred');
  assert(loaded.every(id=>Object.hasOwn(profiles,id)));
  assert.equal(member.parent_person_id,null);
  assert.deepEqual(member.intermediate_person_ids,[null]);
});

test('the received cousin assertion alone does not silently invent the grandfather', async () => {
  const input={id:childId,relations:assertions};
  const result=await traceFamily(input,async id=>profiles[id]);
  assert.deepEqual(result.ancestors,[[],[],[]]);
});

test('unresolved, unsupported or evidence-free assembly proposals do not become displayed ancestors', async () => {
  for(const mutate of [
    row=>{row.status='unresolved';},
    row=>{row.ancestor_connection.type='agnatic_cousin';},
    row=>{row.ancestor_connection.references=[];},
  ]) {
    const input=structuredClone(profiles[childId]);
    mutate(input.assembled_identity);
    const result=await traceFamily(input,async id=>profiles[id]);
    assert.deepEqual(result.ancestors,[[],[],[]]);
  }
});
