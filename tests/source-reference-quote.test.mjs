import {readFileSync} from 'node:fs';
import test from 'node:test';
import assert from 'node:assert/strict';
import {sourceReferenceQuote, personCard} from '../assets/cbr-person.js';
test('explicit Kanripo display removes only line and page markers',()=>{
 const raw='漢亦使曲城侯\n<pb:synthetic>¶名/捷';
 const ref={quote:raw,quote_format:'kanripo_line_wrapped',display_quote:'漢亦使曲城侯名捷'};
 assert.equal(sourceReferenceQuote(ref),'漢亦使曲城侯名捷');assert.equal(ref.quote,raw);
});
test('a different name in the display quote falls back to original wording',()=>{
 const ref={quote:'名/捷¶',quote_format:'kanripo_line_wrapped',display_quote:'名達'};assert.equal(sourceReferenceQuote(ref),ref.quote);
});
test('unmarked prose and fractions are never rewritten',()=>{
 const ref={quote:'A / B 1/2',display_quote:'AB12'};assert.equal(sourceReferenceQuote(ref),'A / B 1/2');
});
test('without an approved display form all raw source markers remain available',()=>{
 const ref={quote:'<pb:synthetic>¶原/字',quote_format:'kanripo_line_wrapped'};assert.equal(sourceReferenceQuote(ref),ref.quote);assert.equal(sourceReferenceQuote(null),'');
});

const jie=JSON.parse(readFileSync(new URL('../data/corpus/profiles/d7u_bgr_wdi_A.json',import.meta.url),'utf8'));
test('the source-bound unresolved tenure warning is visible in the reading card',()=>{
 assert.match(personCard(jie),/person-chronology-warning/);
});
test('a normal profile without that source caution gets no invented warning',()=>{
 const person=structuredClone(jie);person.reading_decisions=person.reading_decisions.map(d=>{delete d.chronology_caution;return d;});
 assert.doesNotMatch(personCard(person),/person-chronology-warning/);
});

const descendant=JSON.parse(readFileSync(new URL('../data/corpus/profiles/d7u_bgr_wdi_***A.json',import.meta.url),'utf8'));
test('the ancestor relation labels its object as ancestor rather than descendant',()=>{
 const html=personCard(descendant,true);assert.match(html,/ · 先祖：/);assert.doesNotMatch(html,/ · 玄孫：/);
});
test('correcting the relationship direction retains the original xuan-sun source text',()=>{
 const html=personCard(descendant,true);assert.match(html,/<p>玄孫<\/p>/);assert.ok(html.includes('元康亖年，達玄孫茂陵公乘宣詔復家。'));
});
