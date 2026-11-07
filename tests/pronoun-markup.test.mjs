import test from 'node:test';
import assert from 'node:assert/strict';
import {chapterParagraph} from '../assets/corpus-reader.js';

test('resolved zhi stays plain while a whole proper name containing zhi opens a card', () => {
  const p={id:'synthetic-p',text:'王羲之見之。',mentions:[
    {id:'synthetic-name',start:0,end:3,surface:'王羲之',kind:'person',person_id:'synthetic-person'},
    {id:'synthetic-pronoun',start:4,end:5,surface:'之',kind:'pronoun',person_id:'synthetic-person',interpretation_note:'已判定的共指'}
  ]};
  const html=chapterParagraph(p);
  assert.match(html,/<a id="synthetic-name"[^>]*class="cbr-person-link"/);
  assert.match(html,/<span id="synthetic-pronoun" class="cbr-pronoun">之<\/span>/);
  assert.equal((html.match(/data-person-id=/g)||[]).length,1);
  assert.doesNotMatch(html,/unresolved-mention|title="已判定的共指"/);
  assert.equal(html.replace(/<[^>]*>/g,''),p.text);
});
