import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {namespaceNavigation,traceFamily} from '../assets/person-family.js';
import {personCard} from '../assets/cbr-person.js';
const f=JSON.parse(fs.readFileSync(new URL('../registry/family-assemblies.json',import.meta.url)));
const a=f.assemblies.find(a=>a.id==='family-song045-cheng-brothers');
const g=a.collateral_root_group, ids=g.root_person_ids;
function person(id){return {id,person_ids:[id],label:id===ids[0]?'程道養':'程道助',relations:[],assembled_identity:{...a.members.find(x=>x.person_id===id),assembly_id:a.id,root_person_id:null,namespace_id:a.namespace_id,namespace_entry_person_id:a.entry_person_id,collateral_root_group:structuredClone(g)}};}
const load=async id=>{assert.notEqual(id,a.namespace_id);return person(id);};
test('real namespace reads exactly two persons, never parent namespace',async()=>{const n=await namespaceNavigation(person(ids[0]),load);assert.equal(n.roots.length,2);assert.equal(n.common_parent_person_id,null);assert.equal(n.qualification,'source_attested_brothers_parent_unidentified');assert.ok(n.roots.every(x=>x.role==='source_attested'));});
test('no father inferred in ordinary traceFamily',async()=>{const n=await traceFamily(person(ids[0]),load);assert.ok(n.ancestors.every(x=>x.length===0));assert.equal(n.family_namespace.roots.length,2);});
test('exact type has separate readable card label',async()=>{const p=person(ids[0]),family=await traceFamily(p,load);p.names=[];p.titles=[];p.addresses=[];p.sources=[];p.occurrences=[];p.table_occurrences=[];const html=personCard(p,false,'main',family);assert.match(html,/明文弟兄|Source-attested brothers/);assert.doesNotMatch(html,/同族旁支（編輯接合/);});
test('named parent or wrong generation cannot surface',async()=>{for(const mutate of [p=>p.assembled_identity.collateral_root_group.common_parent_name='某',p=>p.assembled_identity.root_person_id=ids[0],p=>p.assembled_identity.collateral_root_group.root_person_ids[1]+='A']){const p=person(ids[0]);mutate(p);assert.equal(await namespaceNavigation(p,load),null);}});
test('wrong order, missing proof and pseudo-parent flags fail closed',async()=>{for(const mutate of [g=>g.relative_age.operator='gt',g=>g.references=[],g=>g.common_parent_registered=true,g=>g.relative_age.older_ordinal=1]){const p=person(ids[0]);mutate(p.assembled_identity.collateral_root_group);assert.equal(await namespaceNavigation(p,load),null);}});
test('legacy cousin namespace retains prior shape',async()=>{const ns='abc_def_123',roots=[ns+'_A',ns+'_B'];const p={id:roots[0],assembled_identity:{namespace_id:ns,root_person_id:null,namespace_entry_person_id:roots[0],collateral_root_group:{type:'unknown_shared_father_from_qualified_first_cousins',status:'contextual_provisional',references:[{quote:'舊來源'}],root_person_ids:roots,common_parent_person_id:null,common_parent_name:null,common_parent_registered:false,relative_age:'unknown',rationale:'舊資格'}}};const n=await namespaceNavigation(p,async id=>({id,label:id}));assert.equal(n.qualification,'assembly_inferred');assert.equal(n.namespace_kind,undefined);assert.ok(n.roots.every(x=>x.role==='assembly_inferred'));});

test('actual impersonation occurrence shows its existing readable qualification',()=>{const ch=JSON.parse(fs.readFileSync(new URL('../corpus/songshu/045-wyd1739-liucui.json',import.meta.url)));const mark=ch.paragraphs.flatMap(p=>p.mentions).find(m=>m.surface==='飛龍'&&m.interpretation_note?.includes('道養被迫冒稱'));assert.ok(mark);const p=person(ids[0]);Object.assign(p,{names:[],titles:[],addresses:[],sources:[],occurrences:[],table_occurrences:[]});const html=personCard(p,false,'main',null,mark);assert.match(html,/道養被迫冒稱飛龍/);});

test('actual exported namespace profiles render the source-attested brothers without a father',async()=>{
 const exported=id=>JSON.parse(fs.readFileSync(new URL('../data/corpus/profiles/'+id+'.json',import.meta.url)));
 const p=exported(ids[0]);assert.deepEqual(p.assembled_identity.collateral_root_group,g);
 const family=await traceFamily(p,async id=>{assert.notEqual(id,a.namespace_id);return exported(id);});
 assert.equal(family.family_namespace.namespace_kind,g.type);
 assert.deepEqual(family.family_namespace.roots.map(r=>r.id),ids);
 assert.equal(family.family_namespace.common_parent_person_id,null);
 assert.ok(family.ancestors.every(rows=>rows.length===0));
 const html=personCard(p,false,'main',family);assert.match(html,/明文弟兄|Source-attested brothers/);
 assert.doesNotMatch(html,/同族旁支（編輯接合/);
});
test('explicit namespace rejects missing source qualification or non-sibling branch shape',async()=>{
 for(const mutate of [g=>g.biological_verification=true,g=>g.brother_assertion_id='',g=>g.name_record_ids=[],g=>g.relative_age.scope='children',g=>g.relative_age.younger_person_id=g.root_person_ids[0],g=>g.root_person_ids[1]+='A']){
  const p=person(ids[0]);mutate(p.assembled_identity.collateral_root_group);assert.equal(await namespaceNavigation(p,load),null);
 }
});
