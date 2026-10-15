import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {traceFamily} from '../assets/person-family.js';
test('仲居的父祖由首選來源JSON逐代追溯，原異說仍在',async()=>{
 const load=async id=>JSON.parse(readFileSync(new URL('../data/corpus/profiles/'+id+'.json',import.meta.url)));
 const p=await load('fvm_66f_0k3_CA'),family=await traceFamily(p,load);
 assert.deepEqual(family.ancestors[0].map(x=>x.id),['fvm_66f_0k3_C']);
 assert.deepEqual(family.ancestors[1].map(x=>x.id),['fvm_66f_0k3']);
 assert.ok(p.relations.some(a=>a.id==='a-shiji098-006' && a.object_person_id==='fvm_66f_0k3'));
 assert.ok(p.relations.some(a=>a.id==='a-hanshu041-zhou-003' && a.object_person_id==='fvm_66f_0k3_C'));
 assert.ok(!Object.hasOwn(p,'ancestors'));
});
