import test from 'node:test';import assert from 'node:assert/strict';import{workTitleMap,workMentionHTML}from'../assets/work-titles.js';
const m={id:'m',work_id:'w-jinshu-ref',surface:'晉書'};
test('explicit citation title separate qualification and aria',()=>{const t=workTitleMap({schema_version:1,works:[{id:m.work_id,title:'晉書',qualification:'裴注所引，作者未詳；非唐修本'}]});const s=workMentionHTML(m,t);assert.match(s,/data-work-title="晉書"/);assert.match(s,/引書《晉書》；裴注所引/);assert.doesNotMatch(s,/《晉書.*作者未詳》|著作全稱/);assert.match(s,/>晉書<\/button>/);});
test('no runtime parentheses parsing, old no-field row stays literal',()=>{const s=workMentionHTML(m,workTitleMap({schema_version:1,works:[{id:m.work_id,title:'晉書（來源限定）'}]}));assert.match(s,/data-work-title="晉書（來源限定）"/);});
test('unproved full title stays source title, not expansion',()=>{const s=workMentionHTML({...m,surface:'世語'}, {[m.work_id]:{title:'世語',qualification:'完整題名未核'}});assert.match(s,/引書《世語》；完整題名未核/);assert.doesNotMatch(s,/魏晉世語|全稱/);});
test('qualification escaped; unknown unchanged',()=>{assert.match(workMentionHTML(m,{[m.work_id]:{title:'晉書',qualification:'<img onerror="x">'}}),/&lt;img/);assert.match(workMentionHTML(m,{}),/^<cite /);});
test('bad qualifications rejected',()=>{for(const q of[null,42,''])assert.throws(()=>workTitleMap({schema_version:1,works:[{id:m.work_id,title:'晉書',qualification:q}]}));});
