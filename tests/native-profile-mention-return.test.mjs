import test from 'node:test';
import assert from 'node:assert/strict';
import {chapterParagraph,profileSourceContext} from '../assets/corpus-reader.js';
const paragraph={id:'synthetic-paragraph',text:'甲，甲',mentions:[{id:'synthetic-first',surface:'甲',kind:'person',person_id:'synthetic-person',start:0,end:1},{id:'synthetic-second',surface:'甲',kind:'person',person_id:'synthetic-person',start:2,end:3}]};
const context={work_id:'w-songshu',book_id:'b-songshu-056',chapter_id:'synthetic-chapter'};
const person={occurrences:[{...context,work_title:'合成書',title:'合成篇',paragraph_id:paragraph.id,paragraph_ids:[paragraph.id],mention_ids:['synthetic-first','synthetic-second'],mention_paragraph_ids:{'synthetic-first':paragraph.id,'synthetic-second':paragraph.id}}]};
for(const layout of [false,true])test(`same-person mentions return to the selected name with reading layout ${layout}`,()=>{
 const html=chapterParagraph(paragraph,{}, {...context,...(layout?{reading_layout:true}:{})});
 assert.equal(html.replace(/<[^>]*>/g,''),paragraph.text);
 const links=[...html.matchAll(/href="([^"]+)"/g)].map(m=>new URL(m[1].replaceAll('&amp;','&'),'https://synthetic.invalid/'));
 assert.equal(links.length,2);assert.equal(links[0].searchParams.get('mention'),'synthetic-first');assert.equal(links[1].searchParams.get('mention'),'synthetic-second');
 const back=profileSourceContext(person,links[1].searchParams);const p=new URLSearchParams(back.href.split('#')[1]);
 assert.equal(p.get('passage'),paragraph.id);assert.equal(p.get('mention'),'synthetic-second');assert.equal(p.get('chapter'),context.chapter_id);
});
test('forged mention cannot be carried through a profile return',()=>{
 const p=new URLSearchParams({work:context.work_id,book:context.book_id,chapter:context.chapter_id,passage:paragraph.id,mention:'synthetic-forged'});
 const back=profileSourceContext(person,p);assert(!new URLSearchParams(back.href.split('#')[1]).has('mention'));
});
