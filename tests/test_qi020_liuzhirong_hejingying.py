from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import unittest

from scripts.liang021_print_columns import errors as print_errors
from scripts.maternal_roles import maternal_role_valid
from scripts.pei_royal_biographies import errors as pei_errors
from scripts.six_dynasties_inventory import chapter_passage, source_paragraphs, source_passage


ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_bytes())


class QiConsorts(unittest.TestCase):
    def test_liuzhirong_received_ancestry_and_two_dates(self):
        stem = 'corpus/nanqishu/020-liuzhirong-ancestry'
        q = read(stem + '.json')
        self.assertEqual(pei_errors(q, ROOT), [])
        self.assertEqual([p['source_position']['first_line'] for p in q['paragraphs']], [19, 21])
        self.assertEqual([m['surface'] for m in q['paragraphs'][0]['mentions']], ['智容','玄之','壽之'])
        self.assertEqual(q['annotation']['age_assertions'][0]['value'], 50)
        edges = read(stem + '-assertions.json')['assertions']
        self.assertEqual({a['subject_person_id'] for a in edges if a['predicate'] == 'father'
                          and '壽之子' in a['qualifiers']['source_term']},
                         {'gm4_alk_hn7_AB','gm4_alk_hn7_AC','gm4_alk_hn7_AD','gm4_alk_hn7_AE'})
        n = read('corpus/nanshi/011-liuzhirong.json')
        self.assertFalse(n['annotation'].get('age_assertions'))
        self.assertIn('年十七，裴方明為子求婚', n['paragraphs'][1]['text'])
        self.assertIn('既而與裴氏不成婚', n['paragraphs'][1]['text'])
        for book, year in [('qi020-liuzhirong-wyd', '三年贈后父'), ('nan011-liuzhirong-izumo','二年贈后父')]:
            ledger = 'wuying-reading.json' if 'wyd' in book else 'izumo-reading.json'
            proof = read('source-evidence/' + book + '/' + ledger)
            text = ''.join(c['reading'] for c in proof['columns'])
            self.assertIn(year,text)
            self.assertIn('上都鄉君' if 'wyd' in book else '上虞都鄉君', text)

    def test_hejingying_mothers_and_wedding_witnesses(self):
        for stem, year, surname in [
            ('nanqishu/020-hejingying','永明二年','劉氏'),
            ('nanqishu/020-hejingying-wyd','永明二年','劉氏'),
            ('nanshi/011-hejingying','永明三年','劉'),
            ('nanshi/011-hejingying-izumo','永明三年','劉'),
        ]:
            with self.subTest(stem=stem):
                c = read('corpus/' + stem + '.json')
                self.assertIn(year,c['paragraphs'][0]['text'])
                edges = read('corpus/' + stem + '-assertions.json')['assertions']
                paragraphs = {p['id']:(c['id'],p) for p in c['paragraphs']}
                role, = [e for e in edges if e['predicate'] == 'maternal_role']
                actual, = [e for e in edges if e['predicate'] == 'mother'
                           and e['subject_person_id'] == role['subject_person_id']]
                self.assertEqual(role['qualifiers']['source_term'],'嫡母'+surname)
                self.assertNotEqual(actual['object_person_id'], role['object_person_id'])
                self.assertNotEqual(role['object_person_id'],'hx8_st4_jdd_C')
                self.assertTrue(maternal_role_valid(role,paragraphs))
                for field, value in [('object_person_id',actual['object_person_id']),
                                     ('subject_person_id',actual['object_person_id'])]:
                    fake = deepcopy(role)
                    fake[field] = value
                    self.assertFalse(maternal_role_valid(fake,paragraphs))
                fake = deepcopy(role)
                fake['qualifiers']['biological_mother'] = True
                self.assertFalse(maternal_role_valid(fake,paragraphs))
                if stem.endswith(('-wyd','-izumo')):
                    self.assertEqual(print_errors(c,ROOT),[])

    def test_nanshi_011_three_readings_cover_the_shared_paragraph(self):
        inventory = read('data/corpus/six-dynasties-biographies.json')
        c = read('corpus/nanshi/011-hejingying.json')
        lines = (ROOT / c['source']['raw_path']).read_text().splitlines()
        p = c['paragraphs'][2]
        self.assertEqual(p['text'],lines[124])
        owner_spans = []
        for title in ('鬱林王妃何婧英','馬澄','楊瑉之（女巫子）'):
            entry, = [e for e in inventory['biographies'] if e['book_id'] == c['book_id'] and e['title'] == title]
            self.assertEqual(chapter_passage(entry,c)[1],
                             source_paragraphs(source_passage(entry,lines,set(),set())))
            spans = entry['paragraph_slices'][p['id']]
            for s in spans if isinstance(spans,list) else [spans]:
                owner_spans.append((s['start'],s['end']))
        cursor=0
        for a,b in sorted(owner_spans):
            self.assertEqual(a,cursor)
            cursor=b
        self.assertEqual(cursor,len(p['text']))
        proof = read('source-evidence/nan011-hejingying-izumo/izumo-reading.json')
        self.assertEqual([(e['title'],len(e['spans'])) for e in proof['embedded_accounts']],
                         [('馬澄',1),('楊瑉之（女巫子）',2)])

    def test_qi_volume_boundaries_follow_original_positions(self):
        proof = read('source-evidence/qi020-hejingying/volume-boundaries.json')
        raw = (ROOT / proof['raw_path']).read_bytes()
        self.assertEqual(sha256(raw).hexdigest(),proof['raw_sha256'])
        text = raw.decode()
        for item in proof['boundary_decisions'] + proof['outside_biographies']:
            self.assertEqual(text[item['raw_start']:item['raw_end']],item['quote'])
        lines = [p['raw_line'] for e in proof['accounts'] for p in e['positions']]
        self.assertEqual(sorted(lines),proof['body_lines'])
        self.assertEqual(len(lines),len(set(lines)))
        self.assertEqual((proof['heading_count'],proof['embedded_count']),(9,1))
