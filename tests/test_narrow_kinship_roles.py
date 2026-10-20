# coding: utf-8
"""Full received paragraphs: legacy positives plus wrong-endpoint regressions."""
import copy,json,unittest
from pathlib import Path
from scripts.maternal_roles import maternal_role_valid
from scripts.uncle_parentage import explicit_maternal_uncle_valid
from scripts.directed_uncle_roles import paternal_uncle_direction_valid
DATA=json.loads((Path(__file__).parent/'fixtures/narrow_kinship_roles.json').read_text())
class NarrowKinshipRoles(unittest.TestCase):
    def test_all_32_uncle_7_maternal_uncle_4_mother_existing_sources(self):
        counts={}
        for row in DATA['existing']:
            a=row['assertion'];k=a['predicate'];counts[k]=counts.get(k,0)+1
            fn={'paternal_uncle':paternal_uncle_direction_valid,'maternal_uncle':explicit_maternal_uncle_valid,'maternal_role':maternal_role_valid}[k]
            if k=='maternal_uncle' and a['qualifiers']['source_term']=='姊子':
                self.assertIn('姊子',a['evidence'][0]['quote']);continue
            with self.subTest(assertion=a['id']):self.assertTrue(fn(a,row['paragraphs']))
        self.assertEqual(counts,{'paternal_uncle':32,'maternal_uncle':7,'maternal_role':4})
    def test_all_32_swapped_uncle_endpoints_rejected(self):
        count=0
        for row in DATA['existing']:
            a=copy.deepcopy(row['assertion'])
            if a['predicate']!='paternal_uncle':continue
            count+=1;a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id']
            for e in a['evidence']:
                if 'subject_person_mention_id' in e:e['subject_person_mention_id'],e['object_person_mention_id']=e['object_person_mention_id'],e['subject_person_mention_id']
            with self.subTest(assertion=a['id']):self.assertFalse(paternal_uncle_direction_valid(a,row['paragraphs']))
        self.assertEqual(count,32)
    def test_source38_original_uncle_direction(self):
        e=DATA['extra'];self.assertTrue(paternal_uncle_direction_valid(e['positive']['assertions'][0],e['paragraphs']))
        self.assertFalse(paternal_uncle_direction_valid(e['negative']['assertions'][0],e['paragraphs']))
    def test_source38_mother_right_child_and_wrong_child(self):
        e=DATA['extra'];self.assertTrue(maternal_role_valid(e['mother'],e['paragraphs']))
        self.assertFalse(maternal_role_valid(e['negative']['assertions'][-1],e['paragraphs']))
    def test_mother_no_biological_or_spouse_inference(self):
        e=DATA['extra']
        for key,value in [('biological_mother',True),('father_person_id','invented')]:
            a=copy.deepcopy(e['mother']);a['qualifiers'][key]=value;self.assertFalse(maternal_role_valid(a,e['paragraphs']))
    def test_nephew_prefix_full_context(self):
        e=DATA['extra'];self.assertTrue(explicit_maternal_uncle_valid(e['nephew'],e['paragraphs']))
    def test_nephew_requires_complete_corroboration_not_quote_crop(self):
        e=DATA['extra'];a=copy.deepcopy(e['nephew']);p=copy.deepcopy(e['paragraphs']);pid=a['evidence'][0]['paragraph_id']
        a['evidence'][0]['quote']=a['qualifiers']['source_term'];self.assertFalse(explicit_maternal_uncle_valid(a,p))
        a=copy.deepcopy(e['nephew']);p[pid][1]['text']=p[pid][1]['text'].replace('舅甥並典兵','二人並典兵');a['evidence'][0]['quote']=p[pid][1]['text'];self.assertFalse(explicit_maternal_uncle_valid(a,p))
    def test_nephew_wrong_endpoints_or_lineage(self):
        e=DATA['extra']
        for mode in ['swap','lineage','mother']:
            a=copy.deepcopy(e['nephew'])
            if mode=='swap':
                a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id'];v=a['evidence'][0];v['subject_person_mention_id'],v['object_person_mention_id']=v['object_person_mention_id'],v['subject_person_mention_id']
            elif mode=='lineage':a['qualifiers']['lineage']='paternal'
            else:a['qualifiers']['mother_person_id']='invented'
            self.assertFalse(explicit_maternal_uncle_valid(a,e['paragraphs']))
    def test_nephew_corroboration_cannot_jump_a_new_person_or_speech(self):
        e=DATA['extra'];pid=e['nephew']['evidence'][0]['paragraph_id']
        for mode in ['other_person','speech']:
            a=copy.deepcopy(e['nephew']);p=copy.deepcopy(e['paragraphs']);v=p[pid][1];at=v['text'].index('舅甥並典兵')-1
            if mode=='other_person':v['mentions'].append({'id':'synthetic-negative-local','kind':'person','person_id':'other','start':at,'end':at+1,'surface':v['text'][at:at+1]})
            else:v['text']=v['text'][:at]+'曰'+v['text'][at+1:];a['evidence'][0]['quote']=v['text']
            self.assertFalse(explicit_maternal_uncle_valid(a,p))
    def test_unrelated_same_paragraph_mother_does_not_use_nearest(self):
        e=DATA['extra'];a=copy.deepcopy(e['mother']);p=e['paragraphs'];pid=a['evidence'][0]['paragraph_id'];v=p[pid][1]
        for m in v['mentions']:
            if m.get('kind')!='person' or m.get('person_id') in [a['subject_person_id'],a['object_person_id']]:continue
            b=copy.deepcopy(a);b['subject_person_id']=m['person_id'];b['evidence'][0]['subject_person_mention_id']=m['id'];self.assertFalse(maternal_role_valid(b,p))
if __name__=='__main__':unittest.main()
