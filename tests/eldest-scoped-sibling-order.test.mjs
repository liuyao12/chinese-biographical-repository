import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {orderChildren} from '../assets/sibling-order.js';
import {traceFamily} from '../assets/person-family.js';
const entries = ids => ids.map(id => ({id,person:{id}}));
const father = (id,parent='p') => ({subject_person_id:id,predicate:'father',object_person_id:parent,qualifiers:{}});
const numbered = (id,n=1,scope='sons_of_parent',parent='p') => ({...father(id,parent),qualifiers:{birth_order:{ordinal:n,scope,parent_person_id:parent}}});
const brother = (id,other) => ({subject_person_id:id,predicate:'brother',object_person_id:other,qualifiers:{}});
const daughter = (id,parent='p') => ({subject_person_id:parent,predicate:'daughter',object_person_id:id,qualifiers:{}});
const result = (ids,relations) => orderChildren(entries(ids),{id:'p',relations}).entries.map(e=>e.id);
test('sole eldest son precedes a proven same-parent unnumbered brother without filling ordinals',()=>{
 const r=[numbered('eldest'),father('other'),brother('other','someone')];const before=JSON.stringify(r);
 assert.deepEqual(result(['other','eldest'],r),['eldest','other']);assert.equal(JSON.stringify(r),before);
});
test('older daughter and unknown-sex child retain priority ahead of eldest son',()=>{
 const r=[numbered('eldest'),father('daughter'),daughter('daughter'),father('unknown'),father('brother'),brother('brother','unknown')];
 assert.deepEqual(result(['daughter','unknown','brother','eldest'],r),['daughter','unknown','eldest','brother']);
});
test('brother object is not male proof',()=>{
 assert.deepEqual(result(['unknown','eldest'],[numbered('eldest'),father('unknown'),brother('eldest','unknown')]),['unknown','eldest']);
});
test('different-parent male and unadopted brother evidence cannot qualify sons scope',()=>{
 const b=brother('unadopted','x');b.qualifiers.adopted_for_family_tree=false;
 assert.deepEqual(result(['other','unadopted','eldest'],[numbered('eldest'),father('other','q'),brother('other','x'),father('unadopted'),b]),['other','unadopted','eldest']);
});
test('second son does not outrank unnumbered son',()=>{
 assert.deepEqual(result(['unknown','second'],[numbered('second',2),father('unknown'),brother('unknown','x')]),['unknown','second']);
});
test('eldest daughter is symmetric and does not precede an unnumbered son',()=>{
 const sis={subject_person_id:'sister',predicate:'sister',object_person_id:'someone',qualifiers:{}};
 assert.deepEqual(result(['son','sister','eldest'],[numbered('eldest',1,'daughters_of_parent'),father('son'),brother('son','x'),father('sister'),sis]),['son','eldest','sister']);
});
test('children ordinal one may precede either sex only with attested same-parent membership',()=>{
 assert.deepEqual(result(['girl','unrelated','first'],[numbered('first',1,'children_of_parent'),daughter('girl'),brother('unrelated','x')]),['unrelated','first','girl']);
});
test('aliases qualify member and brother proof without name or ID suffix inference',()=>{
 const input=entries(['m','first']);input[0].person.person_ids=['m','alias'];
 assert.deepEqual(orderChildren(input,{id:'p',relations:[numbered('first'),father('alias'),brother('alias','x')]}).entries.map(e=>e.id),['first','m']);
});
test('explicit contrary age produces existing SCC conflict rather than deleting claims',()=>{
 const b=brother('other','first');b.qualifiers.relative_birth_order={older_person_id:'other',younger_person_id:'first',scope:'siblings',operator:'lt'};
 const out=orderChildren(entries(['other','first']),{id:'p',relations:[numbered('first'),father('other'),b]});
 assert.deepEqual(out.entries.map(e=>e.id),['other','first']);assert.deepEqual(out.conflicts,[['other','first']]);
});
test('frozen-L actual Xie profiles through production traceFamily preserve eldest and four relative edges',async()=>{
 const z='aa6_83c_juy_DBABA',profiles=new Map();
 for(const suffix of ['','A','B','C','D','E'])profiles.set(z+suffix,JSON.parse(fs.readFileSync(new URL(`fixtures/eldest-xie/${z+suffix}.json`,import.meta.url))));
 const before=JSON.stringify([...profiles]),load=async id=>{if(!profiles.has(id))throw Error('outside captured child scope');return profiles.get(id);};
 const out=await traceFamily(profiles.get(z),load),ids=out.children.map(e=>e.id);
 assert.equal(ids[0],z+'A');for(const suffix of ['A','B','D','E'])assert(ids.indexOf(z+suffix)<ids.indexOf(z+'C'));
 assert.equal(out.child_order_conflicts,undefined);assert.equal(JSON.stringify([...profiles]),before);
 assert.equal(profiles.get(z).relations.filter(r=>r.qualifiers?.birth_order).length,1);
});

test('conflicting sex evidence leaves first-son scope unextended',()=>{
 assert.deepEqual(result(['other','first'],[numbered('first'),daughter('first'),father('other'),brother('other','x')]),['other','first']);
 assert.deepEqual(result(['other','first'],[numbered('first'),father('other'),brother('other','x'),daughter('other')]),['other','first']);
});
