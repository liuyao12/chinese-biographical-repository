import test from 'node:test';
import assert from 'node:assert/strict';
import {markCell, personCard, profileURL, tableOccurrenceURL, personBundleURL} from '../assets/cbr-person.js';
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
  const html = personCard({id: 'yqp_nlb_p1p_ACAF', label: '彭祖', table_occurrences: [{table_id: 'shiji-017', cell_id: 'shiji-017-t1-r052-c17', title: '《史記·漢興以來諸侯王年表》', year: null, quote: '王彭祖元年。景帝子。', mention: {identity_evidence: [{chapter_id: 'c-shiji-059-wuzong', paragraph_id: 'c-shiji-059-wuzong:p017', quote: '趙王彭祖', source_revision: 2621125}]}}]}, true);
  assert.match(html, /人物同指的篇文證據/);
  assert.match(html, /趙王彭祖/);
  assert.match(html, /chapter=59/);
  assert.match(html, /passage=c-shiji-059-wuzong/);
  assert.match(html, /2621125/);
});

test('profile preserves alternative death years and marks the scoped provisional default', () => {
 const p={id:'abc_def_123',label:'synthetic person',dates:[{era:'BCE',era_year:252,record_id:'old',original_quote:'synthetic earlier account'},{era:'BCE',era_year:251,record_id:'new',original_quote:'synthetic other account'}],life_event_date_decisions:[{candidate_event_ids:['old','new'],preferred_event_id:'new',status:'editorial_provisional',rationale:'synthetic comparison <script>',evidence:[]}],life_events:[{event_type:'death',date_expression:'synthetic year',source_term:'synthetic death',evidence:[]}]};
 const html=personCard(p,true);
 assert.match(html,/西元前252年/);assert.match(html,/西元前251年/);
 assert.match(html,/來源異說/);assert.match(html,/本項預設/);assert.ok(html.indexOf('西元前251年') < html.indexOf('西元前252年'));
 assert.match(html,/來源所記生卒/);assert.match(html,/synthetic comparison &lt;script&gt;/);
 p.life_event_date_decisions[0].status='unresolved';p.life_event_date_decisions[0].preferred_event_id=null;
 assert.doesNotMatch(personCard(p,true),/本項預設/);assert.match(personCard(p,true),/取捨未定/);
});

test('office event counts stay separate from title duration and retain each source record', () => {
 const title={title:'synthetic office',period:'未定 → 未定',reported_office_event_counts:{departure:{value:3,source_term:'synthetic departure'},reinstatement:{value:3,source_term:'synthetic reinstatement'}}};
 const html=personCard({id:'abc_def_123',label:'synthetic person',titles:[{title:title.title,period:title.period},title]},true);
 assert.match(html,/離相 3 次/);assert.match(html,/復位 3 次/);assert.doesNotMatch(html,/各次起訖未定/);
 assert.doesNotMatch(html,/任職三年|任職3年/);
});


test('source JSON links use the deployed exact commit with a bounded fallback', () => {
 const ref = 'a'.repeat(40);
 const url = personBundleURL('abc_def_123', ref);
 assert.equal(url, 'https://github.com/liuyao12/chinese-biographical-repository/blob/'+ref+'/exports/persons/abc_def_123.json');
 assert.match(personBundleURL('a#b', 'javascript:alert(1)'), /blob\/main\/exports\/persons\/a%23b\.json$/);
 assert.match(personCard({id:'abc_def_123',label:'synthetic'},true,ref), new RegExp('blob/'+ref+'/exports/persons'));
});


test('missing fields and entire empty sections are omitted in both card and profile', () => {
 const p={id:'abc_def_123',label:'甲'};
 const family={ancestors:[[],[],[]],mother:[],spouses:[],children:[]};
 for(const full of [false,true]) {
  const html=personCard(p,full,'main',family);
  assert.doesNotMatch(html,/person-aliases|person-life-summary|person-family|person-facts|表中原文|出現篇章|未詳|尚未整理/);
 }
});
test('known grandfather survives a missing father and undated death retains source evidence', () => {
 const family={ancestors:[[],[{id:'g',label:'祖甲',evidence:[]}],[]],mother:[],spouses:[],children:[]};
 const p={id:'abc_def_123',label:'甲',life_events:[{person_id:'abc_def_123',event_type:'death',source_term:'甲卒',evidence:[{quote:'甲卒'}]}],age_assertions:[{person_id:'abc_def_123',value:70,evidence:[]}],titles:[{title:'君',period:'未定 → 未定'}]};
 const html=personCard(p,true,'main',family);
 assert.match(html,/<dt>祖<\/dt>/);assert.doesNotMatch(html,/<dt>(父|曾祖|生母|配偶|子女|生|卒)<\/dt>/);
 assert.match(html,/70 歲/);assert.match(html,/甲卒/);assert.match(html,/稱號與持職/);
 assert.doesNotMatch(html,/起訖未定|原文未明紀年|來源所記地望/);
});
test('a dated death shows its available year without an absent birth or Chinese date placeholder', () => {
 const p={id:'abc_def_123',label:'甲',life_events:[{person_id:'abc_def_123',event_type:'death',normalized_date:{era:'BCE',era_year:243},evidence:[]}]};
 for(const full of [false,true]) {
  const html=personCard(p,full);
  assert.match(html,/<dt>卒<\/dt>/);assert.match(html,/西元前243年/);
  assert.doesNotMatch(html,/<dt>(生|年齡)<\/dt>|原文未明紀年/);
 }
});
