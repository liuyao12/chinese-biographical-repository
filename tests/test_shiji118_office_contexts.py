# coding: utf-8
import copy,json,unittest
from pathlib import Path
from scripts.lexical_annotations import non_person_errors
from scripts.render_corpus import render

ROOT=Path(__file__).resolve().parents[1]
class HuainanOfficeContexts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c=json.loads((ROOT/'corpus/shiji/118.json').read_text());cls.ms={m['id']:(p,m) for p in cls.c['paragraphs'] for m in p['mentions']}
    def test_three_absent_princes_have_no_person_identity(self):
        for suffix in ['m015-0097','m015-0228','m018-0028']:
            p,m=self.ms['c-shiji-118-huainan:'+suffix];self.assertEqual((m['kind'],m['lexical_role'],m['person_id']),('non_person','vacant_office',None));self.assertEqual(non_person_errors(m,p['text']),[])
    def test_desired_sovereignty_and_seal_do_not_create_an_emperor(self):
        for suffix,quote in [('m027-0531','刻天子璽'),('m027-0577','求即天子位')]:
            p,m=self.ms['c-shiji-118-huainan:'+suffix];self.assertEqual(m['basis_quote'],quote);self.assertEqual((m['kind'],m['lexical_role'],m['person_id']),('non_person','sovereign_status',None));self.assertEqual(non_person_errors(m,p['text']),[])
    def test_nominal_classifications_require_their_actual_context(self):
        p,m=self.ms['c-shiji-118-huainan:m015-0097']
        for change in [{'person_id':'synthetic-person'},{'work_id':'synthetic-work'},{'basis_quote':'上有太子'},{'lexical_role':'sovereign_status'},{'surface':'上'},{'human_reviewed':True}]:
            item=copy.deepcopy(m);item.update(change);self.assertTrue(non_person_errors(item,p['text']),change)
        p,m=self.ms['c-shiji-118-huainan:m027-0531'];item=copy.deepcopy(m);item['basis_quote']='無為吳王之所悔';self.assertTrue(non_person_errors(item,p['text']))
    def test_actual_named_princes_remain_persons(self):
        p=next(p for p in self.c['paragraphs'] if p['id'].endswith('p027'))
        self.assertTrue(any(m['surface']=='太子爽' and m['person_id']=='yqp_nlb_p1p_AFCA' for m in p['mentions']))
        self.assertEqual(self.ms['c-shiji-118-huainan:m021-0916'][1]['person_id'],'5dd_l1c_6g8')
    def test_four_final_plan_targets_have_source_specific_identity_decisions(self):
        decisions={d['id']:d for d in json.loads((ROOT/'corpus/shiji/118-identities.json').read_text())['decisions']}
        for key,pid,suffixes in [('d-shiji118-qing-final-plan','5dd_l1c_6g8',['m021-0579','m021-0899']),('d-shiji118-hong-final-plan','q69_35n_f3h',['m021-0903','m021-0923'])]:
            d=decisions[key];self.assertEqual(d['person_id'],pid);self.assertEqual(d['identification_basis']['target_mention_ids'],['c-shiji-118-huainan:'+s for s in suffixes]);self.assertFalse(d['human_reviewed']);self.assertTrue(all('/73c4d2ba067d99a6de924ac952fd6921a958c7e7/' in r['url'] for r in d['references']))
            for s in suffixes:self.assertEqual(self.ms['c-shiji-118-huainan:'+s][1]['person_id'],pid)
    def test_forged_office_list_does_not_inherit_those_identities(self):
        for s in ['m021-0693','m021-0695','m021-0838','m021-0842','m021-0845','m021-0848']:
            m=self.ms['c-shiji-118-huainan:'+s][1];self.assertEqual((m['kind'],m['person_id']),('unresolved',None))
    def test_xml_preserves_nominal_words_as_non_person_segments(self):
        import xml.etree.ElementTree as ET
        root=ET.fromstring(render(self.c));nodes={n.attrib.get('id'):n for n in root.iter()}
        for s in ['m015-0097','m015-0228','m018-0028','m027-0531','m027-0577']:
            p,m=self.ms['c-shiji-118-huainan:'+s];n=nodes[m['id']];self.assertEqual((n.tag,n.attrib['type'],n.attrib['subtype'],n.text),('seg','non-person',m['lexical_role'],m['surface']))

if __name__=='__main__':unittest.main()
