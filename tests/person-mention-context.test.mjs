import test from 'node:test';
import assert from 'node:assert/strict';
import {chapterParagraph} from '../assets/corpus-reader.js';
import {markCell,personCard} from '../assets/cbr-person.js';
import {setLocale} from '../assets/i18n.js';

test('identical source spellings keep different occurrence readings and original text',()=>{
 const paragraph={id:'synthetic-p',text:'甲與甲',mentions:[{id:'synthetic-m1',start:0,end:1,surface:'甲',kind:'person',person_id:'synthetic-a',interpretation_note:'本故事所指乙；原字不改。'},{id:'synthetic-m2',start:2,end:3,surface:'甲',kind:'person',person_id:'synthetic-b',interpretation_note:'本處校舉字面甲，不作故事參與者。'}]};
 const saved=structuredClone(paragraph),html=chapterParagraph(paragraph);
 assert(html.includes('data-person-reading-note="本故事所指乙；原字不改。"'));
 assert(html.includes('data-person-reading-note="本處校舉字面甲，不作故事參與者。"'));
 assert.equal(html.replace(/<[^>]*>/g,''),'甲與甲');assert.deepEqual(paragraph,saved);
});

test('table and text annotations escape reading attributes and omit absent notes',()=>{
 const note='" onclick="bad() <img src=x>',mention={id:'synthetic-m1',start:0,end:1,surface:'甲',kind:'person',person_id:'synthetic-a',interpretation_note:note};
 for(const html of [chapterParagraph({id:'synthetic-p',text:'甲',mentions:[mention]}),markCell({text:'甲',person_mentions:[mention]})]){
  assert.match(html,/data-person-reading-note="&quot; onclick=&quot;bad\(\) &lt;img src=x&gt;"/);assert.doesNotMatch(html,/" onclick="|<img/);
 }
 assert.doesNotMatch(markCell({text:'甲',person_mentions:[{...mention,interpretation_note:''}]}),/data-person-reading-note/);
 assert.doesNotMatch(chapterParagraph({id:'synthetic-p',text:'甲',mentions:[{...mention,interpretation_note:undefined}]}),/data-person-reading-note/);
});

test('card reading belongs only to the current occurrence and never changes the profile',()=>{
 const person={id:'synthetic-a',label:'合成人物'},saved=structuredClone(person);
 const first=personCard(person,false,'main',null,{surface:'原稱甲',interpretation_note:'本次事件首選乙。'});
 const second=personCard(person,false,'main',null,{surface:'原稱乙',interpretation_note:'另一篇引用的不同角色。'});
 assert.match(first,/本處「原稱甲」的辨識/);assert.match(first,/本次事件首選乙。/);assert.doesNotMatch(second,/本次事件首選乙/);
 assert.doesNotMatch(personCard(person),/person-mention-reading/);
 assert.doesNotMatch(personCard(person,true,'main',null,{surface:'甲',interpretation_note:'不變成全域生平。'}),/不變成全域生平|person-mention-reading/);
 assert.deepEqual(person,saved);
});

test('reading labels translate while source wording remains escaped and unchanged',()=>{
 const person={id:'synthetic-a',label:'合成人物'},context={surface:'<img>',interpretation_note:'原稱保留。<script>bad()</script>'};
 try{
  setLocale('en');const en=personCard(person,false,'main',null,context);assert.match(en,/Identification of “&lt;img&gt;” here/);assert.match(en,/原稱保留。&lt;script&gt;bad\(\)&lt;\/script&gt;/);assert.doesNotMatch(en,/<script>|<img>/);
  setLocale('zh-Hant');assert.match(personCard(person,false,'main',null,context),/本處「&lt;img&gt;」的辨識/);
 }finally{setLocale('zh-Hant');}
});
