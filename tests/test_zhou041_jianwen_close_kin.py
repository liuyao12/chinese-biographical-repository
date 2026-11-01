import copy
import hashlib
import json
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch
from scripts.fixed_zhou041_wangbao import proof, guard_bundle
from scripts.person_bundle import load_catalog, bundle
from scripts.zhou041_jianwen_close_kin import CH, REF, contract, expand, family_valid

ROOT = Path(__file__).resolve().parents[1]

class JianwenCloseKin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ch, _, cls.roles = proof(ROOT)
        cls.people, cls.records = load_catalog(ROOT)
        cls.c = contract(ROOT)
        cls.side = expand(cls.c['sidecar_template'], cls.roles)
        cls.anchors = {m['id']:m for p in cls.ch['paragraphs'] for m in p['mentions']}
        cls.paragraphs = {p['id']:(cls.ch['id'],p) for p in cls.ch['paragraphs']}

    def overlay(self, changes):
        oldb, oldt = Path.read_bytes, Path.read_text
        def raw(p):
            rel = str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else None
            v = changes.get(rel)
            if v is None: return None
            return v if isinstance(v,bytes) else (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
        stack = ExitStack()
        stack.enter_context(patch.object(Path,'read_bytes',lambda p: raw(p) if raw(p) is not None else oldb(p)))
        stack.enter_context(patch.object(Path,'read_text',lambda p,*a,**k: raw(p).decode() if raw(p) is not None else oldt(p,*a,**k)))
        return stack

    def test_actual_current_identity_and_three_precise_relations(self):
        self.assertEqual(self.people[self.roles['$liangjian']]['label'],'綱（晉安王）')
        self.assertEqual(self.anchors[self.c['target_mid']]['surface'],'簡文帝')
        self.assertEqual(self.anchors[self.c['target_mid']]['person_id'],self.roles['$liangjian'])
        for a in self.side['assertions']:
            self.assertTrue(family_valid(a,self.paragraphs,ROOT))
        father,younger,inlaw = self.side['assertions']
        self.assertEqual((father['subject_person_id'],father['object_person_id']),(self.roles['$daqi'],self.roles['$liangjian']))
        self.assertEqual(younger['qualifiers']['relative_birth_order']['older_person_id'],self.roles['$liangwu'])
        self.assertIsNone(inlaw['qualifiers']['spouse_person_id'])
        self.assertIsNone(father['qualifiers']['all_children_ordinal'])
        self.assertNotIn('birth_order',father['qualifiers'])

    def test_normal_bundles_include_source_and_typed_relations(self):
        for role in ('liangjian','daqi','hui','bao'):
            pid=self.roles['$'+role];b=bundle(pid,ROOT,catalog=(self.people,self.records))
            self.assertEqual(b['canonical_person_id'],pid)
            self.assertTrue(any(a['id'].startswith('a-zhou041-close-kin-') for a in b['relations']))

    def test_wrong_jin_emperor_or_single_endpoint_cannot_replace_liang(self):
        wrong=copy.deepcopy(self.ch)
        m=next(m for p in wrong['paragraphs'] for m in p['mentions'] if m['id']==self.c['target_mid'])
        m['person_id']='dkn_ge4_286_AAAAAAAF'
        with self.overlay({CH:wrong}),self.assertRaises(AssertionError): proof(ROOT)
        wrong=copy.deepcopy(self.side);wrong['assertions'][0]['object_person_id']='dkn_ge4_286_AAAAAAAF'
        with self.overlay({self.c['sidecar_path']:wrong}),self.assertRaises(AssertionError): proof(ROOT)

    def test_wrong_father_reversal_or_unqualified_first_son_rejected(self):
        for mutate in (lambda a:a.update(object_person_id=self.roles['$hui']),
                       lambda a:a.update(subject_person_id=a['object_person_id'],object_person_id=a['subject_person_id']),
                       lambda a:a['qualifiers'].update(all_children_ordinal=1),
                       lambda a:a['qualifiers'].update(birth_order={'ordinal':1,'scope':'sons_of_parent'})):
            a=copy.deepcopy(self.side['assertions'][0]);mutate(a)
            self.assertFalse(family_valid(a,self.paragraphs,ROOT))

    def test_wrong_younger_or_wrong_marriage_recipient_and_named_wife_rejected(self):
        a=copy.deepcopy(self.side['assertions'][1]);a['qualifiers']['relative_birth_order']['older_person_id']=self.roles['$hui']
        self.assertFalse(family_valid(a,self.paragraphs,ROOT))
        for field,value in [('subject_person_id','okz_h8f_ji3'),('object_person_id',self.roles['$liangwu'])]:
            a=copy.deepcopy(self.side['assertions'][2]);a[field]=value
            self.assertFalse(family_valid(a,self.paragraphs,ROOT))
        a=copy.deepcopy(self.side['assertions'][2]);a['qualifiers']['spouse_person_id']=self.roles['$daqi']
        self.assertFalse(family_valid(a,self.paragraphs,ROOT))

    def test_reverse_or_alias_loss_and_fake_fullname_alias_rejected(self):
        pid=self.roles['$liangjian']
        for field in ('evidence','aliases'):
            people=copy.deepcopy(self.people)
            if field=='evidence':people[pid][field]=[e for e in people[pid][field] if e.get('mention_id')!=self.c['target_mid']]
            else:people[pid][field]=[a for a in people[pid][field] if self.c['target_mid'] not in a['mention_ids']]
            with self.assertRaises(AssertionError):proof(ROOT,people=people)
        people=copy.deepcopy(self.people);people[pid]['aliases'].append({'surface':'蕭綱','mention_ids':[self.c['target_mid']]})
        with self.assertRaises(AssertionError):proof(ROOT,people=people)

    def test_owner_cannot_hide_by_caller_reverse_and_sidecar_omission(self):
        records=[r for r in self.records if r!=self.side]
        for role in ('liangjian','daqi','hui','bao'):
            pid=self.roles['$'+role]
            with self.assertRaises(AssertionError):guard_bundle(ROOT,pid,self.people,records)
        pid=self.roles['$liangjian'];people=copy.deepcopy(self.people)
        people[pid]['evidence']=[e for e in people[pid]['evidence'] if e.get('chapter_id')!=self.ch['id']]
        with self.assertRaises(AssertionError):guard_bundle(ROOT,pid,people,records)

    def test_fixed_link_and_print_qualification_cannot_be_upgraded(self):
        p=self.c['readings_path'];r=json.loads((ROOT/p).read_bytes())
        for key in ('fixed_raw_obtained','image_verified','human_reviewed','actual_print_edition_verified'):
            wrong=copy.deepcopy(r);wrong[key]=True
            with self.overlay({p:wrong}),self.assertRaises(AssertionError):proof(ROOT)

    def test_coherent_current_endpoint_rekey_preserves_capture_and_opaque_ids(self):
        if (ROOT/'source-evidence/liang-xiao-close-family/family-source-contract.json').exists():
            from tests.test_liang_xiao_close_family import coherent_family_rekey_fixture
            changes,people,records,mapping=coherent_family_rekey_fixture(ROOT,self.people,self.records)
            captures={p:p.read_bytes()for p in (ROOT/'source-evidence/zhou041-wangbao-ws2432538').iterdir()if p.is_file()}
            with self.overlay(changes):
                ch,_,roles=proof(ROOT,people=people)
                self.assertEqual(roles['$liangjian'],mapping[self.roles['$liangjian']])
                guard_bundle(ROOT,roles['$liangjian'],people,records)
                for p,b in captures.items():self.assertEqual(p.read_bytes(),b)
                people[roles['$liangjian']]['evidence']=[]
                with self.assertRaises(AssertionError):proof(ROOT,people=people)
            return
        old=self.roles['$liangjian'];new='z98_2zz_kk4';self.assertNotIn(new,self.people)
        def move(x):
            if isinstance(x,list):return[move(v)for v in x]
            if isinstance(x,dict):
                return {k:(new if v==old and k in ('person_id','subject_person_id','object_person_id','older_person_id','younger_person_id') else move(v))for k,v in x.items()}
            return x
        people=copy.deepcopy(self.people);people[new]=people.pop(old);people[new]['id']=new
        changes={CH:move(self.ch),self.c['sidecar_path']:move(self.side)}
        source_path=self.c['seed']['path'];changes[source_path]=move(json.loads((ROOT/source_path).read_bytes()))
        before=[(m['id'],m['start'],m['end'],m['surface'])for p in self.ch['paragraphs']for m in p['mentions']]
        captures={str(p.relative_to(ROOT)):p.read_bytes()for p in (ROOT/'source-evidence/zhou041-wangbao-ws2432538').iterdir()if p.is_file()}
        with self.overlay(changes):
            ch,_,roles=proof(ROOT,people=people)
            self.assertEqual(roles['$liangjian'],new)
            self.assertEqual(before,[(m['id'],m['start'],m['end'],m['surface'])for p in ch['paragraphs']for m in p['mentions']])
            for rel,b in captures.items():self.assertEqual((ROOT/rel).read_bytes(),b)
            records=[move(r) if r.get('record_type') in ('marked_chapter','person_assertion_set') else r for r in self.records]
            guard_bundle(ROOT,new,people,records)
            people[new]['evidence']=[e for e in people[new]['evidence']if e.get('mention_id')!=self.c['target_mid']]
            with self.assertRaises(AssertionError):proof(ROOT,people=people)

if __name__=='__main__': unittest.main()
