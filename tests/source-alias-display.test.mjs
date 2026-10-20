import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
const root=process.env.CBR_QA_ROOT || fileURLToPath(new URL('../',import.meta.url));
import {personCard} from '../assets/cbr-person.js';
const alias=html=>html.match(/<p class="person-aliases">(.*?)<\/p>/)?.[1].replace(/<[^>]*>/g,'')||'';
const sourceNames=html=>html.match(/<details class="person-source-names">(.*?)<\/details>/s)?.[1]||'';
for(const full of [false,true]){
 test(`untyped source kinship/title/pronoun remain source expressions only (${full})`,()=>{
  for(const names of [['男','子'],['公','中軍大將軍'],['臣','帝'],['子']]){
   const p={id:'synthetic',label:'已知人物',names};const before=JSON.stringify(p);const html=personCard(p,full);assert.equal(alias(html),'');for(const n of names)assert(sourceNames(html).includes(n));assert.equal(JSON.stringify(p),before);
  }
 });
 test(`an explicitly named 子 is preserved without a lexical blacklist (${full})`,()=>{
  const p={id:'synthetic',label:'甲子',names:['子'],name_components:[{surname:'甲',ming:'子',additional_names:['別名乙'],quote:'合成姓名依據'}]};const html=personCard(p,full);assert.match(html,new RegExp(`<h${full?1:3}>甲子<`));assert.equal(alias(html),'別名乙');assert(sourceNames(html).includes('子'));assert(html.includes('合成姓名依據'));
 });
 test(`typed courtesy and childhood names remain badges (${full})`,()=>{
  const p={id:'synthetic',label:'甲乙',names:['公','子','臣'],name_components:[{surname:'甲',ming:'乙',zi:'子丙',xiaozhi:'子',additional_names:[],quote:'合成姓名依據'}]};const html=personCard(p,full);assert.equal(alias(html),'字 子丙 小字 子');assert(sourceNames(html).includes('公、子、臣'));
 });
 test(`real He Yan child preserves profile data and raw source names (${full})`,()=>{
  const p=JSON.parse(readFileSync(root+'/data/corpus/profiles/0db_22c_332_*AA.json'));const before=JSON.stringify(p);assert.deepEqual(p.names,['男','子']);const html=personCard(p,full);assert.equal(alias(html),'');assert(sourceNames(html).includes('男、子'));assert(html.includes('五六'));assert.equal(JSON.stringify(p),before);
 });
}
