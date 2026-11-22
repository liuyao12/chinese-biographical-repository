from collections import Counter
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import unittest

from scripts.chenshu023_shenjunli import daughter_valid, proposal_valid as shen_proposal, succession_valid
from scripts.chenshu023_lushan import family_valid, proposal_valid as lu_proposal

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_bytes())


class Chen23Families(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shen = read('corpus/chenshu/023-shenjunli-complete.json')
        cls.lu = read('corpus/chenshu/023-lushan-complete.json')
        cls.shen_kin = read('corpus/chenshu/023-shenjunli-complete-assertions.json')['assertions']
        cls.lu_kin = read('corpus/chenshu/023-lushan-complete-assertions.json')['assertions']

    def test_volume_accounts_own_all_original_characters_once(self):
        volume = read('source-evidence/chenshu023-shenwanglu/volume-boundaries.json')
        raw = (ROOT / volume['raw_path']).read_bytes()
        self.assertEqual(sha256(raw).hexdigest(), volume['raw_sha256'])
        lines = raw.decode().splitlines()
        source = Counter((n,offset) for n in range(11,44) if lines[n-1].startswith('　　')
                         for offset in range(len(lines[n-1])))
        self.assertEqual(len(source), 2802)
        def mapped(entries):
            parts = Counter()
            for entry in entries:
                for span in entry['spans']:
                    for n in range(span['first_line'],span['last_line']+1):
                        start = span['start'] if n == span['first_line'] else 0
                        end = span['end'] if n == span['last_line'] else len(lines[n-1])
                        parts.update((n,k) for k in range(start,end))
            return parts
        self.assertEqual(len(volume['entries']),12)
        self.assertEqual(mapped(volume['entries']),source)
        for delta in (-1,1):
            rows=deepcopy(volume['entries'])
            rows[0]['spans'][0]['end']+=delta
            self.assertNotEqual(mapped(rows),source)
        review=read('corpus/chenshu/023-shen-wang-lu-appraisal.json')
        self.assertEqual(len({r['person_id'] for r in review['annotation']['source_reading_cases']
                              if r['kind']=='collective_appraisal'}),3)

    def test_succession_and_natal_father_remain_independent(self):
        row, = (a for a in self.shen_kin if a['predicate']=='ritual_successor_of')
        paragraphs={p['id']:(self.shen['id'],p) for p in self.shen['paragraphs']}
        self.assertTrue(succession_valid(row,paragraphs))
        native, = (a for a in self.shen_kin if a['subject_person_id']==row['subject_person_id'] and a['predicate']=='father')
        self.assertNotEqual(row['object_person_id'],native['object_person_id'])
        wrong=deepcopy(row)
        wrong['object_person_id']=native['object_person_id']
        wrong['evidence'][0]['object_person_mention_id']=native['evidence'][0]['object_person_mention_id']
        self.assertFalse(succession_valid(wrong,paragraphs))

    def test_parent_and_spouse_are_both_tied_to_jungao_daughter(self):
        rows=[a for a in self.shen_kin if a['qualifiers'].get('reading_basis',{}).get('kind')=='chen023_jungao_daughter']
        self.assertEqual({a['predicate'] for a in rows},{'father','spouse'})
        for a in rows:
            self.assertTrue(daughter_valid(a,a['evidence'][0],self.shen))
            changed=deepcopy(a)
            changed['object_person_id']=a['subject_person_id']
            self.assertFalse(daughter_valid(changed,changed['evidence'][0],self.shen))

    def test_nephew_is_bound_to_the_unnamed_brother(self):
        rows=[a for a in self.lu_kin if a['qualifiers'].get('reading_basis',{}).get('kind')=='chen023_lu_nephew']
        self.assertEqual({a['predicate'] for a in rows},{'father','brother'})
        for a in rows:
            e=a['evidence'][0]
            self.assertTrue(family_valid(a,e,self.lu))
            changed=deepcopy(a)
            changed['qualifiers']['reading_basis']['role_anchor']['start']+=1
            self.assertFalse(family_valid(changed,e,self.lu))

    def test_court_proposals_keep_their_exact_outcome(self):
        for ch,validator,count in [(self.shen,shen_proposal,11),(self.lu,lu_proposal,1)]:
            proposals=ch['annotation']['title_proposals']
            self.assertEqual(len(proposals),count)
            for p in proposals:
                self.assertTrue(validator(p,ch))
                changed=deepcopy(p)
                changed['non_assumption_anchor']['start']+=1
                self.assertFalse(validator(changed,ch))
        outcomes = [v['source_quote'] for v in self.lu['annotation']['source_reading_cases'] if v['kind']=='appointment_outcome']
        self.assertEqual(outcomes,['固辭，不許，乃權換廨宇徙居之'])
