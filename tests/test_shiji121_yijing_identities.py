# coding: utf-8
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(rel):return json.loads((ROOT/rel).read_text())
def fixture():return read('tests/fixtures/shiji121-yijing-identities.json')
class YijingSourceTests(unittest.TestCase):
    def test_six_original_spans_preserve_names_and_dates(self):
        f=fixture();self.assertEqual(len(f['mentions']),6)
        for row in f['mentions']:
            p=next(p for p in read(row['path'])['paragraphs'] if p['id']==row['paragraph_id'])
            self.assertEqual(p['text'],row['text']);self.assertEqual(next(m for m in p['mentions'] if m['id']==row['marker']['id']),row['marker'])
        p=next(p for p in read('corpus/shiji/067.json')['paragraphs'] if p['id'].endswith(':p083'))
        self.assertIn('王子中同',p['text']);self.assertIn('何元朔中以治易爲漢中大夫',p['text'])
        p=next(p for p in read('corpus/shiji/121.json')['paragraphs'] if p['id'].endswith(':p019'))
        self.assertIn('王同子仲',p['text']);self.assertIn('元光元年徵，官至中大夫',p['text'])
    def test_three_decisions_have_both_chapters_and_variants(self):
        ds=[d for d in read('corpus/shiji/121-identities.json')['decisions'] if d['id'].startswith('d-shiji121-yijing-')]
        self.assertEqual(len(ds),3)
        for d in ds:
            self.assertEqual(set(d['chapter_ids']),{'c-shiji-067-disciples','c-shiji-121-rulin'})
            self.assertFalse(d['human_reviewed']);self.assertIsNone(d['model'])
        wang=next(d for d in ds if d['person_id']=='yuy_gbn_g7e');self.assertIn('子中',wang['rationale']);self.assertIn('子仲',wang['rationale'])
    def test_registry_consolidates_aliases_without_inventing_family(self):
        ps={p['id']:p for p in read('registry/persons.json')['persons']}
        for old,new in fixture()['mapping'].items():self.assertNotIn(old,ps);self.assertIn(new,ps);self.assertNotIn('family_path',ps[new])
        for pid,forms in [('aly_3ph_2la',['田何','田子莊何']),('yuy_gbn_g7e',['王同','王子中同']),('rpk_mne_stx',['楊何'])]:
            aliases={a['surface'] for a in ps[pid]['aliases']};self.assertTrue(set(forms).issubset(aliases))
class YijingPublicTests(unittest.TestCase):
    def test_old_public_ids_are_removed(self):
        for old in fixture()['mapping']:
            for folder in ['exports/persons','data/corpus/profiles']:self.assertFalse((ROOT/folder/(old+'.json')).exists())
    def test_each_profile_has_both_source_chapters(self):
        for new in fixture()['mapping'].values():
            p=read('data/corpus/profiles/'+new+'.json');chapters={o['chapter_id'] for o in p['occurrences']}
            self.assertTrue({'c-shiji-067-disciples','c-shiji-121-rulin'}.issubset(chapters))
if __name__=='__main__':unittest.main()
