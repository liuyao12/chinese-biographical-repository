import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {personCard} from '../assets/cbr-person.js';
import {summarizeNameComponents,nameAliases} from '../assets/name-components.js';
const data=JSON.parse(readFileSync(new URL('../corpus/jinshu/040-jiachong-family-name-components.json',import.meta.url),'utf8')).records;
test('actual Han/Jia source usages remain readable without first-record surname selection',()=>{
 const uses=data.filter(n=>n.source_name_usage), id=uses[0].person_id, rows=data.filter(n=>n.person_id===id);
 for(const ordered of [rows,[...rows].reverse()]) {
  const s=summarizeNameComponents(ordered);
  assert.equal(s.coreConflict,true);assert.equal(s.canHead,false);assert.equal(s.names.surname,undefined);
  assert.deepEqual([...s.conflicts.find(c=>c.field==='surname').values].sort(),['賈','韓'].sort());
  const aliases=nameAliases(s.names).map(a=>a.value);assert.ok(aliases.includes('本源稱韓謐'));assert.ok(aliases.includes('本源稱賈謐'));assert.ok(aliases.includes('長深'));
 }
});
test('actual also-called names are readable without implying former-name chronology',()=>{
 const rows=data.filter(n=>n.additional_name_components?.length);assert.equal(rows.length,2);
 for(const n of rows){const s=summarizeNameComponents([n]);assert.ok(nameAliases(s.names).some(a=>a.value===`一名${n.additional_name_components[0].value}`));assert.equal(s.names.former_ming,undefined);}
});
test('actual unnamed clan profiles omit invented ming and courtesy fields',()=>{
 for(const n of data.filter(n=>n.fixed_biography_name_binding.mode==='clan_only')){const s=summarizeNameComponents([n]);assert.equal(s.names.ming,undefined);assert.equal(s.names.zi,undefined);assert.equal(s.names.clan_style.value,n.surname+'氏');}
});

const labels=new Map(JSON.parse(readFileSync(new URL('../registry/persons.json',import.meta.url),'utf8')).persons.map(p=>[p.id,p.label]));
test('actual surname-only source data preserves existing headings in compact and full profiles',()=>{
 for(const n of data.filter(n=>['role_only','surname_title'].includes(n.fixed_biography_name_binding.mode))){
  const p={id:n.person_id,label:labels.get(n.person_id),name_components:data.filter(x=>x.person_id===n.person_id)};
  for(const full of [false,true]){const html=personCard(p,full),heading=html.match(/<h[13]>(.*?)<\/h[13]>/)?.[1];assert.equal(heading,p.label);assert.notEqual(heading,n.surname);assert.ok(!heading.includes('null'));assert.ok(!heading.includes('undefined'));}
 }
});
