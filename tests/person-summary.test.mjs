import test from 'node:test';
import assert from 'node:assert/strict';
import {createSummaryLoader, personSummaryCard} from '../assets/person-summary.js';

test('a card needs one small request; concurrent and subsequent openings reuse it', async () => {
  const requests = [];
  const load = createSummaryLoader(async url => {requests.push(url); return {ok:true, json:async () => ({schema_version:1,id:'synthetic_*A',heading:'測試人物'})};});
  const [a,b] = await Promise.all([load('synthetic_*A'),load('synthetic_*A')]);
  assert.equal(a,b); assert.equal(await load('synthetic_*A'),a);
  assert.deepEqual(requests,['data/corpus/summaries/synthetic_*A.json']);
});

test('missing or mismatched summary retries without fetching a full profile', async () => {
  const requests=[];
  const load=createSummaryLoader(async url=>{requests.push(url);return requests.length===1?{ok:false}:{ok:true,json:async()=>({schema_version:1,id:'another',heading:'另一人物'})};});
  await assert.rejects(load('synthetic'),/尚未載入/);
  await assert.rejects(load('synthetic'),/格式不符/);
  assert.deepEqual(requests,Array(2).fill('data/corpus/summaries/synthetic.json'));
});

test('essential summary keeps life and family qualifications, omits source apparatus and absent fields', () => {
  const html=personSummaryCard({id:'synthetic',heading:'測試公 測試甲',aliases:[{kind:'zi',value:'測試字'}],life:{death:[{year_label:'西元300年',source_date:'測試年',choice:'alternative'}],ages:[{label:'15歲（生前報齡）'}]},family:{ancestors:[[{id:'synthetic_parent',label:'測試父',role:'assembly_inferred',route_qualification:['assembly_inferred']}],[],[]],spouses:[{id:'synthetic_spouse',label:'測試配偶',marriage_status:'source_attested_divorce'}],unresolved_spouse_groups:[{id:'unresolved'}]},sources:[{quote:'SHOULD_NOT_RENDER'}],evidence:[{quote:'SHOULD_NOT_RENDER'}]});
  assert.match(html,/測試公 測試甲/);assert.match(html,/<small>.*測試字/);
  assert.match(html,/西元300年/);assert.match(html,/測試年/);assert.match(html,/來源異說/);
  assert.match(html,/父系暫定/);assert.match(html,/離婚/);assert.match(html,/配偶指涉未決/);
  assert.match(html,/15歲（生前報齡）/);assert.match(html,/person.html#synthetic_parent/);
  assert.doesNotMatch(html,/SHOULD_NOT_RENDER|<details|<blockquote|\.json|享年|<dt>.*生母/);
  assert.match(html,/閱讀完整人物頁/);
  assert.doesNotMatch(personSummaryCard({id:'empty',heading:'只有姓名'}),/<dl>|籍貫|年齡/);
});

test('summary values are escaped and links are restricted to the local profile route',()=>{
  const html=personSummaryCard({id:'javascript:alert(1)',heading:'<script>',family:{spouses:[{id:'<bad>',label:'<img src=x>'}]}});
  assert.doesNotMatch(html,/<script>|<img|href="javascript:/);
  assert.match(html,/&lt;script&gt;/);assert.match(html,/person.html#%3Cbad%3E/);
});


test('reported age retains its calendar context and approximation, without evidence apparatus', () => {
  const html=personSummaryCard({id:'synthetic_age',heading:'測試人物',life:{ages:[{label:'72 歲（來源報齡）',source_date:'永興二年',year_label:'西元305年',context:'at_death',approximate:true}]}});
  assert.match(html,/永興二年/); assert.match(html,/西元305年/);
  assert.match(html,/來源約數/); assert.doesNotMatch(html,/<details|<blockquote/);
});

test('the current name interpretation uses existing DOM context and remains escaped', () => {
  const html=personSummaryCard({id:'synthetic_king',heading:'齊湣王'}, {surface:'齊王',interpretation_note:'測試判讀 <script>不可執行</script>'});
  assert.match(html,/齊王/); assert.match(html,/測試判讀 &lt;script&gt;/);
  assert.doesNotMatch(html,/<script>|<details|<blockquote/);
});
