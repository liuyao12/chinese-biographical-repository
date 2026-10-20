import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {personCard} from '../assets/cbr-person.js';
const production=JSON.parse(readFileSync(new URL('./fixtures/partial-name-title-profiles.json',import.meta.url),'utf8')).profiles;
const heading=(p,full)=>personCard(p,full).match(full?/<h1>(.*?)<\/h1>/s:/<h3>(.*?)<\/h3>/s)?.[1];
for(const [id,label] of [['3xx_gdy_or6_AAAA','周閔'],['2n6_7xk_5ov','江夏王義恭'],['9df_923_1a1','竟陵王義宣'],['r5s_lra_wfi','東甌王 廣武侯望']]) {
 test(`actual partial name keeps the whole canonical label without combining source rank: ${label}`,()=>{
  const p=production.find(x=>x.id===id);assert(p);const before=structuredClone(p);
  assert.equal(p.label,label);assert(p.name_components.some(x=>x.ming&&!x.surname));
  for(const full of [false,true])assert.equal(heading(p,full),label);
  assert.deepEqual(p,before); // This is a display decision; all source names/ranks/evidence survive.
 });
}
test('label fallback is independent of matching title prefixes, including incompatible ranks',()=>{
 for(const label of ['竟陵王義宣','東甌王 廣武侯望','既有爵望']) {
  const ming=label.endsWith('義宣')?'義宣':'望';
  const p={id:'synthetic',label,name_components:[{title:'完全不同的來源爵',surname:null,ming,quote:'合成原文'}]};
  for(const full of [false,true])assert.equal(heading(p,full),label);
 }
});
test('complete names, clan styles, surname-only, explicit full name and nonmatching labels keep their branches',()=>{
 const cases=[
  {label:'舊標籤',components:{title:'來源侯',surname:'甲',ming:'乙'},expected:'來源侯 甲乙'},
  {label:'舊標籤',components:{title:'來源侯',surname:null,ming:'乙',full_name:'原文全名'},expected:'來源侯 原文全名'},
  {label:'舊標籤',components:{title:'來源侯',surname:null,ming:'乙',clan_style:{value:'甲氏'}},expected:'來源侯 甲氏'},
  {label:'完整既有姓名',components:{title:'來源侯',surname:'甲',ming:null},expected:'來源侯 甲'},
  {label:'標籤不含本名',components:{title:'來源侯',surname:null,ming:'乙'},expected:'來源侯 乙'},
 ];
 for(const c of cases)for(const full of [false,true])assert.equal(heading({id:'synthetic',label:c.label,name_components:[c.components]},full),c.expected);
});

test('nine actual labels equal to their ming do not claim label completion or lose source titles',()=>{
 const fixtures=JSON.parse(readFileSync(new URL('./fixtures/partial-name-title-profiles.json',import.meta.url),'utf8')).equal_ming_label_profiles;
 const expected=new Map([['43i_62q_gf6','開陵侯 敖'],['4zn_n9v_k0v','戈船將軍 嚴'],['7ty_ab1_ab9','無錫侯 多軍'],['98i_dd4_aof','夜郎侯 多同'],['bvb_d1z_fd0_*A','南越王 胡'],['dzl_mvt_l93','馳義侯 遺'],['h0h_wsl_1nf','滇王 嘗羌'],['iw9_udd_jr2','下瀨將軍 甲'],['z9d_qn5_wg8','朝鮮相 路人']]);
 assert.equal(fixtures.length,9);
 for(const p of fixtures){const before=structuredClone(p);assert(p.name_components.some(x=>x.ming===p.label));for(const full of [false,true])assert.equal(heading(p,full),expected.get(p.id));assert.deepEqual(p,before);}
});
