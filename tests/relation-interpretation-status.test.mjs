import test from 'node:test';
import assert from 'node:assert/strict';
import {personCard} from '../assets/cbr-person.js';

test('contextual subject resolution is visible in source-attested kinship', () => {
  const person = {
    id: 'younger', person_ids: ['younger'], label: '定', names: [], name_components: [],
    titles: [], addresses: [], occurrences: [], table_occurrences: [], preferred_relations: [],
    related_people: {younger: '定', elder: '襲'}, dates: [], sources: [],
    relations: [{
      subject_person_id: 'younger', predicate: 'brother', object_person_id: 'elder',
      status: 'source_attested',
      qualifiers: {
        source_term: '弟定', interpretation_status: 'contextual_provisional',
        interpretation_note: '主語襲由上下文承接，判讀可修訂。'
      },
      evidence: [{quote: '襲弟彪祕書郎弟定'}]
    }]
  };
  const html = personCard(person, true);
  assert.match(html, /兄弟：/);
  assert.match(html, /主語承接暫定/);
  assert.match(html, /主語襲由上下文承接，判讀可修訂。/);
});
