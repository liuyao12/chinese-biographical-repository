import test from 'node:test';
import assert from 'node:assert/strict';
import {markCell, personCard, profileURL} from '../assets/cbr-person.js';
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
