import copy
import json
import unittest
from pathlib import Path

from scripts.directed_uncle_roles import paternal_uncle_direction_valid
from scripts.inscription_family_lists import valid as family_list_valid
from scripts.web_inscription_excerpts import facts_valid, source_errors


ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


class QingheCuiEpitaphs(unittest.TestCase):
    def test_actual_witness_and_separate_death_and_reburial_days(self):
        documents = [read(p) for p in sorted((ROOT / 'corpus/epitaph-cuihun').glob('*.json'))]
        chapter = next(d for d in documents if d['record_type'] == 'marked_chapter')
        works = {w['id']: w for w in read('registry/works.json')['works']}
        books = {b['id']: b for w in works.values() for b in w['books']}
        self.assertEqual(source_errors(chapter, ROOT, works, books), [])
        changed = copy.deepcopy(chapter)
        changed['source']['image_verified'] = True
        self.assertTrue(source_errors(changed, ROOT, works, books))
        changed = copy.deepcopy(chapter)
        changed['paragraphs'][1]['text'] = changed['paragraphs'][1]['text'].replace('飲粒不？', '飲粒不進')
        self.assertTrue(source_errors(changed, ROOT, works, books))
        self.assertTrue(facts_valid(chapter, documents))
        death = next(d for d in documents if d['record_type'] == 'person_life_event_assertion_set')['events'][0]
        burial = next(d for d in documents if d['record_type'] == 'person_event_assertion_set')['events'][0]
        burial['epitaph_date_parts']['day_anchor'] = death['epitaph_date_parts']['day_anchor']
        self.assertFalse(facts_valid(chapter, documents))

    def test_family_list_and_named_uncle_have_directed_roles(self):
        chapter = read('corpus/epitaph-cuihong/excerpts.json')
        claims = read('corpus/epitaph-cuihong/excerpts-assertions.json')['assertions']
        son = next(a for a in claims if a['qualifiers']['source_term'] == '次息子文')
        self.assertTrue(family_list_valid(son, chapter))
        wrong = copy.deepcopy(son)
        other = next(a for a in claims if a['qualifiers']['source_term'] == '次息子真')
        wrong['context']['member_mention_id'] = other['context']['member_mention_id']
        self.assertFalse(family_list_valid(wrong, chapter))
        base = 'corpus/weishu-weishou/067-wei67'
        history = read(base + '.json')
        paragraphs = {p['id']: (history['id'], p) for p in history['paragraphs']}
        uncle = next(a for a in read(base + '-assertions.json')['assertions'] if a['qualifiers']['source_term'] == '叔鵾')
        self.assertTrue(paternal_uncle_direction_valid(uncle, paragraphs))
        wrong = copy.deepcopy(uncle)
        wrong['subject_person_id'], wrong['object_person_id'] = uncle['object_person_id'], uncle['subject_person_id']
        e = wrong['evidence'][0]
        e['subject_person_mention_id'], e['object_person_mention_id'] = e['object_person_mention_id'], e['subject_person_mention_id']
        self.assertFalse(paternal_uncle_direction_valid(wrong, paragraphs))
