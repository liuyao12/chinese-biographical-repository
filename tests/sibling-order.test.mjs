import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {orderChildren} from '../assets/sibling-order.js';
import {traceFamily} from '../assets/person-family.js';
const entries = ids => ids.map(id => ({id, person:{id}}));
const rel = (older, younger, extra = {}) => ({qualifiers:{relative_birth_order:{older_person_id:older,
  younger_person_id:younger, operator:'lt', scope:'siblings', ...extra}}});
const read = path => JSON.parse(fs.readFileSync(new URL(`../${path}`, import.meta.url)));

test('relative older brother precedes younger without assigning absolute ordinals', () => {
  const parent = {id:'p',relations:[rel('older','younger')]};
  const input = entries(['younger','older']);
  const snapshot = JSON.stringify({parent,input});
  assert.deepEqual(orderChildren(input,parent).entries.map(e=>e.id),['older','younger']);
  assert.equal(JSON.stringify({parent,input}),snapshot);
});

test('absolute ordinals compare only within their attested parent and scope', () => {
  const ordinal = (id,n,scope,parent='p') => ({subject_person_id:id,predicate:'father',object_person_id:parent,
    qualifiers:{birth_order:{ordinal:n,parent_person_id:parent,scope}}});
  const parent={id:'p',relations:[ordinal('b',2,'sons_of_parent'),ordinal('a',1,'sons_of_parent'),
    ordinal('d',1,'daughters_of_parent'),ordinal('unknown',1,'sons_of_parent','other')]};
  assert.deepEqual(orderChildren(entries(['b','a','d','unknown']),parent).entries.map(e=>e.id),['a','b','d','unknown']);
});

test('unknown order preserves input order and never reads family ID letters', () => {
  assert.deepEqual(orderChildren(entries(['family_Z','family_A','other']),{id:'p'}).entries.map(e=>e.id),
    ['family_Z','family_A','other']);
});

test('cousin relative ages and unadopted statements do not order siblings', () => {
  const a=rel('a','b',{scope:'paternal_cousins'}), b=rel('a','b');
  b.qualifiers.adopted_for_family_tree=false;
  assert.deepEqual(orderChildren(entries(['b','a']),{id:'p',relations:[a,b]}).entries.map(e=>e.id),['b','a']);
});

test('contradictory cycles retain members and source order while other constraints still apply', () => {
  const result=orderChildren(entries(['b','a','d','c']),{id:'p',relations:[rel('a','b'),rel('b','a'),rel('c','d')]});
  assert.deepEqual(result.entries.map(e=>e.id),['b','a','c','d']);
  assert.deepEqual(result.conflicts,[['b','a']]);
});

test('identity aliases resolve before applying order constraints', () => {
  const input=entries(['b','a']);input[1].person.person_ids=['a','aliasA'];
  assert.deepEqual(orderChildren(input,{id:'p',relations:[rel('aliasA','b')]}).entries.map(e=>e.id),['a','b']);
});

test('complete Zheng sibling report implies display order without writing unknown ordinals', () => {
  const relations=read('corpus/jinshu/032-assertions.json').assertions.filter(r=>r.qualifiers?.source_sibling_group);
  const group=relations[0].qualifiers.source_sibling_group;
  const input=entries([...group.member_person_ids].reverse());
  const snapshot=JSON.stringify(relations);
  assert.deepEqual(orderChildren(input,{id:'synthetic-parent',relations}).entries.map(e=>e.id),group.member_person_ids);
  assert.equal(JSON.stringify(relations),snapshot);
  assert.equal(group.member_roles[1].ordinal,null);
  assert.equal(group.member_roles[3].ordinal,null);
});

test('incomplete reported group does not infer absent slots or new absolute ordinals', () => {
  const group={id:'synthetic-group',reported_count:4,member_person_ids:['a','b','c','d'],
    member_roles:[{person_id:'a',ordinal:1},{person_id:'b',ordinal:null},
      {person_id:'c',ordinal:3},{person_id:'d',ordinal:null,position:'youngest'}]};
  const input=entries(['c','b']);
  assert.deepEqual(orderChildren(input,{id:'p',relations:[{qualifiers:{source_sibling_group:group}}]}).entries.map(e=>e.id),['c','b']);
});

test('real Sima father profile shows Lang before Yi through sourced brother evidence', async () => {
  const root='dkn_ge4_286', father=root+'_AAA', yi=root+'_AAAA', lang=root+'_AAAB';
  const relations=read('corpus/jinshu/001-assertions.json').assertions;
  const family=read('registry/family-assemblies.json').assemblies.find(a=>a.id==='family-sima-jun-near-ancestry');
  const inferred=family.members.find(m=>m.person_id===lang);
  const parent={id:father,relations,assembled_children:[{...inferred,assembly_id:family.id,status:family.status}]};
  const profiles={};
  profiles[yi]={id:yi,relations};profiles[lang]={id:lang,relations};
  const output=await traceFamily(parent,async id=>{if(!profiles[id])throw new Error('unavailable');return profiles[id];});
  assert.deepEqual(output.children.map(e=>e.id),[lang,yi]);
  assert.equal(output.child_order_conflicts,undefined);
});
