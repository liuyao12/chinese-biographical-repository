# coding: utf-8
import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(rel):return json.loads((ROOT/rel).read_text())
def fixture():return read('tests/fixtures/shiji121-court-identities.json')
class CourtSourceTests(unittest.TestCase):
    def test_all_sixty_one_source_markers_and_text_preserved(self):
        f=fixture();self.assertEqual(len(f['mapping']),12);self.assertEqual(len(f['mentions']),61)
        ps={p['id']:p for p in read('corpus/shiji/121.json')['paragraphs']}
        for item in f['mentions']:
            p=ps[item['paragraph_id']];self.assertEqual(p['text'],item['text'])
            self.assertEqual(next(m for m in p['mentions'] if m['id']==item['marker']['id']),item['marker'])
    def test_twelve_decisions_retain_two_source_contexts(self):
        ds=[d for d in read('corpus/shiji/121-identities.json')['decisions'] if d['id'].startswith('d-shiji121-court-')]
        self.assertEqual(len(ds),12)
        for d in ds:
            self.assertFalse(d['human_reviewed']);self.assertIsNone(d['model'])
            self.assertIn('c-shiji-121-rulin',d['chapter_ids']);self.assertGreaterEqual(len(d['chapter_ids']),2)
            self.assertTrue(d['rationale']);self.assertTrue(d['evidence'])
    def test_emperor_markers_do_not_expand_into_generic_uses(self):
        ps={p['id']:p for p in read('corpus/shiji/121.json')['paragraphs']}
        markers=[m for p in ps.values() for m in p['mentions'] if m['person_id']=='yqp_nlb_p1p_ACAA']
        self.assertEqual(len(markers),22)
        p=ps['c-shiji-121-rulin:p006']
        start=p['text'].index('十八已上')
        self.assertFalse(any(m['person_id']=='yqp_nlb_p1p_ACAA' and start<=m['start']<start+4 for m in p['mentions']))
        p=ps['c-shiji-121-rulin:p010']
        self.assertFalse(any(m['person_id']=='yqp_nlb_p1p_ACAA' for m in p['mentions']))
    def test_retired_registry_ids_absent_and_kongjia_stays_distinct(self):
        people={p['id']:p for p in read('registry/persons.json')['persons']}
        for old,new in fixture()['mapping'].items():self.assertNotIn(old,people);self.assertIn(new,people)
        p=next(p for p in read('corpus/shiji/121.json')['paragraphs'] if p['id'].endswith(':p003'))
        kong=next(m for m in p['mentions'] if m['surface']=='孔甲');self.assertNotIn(kong['person_id'],fixture()['mapping'].values())
class CourtPublicTests(unittest.TestCase):
    def test_old_public_files_removed_and_canonical_bundles_have_chapter(self):
        for old,new in fixture()['mapping'].items():
            for folder in ['exports/persons','data/corpus/profiles']:self.assertFalse((ROOT/folder/(old+'.json')).exists())
            bundle=read('exports/persons/'+new+'.json')
            self.assertIn('c-shiji-121-rulin',json.dumps(bundle,ensure_ascii=False))
    def test_each_profile_has_readable_source_and_person_id(self):
        for new in fixture()['mapping'].values():
            p=read('data/corpus/profiles/'+new+'.json')
            text=json.dumps(p,ensure_ascii=False);self.assertIn(new,text);self.assertIn('c-shiji-121-rulin',text)
if __name__=='__main__':unittest.main()
