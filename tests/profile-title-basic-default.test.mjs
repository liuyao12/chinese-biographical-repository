import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {personCard} from '../assets/cbr-person.js';
import {profileTitlePreference} from '../assets/profile-title.js';
import {setLocale} from '../assets/i18n.js';
const read=path=>JSON.parse(fs.readFileSync(new URL('../'+path,import.meta.url),'utf8'));
const prefix='corpus/songshu/063-wyd1739-wangtanshou-';
function profile(){
 const h=read(prefix+'titles.json').holdings[0],d=read(prefix+'profile-title.json').decisions[0];
 const names=read(prefix+'name-components.json').records.filter(n=>n.person_id===h.person_id);
 const legacy=read('data/corpus/profile-names.json').records.filter(n=>n.person_id===h.person_id);
 return {id:h.person_id,label:'王弘',name_components:[...legacy,...names],titles:[h],sources:[],relations:[],occurrences:[],default_profile_title:{decision_id:d.id,person_id:d.person_id,holding_id:d.holding_id,attestation_id:d.attestation_id,title:h.title,kind:h.kind,mode:h.mode,status:d.status,rationale:d.rationale,source_ref:d.source_ref}};
}
test('actual source holding/selection prefixes the source title/name and preserves raw component data',()=>{
 const p=profile(),before=JSON.stringify(p);assert.equal(profileTitlePreference(p).mode,'attestation');
 assert.ok(p.name_components.some(n=>n.title==='車騎將軍'));
 for(const full of[false,true]){
  const html=personCard(p,full),tag=full?'h1':'h3',at=html.indexOf('<'+tag),heading=html.slice(at,html.indexOf('</'+tag+'>',at)).replace(/<[^>]*>/g,'').replace(/\s/g,'');
  assert.equal(heading,'太保王弘');assert.match(html,/來源用稱/);assert.match(html,/編輯選稱/);assert.match(html,/person-profile-title-source/);
 }
 assert.equal(JSON.stringify(p),before);
});
test('wrong person, proposal endpoint, or arbitrary title cannot be a default heading',()=>{
 for(const change of['person','proposal','title']){
  const p=profile();
  if(change==='person')p.default_profile_title.person_id='another-person';
  if(change==='proposal')p.default_profile_title.holding_id='unassumed-proposal';
  if(change==='title')p.default_profile_title.title='太傅';
  assert.equal(profileTitlePreference(p),null);
 }
});
test('qualification is readable in English; no-preference legacy and partial-name branches are retained',()=>{
 const p=profile();setLocale('en',{persist:false});assert.match(personCard(p,true),/Source attestation/);assert.match(personCard(p,true),/Editorial profile title/);setLocale('zh-Hant',{persist:false});
 const legacy={id:'test-legacy',label:'王弘',name_components:[{surname:'王',ming:'弘',title:'車騎將軍'}]};assert.match(personCard(legacy),/<h3>車騎將軍 王弘<\/h3>/);
 const partial={id:'test-partial',label:'周閔',name_components:[{surname:null,ming:'閔',zi:'子騫'}]};assert.match(personCard(partial),/<h3>周閔<\/h3>/);
});
