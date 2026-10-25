import test from 'node:test';
import assert from 'node:assert/strict';
import {personCard} from '../assets/cbr-person.js';
import {profileTitlePreference} from '../assets/profile-title.js';
import {summarizeNameComponents} from '../assets/name-components.js';
import {setLocale} from '../assets/i18n.js';
function fixture(){
 const id='synthetic-profile';
 const r={work_id:'w-jinshu',book_id:'b-jinshu-035',source_id:'source-synthetic',chapter_id:'c-jinshu-035-peiwei',paragraph_id:'p-synthetic',person_mention_id:'m-synthetic',start:1,end:6,surface:'尚書左僕射'};
 const holding={id:'holding-synthetic',person_id:id,title:r.surface,kind:'office',mode:'grant',status:'source_attested',attestations:[{id:'attestation-synthetic',...r}],evidence:[{...r,quote:'Synthetic title source'}]};
 return{id,label:'裴頠',name_components:[{person_id:id,surname:'裴',ming:'頠',zi:'逸民',quote:'Synthetic source 頠字逸民',additional_names:[]},{person_id:id,surname:'裴',ming:'顗',quote:'Synthetic source 裴顗',additional_names:[]}],titles:[holding],default_profile_title:{decision_id:'choice-synthetic',person_id:id,holding_id:holding.id,attestation_id:'attestation-synthetic',title:holding.title,kind:holding.kind,mode:holding.mode,status:'editorial_provisional',source_ref:r}};
}
const heading=(p,full)=>personCard(p,full).match(new RegExp(`<h${full?1:3}>([\\s\\S]*?)</h${full?1:3}>`))?.[1];
test('validated title prefixes the exact existing fallback label while core alternatives remain in both cards/locales',()=>{
 try{for(const locale of ['zh-Hant','en']){setLocale(locale,{persist:false});for(const full of [false,true]){
  const p=fixture(),before=JSON.stringify(p),nameBefore=summarizeNameComponents(p.name_components);assert.equal(nameBefore.coreConflict,true);assert.equal(nameBefore.canHead,false);assert.equal(profileTitlePreference(p)?.title,'尚書左僕射');
  const html=personCard(p,full);assert.equal(heading(p,full),'尚書左僕射 裴頠');assert.match(html,/頠／顗/);assert.match(html,/person-name-conflict/);assert.match(html,/person-profile-title-source/);assert.match(html,/mention=m-synthetic/);assert.equal(JSON.stringify(p),before);assert.deepEqual(summarizeNameComponents(p.name_components),nameBefore);assert.equal(p.preferred_name_component_readings,undefined);
 }}}finally{setLocale('zh-Hant',{persist:false});}
});
test('fallback label containing alternative forms is kept whole without picking a source spelling',()=>{
 const p=fixture();p.label='裴頠／裴顗';for(const full of[false,true])assert.equal(heading(p,full),'尚書左僕射 裴頠／裴顗');
});
test('partial name still preserves the established label and separate qualified title',()=>{
 const p=fixture();p.name_components=[{surname:null,ming:'頠',additional_names:[]}];for(const full of[false,true]){assert.equal(heading(p,full),'裴頠');assert.match(personCard(p,full),/<strong>尚書左僕射<\/strong>/);}
});
test('no name evidence or only courtesy-name data does not expand the fallback rule',()=>{
 for(const names of[undefined,[],[{zi:'逸民',additional_names:[]}]]){const p=fixture();p.name_components=names;for(const full of[false,true])assert.equal(heading(p,full),'裴頠');}
});
test('empty and missing fallback labels do not produce a title-only core-conflict heading',()=>{
 for(const label of['',undefined]){const p=fixture();p.label=label;for(const full of[false,true])assert.notEqual(heading(p,full),'尚書左僕射 ');}
});
test('an already prefixed fallback label is never given the same title twice',()=>{
 for(const label of['尚書左僕射 裴頠','尚書左僕射裴頠']){const p=fixture();p.label=label;for(const full of[false,true])assert.equal(heading(p,full),label);}
});
test('wrong-person, missing holding, mismatched source and bare label-title choices stay ineligible',()=>{
 for(const change of['person','holding','source','bare']){const p=fixture();if(change==='person')p.default_profile_title.person_id='another-person';if(change==='holding')p.titles=[];if(change==='source')p.default_profile_title.source_ref={...p.default_profile_title.source_ref,surface:'合成官'};if(change==='bare')delete p.default_profile_title;assert.equal(profileTitlePreference(p),null);for(const full of[false,true])assert.equal(heading(p,full),'裴頠');}
});
test('fallback label markup remains escaped without being replaced by reconstructed name fragments',()=>{
 const p=fixture();p.label='<b>裴頠／裴顗</b>';for(const full of[false,true]){assert.equal(heading(p,full),'尚書左僕射 &lt;b&gt;裴頠／裴顗&lt;/b&gt;');assert.doesNotMatch(personCard(p,full),/<b>裴頠/);}
});
test('uncontested personal-name path still uses the selected title rather than combining old titles',()=>{
 const p=fixture();p.name_components=[{surname:'裴',ming:'頠',title:'合成舊官',additional_names:[]}];for(const full of[false,true])assert.equal(heading(p,full),'尚書左僕射 裴頠');
});

test('an uncontested personal name beginning with the same character as a short title is not stripped or suppressed',()=>{
 const p=fixture();p.name_components=[{surname:'成公',ming:'綏',additional_names:[]}];p.titles[0].title=p.default_profile_title.title='成';p.titles[0].kind=p.default_profile_title.kind='honorific';p.titles[0].mode=p.default_profile_title.mode='posthumous_naming';p.titles[0].attestations[0].surface=p.default_profile_title.source_ref.surface='成';p.titles[0].attestations[0].end=p.default_profile_title.source_ref.end=2;assert(profileTitlePreference(p));for(const full of[false,true])assert.equal(heading(p,full),'成 成公綏');
});
