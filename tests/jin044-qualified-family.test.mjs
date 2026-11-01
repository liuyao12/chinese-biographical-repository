import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import {traceFamily} from '../assets/person-family.js';
import {generator} from '../scripts/export_person_summaries.mjs';
import {personSummaryCard} from '../assets/person-summary.js';
const owner='c-jinshu-044-luqin-family-rendered';
function fixture(){
 const connection={type:'fixed_jin044_paternal_nephew_unknown_father',owner,status:'contextual_provisional',placement_status:'editorial_inferred',literal_grandfather_assertion:false,same_father_independently_attested:false,unknown_father_person_id:null,unknown_father_name:null,father_is_hao_asserted:false,human_reviewed:false,nephew_assertion_id:'synthetic-nephew',uncle_father_assertion_id:'synthetic-father',rationale:'合成測例：同父未獨證，父未知，祖連只屬編輯推接。',references:[{assertion_id:'synthetic-nephew',chapter_id:owner,source_id:'s-jinshu044-lu-rendered-oldcapture',paragraph_id:owner+':p007',quote:'Synthetic nephew clause.',scope:'source_nephew'},{assertion_id:'synthetic-father',chapter_id:owner,source_id:'s-jinshu044-lu-rendered-oldcapture',paragraph_id:owner+':p004',quote:'Synthetic named father clause.',scope:'source_uncle_father'}]};
 return {child:{id:'child',label:'合成子',assembled_identity:{person_id:'child',assembly_id:'synthetic-family',status:'editorial_preferred',parent_person_id:null,ancestor_person_id:'grand',connection:'grandfather',generation_distance:2,intermediate_person_ids:[null],ancestor_connection:connection}},grand:{id:'grand',label:'合成祖',relations:[]}};
}
test('qualified unknown-father placement remains inference in trace and essential summary',async()=>{
 const people=fixture(),loads=[];const family=await traceFamily(people.child,async id=>{loads.push(id);return people[id];});
 assert.deepEqual(family.ancestors.map(x=>x.map(p=>p.id)),[[],['grand'],[]]);assert.deepEqual(loads,['grand']);const grand=family.ancestors[1][0];assert.equal(grand.role,'assembly_inferred');assert.equal(grand.inference_basis.independently_attested,false);assert.equal(grand.inference_basis.literal_grandfather_assertion,false);assert.equal(grand.ancestry_paths[0].qualification,'assembly_inferred');assert.equal(grand.ancestry_paths[0].steps[0].inference_basis.unknown_father_person_id,null);
 const root=await fs.mkdtemp(path.join(os.tmpdir(),'jin044-qualified-summary-'));
 try{await fs.mkdir(path.join(root,'data/corpus/profiles'),{recursive:true});await fs.writeFile(path.join(root,'data/corpus/profiles/index.json'),JSON.stringify({profiles:Object.keys(people).map(id=>({id}))}));for(const p of Object.values(people))await fs.writeFile(path.join(root,'data/corpus/profiles',p.id+'.json'),JSON.stringify(p));const g=await generator(root);const summary=await g.project(people.child);const entry=summary.family.ancestors[1][0];assert.equal(entry.role,'assembly_inferred');assert.equal(entry.inference_basis.independently_attested,false);assert.equal(entry.inference_basis.literal_grandfather_assertion,false);assert.match(personSummaryCard(summary),/父系暫定/);assert(!JSON.stringify(summary).includes('Synthetic nephew clause.'));}finally{await fs.rm(root,{recursive:true,force:true});}
});
test('unknown owner, promoted certainty or an invented father cannot become a displayed ancestor',async()=>{
 for(const edit of [r=>{r.ancestor_connection.owner='c-other';},r=>{r.ancestor_connection.same_father_independently_attested=true;},r=>{r.ancestor_connection.literal_grandfather_assertion=true;},r=>{r.ancestor_connection.father_is_hao_asserted=true;},r=>{r.intermediate_person_ids=['invented'];},r=>{r.ancestor_connection.references.pop();}]){const people=fixture();edit(people.child.assembled_identity);const family=await traceFamily(people.child,async id=>people[id]);assert.deepEqual(family.ancestors,[[],[],[]]);}
});
