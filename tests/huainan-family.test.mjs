import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {traceFamily} from '../assets/person-family.js';
test('劉安直記高祖孫與沿父劉長追溯只顯示一位祖父',async()=>{
 const load=async id=>JSON.parse(readFileSync(new URL('../data/corpus/profiles/'+id+'.json',import.meta.url)));
 const p=await load('yqp_nlb_p1p_AFA'),family=await traceFamily(p,load);
 assert.deepEqual(family.ancestors[0].map(x=>x.id),['yqp_nlb_p1p_AF']);
 assert.deepEqual(family.ancestors[1].map(x=>x.id),['yqp_nlb_p1p_A']);
 assert.ok(p.relations.some(a=>a.id==='a-shiji107-015' && a.predicate==='grandfather' && a.object_person_id==='yqp_nlb_p1p_A'));
 assert.ok(!Object.hasOwn(p,'ancestors'));
});
