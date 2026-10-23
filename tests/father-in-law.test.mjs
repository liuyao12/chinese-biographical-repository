import test from 'node:test';
import assert from 'node:assert/strict';
import {personCard} from '../assets/cbr-person.js';
import {setLocale} from '../assets/i18n.js';
const p={id:'subject',label:'婿甲',related_people:{father:'岳父甲'},relations:[{subject_person_id:'subject',predicate:'father_in_law',object_person_id:'father',qualifiers:{source_term:'女婿',spouse_person_id:null},evidence:[{work_id:'w-sanguozhi',book_id:'b-sanguozhi-026',chapter_id:'c-sanguozhi-026-guohuai',paragraph_id:'c-sanguozhi-026-guohuai:unit016',quote:'甲乙皆丙女婿'}]}]};
test('father-in-law has a readable source-backed label, without invented wives',()=>{setLocale('zh');const html=personCard(p,true);assert.match(html,/岳父/);assert.match(html,/女婿/);assert.match(html,/甲乙皆丙女婿/);assert.match(html,/來源原文/);assert.match(html,/unit016/);assert.doesNotMatch(html,/father_in_law/);assert.equal(p.relations[0].qualifiers.spouse_person_id,null);});
test('English label and unaltered Chinese source quote',()=>{setLocale('en');const html=personCard(p,true);assert.match(html,/Father-in-law/);assert.match(html,/甲乙皆丙女婿/);setLocale('zh');});
test('labels and source terms are escaped',()=>{const q=structuredClone(p);q.related_people.father='<script>bad</script>';q.relations[0].qualifiers.source_term='<img src=x onerror=1>';q.relations[0].evidence[0].quote='<script>quote</script>';const html=personCard(q,true);assert.doesNotMatch(html,/<script>|<img src=x/);assert.match(html,/&lt;script&gt;/);});
