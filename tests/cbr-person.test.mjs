import test from 'node:test';
import assert from 'node:assert/strict';
import {markCell, personCard, profileURL, tableOccurrenceURL} from '../assets/cbr-person.js';
test('年表錨點保留原文並連至人物頁，拒絕錯位或交疊',()=>{
 const c={text:'張儀相。',person_mentions:[{start:0,end:2,surface:'張儀',person_id:'abc_def_123'}]};
 const html=markCell(c); assert.match(html,/張儀<\/a>相。/);assert.match(html,/person.html#abc_def_123/);
 assert.throws(()=>markCell({...c,person_mentions:[{...c.person_mentions[0],end:3}]}));
 assert.equal(markCell({text:'<楚>&'}),'&lt;楚&gt;&amp;');
});
test('人物卡片提供跨篇原文與完整人物頁，不以 JSON 代替介面',()=>{
 const p={id:'abc_def_123',label:'張儀',names:['張子'],titles:[{title:'秦相',period:'起訖未定'}],occurrences:[{number:70,category:'liezhuan',title:'張儀列傳',paragraph_id:'p1',quote:'張儀者，魏人也。',count:2}]};
 const html=personCard(p);assert.match(html,/稱號與持職/);assert.match(html,/閱讀完整人物頁/);assert.match(html,/chapter=70&amp;category=liezhuan&amp;passage=p1/);assert.doesNotMatch(html,/\.json/);
 assert.match(personCard({...p,label:'<script>'},true),/&lt;script&gt;/);
 assert.equal(profileURL('a#b'),'person.html#a%23b');
});

test('table occurrences link to their own chapter and mark names inside a cell', () => {
 for (const chapter of [13, 14, 15, 16, 17, 18, 19, 20, 21, 22]) {
  const url=tableOccurrenceURL({table_id: 'shiji-'+String(chapter).padStart(3,'0'),cell_id:'synthetic-cell'});
  assert.match(url,new RegExp('chapter='+chapter+'&'));
 }
 assert.equal(tableOccurrenceURL({table_id:'javascript:alert(1)',cell_id:'x'}),'');
 const html=markCell({text:'甲與乙會盟。',person_mentions:[{start:0,end:1,surface:'甲',person_id:'abc_def_123'},{start:2,end:3,surface:'乙',person_id:'xyz_abc_456'}]});
 assert.equal((html.match(/class="table-person-link"/g)||[]).length,2);
 assert.match(html,/<\/a>與<a/);
 assert.match(html,/<\/a>會盟。$/);
});

test('source-local person card shows received table evidence before opening its page', () => {
  const html = personCard({id: 'abc_def_123', label: '劉成', review: 'source_local_candidate', identity_note: '杏山列，尚未跨篇合併。', table_occurrences: [{table_id: 'shiji-021', cell_id: 'shiji-021-t1-r006-c02', title: '《史記·建元以來王子侯者年表》', year: null, quote: '一。六年後九月壬戌，侯劉成元年。'}]});
  assert.match(html, /侯劉成元年/);
  assert.match(html, /杏山列/);
  assert.match(html, /chapter=21/);
});

test('person navigation retains a bounded source-table context', () => {
  assert.equal(profileURL('abc_def_123', 'shiji-021'), 'person.html?table=shiji-021#abc_def_123');
  assert.equal(profileURL('abc_def_123', 'https://example.com'), 'person.html#abc_def_123');
  assert.match(markCell({id: 'shiji-021-t1-r006-c02', text: '侯劉成元年。', person_mentions: [{start: 1, end: 3, surface: '劉成', person_id: 'abc_def_123'}]}), /person.html\?table=shiji-021#abc_def_123/);
});

test('full person page renders the checked primary passage for a table identity decision', () => {
  const html = personCard({id: '1c8_u63_bk4_G', label: '彭祖', table_occurrences: [{table_id: 'shiji-017', cell_id: 'shiji-017-t1-r052-c17', title: '《史記·漢興以來諸侯王年表》', year: null, quote: '王彭祖元年。景帝子。', mention: {identity_evidence: [{chapter_id: 'c-shiji-059-wuzong', paragraph_id: 'c-shiji-059-wuzong:p017', quote: '趙王彭祖', source_revision: 2621125}]}}]}, true);
  assert.match(html, /人物同指的篇文證據/);
  assert.match(html, /趙王彭祖/);
  assert.match(html, /chapter=59/);
  assert.match(html, /passage=c-shiji-059-wuzong/);
  assert.match(html, /2621125/);
});
