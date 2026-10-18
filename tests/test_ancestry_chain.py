# coding: utf-8
import copy
import json
import unittest
from pathlib import Path
from scripts.ancestry_chain import consecutive_ancestor_parent_valid
from scripts.family_assemblies import load_assemblies
from scripts.person_bundle import load_catalog
ROOT=Path(__file__).resolve().parents[1]

class ConsecutiveAncestors(unittest.TestCase):
    def fixture(self):
        body='synthetic child names parent, grandfather and great-grandfather'
        evidence={'chapter_id':'chapter','paragraph_id':'para','source_id':'source','quote':body}
        near={'id':'near','subject_person_id':'child','predicate':'grandfather','object_person_id':'grand','status':'source_attested','qualifiers':{'lineage':'paternal'},'evidence':[evidence]}
        far=dict(near,id='far',predicate='great_grandfather',object_person_id='great')
        refs=[dict(evidence,assertion_id=k,scope='Synthetic consecutive generations.',url='https://example.org/fixed-witness') for k in ['near','far']]
        member={'person_id':'grand','source_person_ids':['grand'],'parent_person_id':'great','source_assertion_id':None,'parent_connection':{'type':'parent_between_consecutive_ancestors','chain_subject_person_id':'child','nearer_ancestor_assertion_id':'near','farther_ancestor_assertion_id':'far','status':'contextual_provisional','human_reviewed':False,'rationale':'Synthetic contiguous paternal generations.','references':refs}}
        rows={k:{'source_person_ids':[k]}for k in ['child','great']}
        chapters={'chapter':{'source_id':'source','source':{'permalink':'https://example.org/fixed-witness'},'paragraphs':[{'id':'para','text':body,'text_layer':'received_chapter','mentions':[{'kind':'person','person_id':k}for k in ['child','grand','great']]}]}}
        return member,rows,{'near':near,'far':far},chapters
    def test_consecutive_named_generations_support_an_editorial_edge(self):
        self.assertTrue(consecutive_ancestor_parent_valid(*self.fixture()))
    def test_missing_generation_and_reversed_distances_do_not_become_father(self):
        for pred in ['father','grandfather','ancestor','mother']:
            m,r,a,c=self.fixture();a['far']['predicate']=pred;self.assertFalse(consecutive_ancestor_parent_valid(m,r,a,c))
    def test_different_descendants_or_unknown_lineage_do_not_support_chain(self):
        for change in ['subject','lineage','status','endpoint']:
            m,r,a,c=self.fixture()
            if change=='subject':a['far']['subject_person_id']='other'
            if change=='lineage':a['far']['qualifiers']={'lineage':'maternal'}
            if change=='status':a['far']['status']='unresolved'
            if change=='endpoint':a['near']['object_person_id']='other'
            self.assertFalse(consecutive_ancestor_parent_valid(m,r,a,c))
    def test_quoted_source_must_be_the_same_received_passage(self):
        for change in ['paragraph','quote','layer','source','url','missing_mention']:
            m,r,a,c=copy.deepcopy(self.fixture())
            if change=='paragraph':a['far']['evidence'][0]['paragraph_id']='other'
            if change=='quote':m['parent_connection']['references'][0]['quote']='invented'
            if change=='layer':c['chapter']['paragraphs'][0]['text_layer']='witness_appended_bangu_note'
            if change=='source':m['parent_connection']['references'][0]['source_id']='other'
            if change=='url':m['parent_connection']['references'][0]['url']='https://example.org/other'
            if change=='missing_mention':c['chapter']['paragraphs'][0]['mentions'].pop()
            self.assertFalse(consecutive_ancestor_parent_valid(m,r,a,c),change)
    def test_explicit_conflicting_father_cannot_be_silently_overridden(self):
        m,r,a,c=self.fixture();a['conflict']={'predicate':'father','subject_person_id':'grand','object_person_id':'different'};self.assertFalse(consecutive_ancestor_parent_valid(m,r,a,c))
    def test_no_claim_of_a_direct_source_assertion_or_human_review(self):
        for change in ['human','direct','references','self']:
            m,r,a,c=self.fixture()
            if change=='human':m['parent_connection']['human_reviewed']=True
            if change=='direct':m['source_assertion_id']='fabricated-father'
            if change=='references':m['parent_connection']['references'].pop()
            if change=='self':a['far']['object_person_id']='child'
            self.assertFalse(consecutive_ancestor_parent_valid(m,r,a,c))
    def test_real_xun_family_keeps_two_derived_edges_out_of_source_assertions(self):
        source,rows=load_assemblies(ROOT,load_catalog(ROOT));stem='yoo_ox0_545'
        for suffix,parent in [('FA','F'),('FAA','FA')]:
            row=source[stem+'_'+suffix];self.assertEqual(row['parent_person_id'],stem+'_'+parent);self.assertIsNone(row['source_assertion_id']);self.assertEqual(row['parent_connection']['type'],'parent_between_consecutive_ancestors')
        assertions=json.loads((ROOT/'corpus/jinshu/039-assertions.json').read_text())['assertions']
        self.assertFalse(any(a['predicate']=='father' and a['subject_person_id']in[stem+'_FA',stem+'_FAA']for a in assertions))
        self.assertEqual(next(a for a in assertions if a['subject_person_id']==stem+'_BAA')['qualifiers']['birth_order']['ordinal'],6)

    def test_distant_source_claim_is_exported_but_not_adopted_as_a_family_path(self):
        from scripts.person_bundle import bundle
        catalog=load_catalog(ROOT);payload=bundle('yoo_ox0_545',root=ROOT,include_provisional=True,catalog=catalog)
        claim=next(a for a in payload['relations'] if a['predicate']=='ancestor')
        self.assertEqual(claim['object_person_id'],'wuo_ghc_ajx')
        self.assertIs(claim['qualifiers']['adopted_for_family_tree'],False)
        self.assertEqual(claim['qualifiers']['reported_generation_number'],11)
        self.assertIsNone(claim['qualifiers']['generation_distance'])
        source,rows=load_assemblies(ROOT,catalog)
        root=source['yoo_ox0_545'];self.assertIsNone(root['parent_person_id']);self.assertNotIn('ancestor_person_id',root)
        self.assertNotIn('wuo_ghc_ajx',{p for m in rows.values()if m['assembly_id']==root['assembly_id']for p in m['source_person_ids']})
