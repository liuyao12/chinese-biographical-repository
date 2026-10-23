import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {summarizeNameComponents} from '../assets/name-components.js';
import {personCard} from '../assets/cbr-person.js';
import {setLocale} from '../assets/i18n.js';
const all=JSON.parse(readFileSync(new URL('../corpus/jinshu/040-jiachong-family-name-components.json',import.meta.url),'utf8')).records;
const id=all.find(n=>n.source_name_usage).person_id;
const rows=all.filter(n=>n.person_id===id);
test('actual natal and heir-house surnames remain distinct usages without selecting a surname',()=>{
 for(const records of [rows,[...rows].reverse()]){
  const before=structuredClone(records),s=summarizeNameComponents(records);
  assert.equal(s.names.surname,undefined);assert.equal(s.canHead,false);assert.equal(s.coreConflict,true);
  assert.equal(s.conflicts.find(x=>x.field==='surname').context,'source_family_name_usage');
  for(const full of [false,true]){
   setLocale('zh-Hant');const html=personCard({id,label:'賈謐',name_components:records},full);
   assert.match(html,/原文家系稱用/);assert.match(html,/韓/);assert.match(html,/賈/);assert.doesNotMatch(html,/姓名構件有異說/);
  }
  assert.deepEqual(records,before);
 }
 setLocale('en');assert.match(personCard({id,label:'賈謐',name_components:rows},true),/Family-name usages in the source/);setLocale('zh-Hant');
});
test('missing, mixed or unbound usage evidence does not conceal a surname disagreement',()=>{
 const variants=[r=>delete r[0].source_name_usage,r=>r[0].source_name_usage.preferred=true,r=>r[0].source_name_usage.change_year=300,r=>r[0].source_name_usage.adoption_assertion_id='different-event',r=>r[0].source_name_usage.family_role='heir_family_designation',r=>r[0].source_name_usage.source_mention_id='wrong-mention',r=>r[0].person_id='another-person'];
 for(const mutate of variants){const records=structuredClone(rows);mutate(records);const s=summarizeNameComponents(records);assert.equal(s.conflicts.find(x=>x.field==='surname').context,undefined);assert.match(personCard({id,label:'賈謐',name_components:records},true),/姓名構件有異說/);}
});
test('a separate courtesy-name disagreement remains visible alongside family-name usages',()=>{
 const records=structuredClone(rows);records.push({...records[0],surname:null,zi:'另一字',source_name_usage:undefined});
 const html=personCard({id,label:'賈謐',name_components:records},true);
 assert.match(html,/原文家系稱用/);assert.match(html,/姓名構件有異說/);assert.match(html,/另一字/);
});
