import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {familyPersonLabel, traceFamily, namespaceNavigation} from '../assets/person-family.js';
import {generator} from '../scripts/export_person_summaries.mjs';
const person=(label,names,extra={})=>({id:'synthetic',label,name_components:names,...extra});

test('family labels use attested names without titles and keep conflicts or incomplete identity labels',()=>{
 const cases=[
  [person('秀',[{surname:'裴',ming:'秀',title:'鉅鹿公'}]),'裴秀'],
  [person('原稱',[{full_name:'宗敬'}]),'宗敬'],
  [person('某人之妻',[{surname:'王',clan_style:{value:'王氏'}}]),'王氏'],
  [person('裴秀',[{ming:'秀'}]),'裴秀'],
  [person('裴秀〔來源辨識附語〕',[{ming:'秀'}]),'裴秀〔來源辨識附語〕'],
  [person('未名裴氏女',[{surname:'裴'}]),'未名裴氏女'],
  [person('來源甲乙',[{surname:'裴',ming:'秀'},{surname:'裴',ming:'頠'}]),'來源甲乙'],
  [person('原稱',[{surname:'裴',ming:'秀',full_name:'王秀'}]),'原稱'],
  [person('原稱',[]),'原稱'],
  [{id:'missing'},'missing'],
  [{id:'given-only',name_components:[{ming:'秀'}]},'秀']
 ];
 for(const [input,want]of cases){const copy=structuredClone(input);assert.equal(familyPersonLabel(input),want);assert.deepEqual(input,copy);}
});

test('family names honor only the same exact preferred reading records as profile names',()=>{
 const records=[{id:'n1',person_id:'p',surname:'桓',ming:'温'},{id:'n2',person_id:'p',surname:'桓',ming:'溫'}];
 const choice={field:'ming',coverage:'listed_records_only',status:'editorial_provisional',human_reviewed:false,person_id:'p',source_values:['温','溫'],preferred_value:'溫',records:records.map(record=>({record:{id:record.id,person_id:'p'}}))};
 const p={id:'p',label:'原標籤',name_components:records,preferred_name_component_readings:[choice]};
 assert.equal(familyPersonLabel(p),'桓溫');
 assert.equal(familyPersonLabel({...p,preferred_name_component_readings:[]}), '原標籤');
 assert.equal(familyPersonLabel({...p,name_components:[...records,{id:'n3',person_id:'p',surname:'桓',ming:'温'}]}),'原標籤');
 assert.equal(familyPersonLabel({...p,preferred_name_component_readings:[{...choice,person_id:'other'}]}),'原標籤');
});

test('loaded relatives and inference path labels share names without extra lookup or changing missing fallbacks',async()=>{
 const connection={type:'shared_father_through_sibling',status:'contextual_provisional',rationale:'Synthetic sourced inference.',references:[{quote:'Synthetic father and sibling evidence.'}]};
 const a={id:'a',label:'秀',name_components:[{surname:'裴',ming:'秀'}],assembled_identity:{person_id:'a',parent_person_id:'f',assembly_id:'s',status:'editorial_preferred',parent_connection:connection},relations:[{subject_person_id:'a',object_person_id:'missing',predicate:'mother',evidence:[]}],related_people:{missing:'未載母名'}};
 const f={id:'f',label:'茂',name_components:[{surname:'裴',ming:'茂'}]};
 const calls=[];const family=await traceFamily(a,async id=>{calls.push(id);if(id==='f')return f;throw Error('unavailable');});
 assert.deepEqual(calls,['f','missing']);assert.equal(family.ancestors[0][0].label,'裴茂');
 const step=family.ancestors[0][0].ancestry_paths[0].steps[0];assert.equal(step.from_label,'裴秀');assert.equal(step.to_label,'裴茂');
 assert.equal(family.mother[0].label,'未載母名');assert.equal(family.mother[0].unavailable,true);assert.equal(f.label,'茂');
});

test('namespace roots use structured names and keep unavailable roots as their IDs',async()=>{
 const roots=['synthetic_A','synthetic_B'];const p={id:roots[0],assembled_identity:{namespace_id:'synthetic',root_person_id:null,namespace_entry_person_id:roots[0],collateral_root_group:{type:'unknown_shared_father_from_qualified_first_cousins',status:'contextual_provisional',references:[{quote:'Synthetic cousins.'}],root_person_ids:roots,common_parent_person_id:null,common_parent_name:null,common_parent_registered:false,relative_age:'unknown'}}};
 const calls=[];const out=await namespaceNavigation(p,async id=>{calls.push(id);if(id===roots[0])return{id,label:'甲',name_components:[{surname:'王',ming:'甲'}]};throw Error('missing');});
 assert.deepEqual(calls,roots);assert.equal(out.roots[0].label,'王甲');assert.equal(out.roots[1].label,roots[1]);assert.equal(out.roots[1].unavailable,true);
});

test('actual Pei Hui trace and one normal compact export name Pei Mao from existing structured evidence',async()=>{
 const root=fileURLToPath(new URL('..',import.meta.url));const g=await generator(root);const hui=await g.load('kbq_kjc_n2f_B');const mao=await g.load('kbq_kjc_n2f');
 assert.equal(mao.label,'茂');assert.ok(mao.name_components.some(n=>n.surname==='裴'&&n.ming==='茂'));
 const before=JSON.stringify(mao);const traced=await traceFamily(hui,g.load);assert.equal(traced.ancestors[0].find(x=>x.id===mao.id).label,'裴茂');
 const summary=await g.project(hui);assert.equal(summary.family.ancestors[0].find(x=>x.id===mao.id).label,'裴茂');
 assert.equal(JSON.stringify(mao),before);assert.ok(!JSON.stringify(summary.family).includes('"person":'));assert.ok(!JSON.stringify(summary.family).includes('"quote":'));
 const saved=JSON.parse(await fs.readFile(new URL('../data/corpus/profiles/kbq_kjc_n2f.json',import.meta.url),'utf8'));assert.equal(saved.label,'茂');
});
