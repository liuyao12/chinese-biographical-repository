import unittest

from scripts.person_bundle import validate_clan_style


class ClanNames(unittest.TestCase):
    def fixture(self, inferred=False):
        term='司馬景王文王之妺也' if inferred else '鍾氏'
        quote='乙妻'+term if inferred else '鍾氏，字琰。'
        style=dict(kind='sibling_clan_appellation' if inferred else 'received_clan_appellation',
                   value='司馬氏' if inferred else '鍾氏',source_term=term,
                   assertion_ids=['sister'] if inferred else [],
                   status='editorial_provisional' if inferred else 'source_attested',
                   rationale='Synthetic appellation evidence.',human_reviewed=False)
        name=dict(person_id='woman',surname='司馬' if inferred else '鍾',ming=None,
                  quote=quote,paragraph_id='p',clan_style=style)
        paragraph=dict(text=quote,mentions=[dict(person_id='woman',surface='妺' if inferred else '鍾氏')])
        relations=[dict(id='sister',predicate='sister',subject_person_id='woman',object_person_id='brother',
                        qualifiers={'source_term':term},evidence=[dict(paragraph_id='p',quote=quote)])]
        return name,paragraph,relations

    def test_received_clan_appellation_does_not_require_a_known_ming(self):
        self.assertIsNone(validate_clan_style(*self.fixture()))

    def test_inferred_clan_appellation_requires_explicit_sister_evidence(self):
        self.assertIsNone(validate_clan_style(*self.fixture(True)))
        name,paragraph,relations=self.fixture(True)
        with self.assertRaises(ValueError):validate_clan_style(name,paragraph,[])
        relations[0]['qualifiers']['shared_father']=False
        with self.assertRaises(ValueError):validate_clan_style(name,paragraph,relations)

    def test_courtesy_name_cannot_be_filled_as_ming_for_clan_style(self):
        name,paragraph,relations=self.fixture();name['ming']='琰'
        with self.assertRaises(ValueError):validate_clan_style(name,paragraph,relations)

    def test_clan_display_cannot_be_overridden_by_an_unrelated_string(self):
        name,paragraph,relations=self.fixture();name['clan_style']['value']='Different person'
        with self.assertRaises(ValueError):validate_clan_style(name,paragraph,relations)
