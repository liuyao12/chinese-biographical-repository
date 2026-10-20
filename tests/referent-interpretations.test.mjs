import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {referentInterpretations, referentCasesHTML} from '../assets/referent-interpretations.js';
import {chapterParagraph} from '../assets/corpus-reader.js';
import {personCard} from '../assets/cbr-person.js';
import {setLocale} from '../assets/i18n.js';
const chapter=JSON.parse(readFileSync(new URL('../corpus/shiji/117.json',import.meta.url)));
test('attributed alternatives are outside the unchanged received paragraph, with no person link on the unresolved name',()=>{
  const p=chapter.paragraphs.find(p=>p.id.endsWith(':p007'));
  const source=chapterParagraph(p);
  assert.match(source,/<span id="c-shiji-117-xiangru:m007-0066" class="unresolved-mention"/);
  assert.doesNotMatch(source,/data-person-id="3go_52y_0mp"/);
  assert.equal(source.replace(/<[^>]*>/g,''),p.text);
  const notes=referentInterpretations(chapter,p.id,{'3go_52y_0mp':{label:'伯樂'}});
  assert.match(notes,/編者指稱判讀/);assert.match(notes,/陽陵/);assert.match(notes,/候選人物/);
  assert.match(notes,/candidate-profile/);assert.doesNotMatch(notes,/data-person-id=/);
  assert.equal(referentInterpretations(chapter,'missing-paragraph'),'');
});
test('profile keeps alternative-source evidence but compact identity card omits it',()=>{
  const profile={id:'3go_52y_0mp',label:'伯樂',names:['伯樂'],titles:[],addresses:[],occurrences:[],sources:[],relations:[],related_people:{'3go_52y_0mp':'伯樂'},referent_interpretations:[chapter.annotation.referent_interpretations[0]]};
  const full=personCard(profile,true),compact=personCard(profile,false);
  assert.match(full,/編者指稱判讀/);assert.match(full,/尚未定指/);assert.match(full,/chapter=117/);
  assert.doesNotMatch(compact,/referent-interpretations/);
});
test('untrusted commentary is escaped, unsafe source URLs omitted, and switching language retains source text',()=>{
  const c=structuredClone(chapter.annotation.referent_interpretations[0]);
  c.references[0].url='javascript:alert(1)';c.alternatives[0].interpretation='<img onerror=alert(1)>';
  let html=referentCasesHTML([c]);assert.match(html,/&lt;img/);assert.doesNotMatch(html,/<img|href="javascript:/);
  setLocale('en',{persist:false});
  try {html=referentCasesHTML([c]);assert.match(html,/Referent interpretations/);assert.match(html,/陽子/);assert.match(html,/漢書音義/);} finally {setLocale('zh-Hant',{persist:false});}
});
test('preferred nonpersonal readings are attributed without person links or changes to received text',()=>{
  const cases=chapter.annotation.referent_interpretations.filter(c=>['ri-shiji117-lieque','ri-shiji117-tiandi'].includes(c.id));
  assert.equal(cases.length,2);
  const html=referentCasesHTML(cases);
  assert.equal((html.match(/class="referent-preferred"/g)||[]).length,2);
  assert.match(html,/自然現象/);assert.match(html,/天帝/);
  assert.doesNotMatch(html,/candidate-profile|data-person-id=/);
  const p=chapter.paragraphs.find(p=>p.id.endsWith(':p064'));
  assert.match(p.text,/帝以享祉/);
  assert.equal(chapterParagraph(p).replace(/<[^>]*>/g,''),p.text);
  const unresolved=referentCasesHTML(chapter.annotation.referent_interpretations.filter(c=>c.status==='unresolved'));
  assert.doesNotMatch(unresolved,/class="referent-preferred"/);
  assert.match(unresolved,/北僑/);assert.match(unresolved,/伯僑/);
});
test('Luli retains divine and mythical-bird readings in both UI languages without individual links',()=>{
  const c=chapter.annotation.referent_interpretations.find(c=>c.id==='ri-shiji117-luli');
  let html=referentCasesHTML([c]);assert.match(html,/神話生靈讀法/);assert.match(html,/陸離/);assert.match(html,/長離/);assert.doesNotMatch(html,/candidate-profile|class="referent-preferred"/);
  setLocale('en',{persist:false});
  try{html=referentCasesHTML([c]);assert.match(html,/Mythical creature reading/);assert.match(html,/陸離/);assert.match(html,/長離/);}finally{setLocale('zh-Hant',{persist:false});}
});
test('the five celestial emperors are classified as a group without materializing five people',()=>{
  const c=chapter.annotation.referent_interpretations.find(c=>c.id==='ri-shiji117-five-celestial-emperors');
  const html=referentCasesHTML([c]);assert.match(html,/群體泛稱讀法/);assert.equal((html.match(/class="referent-preferred"/g)||[]).length,1);assert.doesNotMatch(html,/candidate-profile|data-person-id=/);assert.match(html,/五畤/);assert.match(html,/五時/);
});
