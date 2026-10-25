import test from 'node:test';
import assert from 'node:assert/strict';
import {personCard} from '../assets/cbr-person.js';
import {traceFamily} from '../assets/person-family.js';
import {setLocale} from '../assets/i18n.js';
const relation=()=>({subject_person_id:'child',predicate:'maternal_role',object_person_id:'principal',qualifiers:{role:'principal_mother',source_term:'嫡母',biological_mother:null},evidence:[]});
const person=(r=relation())=>({id:'child',label:'來源主體',related_people:{principal:'來源婦人'},relations:[r]});
test('explicit principal mother retains qualified source role in Chinese and English',()=>{
 try{for(const [locale,label]of[['zh-Hant','嫡母（原文稱謂）'],['en','Principal mother (source wording)']]){setLocale(locale,{persist:false});const p=person(),before=JSON.stringify(p),html=personCard(p,true);assert(html.includes(label));assert.match(html,/<p>嫡母<\/p>/);assert.equal(JSON.stringify(p),before);assert.doesNotMatch(html,/後母：|生母：/);}}finally{setLocale('zh-Hant',{persist:false});}
});
test('unknown or missing roles, wrong source term and biological claims cannot acquire principal label',()=>{
 for(const q of[{role:'unknown',source_term:'嫡母',biological_mother:null},{source_term:'嫡母',biological_mother:null},{role:'principal_mother',source_term:'母',biological_mother:null},{role:'principal_mother',source_term:'嫡母',biological_mother:true},{role:'principal_mother',source_term:'嫡母'}]){const r=relation();r.qualifiers=q;const html=personCard(person(r),true);assert.doesNotMatch(html,/嫡母（原文稱謂）/);assert.match(html,/母（未明生育）/);}
});
test('principal role does not replace the existing prior mother or unspecified role labels',()=>{
 for(const[role,label]of[['prior_mother','前母（原稱）'],['mother_unspecified','母（未明生育）']]){const r=relation();r.qualifiers.role=role;assert(personCard(person(r),true).includes(label));}
});
test('the principal role is never a birth mother, stepmother, spouse or child traversal edge',async()=>{
 const p=person();const family=await traceFamily(p,async id=>({id,label:id}));assert.deepEqual(family.mother,[]);assert.deepEqual(family.spouses,[]);assert.deepEqual(family.children,[]);
 const reverse={id:'principal',label:'來源婦人',relations:p.relations};assert.deepEqual((await traceFamily(reverse,async id=>({id,label:id}))).children,[]);
});
test('a separate explicit birth mother edge remains distinct from the source principal role',async()=>{
 const p=person();p.relations.push({subject_person_id:'child',predicate:'mother',object_person_id:'birth',evidence:[]});const f=await traceFamily(p,async id=>({id,label:id}));assert.deepEqual(f.mother.map(x=>x.id),['birth']);assert.deepEqual(f.spouses,[]);assert(personCard(p,true).includes('嫡母（原文稱謂）'));
});
test('absence omits role fields and compact cards do not invent a principal mother summary',()=>{
 assert.doesNotMatch(personCard({id:'child',label:'來源主體'},true),/嫡母|來源所記親屬/);assert.doesNotMatch(personCard(person(),false),/嫡母/);
});
test('literal source text is escaped and does not activate a mismatched role',()=>{
 const r=relation();r.qualifiers.source_term='嫡母<script>';const html=personCard(person(r),true);assert.match(html,/嫡母&lt;script&gt;/);assert.doesNotMatch(html,/<script>|嫡母（原文稱謂）/);
});
test('another predicate cannot acquire the source principal mother label',()=>{
 const r=relation();r.predicate='stepmother';const html=personCard(person(r),true);assert.match(html,/後母/);assert.doesNotMatch(html,/嫡母（原文稱謂）/);
});
