import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {personCard,loadPerson} from '../assets/cbr-person.js';
import {sourceDetailsHTML,dutyObservationHTML} from '../assets/person-source-details.js';
import {setLocale} from '../assets/i18n.js';
const evidence=(paragraph='synthetic:report',quote='合成原文')=>({work_id:'w-synthetic',book_id:'b-synthetic-1',source_id:'s-synthetic',chapter_id:'synthetic',paragraph_id:paragraph,person_mention_id:paragraph+':m1',quote});
const q={kind:'reported_office_challenged_by_commentary',reported_work_id:'w-quoted-synthetic',objection_evidence:evidence('synthetic:critique','合成注家異議'),interpretation_note:'合成限定',preferred_historical_office_assertion_id:null};
const title={id:'synthetic-report',title:'合成官',kind:'office',mode:'attestation',period:'未定 → 未定',evidence:[evidence()],source_qualification:q};
const person={id:'synthetic-person',label:'合成人',source_work_titles:{'w-synthetic':'合成史','w-quoted-synthetic':{title:'合成引書'}},titles:[title]};
const details=[
 {id:'synthetic-1',person_id:person.id,kind:'official_duty',source_term:'掌選舉',values:{duty_code:'personnel_selection',office_source_name:'合成官'}},
 {id:'synthetic-2',person_id:person.id,kind:'official_duty',source_term:'總署行臺',values:{duty_code:'general_administration_of_mobile_secretariat',organ_source_name:'行臺'}},
 {id:'synthetic-3',person_id:person.id,kind:'command_authority',source_term:'詔合成群受某節度',values:{authority_code:'command_over_source_group',subordinate_group_source_name:'合成群'}},
 {id:'synthetic-4',person_id:person.id,kind:'fief_household_count',source_term:'增邑二千六百尸',values:{aggregation:'cumulative_across_unspecified_awards',increase:2600,total:null,unit_source_name:'尸',actual_revenue:null}},
 {id:'synthetic-5',person_id:person.id,kind:'unnamed_family_title_grants',source_term:'賜子弟一人亭侯二人關内侯',values:{recipient_group_source_term:'子弟',recipient_person_ids:[],biological_children_only:false,grants:[{source_rank:'亭侯',recipient_count:1},{source_rank:'關内侯',recipient_count:2}]}}
].map(d=>({...d,interpretation_note:'合成限定：未知未補。',evidence:[evidence('synthetic:detail',d.source_term)]}));
const observation={kind:'source_duty_event_observation_window',duration:false,tenure_boundary:false,calendar:'chinese_civil',precision:'year_range',earliest:257,latest:258,record_id:details[1].id,person_id:person.id,local_context:{surface:'合成局部職掌原文'},proof:{url:'https://example.org/fixed',anchors:{rebellion:{quote:'合成紀年原文'}}},calendar_reference:{url:'https://example.org/calendar'},rationale:'合成觀察，非任期。'};
test('challenged title row visibly labels the report and opens both source quotations and work names',()=>{
 const html=personCard(person,true);assert.match(html,/<strong>合成官<\/strong><small class="person-office-source-warning">/);assert.match(html,/引書用稱 · 注家存疑/);assert.match(html,/合成引書/);assert.match(html,/合成史/);assert.match(html,/合成注家異議/);assert.match(html,/未選為確定實任/);
 const links=[...html.matchAll(/class="person-detail-source-link" href="([^"]+)"/g)].map(m=>new URL(m[1].replaceAll('&amp;','&'),'https://example.invalid/'));assert(links.some(u=>new URLSearchParams(u.hash.slice(1)).get('passage')==='synthetic:report'));assert(links.some(u=>new URLSearchParams(u.hash.slice(1)).get('passage')==='synthetic:critique'));
});
test('qualification participates in group identity instead of disappearing into an identical normal office',()=>{
 const normal={...title,id:'synthetic-normal',source_qualification:undefined};const html=personCard({...person,titles:[normal,title]},true);assert.equal((html.match(/class="person-title"/g)||[]).length,2);assert.equal((html.match(/class="person-office-source-warning"/g)||[]).length,1);
});
test('challenged holding cannot acquire a preferred-reading label and compact display prioritizes normal titles',()=>{
 const p={...person,preferred_title_readings:[{holding_id:title.id,preferred_title:'不應成為首選',source_title:title.title}],titles:[title,...['甲官','乙官'].map((name,i)=>({...title,id:'synthetic-normal-'+i,title:name,source_qualification:undefined}))]};
 assert.doesNotMatch(personCard(p,true),/不應成為首選/);assert.doesNotMatch(personCard(p,false),/person-office-source-warning/);assert.match(personCard(person,false),/引書用稱 · 注家存疑/);
});
test('all five detail types render labels, original terms, qualifiers and source links without turning groups into children',()=>{
 const html=sourceDetailsHTML({...person,source_details:details});for(const s of ['選舉職掌','行臺職掌','節度權限','累計增邑','子弟授爵（未具名）','2600尸','原記受授人數：1','原記受授人數：2','並非已辨識子女名單','合成限定'])assert(html.includes(s),s);
 assert.equal((html.match(/class="person-source-detail"/g)||[]).length,5);assert.doesNotMatch(html,/2600戶|原記總數|實收|null|undefined|person\.html/);assert.equal((html.match(/person-detail-source-link/g)||[]).length,5);
});
test('full page wires details while compact card omits the extra section',()=>{
 const p={...person,source_details:details};assert.match(personCard(p,true),/person-source-details/);assert.doesNotMatch(personCard(p,false),/person-source-details/);
});
test('lecture duty resolves its explicitly linked office for the same person without inventing another office',()=>{
 const duty={...details[0],source_term:'侍講',values:{duty_code:'lecture_attendance',independent_substantive_office:false,office_title_holding_id:'synthetic-linked-office'}};
 const office={...title,id:'synthetic-linked-office',person_id:person.id,title:'合成常侍',source_qualification:undefined};
 const html=sourceDetailsHTML({...person,titles:[office],source_details:[duty]});
 assert.match(html,/侍講職掌/);assert.match(html.replace(/<[^>]*>/g,''),/所屬官稱：合成常侍/);assert.doesNotMatch(html,/獨立實官|null|undefined/);
 const mismatched=sourceDetailsHTML({...person,titles:[{...office,person_id:'another-person'}],source_details:[duty]});
 assert.doesNotMatch(mismatched,/合成常侍|所屬官稱/);assert.match(mismatched,/侍講職掌/);
});
test('missing details and unknown optional scalar fields do not produce empty fields',()=>{
 assert.equal(sourceDetailsHTML(person),'');assert.equal(sourceDetailsHTML({...person,source_details:[{source_term:null}]}),'');const html=sourceDetailsHTML({...person,source_details:[{...details[3],values:{increase:null,total:null,unit_source_name:null}}]});assert.doesNotMatch(html,/原記增加|原記總數|null|undefined/);
});
test('unknown existing detail kind retains source wording and qualification without dumping machine fields',()=>{
 const html=sourceDetailsHTML({...person,source_details:[{...details[0],kind:'unknown-future-kind',values:{secret:'do-not-dump'}}]});assert.match(html,/掌選舉/);assert.match(html,/合成限定/);assert.doesNotMatch(html,/do-not-dump/);
});
test('every rendered source string is escaped and unsafe source/reference URLs cannot create script links',()=>{
 const unsafe='<img src=x onerror=alert(1)>';const bad={...person,source_work_titles:{'w-synthetic':unsafe,'w-quoted-synthetic':unsafe},titles:[{...title,title:unsafe,source_qualification:{...q,interpretation_note:unsafe,objection_evidence:{...evidence(),work_id:'javascript:bad',quote:unsafe,url:'javascript:bad'}}}]};
 const html=personCard(bad,true)+sourceDetailsHTML({...bad,source_details:[{...details[4],id:unsafe,source_term:unsafe,interpretation_note:unsafe,values:{...details[4].values,grants:[{source_rank:unsafe,recipient_count:1}]},evidence:[{...evidence(),work_id:'javascript:bad',quote:unsafe}]}]});assert.doesNotMatch(html,/<img|href="javascript:|onerror="/);assert.match(html,/&lt;img/);
});
test('observation window is displayed as non-tenure with expandable primary/calendar evidence',()=>{
 const d={...details[1],date_observation:observation};const html=dutyObservationHTML(d,person);assert.match(html,/職掌見於257–258年間；非任期/);assert.match(html,/合成紀年原文/);assert.match(html,/https:\/\/example.org\/fixed/);assert.match(html,/年號對照/);assert.doesNotMatch(html,/原記時長|任職257/);
});
test('duration flags, precision and subject/record identity are mandatory for an observation label',()=>{
 for(const patch of [{duration:true},{tenure_boundary:true},{precision:'day'},{earliest:'257'},{person_id:'other'},{record_id:'other'}])assert.equal(dutyObservationHTML({...details[1],date_observation:{...observation,...patch}},person),'');assert.equal(dutyObservationHTML(details[1],person),'');
});
test('unsafe observation witness links are omitted and observation text remains escaped',()=>{
 const html=dutyObservationHTML({...details[1],date_observation:{...observation,proof:{url:'javascript:bad',anchors:{era:{quote:'<script>bad</script>'}}},calendar_reference:{url:'data:bad'},rationale:'<b>bad</b>'}},person);assert.doesNotMatch(html,/href="(?:javascript|data):|<script>|<b>/);assert.match(html,/&lt;script&gt;/);
});
test('rendering preserves all source data including future optional event_observation fields',()=>{
 const p=structuredClone({...person,source_details:details});p.source_details[1].date_observation=observation;p.source_details[0].event_observation={future:'preserve',duration:false};const before=JSON.stringify(p);personCard(p,true);assert.equal(JSON.stringify(p),before);
});
test('English labels switch while Chinese received wording remains untouched',()=>{
 try{setLocale('en');const html=personCard({...person,source_details:details},true);assert.match(html,/Quoted office name · questioned by commentator/);assert.match(html,/Cumulative fief increase/);assert.match(html,/增邑二千六百尸/);}finally{setLocale('zh-Hant');}
});
test('actual native Chen Tai profile keeps five details and both Taichang sources visible',()=>{
 const p=JSON.parse(fs.readFileSync(new URL('../data/corpus/profiles/9w8_tqh_ysn_AAA.json',import.meta.url)));const native=JSON.parse(fs.readFileSync(new URL('../corpus/sanguozhi/022-chentai-source-details.json',import.meta.url))).records;const original=JSON.stringify(p);const view={...p,source_details:native};const html=personCard(view,true);assert.equal((html.match(/class="person-source-detail"/g)||[]).length,5);assert.match(html,/本傳泰不為太常/);assert.match(html,/太常陳泰不至/);assert.match(html,/2600尸/);assert.match(html,/職掌見於257–258年間；非任期/);assert.equal(JSON.stringify(p),original);
});
test('loadPerson reads the existing work title index once and enriches a copy, not the raw profile',async()=>{
 const previous=globalThis.fetch,calls=[];const raw={id:'synthetic-loading-ui',label:'合成人',titles:[title]};globalThis.fetch=async url=>{calls.push(url);return {ok:true,json:async()=>url==='data/corpus/work-titles.json'?{schema_version:1,works:[{id:'w-quoted-synthetic',title:'合成引書全題'}]}:raw};};
 try{const p=await loadPerson(raw.id);assert.equal(p.source_work_titles['w-quoted-synthetic'],'合成引書全題');assert.equal(raw.source_work_titles,undefined);await loadPerson(raw.id);assert.equal(calls.filter(x=>x==='data/corpus/work-titles.json').length,1);}finally{globalThis.fetch=previous;}
});
