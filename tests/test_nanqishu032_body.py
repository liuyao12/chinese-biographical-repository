# coding: utf-8
import json
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def read(f):return json.loads((ROOT/f).read_text())

class WangYanzhiBody(unittest.TestCase):
    def setUp(self):
        self.c=read('corpus/nanqishu/032.json')
        self.p={p['source_position']['first_line']:p for p in self.c['paragraphs']}
        self.a={a['id']:a for a in read('corpus/nanqishu/032-assertions.json')['assertions']}

    def test_seven_complete_units_expand_only_layout_and_year_template(self):
        excerpts={e['proposed_paragraph_id']:e for e in self.c['source']['normalization']['excerpts']}
        for line in [77,79,81,83,85,87,89]:
            p=self.p[line];raw=excerpts[p['id']]['raw_quote']
            expected=re.sub(r'\{\{YL\|([^}|]+)\}\}',r'\1',raw).strip()
            self.assertEqual(p['text'],expected)
            self.assertFalse(p['source_position']['editorial_excerpt_boundary'])

    def test_father_uncle_and_grandfather_are_different_roles(self):
        father=self.a['a-nanqishu032-yanzhi-father']
        uncle=self.a['a-nanqishu032-yanzhi-paternal-uncle']
        grandfather=self.a['a-nanqishu032-yanzhi-grandfather']
        self.assertEqual(father['subject_person_id'],uncle['subject_person_id'])
        self.assertEqual(len({father['object_person_id'],uncle['object_person_id'],grandfather['object_person_id']}),3)
        song=read('corpus/songshu/066-assertions.json')['assertions']
        zan=next(a['subject_person_id']for a in song if a['id']=='a-songshu066-family-zanzhi-brother')
        self.assertNotEqual(uncle['object_person_id'],zan)
        gaozu=next(m['person_id']for m in read('corpus/songshu/066.json')['paragraphs'][0]['mentions']if m['surface']=='高祖')
        self.assertNotEqual(grandfather['object_person_id'],gaozu)

    def test_earlier_song_emperor_and_later_qi_emperors_keep_scope(self):
        ming=next(m['person_id']for m in self.p[79]['mentions']if m['surface']=='宋明帝')
        taizu=next(m['person_id']for m in self.p[83]['mentions']if m['surface']=='太祖')
        shizu=next(m['person_id']for m in self.p[87]['mentions']if m['surface']=='世祖')
        self.assertEqual(len({ming,taizu,shizu}),3)
        self.assertTrue(all(m['person_id']==ming for m in self.p[81]['mentions']if m['surface']in ['明帝','帝']))
        self.assertTrue(all(m['person_id']==shizu for m in self.p[89]['mentions']if m['surface']=='世祖'))
        songtaizu=next(d['person_id']for d in read('corpus/songshu/066-identities.json')['decisions']if d['id']=='d-songshu066-full-taizu')
        self.assertNotEqual(taizu,songtaizu)

    def test_known_two_person_group_is_not_a_single_person(self):
        group=next(m for m in self.p[83]['mentions']if m['surface']=='二王')
        self.assertIsNone(group['person_id'])
        self.assertEqual(len(group['group_member_person_ids']),2)
        self.assertEqual(group['group_membership_status'],'complete')
        household=next(m for m in self.p[85]['mentions']if m['surface']=='劉家')
        self.assertNotIn('group_member_person_ids',household)
        self.assertIsNone(household['person_id'])

if __name__=='__main__':unittest.main()
