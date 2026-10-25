import test from 'node:test';
import assert from 'node:assert/strict';
import {personCard} from '../assets/cbr-person.js';
import {profileTitlePreference} from '../assets/profile-title.js';
function fixture(){
 const r={work_id:'w-jinshu',book_id:'book-test',source_id:'source-test',chapter_id:'chapter-test',paragraph_id:'paragraph-test',person_mention_id:'subject-test',start:8,end:11,surface:'關内侯'};
 const unknown={status:'unknown',date_expression:null,evidence:[]};
 const h={id:'holding-test',person_id:'person-test',title:'關内侯',kind:'noble_rank',mode:'attestation',status:'source_attested',appointment_role:'source_attested_use',source_career_role:{kind:'attached_received_biography_frame',frame:'trusted-source-frame'},effective_period:{start:unknown,end:unknown},attestations:[{id:'att-test',...r}],evidence:[{...r,quote:'祖甲仕某朝官至長史關内侯'}]};
 const d={decision_id:'choice-test',person_id:'person-test',holding_id:h.id,attestation_id:'att-test',title:h.title,kind:h.kind,mode:h.mode,status:'editorial_provisional',source_ref:r};
 return{id:'person-test',label:'崔某',name_components:[{surname:'崔',ming:'某',additional_names:[]}],titles:[h],default_profile_title:d};
}
test('source-used noble rank is explicitly qualified in compact and full headings',()=>{
 for(const full of[false,true]){const p=fixture(),html=personCard(p,full);assert.equal(profileTitlePreference(p).mode,'attestation');assert.match(html,new RegExp(`<h${full?1:3}>關内侯 崔某</h`));assert.match(html,/來源用稱/);assert.match(html,/編輯選稱/);assert.match(html,/mention=subject-test/);assert.doesNotMatch(html,/已授|追贈/);assert.equal(p.titles[0].effective_period.start.date_expression,null);}
});
test('bare legacy attestations, wrong type or manufactured service are not heading choices',()=>{
 for(const mode of['no_frame','office','dated']){const p=fixture();if(mode==='no_frame')delete p.titles[0].source_career_role;else if(mode==='office')p.titles[0].kind=p.default_profile_title.kind='office';else p.titles[0].effective_period.start={status:'source_event',date_expression:'某年'};assert.equal(profileTitlePreference(p),null);}
});
test('partial name still preserves existing whole label and displays source title separately',()=>{
 const p=fixture();p.name_components=[{surname:null,ming:'某',additional_names:[]}];const html=personCard(p,true);assert.match(html,/<h1>崔某<\/h1>/);assert.match(html,/<strong>關内侯<\/strong>/);assert.match(html,/來源用稱/);
});
