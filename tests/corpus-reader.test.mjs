import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {chapterURL, chapterParagraph, filteredChapters} from '../assets/corpus-reader.js';
const index = JSON.parse(readFileSync(new URL('../data/corpus/index.json', import.meta.url)));
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
