import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {chapterParagraph} from '../assets/corpus-reader.js';
const chapter = JSON.parse(readFileSync(new URL('../corpus/jinshu/035-peixiu-peiwei.json', import.meta.url)));
test('all six first-person references retain plain anchors without a personal-name link',()=>{
 let count=0;
 for(const p of chapter.paragraphs)for(const m of p.mentions)if(m.kind==='pronoun'){
  count++;
  const html=chapterParagraph(p);
  assert.ok(html.includes(`<span id="${m.id}" class="cbr-pronoun">${m.surface}</span>`));
  assert.ok(!html.includes(`<a id="${m.id}"`));
 }
 assert.equal(count,6);
});
test('proper-name fragment exception remains a person and 之 remains a plain pronoun',()=>{
 const source=JSON.parse(readFileSync(new URL('../corpus/songshu/044-wyd1739.json',import.meta.url)));
 const p=source.paragraphs.find(p=>p.id.endsWith(':p008'));
 const m=p.mentions.find(m=>m.id.endsWith(':m0000'));
 assert.equal(m.kind,'person');assert.ok(chapterParagraph(p).includes(`<a id="${m.id}"`));
 const z={id:'synthetic-p',text:'見之',mentions:[{id:'synthetic-zhi',start:1,end:2,surface:'之',kind:'pronoun',person_id:'synthetic-person'}]};
 assert.ok(chapterParagraph(z).includes('class="cbr-pronoun"'));
});

test('renderer presents arbitrary typed pronouns safely without validating their provenance',()=>{
 const id='synthetic-typed-"<&';
 const p={id:'synthetic-p',text:'朕臣吾<',mentions:[
  {id,start:0,end:1,surface:'朕',kind:'pronoun',person_id:'untrusted-id',interpretation_note:'<img onerror=bad>'},
  {id:'synthetic-chen',start:1,end:2,surface:'臣',kind:'pronoun',person_id:'another-id'},
  {id:'synthetic-wu',start:2,end:3,surface:'吾',kind:'pronoun',person_id:'third-id'},
 ]};
 const html=chapterParagraph(p);
 assert.ok(html.includes('id="synthetic-typed-&quot;&lt;&amp;" class="cbr-pronoun">朕</span>'));
 assert.equal((html.match(/class="cbr-pronoun"/g)||[]).length,3);
 assert.ok(html.includes('吾</span>&lt;'));
 assert.ok(!/data-person-id|href=|cbr-person-link|unresolved-mention/.test(html));
 // Presentation does not classify an untrusted reference as source-valid.
 assert.equal(p.mentions[0].person_id,'untrusted-id');
});
