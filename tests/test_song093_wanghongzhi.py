from copy import deepcopy
from pathlib import Path
import hashlib
import json
import unittest
from scripts.song093_wanghongzhi import errors, kin_valid, date_valid

ROOT=Path(__file__).resolve().parents[1]

def read(name):return json.loads((ROOT/name).read_text())

class WangHongzhi(unittest.TestCase):
    def test_accepted_readings_and_rejected_role_changes(self):
        ch=read('corpus/songshu/093.json')
        rows=read('corpus/songshu/093-assertions.json')['assertions']
        self.assertFalse(errors(ch,ROOT))
        care=next(row for row in rows if row['id']=='a-song093-wanghongzhi-care')
        self.assertTrue(kin_valid(care,ch,ROOT))
        care['predicate']='father'
        self.assertFalse(kin_valid(care,ch,ROOT))
        bad=deepcopy(ch)
        ref=next(r for r in bad['annotation']['person_reference_occurrences']if r['surface']=='母' and r['paragraph_id'].endswith('line062'))
        ref['person_id']='3ea_uzt_2n2_A'
        self.assertTrue(errors(bad,ROOT))

    def test_omitted_year_and_printed_variants(self):
        ch=read('corpus/songshu/093.json')
        event=next(e for e in read('corpus/songshu/093-life-events.json')['events'] if e['id']=='le-songshu-093-66-wang-received')
        date=event['normalized_date']; chapters={ch['id']:ch}
        number=lambda text:4 if text=='四' else None
        self.assertTrue(date_valid(date,event,chapters,number,ROOT))
        bad=deepcopy(event);bad['normalized_date']['evidence'].pop(1)
        self.assertFalse(date_valid(bad['normalized_date'],bad,chapters,number,ROOT))
        packet=read('source-evidence/song093-wanghongzhi/song093-wyd-columns.json')
        by={(c['page'],c['leaf_side'],c['column']):c['quote'] for c in packet['columns']}
        self.assertIn('何淮',by[9,'L',2]);self.assertIn('每隨兄',by[9,'L',7]);self.assertIn('始寧汰川',by[10,'L',3]);self.assertIn('奔會稽',by[11,'R',6]);self.assertIn('左民尚書',by[11,'L',1]);self.assertEqual(len(by),44)
        for c in packet['columns']:self.assertEqual(hashlib.sha256(c['quote'].encode()).hexdigest(),c['sha256'])
