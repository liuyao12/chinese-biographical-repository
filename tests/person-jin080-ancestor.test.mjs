import test from 'node:test';import assert from 'node:assert/strict';import {traceFamily} from '../assets/person-family.js';
const KIND='fixed_jin080_paternal_nephew_to_uncle_father';
function person(){return{id:'nephew',assembled_identity:{person_id:'nephew',assembly_id:'family-test',status:'editorial_preferred',parent_person_id:null,ancestor_person_id:'grandfather',connection:'grandfather',generation_distance:2,intermediate_person_ids:[null],ancestor_connection:{type:KIND,status:'contextual_provisional',human_reviewed:false,rationale:'明叔侄與叔父明父，父名未知',nephew_assertion_id:'a-uncle',uncle_father_assertion_id:'a-father',references:['a-uncle','a-father'].map(assertion_id=>({assertion_id,quote:'完整已驗原句',source_id:'source',chapter_id:'chapter',paragraph_id:'paragraph',scope:'來源限定'}))}}};}
const run=async p=>traceFamily(p,async id=>({id,label:id}));
test('fixed080 grandfather is inferred, leaves father empty and retains both proofs',async()=>{const f=await run(person());assert.deepEqual(f.ancestors.map(row=>row.map(p=>p.id)),[[],['grandfather'],[]]);assert.equal(f.ancestors[1][0].role,'assembly_inferred');assert.equal(f.ancestors[1][0].evidence.length,2);});
for(const[name,mutate]of[
 ['unknown kind',p=>p.assembled_identity.ancestor_connection.type='unknown'],
 ['wrong subject endpoint',p=>p.assembled_identity.person_id='someone-else'],
 ['self ancestor',p=>p.assembled_identity.ancestor_person_id='nephew'],
 ['no references',p=>p.assembled_identity.ancestor_connection.references=[]],
 ['missing father proof',p=>p.assembled_identity.ancestor_connection.references.pop()],
 ['fake string references',p=>p.assembled_identity.ancestor_connection.references='proof'],
 ['missing quote',p=>p.assembled_identity.ancestor_connection.references[0].quote=''],
 ['wrong distance',p=>p.assembled_identity.generation_distance=3],
 ['boolean distance',p=>p.assembled_identity.generation_distance=true],
 ['missing intermediate',p=>p.assembled_identity.intermediate_person_ids=[]],
 ['named intermediate',p=>p.assembled_identity.intermediate_person_ids=['guessed-father']],
 ['invented father',p=>p.assembled_identity.parent_person_id='guessed-father'],
 ['wrong relationship',p=>p.assembled_identity.connection='great_grandfather'],
 ['human qualification drift',p=>p.assembled_identity.ancestor_connection.human_reviewed=0],
])test('fixed080 refuses '+name,async()=>{const p=person();mutate(p);const f=await run(p);assert.deepEqual(f.ancestors,[[],[],[]]);});
for(const kind of['shared_ancestor_through_sibling','wyd_song044_paternal_nephew_to_uncle_father'])test('legacy '+kind+' admission unchanged',async()=>{const p=person();p.assembled_identity.ancestor_connection.type=kind;delete p.assembled_identity.generation_distance;delete p.assembled_identity.intermediate_person_ids;const f=await run(p);assert.equal(f.ancestors[1][0].id,'grandfather');});
test('ordinary direct grandfather route remains source-linked',async()=>{const f=await run({id:'nephew',relations:[{subject_person_id:'nephew',predicate:'grandfather',object_person_id:'grandfather',evidence:[]}]});assert.equal(f.ancestors[1][0].id,'grandfather');assert.equal(f.ancestors[1][0].role,undefined);});
