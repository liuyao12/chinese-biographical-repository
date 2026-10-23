# coding: utf-8
"""Synthetic source frames: adjacency alone must not establish an office."""
import hashlib
import unittest
from scripts.layered_biography_titles import holding_valid

def case(rule, title):
    appellation = rule == 'appellation_title_attestation'
    text = '張' + title if appellation else ('故' if rule == 'past_prefix_office' else '') + title + '張三'
    person_start = 0 if appellation else len(text) - 2
    person = {'id':'synthetic-mention','kind':'person','person_id':'synthetic-person','surface':text[person_start:],'start':person_start,'end':len(text)}
    paragraph = {'id':'synthetic-paragraph','text':text,'mentions':[person]}
    chapter = {'id':'synthetic-chapter','work_id':'synthetic-work','book_id':'synthetic-book','source_id':'synthetic-source','source':{'revision_id':'synthetic-revision'},'paragraphs':[paragraph]}
    def anchor(a,b):
        return {'paragraph_id':paragraph['id'],'start':a,'end':b,'surface':text[a:b]}
    start = 1 if appellation or rule == 'past_prefix_office' else 0
    office = anchor(start,start+len(title))
    unknown = {'status':'unknown','date_expression':None,'evidence':[]}
    role = {'kind':'layered_biographical_role_frame','human_reviewed':False,'source_revision':'synthetic-revision','paragraph_id':paragraph['id'],'paragraph_sha256':hashlib.sha256(text.encode()).hexdigest(),'scope_anchor':anchor(0,len(text)),'rule':rule,'roles':{'subject':person['id']},'fields':{'prefix':anchor(0,1),'title':office} if appellation else {'office':office},'slot':'office','recipient_role':'subject'}
    holding = {'id':'synthetic-holding','person_id':person['person_id'],'title':title,'kind':'office','mode':'attestation','appointment_role':'source_appellation' if appellation else ('past_source_report' if rule == 'past_prefix_office' else 'source_report'),'status':'source_attested','human_reviewed':False,'source_career_role':role,'effective_period':{'start':dict(unknown),'end':dict(unknown)},'attestations':[dict(office,person_mention_id=person['id'],date_expression=None)],'evidence':[{'quote':text,'person_mention_id':person['id'],'work_id':chapter['work_id'],'book_id':chapter['book_id'],'chapter_id':chapter['id'],'source_id':chapter['source_id']}]}
    return holding, chapter

class LayeredOfficeWords(unittest.TestCase):
    def test_prefix_adjacency_rejects_prose(self):
        self.check_rule('prefix_office')
    def test_past_prefix_does_not_license_prose(self):
        self.check_rule('past_prefix_office')
    def test_person_appellation_requires_an_office_noun(self):
        self.check_rule('appellation_title_attestation')
    def check_rule(self,rule):
        for text in ('少與','能通','清靜','好學','字子家'):
            with self.subTest(rule=rule,text=text):
                self.assertFalse(holding_valid(*case(rule,text)))
        for title in ('中郎','將軍'):
            with self.subTest(rule=rule,title=title):
                self.assertTrue(holding_valid(*case(rule,title)))
