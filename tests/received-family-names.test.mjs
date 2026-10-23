import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {personCard} from '../assets/cbr-person.js';
import {summarizeNameComponents} from '../assets/name-components.js';
import {setLocale} from '../assets/i18n.js';
const read=p=>JSON.parse(fs.readFileSync(new URL(p,import.meta.url),'utf8'));
const n=read('../corpus/sanguozhi/026-guohuai-name-components.json').records;
const g=read('../corpus/jinshu/043-wangyan-wife-name-components.json').records;
const chapter=read('../corpus/sanguozhi/026-guohuai.json');
const p=record=>({id:record.person_id,label:'來源省稱〔保留登記〕',name_components:[record],relations:[],sources:[],related_people:{}});
test('actual received male names and courtesy words render, preserving source quote',()=>{
 setLocale('zh');
 for(const r of n.filter(r=>r.ming)){
  const html=personCard(p(r),true);
  assert.match(html,new RegExp(`<h1>${r.surname}${r.ming}</h1>`));
  if(r.zi)assert.ok(html.includes(r.zi));
  assert.ok(html.includes(r.quote));
  assert.equal(p(r).label,'來源省稱〔保留登記〕');
 }
});
test('two women show clan only and do not invent given names',()=>{
 for(const r of [...n,...g].filter(r=>r.clan_style)){
  const html=personCard(p(r),true);assert.ok(html.includes(`<h1>${r.surname}氏</h1>`));assert.equal(r.ming,null);assert.doesNotMatch(html,/<h1>[^<]*(null|undefined)/);
 }
});
test('real Taiye/Daye source values stay a nonpreferred conflict, invariant under order',()=>{
 const r=n.find(r=>r.ming==='奕');
 const c=read('../corpus/jinshu/045-guoyi.json');const q=c.paragraphs.find(p=>p.text.includes('字大業'));
 assert.ok(q);const other={...r,id:'display-test-045-source-record',chapter_id:c.id,paragraph_id:q.id,quote:q.text,zi:'大業'};
 for(const rows of [[r,other],[other,r]]){
  const summary=summarizeNameComponents(rows);assert.equal(summary.names.zi,undefined);assert.deepEqual(new Set(summary.conflicts.find(x=>x.field==='zi').values),new Set(['泰業','大業']));
  const html=personCard({...p(r),name_components:rows},true);assert.ok(html.includes('<h1>郭奕</h1>'));assert.ok(html.includes('泰業'));assert.ok(html.includes('大業'));
 }
});
