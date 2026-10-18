import test from 'node:test';
import assert from 'node:assert/strict';
import {personCard} from '../assets/cbr-person.js';

test('formal names keep generic source expressions out of additional names without hiding typed courtesy names', () => {
  const synthetic={id:'synthetic_person',label:'甲乙',names:['王','某王'],name_components:[{surname:'甲',ming:'乙',title:'某王',additional_names:[],quote:'合成測試文字',note:'synthetic fixture'}]};
  const html=personCard(synthetic,true);
  assert.doesNotMatch(html,/<p class="person-aliases">/);
  assert.match(html,/class="person-source-names"/);
  assert.match(html,/<p>王、某王<\/p>/);
  const courtesy=personCard({...synthetic,name_components:[{...synthetic.name_components[0],zi:'子丙'}]},true);
  assert.equal(courtesy.match(/<p class="person-aliases">(.*?)<\/p>/)[1].replace(/<[^>]*>/g,''),'字 子丙');
  assert.match(courtesy,/<p>王、某王<\/p>/);
  assert.match(personCard({...synthetic,name_components:[]}),/<p class="person-aliases">/);
});
