import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {chapterURL, chapterParagraph, filteredChapters, sourcePassageURL, profileSourceContext} from '../assets/corpus-reader.js';
const index = JSON.parse(readFileSync(new URL('../data/corpus/index.json', import.meta.url)));
test('a direct native-work profile returns to its principal source without overriding an explicit context',()=>{
 const native={work_id:'w-jinshu',work_title:'晉書',book_id:'b-jinshu-075',chapter_id:'c-jinshu-075-synthetic',paragraph_id:'synthetic-p1',paragraph_ids:['synthetic-p1'],title:'Synthetic source',count:10};
 const person={occurrences:[native,{work_id:'w-shiji',chapter_id:'c-shiji-075-synthetic',count:2}]};
 const result=profileSourceContext(person,new URLSearchParams());
 assert.match(result.text,/晉書/);
 assert.equal(new URLSearchParams(result.href.split('#')[1]).get('book'),'b-jinshu-075');
 assert.equal(profileSourceContext(person,new URLSearchParams({work:'w-jinshu',chapter:native.chapter_id,book:'b-jinshu-999'})),null);
 assert.equal(profileSourceContext({occurrences:[{work_id:'w-shiji',count:20},native]},new URLSearchParams()),null);
});
test('Shiji contents use five historical categories and retain all 130 entries, including pending texts', () => {
  assert.equal(index.chapters.length,130);
  for (const [category,count] of [['benji',12],['biao',10],['shu',8],['shijia',30],['liezhuan',70]]) assert.equal(filteredChapters(index,category).length,count);
  assert.equal(filteredChapters(index,'all','秦始皇')[0].number,6);
  assert.equal(filteredChapters(index,'shu')[0].available,'pending');
  assert.equal(index.chapters.filter(e=>e.available==='marked_text').length,112);
  assert.deepEqual(index.chapters.filter(e=>e.available==='table').map(e=>e.number),[13,14,15,16,17,18,19,20,21,22]);
});
test('source markup uses Unicode code points and escapes text, preserving unresolved references', () => {
  const paragraph={id:'synthetic-p',text:'𠮷甲<乙&丙',mentions:[{id:'synthetic-m1',start:0,end:2,surface:'𠮷甲',kind:'person',person_id:'synthetic_person'},{id:'synthetic-m2',start:3,end:4,surface:'乙',kind:'unresolved',person_id:null}]};
  const html=chapterParagraph(paragraph,{'synthetic_person':{label:'甲'}});
  assert.match(html,/class="cbr-person-link"/);
  assert.match(html,/𠮷甲<\/a>&lt;/);
  assert.match(html,/unresolved-mention/);
  assert.match(html,/&amp;丙/);
  assert.throws(()=>chapterParagraph({...paragraph,mentions:[{...paragraph.mentions[0],surface:'wrong'}]}),/錨點/);
});
test('chapter links preserve category and source paragraph without injecting URL structure', () => {
  const url=chapterURL(6,'benji','synthetic-p&extra=1');
  const params=new URLSearchParams(url.split('#')[1]);
  assert.equal(params.get('category'),'benji');
  assert.equal(params.get('passage'),'synthetic-p&extra=1');
  assert.equal(params.get('extra'),null);
});
test('body names open readable profiles with the exact source paragraph context', () => {
  const html=chapterParagraph({id:'c-shiji-006-synthetic:p002',text:'甲',mentions:[{id:'synthetic-m',start:0,end:1,surface:'甲',kind:'person',person_id:'synthetic_person'}]});
  assert.match(html,/person\.html\?chapter=6&amp;passage=c-shiji-006-synthetic%3Ap002#synthetic_person/);
  assert.doesNotMatch(html,/github\.com/);
});

test('book title keeps its anchor and does not open a person profile', () => {
  const chapter = JSON.parse(readFileSync(new URL('../corpus/shiji/063.json', import.meta.url)));
  const paragraph = chapter.paragraphs.find(p => p.id.endsWith(':p011'));
  const html = chapterParagraph(paragraph);
  assert.match(html, /<cite id="c-shiji-063-laohan:m011-0079" class="cbr-work-mention" data-work-id="w-shenzi"/);
  assert.doesNotMatch(html, /<a id="c-shiji-063-laohan:m011-0079"/);
  assert.match(html, /<a id="c-shiji-063-laohan:m011-0044"[^>]*data-person-id="vtn_thh_540"/);
  assert.equal(html.replace(/<[^>]*>/g, ''), paragraph.text);
});
test('unresolved interpretation notes remain escaped and never become person links', () => {
  const html=chapterParagraph({id:'synthetic-p',text:'某',mentions:[{id:'synthetic-m',start:0,end:1,surface:'某',kind:'unresolved',person_id:null,interpretation_note:'未知敘者 "<script>" & 異說'}]});
  assert.match(html,/title="未知敘者 &quot;&lt;script&gt;&quot; &amp; 異說"/);
  assert.doesNotMatch(html,/<script>|data-person-id|href=/);
});
test('different works never share a source route merely because volume numbers match',()=>{
 const e={work_id:'w-hanshu',book_id:'b-hanshu-041',chapter_id:'c-hanshu-041-synthetic',paragraph_id:'synthetic-p&extra=1'};
 const url=sourcePassageURL(e),p=new URLSearchParams(url.split('#')[1]);
 assert.ok(url.startsWith('reader.html#'));
 assert.equal(p.get('work'),'w-hanshu');assert.equal(p.get('book'),'b-hanshu-041');
 assert.equal(p.get('passage'),'synthetic-p&extra=1');assert.equal(p.get('extra'),null);
 assert.equal(sourcePassageURL({chapter_id:'c-shiji-041-synthetic',paragraph_id:'synthetic-p'}),'shiji.html#chapter=41&passage=synthetic-p');
 assert.equal(sourcePassageURL({...e,work_id:'https://synthetic.invalid/'}),'');
});
test('other-work person links keep received text and explicit source context',()=>{
 const p={id:'c-hanshu-041-synthetic:p-zhou-001',text:'周惞，',mentions:[{id:'synthetic-m',start:0,end:2,surface:'周惞',kind:'person',person_id:'synthetic_person'}]};
 const html=chapterParagraph(p,{}, {work_id:'w-hanshu',book_id:'b-hanshu-041',chapter_id:'c-hanshu-041-synthetic'});
 assert.equal(html.replace(/<[^>]*>/g,''),'周惞，');
 assert.match(html,/work=w-hanshu&amp;book=b-hanshu-041&amp;chapter=c-hanshu-041-synthetic/);
 assert.doesNotMatch(html,/chapter=41(?:&|#)/);
});
test('profile source return validates work, book, chapter and recorded passage',()=>{
 const occurrence={work_id:'w-hanshu',work_title:'漢書',book_id:'b-hanshu-041',chapter_id:'c-hanshu-041-synthetic',title:'合成篇',paragraph_id:'synthetic-p1',paragraph_ids:['synthetic-p1','synthetic-p2']};
 const p={occurrences:[occurrence]},params=new URLSearchParams({work:'w-hanshu',book:'b-hanshu-041',chapter:'c-hanshu-041-synthetic',passage:'synthetic-p2'});
 assert.equal(new URLSearchParams(profileSourceContext(p,params).href.split('#')[1]).get('passage'),'synthetic-p2');
 params.set('passage','synthetic-forged');assert.equal(new URLSearchParams(profileSourceContext(p,params).href.split('#')[1]).get('passage'),'synthetic-p1');
 params.set('book','b-shiji-041');assert.equal(profileSourceContext(p,params),null);
});

test('non-person grammar keeps source anchors without unresolved styling or profile links',()=>{
 const chapter=JSON.parse(readFileSync(new URL('../corpus/shiji/118.json',import.meta.url)));
 const p=chapter.paragraphs.find(x=>x.id.endsWith(':p014')),html=chapterParagraph(p);
 for(const id of ['m014-0163','m014-0191','m014-0201'])assert.match(html,new RegExp('<span id="c-shiji-118-huainan:'+id+'" class="cbr-non-person"'));
 assert.match(html,/<a id="c-shiji-118-huainan:m014-0197"[^>]*data-person-id="yqp_nlb_p1p_AFC"/);
 assert.equal(html.replace(/<[^>]*>/g,''),p.text);
});
test('non-person classification notes are escaped as inert text',()=>{
 const html=chapterParagraph({id:'synthetic-p',text:'王',mentions:[{id:'synthetic-m',surface:'王',start:0,end:1,kind:'non_person',person_id:null,lexical_role:'verb',interpretation_note:'"<script>" & note'}]});
 assert.match(html,/&quot;&lt;script&gt;&quot; &amp; note/);assert.doesNotMatch(html,/<script>|data-person-id|href=|unresolved-mention/);
});
