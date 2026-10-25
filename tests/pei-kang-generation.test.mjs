import test from 'node:test';
import assert from 'node:assert/strict';
import {traceFamily} from '../assets/person-family.js';
const type='ancestor_from_interpreted_generation_and_known_descendant_chain';
const relation=(subject_person_id,predicate,object_person_id)=>({subject_person_id,predicate,object_person_id,evidence:[]});
const proof={type,status:'contextual_provisional',human_reviewed:false,rationale:'Synthetic qualified generation interpretation; unknown father remains empty.',references:[{quote:'Synthetic source reference.'}]};
const inferred={person_id:'synthetic-mei',parent_person_id:null,source_assertion_id:null,ancestor_person_id:'synthetic-kang',connection:'grandfather',generation_distance:2,intermediate_person_ids:[null],assembly_id:'synthetic-family',status:'editorial_preferred',ancestor_connection:proof};
const make=()=>({'synthetic-mei':{id:'synthetic-mei',assembled_identity:inferred},'synthetic-kang':{id:'synthetic-kang',relations:[relation('synthetic-kang','father','synthetic-hui')]},'synthetic-hui':{id:'synthetic-hui'}});
test('interpreted generation retains empty father and qualifies grandfather and later ancestry',async()=>{
 const people=make();const f=await traceFamily(people['synthetic-mei'],async id=>people[id]);
 assert.deepEqual(f.ancestors.map(g=>g.map(p=>p.id)),[[],['synthetic-kang'],['synthetic-hui']]);
 assert.equal(f.ancestors[1][0].role,'assembly_inferred');assert.equal(f.ancestors[2][0].role,'assembly_inferred');
 assert.equal(people['synthetic-mei'].relations,undefined);
});
test('unresolved, missing evidence and maternal generation claims do not supply ancestors',async()=>{
 for(const change of [{status:'unresolved'},{ancestor_connection:{...proof,references:[]}},{ancestor_connection:{...proof,type:'maternal_generation_claim'}}]){
  const people=make();people['synthetic-mei'].assembled_identity={...inferred,...change};const f=await traceFamily(people['synthetic-mei'],async id=>people[id]);assert.deepEqual(f.ancestors,[[],[],[]]);
 }
});
test('unadopted raw ancestor assertion never becomes a father or exact grandfather on its own',async()=>{
 const p={id:'synthetic-ziye',relations:[{...relation('synthetic-ziye','ancestor','synthetic-kang'),qualifiers:{source_term:'八世孫',reported_generation_number:8,generation_distance:null,adopted_for_family_tree:false}}]};
 const f=await traceFamily(p,async id=>({id}));assert.deepEqual(f.ancestors,[[],[],[]]);
});
