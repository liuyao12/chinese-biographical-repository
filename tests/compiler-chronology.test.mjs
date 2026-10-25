import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {compilerChronologyPlacements} from '../assets/compiler-chronology.js';
import {sourceDetailsHTML} from '../assets/person-source-details.js';
import {summarizeLife} from '../assets/person-life.js';
import {setLocale} from '../assets/i18n.js';
const read=path=>JSON.parse(fs.readFileSync(new URL('../'+path,import.meta.url),'utf8'));
const detail=read('corpus/jinshu/043-wangcheng-compiler-chronology.json').records[0];
const life=read('corpus/jinshu/043-wangcheng-life-events.json').events;
const person={id:detail.person_id,source_details:[detail],life_events:life};
test('actual qualified death placement provides numerical year and mandatory timeline qualification without changing life scalar',()=>{
 const before=summarizeLife({...person,source_details:[]}),after=summarizeLife(person);
 assert.deepEqual(after,before);assert.equal(after.death[0].normalized_date,undefined);
 const [p]=compilerChronologyPlacements(person);assert.equal(p.year,312);assert.equal(p.source_expression,'永嘉六年');
 assert.equal(p.required_qualification,'compiler_editorial_placement_provisional');assert.equal(p.must_display_qualification,true);
 assert.equal(p.replace_source_event_date,false);assert.equal(p.birth_year_inference_permitted,false);
});
test('full source detail shows year, qualified status, complete Kaoyi and fixed source while compact stays unchanged',()=>{
 setLocale('zh-Hant');const html=sourceDetailsHTML(person,true);
 for(const value of ['312','永嘉六年','編年推繫','暫定首選','紀傳皆無年月','故附於此','github.com/kanripo/KR2b0007'])assert(html.includes(value),value);
 assert.equal(sourceDetailsHTML(person,false),'');
 setLocale('en');assert.match(sourceDetailsHTML(person,true),/Compiler chronological placement/);setLocale('zh-Hant');
});
test('foreign person, missing linked event, existing direct death year and stripped qualification cannot become timeline inputs',()=>{
 const variants=[p=>p.id='foreign',p=>p.life_events=[],p=>p.life_events[0].normalized_date={year:312},p=>p.source_details[0].timeline_use.must_display_qualification=false,p=>p.source_details[0].placement.selection_status='source_attested'];
 for(const change of variants){const p=structuredClone(person);change(p);assert.deepEqual(compilerChronologyPlacements(p),[]);}
});

test('editorial reading aid is labelled, escaped, and separate from the complete raw transcription',()=>{
 setLocale('zh-Hant');const html=sourceDetailsHTML(person,true);
 assert.match(html,/class="person-compiler-reading-aid"/);
 assert.match(html,/編輯便讀標點及雙行轉錄讀序整理/);
 assert.match(html,/<details class="person-compiler-raw-witness"><summary><span[^>]*>逐字數位轉錄見證<\/span><\/summary>/);
 const raw=html.slice(html.indexOf('<details class="person-compiler-raw-witness"'));
 assert(raw.includes('&lt;pb:KR2b0007_WYG_088-18a&gt;'));
 assert(!html.slice(0,html.indexOf('<details class="person-compiler-raw-witness"')).includes('&lt;pb:'));
 const x=structuredClone(person);x.source_details[0].external_evidence.anchors[2].reading_aid='<img src=x onerror=alert(1)>';
 assert(!sourceDetailsHTML(x,true).includes('<img'));
 delete x.source_details[0].external_evidence.anchors[2].reading_aid_qualification;
 const fallback=sourceDetailsHTML(x,true);assert(!fallback.includes('person-compiler-reading-aid'));assert(fallback.includes('&lt;pb:'));
});
