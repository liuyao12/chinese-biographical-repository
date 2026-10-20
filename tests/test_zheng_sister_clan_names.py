import copy
import json
import unittest
from pathlib import Path
from scripts.person_bundle import validate_clan_style

ROOT=Path(__file__).resolve().parents[1]

class ZhengSisterClanNames(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.names=json.loads((ROOT/'data/corpus/profile-names.json').read_text())['records']
        cls.chapter=json.loads((ROOT/'corpus/jinshu/032.json').read_text())
        cls.paragraph=next(p for p in cls.chapter['paragraphs'] if p['source_position']['first_line']==66)
        cls.relations=json.loads((ROOT/'corpus/jinshu/032-assertions.json').read_text())['assertions']
        cls.sisters=[n for n in cls.names if n.get('clan_style',{}).get('kind')=='source_sibling_group_appellation']

    def test_three_sisters_have_inferred_clan_appellations_and_unknown_ming(self):
        self.assertEqual(len(self.sisters),3)
        for n in self.sisters:
            self.assertIsNone(validate_clan_style(n,self.paragraph,self.relations))
            self.assertEqual(n['surname'],'鄭')
            self.assertIsNone(n['ming'])
            self.assertEqual(n['clan_style']['status'],'editorial_provisional')
            self.assertEqual(n['clan_style']['value'],'鄭氏')
            self.assertNotIn('full_name',n)

    def test_clan_inference_needs_valid_group_and_explicitly_named_sister(self):
        name=self.sisters[0]
        for mutation in ['count','different-surname','missing-relation','opposite-recipient','not-shared-father','missing-group']:
            n=copy.deepcopy(name);rels=copy.deepcopy(self.relations)
            relation=next(a for a in rels if a['id']==n['clan_style']['assertion_ids'][0])
            if mutation=='count':relation['qualifiers']['source_sibling_group']['reported_count']=3
            elif mutation=='different-surname':n['surname']='王';n['clan_style']['value']='王氏'
            elif mutation=='missing-relation':rels=[]
            elif mutation=='opposite-recipient':relation['subject_person_id'],relation['object_person_id']=relation['object_person_id'],relation['subject_person_id']
            elif mutation=='not-shared-father':relation['qualifiers']['shared_father']=False
            else:relation['qualifiers'].pop('source_sibling_group')
            with self.subTest(mutation=mutation):
                with self.assertRaises(ValueError):validate_clan_style(n,self.paragraph,rels)

    def test_clan_style_cannot_invent_a_personal_name_or_claim_received_status(self):
        for change in ['ming','status','assertion_ids']:
            n=copy.deepcopy(self.sisters[0])
            if change=='ming':n['ming']='阿春'
            elif change=='status':n['clan_style']['status']='source_attested'
            else:n['clan_style']['assertion_ids']*=2
            with self.assertRaises(ValueError):validate_clan_style(n,self.paragraph,self.relations)

    def test_chengdi_eldest_son_is_numeric_and_scoped_to_father(self):
        a=json.loads((ROOT/'corpus/jinshu/007-assertions.json').read_text())['assertions'][0]
        o=a['qualifiers']['birth_order']
        self.assertEqual(o['ordinal'],1)
        self.assertIs(type(o['ordinal']),int)
        self.assertEqual(o['scope'],'sons_of_parent')
        self.assertEqual(o['parent_person_id'],a['object_person_id'])
        self.assertIn('明帝長子',a['evidence'][0]['quote'])

if __name__=='__main__':unittest.main()
