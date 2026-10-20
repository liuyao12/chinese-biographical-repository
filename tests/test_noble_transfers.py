import unittest

from scripts.noble_transfers import noble_transfer_errors


class NobleTransfers(unittest.TestCase):
    def fixture(self, known=True):
        evidence=[{'chapter_id':'chapter','paragraph_id':'p','quote':'Synthetic person 甲改封乙侯。'}]
        start=dict(status='source_event',event_type='transfer',date_expression=None,evidence=evidence)
        previous=dict(id='old',person_id='person',kind='noble_rank',mode='grant',
                      effective_period={'end':dict(start,event_type='explicit_end')})
        holding=dict(id='new',person_id='person',kind='noble_rank',mode='transfer',title='乙侯',
                     effective_period={'start':start},transfer_basis=dict(kind='noble_rank_change',
                     previous_holding_id='old' if known else None,
                     previous_title_status='source_context' if known else 'not_identified',
                     source_term='改封乙侯',actor_mention_id='m',evidence=evidence,
                     rationale='Synthetic explicit change.',status='editorial_provisional',human_reviewed=False))
        return holding, {'old':previous}, {'p':('chapter',{'text':evidence[0]['quote']})}, {'m':('chapter','p',{'surface':'甲','person_id':'person'})}

    def test_known_prior_noble_rank_ends_at_the_same_explicit_change(self):
        self.assertEqual(noble_transfer_errors(*self.fixture()),[])

    def test_unknown_prior_rank_is_preserved_without_inventing_one(self):
        self.assertEqual(noble_transfer_errors(*self.fixture(False)),[])

    def test_cannot_link_another_person_or_a_posthumous_name_as_previous_rank(self):
        for key,value in [('person_id','other'),('kind','office'),('mode','posthumous_naming')]:
            args=self.fixture();args[1]['old'][key]=value
            self.assertTrue(noble_transfer_errors(*args))

    def test_death_or_different_date_cannot_replace_explicit_previous_end(self):
        for change in ['death','date','evidence']:
            args=self.fixture();end=args[1]['old']['effective_period']['end']
            if change=='death':end['event_type']='death'
            if change=='date':end['date_expression']='Different year'
            if change=='evidence':end['evidence']=[]
            self.assertTrue(noble_transfer_errors(*args))

    def test_change_word_and_person_anchor_must_match(self):
        args=self.fixture();args[0]['transfer_basis']['source_term']='初封乙侯'
        self.assertTrue(noble_transfer_errors(*args))
        args=self.fixture();args[3]['m'][2]['person_id']='other'
        self.assertTrue(noble_transfer_errors(*args))
