import test from 'node:test';
import assert from 'node:assert/strict';
import {personCard} from '../assets/cbr-person.js';
import {profileTitlePreference} from '../assets/profile-title.js';
function fixture(){
 const r={work_id:'w-jinshu',book_id:'b-fixture',source_id:'s-fixture',chapter_id:'c-fixture',paragraph_id:'p-fixture',person_mention_id:'m-fixture',start:4,end:6,surface:'太傅'};
 const h={id:'holding',person_id:'synthetic',title:'太傅',kind:'office',mode:'posthumous_grant',status:'source_attested',attestations:[{id:'attestation',...r}],evidence:[{...r,quote:'某人追贈太傅'}]};
 const d={decision_id:'choice',person_id:'synthetic',holding_id:'holding',attestation_id:'attestation',title:'太傅',kind:'office',mode:'posthumous_grant',status:'editorial_provisional',source_ref:r,rationale:'Synthetic choice.'};
 return{id:'synthetic',label:'陳某',name_components:[{surname:'陳',ming:'某',additional_names:[]}],titles:[h],default_profile_title:d};
}
test('card and full title display a source-bound posthumous title with visible qualification',()=>{
 for(const full of[false,true]){const html=personCard(fixture(),full);assert.match(html,new RegExp(`<h${full?1:3}>太傅 陳某</h`));assert.match(html,/追贈/);assert.match(html,/編輯選稱/);assert.match(html,/class="person-profile-title-source"/);assert.match(html,/mention=m-fixture/);assert.doesNotMatch(html,/生前太傅/);}
});
test('legacy headings remain byte-equal when no preference exists',()=>{
 const p=fixture();delete p.default_profile_title;const plain=personCard(p,true);const bad={...p,default_profile_title:{}};assert.equal(personCard(bad,true),plain);assert.match(plain,/<h1>陳某<\/h1>/);
 p.name_components[0].title='舊稱';assert.match(personCard(p,true),/<h1>舊稱 陳某<\/h1>/);
});
test('partial names keep the whole label and show title separately, without guessing surname',()=>{
 const p=fixture();p.label='陳某';p.name_components=[{surname:null,ming:'某',additional_names:[]}];const html=personCard(p,true);assert.match(html,/<h1>陳某<\/h1>/);assert.match(html,/<strong>太傅<\/strong>/);assert.doesNotMatch(html,/<h1>太傅 某/);
});
test('an explicit preference supersedes display only, preserving the old name title as source evidence',()=>{
 const p=fixture();p.name_components[0].title='舊稱';p.name_components[0].quote='舊稱陳某';const html=personCard(p,true);assert.match(html,/<h1>太傅 陳某<\/h1>/);assert.match(html,/本筆姓名來源所列稱號：舊稱/);assert.equal(p.name_components[0].title,'舊稱');
});
test('mismatched person, mode, title and source cannot be used',()=>{
 for(const [key,val]of[['person_id','other'],['mode','grant'],['title','太傅侯']]){const p=fixture();p.default_profile_title[key]=val;assert.equal(profileTitlePreference(p),null);}
 const p=fixture();p.default_profile_title.source_ref={...p.default_profile_title.source_ref,chapter_id:'wrong'};assert.equal(profileTitlePreference(p),null);
});
test('unassumed or challenged office cannot be substituted and unknown choices hide',()=>{
 for(const mode of['attestation','not_assumed']){const p=fixture();p.default_profile_title.mode=p.titles[0].mode=mode;assert.equal(profileTitlePreference(p),null);}
 const p=fixture();p.titles[0].source_qualification={kind:'reported_office_challenged_by_commentary'};assert.equal(profileTitlePreference(p),null);
});
test('source text is escaped, not injected',()=>{
 const p=fixture();p.titles[0].title=p.titles[0].attestations[0].surface=p.default_profile_title.title=p.default_profile_title.source_ref.surface='<x>';const html=personCard(p,true);assert.doesNotMatch(html,/<x>/);assert.match(html,/&lt;x&gt;/);
});
