# coding: utf-8
import copy
import json
import unittest
from pathlib import Path
from scripts import maternal_roles
from scripts.biographical_maternal_title import maternal_title_scope_valid
ROOT = Path(maternal_roles.__file__).resolve().parents[1]

class BiographyGiftedParentsMaternal(unittest.TestCase):
    def setUp(self):
        chapter=json.loads((ROOT/'corpus/nanqishu/020-huiduan-rendered.json').read_text())
        self.p=chapter['paragraphs'][0]
        self.cid=chapter['id']
        self.a=next(a for a in json.loads((ROOT/'corpus/nanqishu/020-huiduan-rendered-assertions.json').read_text())['assertions'] if a['predicate']=='maternal_role')

    def valid(self,a=None,p=None):
        return maternal_roles.maternal_role_valid(a or self.a,{self.p['id']:(self.cid,p or self.p)})

    def test_real_public_entry_preserves_unspecified_mother(self):
        self.assertTrue(self.valid())
        self.assertIsNone(self.a['qualifiers']['biological_mother'])
        self.assertIsNone(self.a['qualifiers']['father_person_id'])

    def test_coherent_rekey_passes_single_endpoint_fails(self):
        a=copy.deepcopy(self.a);p=copy.deepcopy(self.p)
        for old,new in [(a['subject_person_id'],'child-new'),(a['object_person_id'],'mother-new')]:
            for m in p['mentions']:
                if m.get('person_id')==old:m['person_id']=new
            for k in ('subject_person_id','object_person_id'):
                if a[k]==old:a[k]=new
        self.assertTrue(self.valid(a,p))
        a['object_person_id']='single-thief'
        self.assertFalse(self.valid(a,p))

    def test_wrong_child_or_mother_or_father_anchor(self):
        for mid in ('m0003','m0005','m0006','m0007'):
            a=copy.deepcopy(self.a)
            m=next(m for m in self.p['mentions'] if m['id'].endswith(mid))
            a['subject_person_id']=m['person_id']
            a['evidence'][0]['subject_person_mention_id']=m['id']
            self.assertFalse(self.valid(a))
        p=copy.deepcopy(self.p)
        next(m for m in p['mentions'] if m['surface']=='景猷')['person_id']=self.a['subject_person_id']
        self.assertFalse(self.valid(p=p))

    def test_no_birth_or_paternal_or_spousal_inference(self):
        for k,v in [('biological_mother',True),('father_person_id','inferred-father'),('role','biological_mother')]:
            a=copy.deepcopy(self.a);a['qualifiers'][k]=v
            self.assertFalse(self.valid(a))
        a=copy.deepcopy(self.a);a['predicate']='spouse'
        self.assertFalse(self.valid(a))

    def test_changed_quote_span_and_missing_named_child(self):
        a=copy.deepcopy(self.a);a['evidence'][0]['quote']+=' '
        self.assertFalse(self.valid(a))
        p=copy.deepcopy(self.p);p['mentions'][7]['start']-=1
        self.assertFalse(self.valid(p=p))
        p=copy.deepcopy(self.p);p['mentions']=[m for m in p['mentions'] if m['surface']!='惠端']
        self.assertFalse(self.valid(p=p))

    def test_interpolated_name_and_quote_and_nonreceived_reject(self):
        p=copy.deepcopy(self.p);f=next(m for m in p['mentions'] if m['surface']=='景猷')
        p['mentions'].append(dict(f,id='extra-person',person_id='intruder'))
        self.assertFalse(self.valid(p=p))
        p=copy.deepcopy(self.p);p['text_layer']='modern_annotation'
        self.assertFalse(self.valid(p=p))
        p=copy.deepcopy(self.p);p['text']=p['text'].replace('贈父','云父')
        a=copy.deepcopy(self.a);a['evidence'][0]['quote']=p['text']
        self.assertFalse(self.valid(a,p))

    def test_not_any_mother_title_clause(self):
        for before,after in [('贈父','贈子'),('平陽鄉君','平陽有人'),('通直郎','其子也')]:
            p=copy.deepcopy(self.p);p['text']=p['text'].replace(before,after)
            a=copy.deepcopy(self.a);a['evidence'][0]['quote']=p['text']
            self.assertFalse(self.valid(a,p))

    def test_older_zunmu_route_remains(self):
        a=copy.deepcopy(self.a)
        p=dict(id='paragraph',text='甲尊母乙',mentions=[
            dict(id='s',kind='person',person_id='a',surface='甲',start=0,end=1),
            dict(id='o',kind='person',person_id='b',surface='乙',start=3,end=4)])
        a.update(subject_person_id='a',object_person_id='b')
        a['qualifiers']['source_term']='母乙'
        a['evidence']=[dict(paragraph_id='paragraph',chapter_id='chapter',quote=p['text'],subject_person_mention_id='s',object_person_mention_id='o')]
        self.assertTrue(maternal_title_scope_valid(a,{'paragraph':('chapter',p)}))

if __name__=='__main__':unittest.main()

