import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';
import {personCard} from '../assets/cbr-person.js';
test('completed surname remains the person heading and editorial notes stay in a disclosure',()=>{
 const p=JSON.parse(fs.readFileSync(new URL('../data/corpus/profiles/6na_bet_3ch.json',import.meta.url)));const html=personCard(p,true);assert.ok(html.includes('<h1>謝瑤</h1>'));assert.ok(html.includes('<details class="person-identity-note">'));assert.ok(html.includes(p.identity_note));assert.ok(html.includes('姓名依據'));
});
