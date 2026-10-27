"""Source readings, parser output, and rejection of unsupported name changes."""
import copy
import json
import unittest
from pathlib import Path
from scripts import wyd_song044_names as names
from scripts.person_bundle import bundle, load_catalog
ROOT = Path(__file__).resolve().parents[1]

class WydNameComponentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = json.loads((ROOT/'corpus/songshu/044-wyd1739.json').read_text())
        cls.rows = json.loads((ROOT/'corpus/songshu/044-wyd1739-name-components.json').read_text())['records']
        cls.byrole = {n['component_source_binding']['source_role_key']: n for n in cls.rows}
        cls.facts = json.loads((ROOT/'corpus/songshu/044-wyd1739-assertions.json').read_text())['assertions']

    def test_literal_names_and_courtesy_anchor(self):
        for role, surname, ming in [('hui','謝','晦'),('xiedun','謝','遯'),('shiyou','謝','世猷'),('shangxuanshi','商','玄石')]:
            row = self.byrole[role]
            self.assertEqual((row['surname'],row['ming']),(surname,ming))
            p = next(p for p in self.chapter['paragraphs'] if p['id']==row['paragraph_id'])
            m = next(m for m in p['mentions'] if m['id']==row['person_mention_id'])
            self.assertEqual(m['surface'],surname+ming)
        hui = self.byrole['hui']; a = hui['component_source_binding']['courtesy_anchor']
        self.assertEqual(hui['zi'],'宣明')
        self.assertEqual(hui['quote'][a['start']:a['end']],'宣明')
        self.assertEqual(hui['quote'][a['start']-1],'字')

    def test_inferred_surnames_need_named_relationships(self):
        for role, surname, ming in [('lang','謝','朗'),('chong','謝','重'),('xuan-brother','謝','絢'),('shixiu','謝','世休'),('shiji','謝','世基'),('shao','謝','紹'),('huaifu','商','懷福')]:
            row=self.byrole[role]
            self.assertEqual((row['surname'],row['ming']),(surname,ming))
            names.validate_surname(row,self.rows,{names.CID:self.chapter},self.facts,ROOT)
            self.assertTrue(row['surname_basis']['relationship_assertion_ids'])
            self.assertFalse(row['human_reviewed'])

    def test_wife_is_clan_named_and_not_a_named_mother(self):
        row=self.byrole['wife-cao']
        self.assertEqual(row['surname'],'曹'); self.assertIsNone(row['ming'])
        self.assertEqual(row['clan_style']['value'],'曹氏')
        p=next(p for p in self.chapter['paragraphs'] if p['id']==row['paragraph_id'])
        self.assertTrue(names.clan_valid(row,p,self.facts))
        self.assertFalse(any(a['predicate']=='mother' and a.get('object_person_id')==row['person_id'] for a in self.facts))
        mutated=copy.deepcopy(row); mutated['surname']='謝'
        self.assertFalse(names.component_valid(mutated,self.chapter,ROOT))

    def test_kinship_term_is_not_a_surname(self):
        row=self.byrole['zongshuxian']; self.assertIsNone(row['surname'])
        self.assertEqual(row['ming'],'獻')
        for surname in ['宗','王','謝']:
            mutated=copy.deepcopy(row); mutated['surname']=surname
            self.assertFalse(names.component_valid(mutated,self.chapter,ROOT))

    def test_foreign_anchors_and_borrowed_names_rejected(self):
        original=self.byrole['hui']
        for field,value in [('person_mention_id',self.byrole['wife-cao']['person_mention_id']),('zi','宣遠'),('surname','王'),('ming','朗'),('quote',original['quote']+'字宣遠')]:
            mutated=copy.deepcopy(original); mutated[field]=value
            self.assertFalse(names.component_valid(mutated,self.chapter,ROOT),field)
        changed=copy.deepcopy(self.chapter); changed['paragraphs'][0]['text']+='字宣遠'
        self.assertFalse(names.component_valid(original,changed,ROOT))

    def test_reversed_or_adoptive_parent_does_not_support_surname(self):
        row=self.byrole['shixiu']; aid=row['surname_basis']['relationship_assertion_ids'][0]
        for mutation in ['reverse','adoptive','maternal','missing']:
            facts=copy.deepcopy(self.facts); a=next(a for a in facts if a['id']==aid)
            if mutation=='reverse': a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id']
            elif mutation=='adoptive': a['qualifiers']['adoptive']=True
            elif mutation=='maternal': a['qualifiers']['lineage']='maternal'
            else: facts.remove(a)
            with self.assertRaises(ValueError,msg=mutation):
                names.validate_surname(row,self.rows,{names.CID:self.chapter},facts,ROOT)

    def test_actual_person_json_includes_the_structured_readings(self):
        catalog=load_catalog(ROOT)
        for row in self.rows:
            result=bundle(row['person_id'],root=ROOT,catalog=catalog)
            found=next(n for n in result.get('name_components',[]) if n['id']==row['id'])
            self.assertEqual((found['surname'],found['ming']),(row['surname'],row['ming']))
            self.assertEqual(found.get('zi'),row.get('zi'))

if __name__=='__main__': unittest.main()
