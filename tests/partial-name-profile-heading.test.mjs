import test from 'node:test';
import assert from 'node:assert/strict';
import {personCard} from '../assets/cbr-person.js';
for (const full of [false,true]) {
 test(`partial source name preserves the existing person heading (${full ? 'profile' : 'card'})`,()=>{
  const raw={surname:null,ming:'閔',zi:'子騫',quote:'閔字子騫，方直有父風。',additional_names:[]};
  const before=JSON.stringify(raw);
  const html=personCard({id:'synthetic-min',label:'周閔',name_components:[raw]},full);
  assert.match(html,full ? /<h1>周閔<\/h1>/ : /<h3>周閔<\/h3>/);
  assert.match(html.replace(/<[^>]*>/g,''),/子騫/);
  assert.equal(JSON.stringify(raw),before);
  assert.equal(raw.surname,null);
 });
 test(`explicit unsplit full name remains authoritative (${full ? 'profile' : 'card'})`,()=>{
  const html=personCard({id:'synthetic-full',label:'舊標籤',name_components:[{full_name:'明載全名',ming:'名',surname:null}]},full);
  assert.match(html,full ? /<h1>明載全名<\/h1>/ : /<h3>明載全名<\/h3>/);
 });
}
