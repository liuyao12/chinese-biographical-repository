# coding: utf-8
"""Source identifications do not turn divine literary scenes into life events."""
import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(name):return json.loads((ROOT/name).read_text())
class DeitiesAndFengshan(unittest.TestCase):
    def setUp(self):
        self.c=read('corpus/shiji/117.json')
        self.p={p['id']:p for p in self.c['paragraphs']}
        self.m={m['id']:m for p in self.c['paragraphs'] for m in p['mentions']}
    def test_named_deities_are_legendary_and_attested_names_remain_exact(self):
        people={p['id']:p for p in read('registry/persons.json')['persons']}
        for surface,label in [('靈媧','女媧'),('馮夷','馮夷'),('屏翳','屏翳')]:
            # The identifier is obtained from the unique received occurrence, not its modern label.
            m=next(m for m in self.p['c-shiji-117-xiangru:p053']['mentions'] if m['surface']==surface)
            person=people[m['person_id']]
            self.assertEqual(person['label'],label)
            self.assertEqual(person['historicity'],'legendary_tradition')
            self.assertEqual([a['surface'] for a in person['aliases']],[surface])
            self.assertEqual(person['evidence'][0]['quote'],surface)
            self.assertEqual(m['kind'],'person')
    def test_explicit_commentary_is_kept_separate_from_received_text(self):
        ds=[d for d in read('corpus/shiji/117-identities.json')['decisions'] if d['id'].startswith('d-shiji117-p053-')]
        self.assertEqual(len(ds),3)
        for d in ds:
            self.assertFalse(d['human_reviewed']);self.assertIsNone(d['model'])
            self.assertTrue(d['identification_basis']['historical_event_attendance_not_inferred'])
            self.assertTrue(all(not r['image_verified'] and r['source_commit'] in r['url'] for r in d['references']))
        self.assertIn('靈媧鼓瑟',self.p['c-shiji-117-xiangru:p053']['text'])
        self.assertTrue(any('靈媧鼓琴' in r['quote'] for d in ds for r in d['references']))
    def test_deity_identification_does_not_add_biographical_assertions(self):
        ids={d['person_id'] for d in read('corpus/shiji/117-identities.json')['decisions'] if d['id'].startswith('d-shiji117-p053-')}
        for fn,key in [('117-life-events.json','events'),('117-titles.json','holdings'),('117-assertions.json','assertions')]:
            rows=read('corpus/shiji/'+fn)[key]
            self.assertFalse(any(pid in json.dumps(row) for pid in ids for row in rows))
    def test_fengshan_context_keeps_tiandi_and_unidentified_official_separate(self):
        d=next(d for d in read('corpus/shiji/117-identities.json')['decisions'] if d['id']=='d-shiji117-fengshan-addressed-emperor')
        self.assertEqual(len(d['identification_basis']['target_mention_ids']),11)
        self.assertTrue(all(self.m[mid]['person_id']=='yqp_nlb_p1p_ACAA' for mid in d['identification_basis']['target_mention_ids']))
        self.assertIsNone(self.m['c-shiji-117-xiangru:m064-0025']['person_id'])
        self.assertIsNone(self.m['c-shiji-117-xiangru:m059-0002']['person_id'])
        self.assertIn('帝以享祉',self.p['c-shiji-117-xiangru:p064']['text'])
    def test_missing_jun_anchors_do_not_tag_junzi_or_duplicate_shun(self):
        p=self.p['c-shiji-117-xiangru:p063']
        for start in [7,34]:
            m=next(m for m in p['mentions'] if m['start']==start)
            self.assertEqual((m['surface'],m['end']),("君",start+1))
        self.assertEqual(len([m for m in p['mentions'] if m['surface']=='舜']),1)
        generic_starts=[i for i in range(len(p['text'])) if p['text'].startswith('君子',i)]
        self.assertEqual(len(generic_starts),2)
        self.assertFalse(any(m['start'] <= i < m['end'] for i in generic_starts for m in p['mentions']))
    def test_unidentified_deities_are_not_forced_into_similar_names(self):
        for word in ['風伯','雨師','玉女','西王母']:
            m=next(m for m in self.p['c-shiji-117-xiangru:p053']['mentions'] if m['surface']==word)
            self.assertIsNone(m['person_id'])
if __name__=='__main__':unittest.main()
