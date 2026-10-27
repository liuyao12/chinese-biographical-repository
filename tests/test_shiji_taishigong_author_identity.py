# coding: utf-8
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
KEEP='pme_eis_xqi_*A*AAAAA'
TAN='pme_eis_xqi_*A*AAAA'
def read(rel):return json.loads((ROOT/rel).read_text())


class TaishigongAuthorIdentityTests(unittest.TestCase):
    def test_directory_does_not_create_a_person_per_chapter(self):
        people=read('registry/persons.json')['persons']
        self.assertFalse([p for p in people if p['label'].startswith('太史公')])
        by={p['id']:p for p in people}
        self.assertEqual(by[KEEP]['label'],'司馬遷')
        self.assertEqual(by[TAN]['label'],'司馬談')
        self.assertEqual({p['id'] for p in people if any(a['surface']=='太史公' for a in p['aliases'])},{KEEP,TAN})

    def test_every_reviewed_occurrence_points_to_one_author_and_keeps_its_text(self):
        review=read('source-evidence/shiji-taishigong-author-identity/identity-reading.json')
        self.assertEqual(review['removed_source_local_profile_count'],72)
        self.assertEqual(review['source_occurrence_count'],85)
        chapters={d['id']:d for p in (ROOT/'corpus/shiji').glob('*.json')
                  if (d:=json.loads(p.read_text())).get('record_type')=='marked_chapter'}
        for unit in review['source_units']:
            p=next(p for p in chapters[unit['chapter_id']]['paragraphs'] if p['id']==unit['paragraph_id'])
            self.assertEqual(p['text'],unit['quote'])
            for mid in unit['mention_ids']:
                m=next(m for m in p['mentions'] if m['id']==mid)
                self.assertEqual(m['person_id'],KEEP)
                self.assertEqual(p['text'][m['start']:m['end']],m['surface'])

    def test_father_in_self_account_is_not_merged_into_son(self):
        ch=read('corpus/shiji/130.json')
        for suffix in ('p003','p004','p006'):
            p=next(p for p in ch['paragraphs'] if p['id'].endswith(':'+suffix))
            self.assertTrue(any(m['surface']=='太史公' and m['person_id']==TAN for m in p['mentions']))
        p=next(p for p in ch['paragraphs'] if p['id'].endswith(':p143'))
        self.assertEqual(next(m['person_id'] for m in p['mentions'] if m['surface']=='太史公'),KEEP)

    def test_chu_reference_retains_commentary_layer(self):
        for number,pid in [(60,'p018'),(126,'p013')]:
            p=next(p for p in read(f'corpus/shiji/{number:03}.json')['paragraphs'] if p['id'].endswith(':'+pid))
            self.assertEqual(p['text_layer'],'witness_appended_chu_note')
            self.assertTrue(any(m['surface']=='太史公' and m['person_id']==KEEP for m in p['mentions']))

    def test_posthumous_continuation_is_not_automatically_assigned(self):
        ch=read('corpus/shiji/096.json')
        p=next(p for p in ch['paragraphs'] if p['id'].endswith(':p029'))
        m=next(m for m in p['mentions'] if m['surface']=='太史公')
        self.assertEqual((m['kind'],m['person_id']),('unresolved',None))

    def test_old_person_files_and_public_aliases_are_removed(self):
        receipt=read('source-evidence/shiji-taishigong-author-identity/annotation-chain.json')
        self.assertEqual(len(receipt['retired_person_ids']),72)
        current={p['id'] for p in read('registry/persons.json')['persons']}
        for old in receipt['retired_person_ids']:
            self.assertNotIn(old,current)
            self.assertFalse((ROOT/'exports/persons'/f'{old}.json').exists())
            self.assertFalse((ROOT/'data/corpus/profiles'/f'{old}.json').exists())


if __name__=='__main__':unittest.main()
