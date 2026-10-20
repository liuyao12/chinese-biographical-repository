# coding: utf-8
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(rel):return json.loads((ROOT/rel).read_text())
def fixture():return read('tests/fixtures/shiji121-scholars-identities.json')
class ScholarsSourceTests(unittest.TestCase):
    def test_fourteen_source_anchors_are_unchanged(self):
        f=fixture();self.assertEqual(len(f['mentions']),14);self.assertEqual(len(f['mapping']),12)
        ps={p['id']:p for p in read('corpus/shiji/121.json')['paragraphs']}
        for row in f['mentions']:
            p=ps[row['paragraph_id']];self.assertEqual(p['text'],row['text'])
            self.assertEqual(next(m for m in p['mentions'] if m['id']==row['marker']['id']),row['marker'])
    def test_explicit_courtesy_names_identify_the_same_students(self):
        ps=read('corpus/shiji/067.json')['paragraphs']
        for suffix,pid,forms in [('p019','t7x_2x7_1fc',['仲由','子路']),('p051','z8l_wje_08d',['卜商','子夏']),('p056','482_ly0_otk',['顓孫師','子張']),('p062','oxa_rta_lvd',['澹臺滅明','子羽']),('p035','7c4_6v2_yvm',['端木賜','子貢'])]:
            p=next(p for p in ps if p['id'].endswith(':'+suffix))
            for form in forms:self.assertTrue(any(m['surface']==form and m['person_id']==pid for m in p['mentions']))
    def test_homonymous_names_remain_separate(self):
        people={p['id']:p for p in read('registry/persons.json')['persons']}
        self.assertIn('4w5_b4e_vf5_AI',people);self.assertIn('z8l_wje_08d',people)
        self.assertEqual(people['4w5_b4e_vf5_AI']['family_path']['parent_person_id'],'4w5_b4e_vf5_A')
        self.assertTrue(any(a['surface']=='子夏' for a in people['4w5_b4e_vf5_AI']['aliases']))
        self.assertIn('ux3_la0_38d',people);self.assertIn('saz_old_5fi',people)
        for old in fixture()['mapping']:self.assertNotIn(old,people)
    def test_decisions_are_scoped_and_preserve_limits(self):
        ds=[d for d in read('corpus/shiji/121-identities.json')['decisions'] if d['id'].startswith('d-shiji121-scholars-')]
        self.assertEqual(len(ds),12)
        for d in ds:
            self.assertFalse(d['human_reviewed']);self.assertIsNone(d['model']);self.assertGreaterEqual(len(d['chapter_ids']),2)
        wu=next(d for d in ds if d['person_id']=='61h_0sk_4pb');self.assertIn('曾子',wu['rationale']);self.assertIn('子夏',wu['rationale'])
        shang=next(d for d in ds if d['person_id']=='66i_9gx_pc4');self.assertIn('不是父系',shang['rationale'])
class ScholarsPublicTests(unittest.TestCase):
    def test_old_exports_removed_after_relinking(self):
        for old,new in fixture()['mapping'].items():
            for folder in ['exports/persons','data/corpus/profiles']:
                self.assertFalse((ROOT/folder/(old+'.json')).exists());self.assertTrue((ROOT/folder/(new+'.json')).exists())
    def test_each_canonical_bundle_and_profile_has_source_chapter(self):
        for new in fixture()['mapping'].values():
            for folder in ['exports/persons','data/corpus/profiles']:
                self.assertIn('c-shiji-121-rulin',json.dumps(read(folder+'/'+new+'.json'),ensure_ascii=False))
if __name__=='__main__':unittest.main()
