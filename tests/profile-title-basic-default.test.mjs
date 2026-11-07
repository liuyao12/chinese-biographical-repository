import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {personCard} from '../assets/cbr-person.js';
import {profileTitlePreference} from '../assets/profile-title.js';
import {setLocale} from '../assets/i18n.js';
import {directoryDisplay} from '../assets/corpus-discovery.js';
const read=path=>JSON.parse(fs.readFileSync(new URL('../'+path,import.meta.url),'utf8'));
const sourceCase=read('tests/profile-title-source-case.json');
function profile(){return structuredClone(sourceCase.profile);}
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

test('directory and person card share the exact source-backed title selection',()=>{
 const p=profile(),before=JSON.stringify(p);assert.equal(directoryDisplay(p,p.label).title,'太保');
 assert.equal(directoryDisplay(p,p.label).name,'王弘');
 p.default_profile_title.title='太傅';assert.notEqual(directoryDisplay(p,p.label).title,'太傅');
 p.default_profile_title.title='太保';assert.equal(JSON.stringify(p),before);
});

test('generated compact directory retains the exact validated profile title proof',()=>{
 const p=profile(),row=structuredClone(sourceCase.directory);
 assert.equal(profileTitlePreference(row)?.title,'太保');
 assert.equal(directoryDisplay(row,p.label).title,'太保');
 assert.equal(directoryDisplay(row,p.label).name,'王弘');
 const bad=structuredClone(row);bad.titles[0].attestations=[];
 assert.equal(profileTitlePreference(bad),null);
});
