import {fileURLToPath} from 'node:url';
import test from 'node:test';
import fs from 'node:fs/promises';import os from 'node:os';import path from 'node:path';import assert from 'node:assert/strict';import {generator,plan,write,activeIds,check} from '../scripts/export_person_summaries.mjs';
test('compact summaries preserve display semantics and reject invalid exports', async () => {
const root=await fs.mkdtemp(path.join(os.tmpdir(),'cbr-summary-test-'));const dir=path.join(root,'data/corpus/profiles');await fs.mkdir(dir,{recursive:true});
const people=Object.fromEntries(['p','f','g','gg','m','s','c','ad','u'].map(id=>[id,{id,label:id,person_ids:[id],relations:[],sources:[{quote:'source text'}]}]));
const edge=(id,a,b,predicate,qualifiers={})=>({id,subject_person_id:a,object_person_id:b,predicate,qualifiers,evidence:[{quote:'原文',source_id:'source'}]});
people.p.relations=[edge('father','p','f','father'),edge('mother','p','m','mother'),edge('spouse','p','s','spouse',{marriage_termination:{kind:'divorce'}}),edge('child','c','p','father'),edge('adoption','p','ad','adoptive_father'),edge('pending','p','u','spouse')];
people.p.unresolved_relation_identity_groups=[{id:'ug',status:'unresolved',predicate:'spouse',same_person:null,distinct_people:null,common_person_id:'p',candidate_person_ids:['u'],assertion_ids:['pending'],rationale:'配偶身份未決',references:[{quote:'原文'}]}];
people.f.relations=[edge('gf','f','g','father')];people.g.relations=[edge('ggf','g','gg','father')];
people.p.age_assertions=[{person_id:'p',value:30,age_context:{kind:'during_life'}},{person_id:'p',value:60,age_context:{kind:'at_death'}}];people.p.life_events=[{id:'birth',person_id:'p',event_type:'birth',date_expression:'某年'},{id:'death',person_id:'p',event_type:'death',date_expression:'其後'}];
people.p.historicity='legendary_tradition';people.p.name_components=[{person_id:'p',surname:'裴',ming:'秀',zi:'季彥'}];
async function save(){for(const p of Object.values(people))await fs.writeFile(path.join(dir,p.id+'.json'),JSON.stringify(p));await fs.writeFile(path.join(dir,'index.json'),JSON.stringify({profiles:Object.keys(people).map(id=>({id}))}));}await save();
const g=await generator(root),s=await g.project(await g.load('p'));assert.equal(s.heading,'裴秀');assert.equal(s.aliases[0].value,'季彥');assert.equal(s.family.ancestors[2][0].id,'gg');assert.equal(s.family.mother[0].id,'m');assert.equal(s.family.adoptive_father[0].id,'ad');assert.equal(s.family.spouses.length,1);assert.equal(s.family.spouses[0].marriage_status,'source_attested_divorce');assert.equal(s.family.unresolved_spouse_groups[0].id,'ug');assert.equal(s.life.ages.find(x=>x.context==='during_life').label.includes('60'),false);assert.ok(s.life.ages.some(x=>x.context==='at_death'));assert.equal(s.historicity,'legendary_tradition');assert.ok(!('identity_note'in s)&&!('name_summary'in s));
const scan=x=>{if(x&&typeof x==='object')for(const[k,v]of Object.entries(x)){assert.ok(!['evidence','sources','quote','quotes','references','steps','person'].includes(k),k);scan(v);}};scan(s);
people.p.name_components=[{person_id:'p',surname:'裴',ming:'秀',zi:'季彥',hao:'某號',title:'鉅鹿公'}];const titled=await g.project(people.p);assert.equal(titled.heading,'鉅鹿公 裴秀');assert.ok(titled.aliases.some(x=>x.kind==='hao'&&x.value==='某號'));
people.p.name_components=[{person_id:'p',ming:'秀',zi:'季彥'}];people.p.label='裴秀';assert.equal((await g.project(people.p)).heading,'裴秀');
// Explicit source age approximation and typed birthplace/deathplace normalization.
people.p.age_assertions.push({person_id:'p',source_number:'五六',value:6,approximation:{kind:'adjacent_age_numbers'},age_context:{kind:'during_life'}});
people.p.age_assertions.push({person_id:'p',value:7,approximation:{kind:'quoted_kin_age_designation'},age_context:{kind:'during_life'}});
people.p.addresses=[{person_id:'p',relation:'birth_place',status:'source_attested',date_expression:'甲子年',normalized_date:{year:100,era_year:100,era:'CE',year_numbering:'astronomical'}},{person_id:'p',relation:'birth_place',status:'source_attested',date_expression:'元年正月',normalized_date:{year:100,era_year:100,era:'CE',year_numbering:'astronomical'}},{person_id:'p',relation:'death_place',status:'source_attested',date_expression:'二年',normalized_date:{year:101,era_year:101,era:'CE',year_numbering:'astronomical'}},{person_id:'f',relation:'birth_place',status:'source_attested',normalized_date:{year:1,era:'CE',era_year:1}},{person_id:'p',relation:'birth_place',status:'contextual_provisional',normalized_date:{year:2,era:'CE',era_year:2}}];
people.p.life_events.push({id:'alternative',person_id:'p',event_type:'birth',date_expression:'異說',normalized_date:{year:102,era_year:102,era:'CE',year_numbering:'astronomical'}});
await save();const dated=await(await generator(root)).project(people.p);assert.equal(dated.life.ages.filter(x=>x.approximate).length,2);assert.equal(dated.life.birth.length,2);assert.ok(dated.life.birth.some(x=>x.source_date==='甲子年／元年正月'));assert.ok(!dated.life.birth.some(x=>x.source_date==='某年'));assert.ok(dated.life.death[0].year_label);scan(dated);
const choices=structuredClone(people.p);choices.addresses=[];choices.life_events=[{id:'a',person_id:'p',event_type:'birth',date_expression:'元年',normalized_date:{year:100,era_year:100,era:'CE'}},{id:'b',person_id:'p',event_type:'birth',date_expression:'正月',normalized_date:{year:100,era_year:100,era:'CE'}}];choices.life_event_date_decisions=[{candidate_event_ids:['a','b'],status:'editorial_provisional',preferred_event_id:'a'}];const choiceSummary=await(await generator(root)).project(choices);assert.equal(choiceSummary.life.birth.length,2);assert.deepEqual(new Set(choiceSummary.life.birth.map(x=>x.choice)),new Set(['preferred','alternative']));
const regnal=structuredClone(choices);regnal.life_event_date_decisions=[];regnal.life_events=[{id:'a',person_id:'p',event_type:'birth',date_expression:'某帝元年'},{id:'b',person_id:'p',event_type:'birth',date_expression:'某帝二年'}];const regnalSummary=await(await generator(root)).project(regnal);assert.equal(regnalSummary.life.birth[0].source_date,'某帝元年／某帝二年');
// A retired endpoint must fail even though traceFamily catches loader errors.
people.p.relations.push(edge('retired','p','retired','father'));await save();await assert.rejects(async()=>await(await generator(root)).project(people.p),/inactive family/);people.p.relations.pop();
people.p.unresolved_relation_identity_groups[0].candidate_person_ids.push('retired');await save();await assert.rejects(async()=>await(await generator(root)).project(people.p),/inactive family/);people.p.unresolved_relation_identity_groups[0].candidate_person_ids.pop();
// Same production assembly path; no alternate genealogy algorithm.
delete people.p.relations[0];people.p.relations=people.p.relations.filter(Boolean);people.p.assembled_identity={person_id:'p',parent_person_id:'f',assembly_id:'assembly',status:'editorial_preferred',parent_connection:{type:'shared_father_through_sibling',status:'contextual_provisional',rationale:'父系暫定',references:[{quote:'原文'}]}};await save();const inferred=await(await generator(root)).project(people.p);assert.equal(inferred.family.ancestors[0][0].role,'assembly_inferred');assert.ok(inferred.family.ancestors[1][0].route_qualification.includes('assembly_inferred'));
await fs.mkdir(path.join(root,'data/corpus/summaries'),{recursive:true});await fs.writeFile(path.join(root,'data/corpus/summaries/retired.json'),'{}');await write(root);await assert.rejects(fs.stat(path.join(root,'data/corpus/summaries/retired.json')));assert.equal((await plan(root)).size,9);await assert.rejects(plan(root,['p','p']));await assert.rejects(plan(root,['../p']));await fs.unlink(path.join(dir,'u.json'));await assert.rejects(plan(root));
await fs.writeFile(path.join(dir,'index.json'),JSON.stringify({profiles:[{id:'p'},{id:'p'}]}));await assert.rejects(activeIds(root));await fs.rm(root,{recursive:true,force:true});});

test('Qin Shihuang typed birthplace/deathplace dates survive compact export', async () => {
 const codeRoot = fileURLToPath(new URL('..', import.meta.url));
 const g = await generator(codeRoot);
 const p = await g.load('ao3_0fy_d45_AAA');
 const summary = await g.project(p);
 assert.ok(summary.life.birth.some(row => row.year_label.includes('259')));
 assert.ok(summary.life.death.some(row => row.year_label.includes('210')));
});


test('published summaries match every current profile and contain no retired endpoint', async () => {
  const result = await check(fileURLToPath(new URL('..', import.meta.url)));
  assert.ok(result.summaries > 0);
});
