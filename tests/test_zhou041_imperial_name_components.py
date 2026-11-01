import copy
import hashlib
import json
import shutil
import subprocess
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch
from scripts.fixed_zhou041_wangbao import proof, guard_bundle
from scripts.zhou041_imperial_name_components import source_record, validate_surname, CH, REF
from scripts.person_bundle import load_catalog, bundle

ROOT = Path(__file__).resolve().parents[1]

class ThreeXiaoNames(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter, _, cls.roles = proof(ROOT)
        cls.people, cls.records = load_catalog(ROOT)
        cls.name_set = source_record(ROOT, cls.chapter, cls.roles)
        cls.contract = json.loads((ROOT / REF).read_bytes())

    def overlay(self, changes):
        ob, ot = Path.read_bytes, Path.read_text
        def raw(p):
            rel = str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else None
            return (changes[rel] if isinstance(changes[rel],bytes) else json.dumps(changes[rel], ensure_ascii=False).encode()) if rel in changes else None
        stack = ExitStack()
        stack.enter_context(patch.object(Path, 'read_bytes', lambda p: raw(p) if raw(p) is not None else ob(p)))
        stack.enter_context(patch.object(Path, 'read_text', lambda p, *a, **k: raw(p).decode() if raw(p) is not None else ot(p, *a, **k)))
        return stack

    def test_actual_three_bundles_and_name_summary_display(self):
        names = [n for r in self.records if r.get('record_type') == 'person_name_component_set' for n in r['records']]
        chapters = {r['id']: r for r in self.records if r.get('record_type') == 'marked_chapter'}
        script = """import fs from 'node:fs';import {pathToFileURL}from'node:url';
const m=await import(pathToFileURL(process.argv[1]+'/assets/name-components.js'));
const b=JSON.parse(fs.readFileSync(0,'utf8'));
console.log(JSON.stringify(m.summarizeNameComponents(b.name_components,b.preferred_name_component_readings)));"""
        for n in self.name_set['records']:
            validate_surname(n, names, chapters, [], ROOT)
            b = bundle(n['person_id'], ROOT, catalog=(self.people, self.records))
            run = subprocess.run([shutil.which('node'), '--input-type=module', '-e', script, str(ROOT)], input=json.dumps(b), capture_output=True, text=True, check=True)
            result = json.loads(run.stdout)
            self.assertFalse(result['coreConflict'])
            self.assertTrue(result['canHead'])
            self.assertEqual(result['names']['surname'] + result['names']['ming'], '蕭' + n['ming'])
            self.assertEqual(result['names']['title'], n['title'])
            self.assertNotIn('zi', n)
            self.assertEqual(b['canonical_person_id'], n['person_id'])

    def test_wrong_surname_name_title_or_borrowed_zi_rejected(self):
        rel = self.contract['name_path']
        for slot, field, value in [(0, 'surname', '王'), (0, 'ming', '器'), (0, 'title', '宣城王'), (1, 'surname', '司馬'), (1, 'zi', '弘達'), (2, 'surname', '饕餮')]:
            wrong = copy.deepcopy(self.name_set)
            wrong['records'][slot][field] = value
            with self.overlay({rel: wrong}), self.assertRaises(AssertionError):
                proof(ROOT)

    def test_actual_foreign_surname_and_observation_qualification_cannot_change(self):
        rel = self.contract['readings_path']
        primary = json.loads((ROOT / rel).read_bytes())
        for mutate in [lambda x: x['nanshi006_surname'].update(quote=x['nanshi006_surname']['quote'].replace('姓蕭氏', '姓王氏')),
                       lambda x: x['liang008_daqi'].update(fixed_permalink_body_read=True),
                       lambda x: x['liang055_ji'].update(punitive_surname_quote='無改姓報告')]:
            wrong = copy.deepcopy(primary)
            mutate(wrong)
            with self.overlay({rel: wrong}), self.assertRaises(AssertionError):
                proof(ROOT)

    def test_caller_reverse_and_names_omission_cannot_hide_owner(self):
        records = [r for r in self.records if r != self.name_set]
        for n in self.name_set['records']:
            pid = n['person_id']
            with self.assertRaises(AssertionError):
                guard_bundle(ROOT, pid, self.people, records)
            people = copy.deepcopy(self.people)
            people[pid]['evidence'] = [e for e in people[pid]['evidence'] if e.get('chapter_id') != self.chapter['id']]
            with self.assertRaises(AssertionError):
                guard_bundle(ROOT, pid, people, records)

    def test_single_endpoint_wrong_polity_and_fake_literal_alias_rejected(self):
        wrong = copy.deepcopy(self.chapter)
        marker = next(m for p in wrong['paragraphs'] for m in p['mentions'] if m['id'] == self.contract['role_mids']['ji'])
        marker['person_id'] = 'df6_0d0_a2f'
        self.assertIn(marker['person_id'], self.people)
        with self.overlay({CH: wrong}), self.assertRaises(AssertionError):
            proof(ROOT)
        people = copy.deepcopy(self.people)
        n = self.name_set['records'][0]
        people[n['person_id']]['aliases'].append({'surface': '蕭大器', 'mention_ids': [n['person_mention_id']]})
        with self.assertRaises(AssertionError):
            proof(ROOT, people=people)

    def test_original_rank_and_original_surname_scope_preserved(self):
        self.assertEqual(self.name_set['records'][0]['title'], '宣成王')
        n = self.name_set['records'][2]
        self.assertEqual(n['surname_basis']['scope'], 'biographical_original_surname_not_exclusive_lifetime_surname')
        self.assertEqual(n['surname_basis']['reported_later_surname'], '饕餮氏')
        for n in self.name_set['records']:
            self.assertFalse(n['surname_basis']['literal_in_current_mention'])
            self.assertFalse(n['human_reviewed'])

    def test_coherent_current_rekey_preserves_opaque_ids_and_captures(self):
        if (ROOT/'source-evidence/liang-xiao-close-family/family-source-contract.json').exists():
            from tests.test_liang_xiao_close_family import coherent_family_rekey_fixture
            changes,people,records,mapping=coherent_family_rekey_fixture(ROOT,self.people,self.records)
            captures={p:p.read_bytes()for p in (ROOT/'source-evidence/zhou041-wangbao-ws2432538').iterdir()if p.is_file()}
            mids={m['id']for p in self.chapter['paragraphs']for m in p['mentions']}
            with self.overlay(changes):
                ch,_,roles=proof(ROOT,people=people)
                new=roles['$daqi'];self.assertEqual(new,mapping[self.roles['$daqi']])
                result=bundle(new,ROOT,catalog=(people,records));self.assertEqual(result['canonical_person_id'],new)
                self.assertEqual(mids,{m['id']for p in ch['paragraphs']for m in p['mentions']})
                for p,b in captures.items():self.assertEqual(p.read_bytes(),b)
                hidden=[r for r in records if r.get('record_type')!='person_name_component_set']
                people[new]['evidence']=[]
                with self.assertRaises(AssertionError):guard_bundle(ROOT,new,people,hidden)
            return
        old = self.roles['$daqi']
        new = 'z99_4xx_aa1'
        self.assertNotIn(new, self.people)
        def move(x):
            if isinstance(x, str): return new if x == old else x
            if isinstance(x, list): return [move(v) for v in x]
            if isinstance(x, dict): return {k: move(v) for k, v in x.items()}
            return x
        paths = [*sorted((ROOT / 'registry').glob('*.json')), *sorted((ROOT / 'corpus').glob('*/*.json')), ROOT / 'data/corpus/profile-names.json']
        # Preserve untouched serialized bytes, including Tao's protected sidecars.
        # Only actual current endpoint changes participate in this overlay.
        changes = {}
        for p in paths:
            original = json.loads(p.read_bytes())
            moved = move(original)
            if moved != original:
                changes[str(p.relative_to(ROOT))] = moved
        captures = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT / 'source-evidence/zhou041-wangbao-ws2432538').glob('*') if p.is_file()}
        tao = json.loads((ROOT / 'source-evidence/liang041-wanggui-ws1512987/taoshiheng-identity-successor.json').read_bytes())
        captures.update({ROOT / rel: value for rel, value in tao['protected_file_sha256'].items()})
        mids = {m['id'] for p in self.chapter['paragraphs'] for m in p['mentions']}
        with self.overlay(changes):
            ch, _, roles = proof(ROOT)
            self.assertEqual(roles['$daqi'], new)
            people, records = load_catalog(ROOT)
            result = bundle(new, ROOT, catalog=(people, records))
            self.assertEqual(result['canonical_person_id'], new)
            self.assertEqual({m['id'] for p in ch['paragraphs'] for m in p['mentions']}, mids)
            self.assertTrue(all(hashlib.sha256(p.read_bytes()).hexdigest() == h for p, h in captures.items()))
            names = source_record(ROOT, ch, roles)
            hidden = [r for r in records if r != names]
            people[new]['evidence'] = [e for e in people[new]['evidence'] if e.get('chapter_id') != ch['id']]
            with self.assertRaises(AssertionError):
                guard_bundle(ROOT, new, people, hidden)
            wrong = copy.deepcopy(changes[CH])
            m = next(m for p in wrong['paragraphs'] for m in p['mentions'] if m['id'] == self.contract['role_mids']['daqi'])
            m['person_id'] = old
            changes[CH] = wrong
            with self.assertRaises(AssertionError):
                proof(ROOT)

if __name__ == '__main__':
    unittest.main()
