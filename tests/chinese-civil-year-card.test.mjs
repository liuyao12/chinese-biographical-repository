import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {personCard} from '../assets/cbr-person.js';
import {setLocale} from '../assets/i18n.js';
const event=JSON.parse(readFileSync(new URL('./fixtures/chu-wu-chinese-civil-year.json',import.meta.url),'utf8'));
const table=JSON.parse(readFileSync(new URL('../data/historical-tables/shiji-022.json',import.meta.url),'utf8'));
const profile=()=>({id:event.person_id,label:'楚王戊',life_events:[structuredClone(event)],sources:[{work_id:table.source.work_id,book_id:table.source.book_id,chapter_id:table.source.chapter_id,source_id:table.source.id,source:structuredClone(table.source)}]});

test('civil year card exposes original context and table witnesses separately from Gregorian projection',()=>{
  const html=personCard(profile(),true);
  assert.match(html,/中國曆年依據/);assert.match(html,/孝景帝三年正月甲子，初起兵於廣陵。/);
  assert.match(html,/passage=c-shiji-106-wuwang%3Ap009/);
  for (const cell of ['r051-c01','r053-c01','r053-c02','r053-c00'])assert.ok(html.includes('shiji-022-t1-'+cell));
  assert.match(html,/oldid=2607038/);assert.match(html,/數位編者年份對照/);
  assert.match(html,/class="person-gregorian-window"/);assert.match(html,/公曆投影範圍/);
  assert.doesNotMatch(html.match(/<strong>(.*?)<\/strong>/s)[1],/155/);
});
test('English labels preserve Chinese source quotations',()=>{
  try {setLocale('en');const html=personCard(profile(),true);assert.match(html,/154 BCE \(Chinese civil year\)/);assert.match(html,/Chinese civil year evidence/);assert.match(html,/孝景帝三年正月甲子，初起兵於廣陵。/);}
  finally {setLocale('zh-Hant');}
});
test('calendar commentary and fixed-source URLs are treated as untrusted data',()=>{
  const p=profile();p.life_events[0].chinese_civil_year.rationale='<script>synthetic()</script>';p.sources[0].source.revision_url='javascript:synthetic()';
  const html=personCard(p,true);assert.doesNotMatch(html,/<script>/);assert.match(html,/&lt;script&gt;/);assert.doesNotMatch(html,/href="javascript:/);
});
