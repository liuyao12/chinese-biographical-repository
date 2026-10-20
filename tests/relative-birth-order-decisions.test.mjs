import test from 'node:test';
import assert from 'node:assert/strict';
import {orderChildren} from '../assets/sibling-order.js';
import {personCard} from '../assets/cbr-person.js';

const raw={id:'r',subject_person_id:'B',object_person_id:'A',predicate:'brother',evidence:[],qualifiers:{relative_birth_order:{scope:'siblings',operator:'lt',older_person_id:'A',younger_person_id:'B'}}};
const decision={id:'d',assertion_id:'r',preferred_claim_id:null,rationale:'正文兩說相反。',claims:[
 {witness:{quote:'懷肅次弟懷敬',fixed_url:'https://example.org/fixed-song'}},
 {witness:{quote:'懐肅懐敬之弟也',fixed_url:'https://example.org/fixed-tongjian'}}]};

test('preferred sibling relation retains identity while unresolved age never orders children',()=>{
 const preferred={...raw,qualifiers:{source_term:'次弟'}};
 const person={id:'p',relations:[raw],preferred_relations:[preferred]};
 const entries=['B','A'].map(id=>({id,person}));
 assert.deepEqual(orderChildren(entries,person).entries.map(x=>x.id),['B','A']);
 assert.deepEqual(orderChildren(entries.map(x=>({...x,person:{...person,preferred_relations:undefined}})),{...person,preferred_relations:undefined}).entries.map(x=>x.id),['A','B']);
 assert.deepEqual(orderChildren(entries.map(x=>({...x,person:{...person,preferred_relations:[]}})),{...person,preferred_relations:[]}).entries.map(x=>x.id),['B','A']);
});

test('compact warning and full primary quotations distinguish disputed order from a preferred fact',()=>{
 const p={id:'A',label:'懷肅',relations:[raw],preferred_relations:[],relative_birth_order_decisions:[decision]};
 for(const full of [false,true]){
  const html=personCard(p,full);assert.match(html,/兄弟長幼有相反記載，未選定排序/);
  if(full){assert.match(html,/懷肅次弟懷敬/);assert.match(html,/懐肅懐敬之弟也/);assert.match(html,/fixed-tongjian/);}
 }
});

test('order warning follows locale while primary quotations remain unchanged',async()=>{
 const {setLocale}=await import('../assets/i18n.js');
 const p={id:'A',label:'懷肅',relative_birth_order_decisions:[decision]};
 try {setLocale('en');const html=personCard(p,true);assert.match(html,/Sibling age order has conflicting accounts/);assert.match(html,/Age-order accounts and sources/);assert.match(html,/Fixed source text/);assert.match(html,/懷肅次弟懷敬/);assert.match(html,/懐肅懐敬之弟也/);} finally {setLocale('zh-Hant');}
 assert.match(personCard(p,false),/兄弟長幼有相反記載/);
});
