"""Negative witness cases use small scoped fixtures, never a full corpus copy."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from scripts import fixed_repository_witness as witness

ROOT = Path(__file__).resolve().parents[1]
CID = 'c-jinshu-043-wyd1739-wangrong'

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

class RepositoryWitnessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        rel = witness.RECEIPTS[CID][1]
        receipt = json.loads((ROOT/rel).read_bytes())
        paths = [rel, receipt['seed_path'], receipt['chapter_path'], *receipt['fixed_files'], *receipt['sidecars']]
        for path in paths:
            dest = self.root/path
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes((ROOT/path).read_bytes())
        seed = self.read(receipt['seed_path'])
        mids = {m['id']: m for p in seed['paragraphs'] for m in p['mentions']}
        ids = {mids[r['seed_mid']]['person_id'] for r in receipt['roles']}
        people = json.loads((ROOT/'registry/persons.json').read_bytes())
        people['persons'] = [p for p in people['persons'] if p['id'] in ids]
        write(self.root/'registry/persons.json', people)
        self.receipt = receipt
        self.chapter = self.read(receipt['chapter_path'])

    def read(self, path):
        return json.loads((self.root/path).read_bytes())

    def save_chapter(self):
        write(self.root/self.receipt['chapter_path'], self.chapter)

    def run_valid(self):
        return witness.validate_source(self.chapter, self.root)

    def test_complete_projection_and_unknown_glyphs(self):
        self.assertEqual(len(self.run_valid()), 55)
        self.assertEqual(sum(p['text'].count('〓') for p in self.chapter['paragraphs']), 3)
        self.assertFalse(self.chapter['source']['image_verified'])

    def test_full_source_qualification_not_relabelled_as_human(self):
        self.chapter['source']['image_verified'] = True
        self.save_chapter()
        with self.assertRaises(ValueError): self.run_valid()

    def test_whole_source_extent_cannot_include_wangyan(self):
        self.chapter['source']['extent'] += '王衍以下'
        self.save_chapter()
        with self.assertRaises(ValueError): self.run_valid()

    def test_raw_byte_mutation_rejected(self):
        path = self.root/self.receipt['raw_path']
        path.write_bytes(path.read_bytes().replace('王'.encode(), '玉'.encode(), 1))
        with self.assertRaises(ValueError): self.run_valid()

    def test_projection_gap_rejected(self):
        rel = next(p for p in self.receipt['fixed_files'] if p.endswith('transcription-projection.json'))
        doc = self.read(rel)
        doc['units'][0]['raw_runs'][0]['raw_start'] += 1
        write(self.root/rel, doc)
        with self.assertRaises(ValueError): self.run_valid()

    def test_new_endpoint_only_swap_rejected(self):
        marker = self.chapter['paragraphs'][0]['mentions'][0]
        other = self.chapter['paragraphs'][0]['mentions'][2]
        marker['person_id'] = other['person_id']
        self.save_chapter()
        with self.assertRaises(ValueError): self.run_valid()

    def test_reverse_evidence_required(self):
        doc = self.read('registry/persons.json')
        pid = self.chapter['paragraphs'][0]['mentions'][0]['person_id']
        person = next(p for p in doc['persons'] if p['id'] == pid)
        mid = self.chapter['paragraphs'][0]['mentions'][0]['id']
        person['evidence'] = [e for e in person['evidence'] if e.get('mention_id') != mid]
        write(self.root/'registry/persons.json', doc)
        with self.assertRaises(ValueError): self.run_valid()

    def test_seed_full_paragraph_required(self):
        doc = self.read(self.receipt['seed_path'])
        doc['paragraphs'][0]['text'] += '。'
        write(self.root/self.receipt['seed_path'], doc)
        with self.assertRaises(ValueError): self.run_valid()

    def test_sidecar_missing_rejected(self):
        (self.root/next(iter(self.receipt['sidecars']))).unlink()
        with self.assertRaises(OSError): self.run_valid()

    def test_all_current_endpoints_can_be_rekeyed(self):
        pid = self.chapter['paragraphs'][0]['mentions'][0]['person_id']
        replacement = 'x9q_7rn_2jm_AA'
        def rekey(v):
            if isinstance(v, str): return replacement if v == pid else v
            if isinstance(v, list): return [rekey(x) for x in v]
            if isinstance(v, dict): return {k: rekey(x) for k, x in v.items()}
            return v
        for rel in [self.receipt['chapter_path'], self.receipt['seed_path'], *self.receipt['sidecars'], 'registry/persons.json']:
            write(self.root/rel, rekey(self.read(rel)))
        self.chapter = self.read(self.receipt['chapter_path'])
        self.assertIn(replacement, self.run_valid().values())

    def test_api_catalog_omission_rejected(self):
        doc = self.read('registry/persons.json')
        people = {p['id']: p for p in doc['persons']}
        pid = self.chapter['paragraphs'][0]['mentions'][0]['person_id']
        with self.assertRaises(ValueError): witness.guard_bundle(self.root, pid, people, [])

    def test_api_catalog_and_disk_must_agree(self):
        people = {p['id']: p for p in self.read('registry/persons.json')['persons']}
        pid = self.chapter['paragraphs'][0]['mentions'][0]['person_id']
        records = [self.chapter] + [self.read(p) for p in self.receipt['sidecars']]
        witness.guard_bundle(self.root, pid, people, records)
        records[0] = copy.deepcopy(self.chapter)
        records[0]['paragraphs'][0]['text'] += '。'
        with self.assertRaises(ValueError): witness.guard_bundle(self.root, pid, people, records)

    def test_registry_full_paragraph_is_not_person_quote(self):
        doc = self.read('registry/persons.json')
        marker = self.chapter['paragraphs'][0]['mentions'][0]
        person = next(p for p in doc['persons'] if p['id'] == marker['person_id'])
        row = next(e for e in person['evidence'] if e.get('mention_id') == marker['id'])
        row['quote'] = self.chapter['paragraphs'][0]['text']
        write(self.root/'registry/persons.json', doc)
        with self.assertRaises(ValueError): self.run_valid()

    def test_registry_quote_is_exact_person_surface(self):
        people = {p['id']: p for p in self.read('registry/persons.json')['persons']}
        for p in self.chapter['paragraphs']:
            for m in p['mentions']:
                if m['kind'] == 'person':
                    rows = [e for e in people[m['person_id']]['evidence'] if e.get('mention_id') == m['id']]
                    self.assertEqual(len(rows), 1)
                    self.assertEqual(rows[0]['quote'], m['surface'])

    def test_api_forged_people_and_catalog_omission_rejected(self):
        people = {p['id']: p for p in self.read('registry/persons.json')['persons']}
        pid = self.chapter['paragraphs'][0]['mentions'][0]['person_id']
        for p in people.values():
            p['evidence'] = [e for e in p['evidence'] if e.get('chapter_id') != CID]
        with self.assertRaises(ValueError): witness.guard_bundle(self.root, pid, people, [])

    def test_installed_receipt_missing_source_rejected(self):
        people = {p['id']: p for p in self.read('registry/persons.json')['persons']}
        pid = self.chapter['paragraphs'][0]['mentions'][0]['person_id']
        (self.root/self.receipt['chapter_path']).unlink()
        for p in people.values():
            p['evidence'] = [e for e in p['evidence'] if e.get('chapter_id') != CID]
        with self.assertRaises(ValueError): witness.guard_bundle(self.root, pid, people, [])

    def test_both_dimensions_renamed_at_owned_path_rejected(self):
        self.chapter['id'] = 'c-forged'
        self.chapter['source_id'] = 's-forged'
        self.assertTrue(witness.source_errors(self.chapter, self.root, self.root/self.receipt['chapter_path']))

    def test_unknown_data_receipt_does_not_activate_gate(self):
        self.assertEqual(witness.source_errors({'id': 'c-unknown', 'source_id': 's-unknown', 'annotation': {'fixed_transcription_contract': CID}}, self.root), [])

if __name__ == '__main__': unittest.main()
