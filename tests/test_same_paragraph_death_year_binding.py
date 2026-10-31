"""Real rendered source; source/recipient binding is an offline editorial reading."""
import copy
import json
import unittest
import hashlib
import tempfile
from pathlib import Path
from scripts.local_death_date_evidence import local_death_date_evidence_valid
from scripts.validate_corpus import source_age_number, normalized_date_errors

ROOT = Path(__file__).resolve().parents[1]
EVENT_PATH = None  # External candidate runner supplies only the proposed sidecar.

class SameParagraphDeathYearBinding(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ch = json.loads((ROOT / 'corpus/liangshu/033-wangyun-rendered.json').read_text())
        cls.chapters = {cls.ch['id']: cls.ch}
        path = EVENT_PATH or ROOT / 'corpus/liangshu/033-wangyun-rendered-life-events.json'
        cls.base = json.loads(path.read_text())['events'][0]

    def valid(self, e, chapters=None):
        return local_death_date_evidence_valid(e['normalized_date'], e, chapters or self.chapters, source_age_number, root=ROOT)

    def changed(self):
        e = copy.deepcopy(self.base)
        return e, e['normalized_date']['event_evidence_binding']

    def test_real_full_event_and_three_precise_date_anchors(self):
        e = self.base
        self.assertTrue(self.valid(e))
        self.assertEqual([], normalized_date_errors(e['normalized_date'], self.chapters))
        self.assertEqual(549, e['normalized_date']['year'])
        self.assertEqual(self.ch['paragraphs'][4]['text'], e['evidence'][0]['quote'])
        self.assertEqual([(193,209),(193,209),(209,256)], [(x['source_quote_anchor']['start'],x['source_quote_anchor']['end']) for x in e['normalized_date']['evidence']])
        self.assertNotEqual(e['evidence'], e['normalized_date']['evidence'])

    def test_other_person_cannot_become_deceased(self):
        e, b = self.changed()
        host = next(m for m in self.ch['paragraphs'][4]['mentions'] if m['id'].endswith(':m0008'))
        e['person_id'] = b['person_id'] = host['person_id']
        self.assertFalse(self.valid(e))

    def test_host_cannot_replace_resumed_subject(self):
        e,b = self.changed(); b['death_subject_reference']['person_mention_id'] = b['non_deceased_references'][-1]['person_mention_id']
        self.assertFalse(self.valid(e))

    def test_changed_anchor_type_and_position_rejected(self):
        for value in (True, 210):
            e,b = self.changed(); b['event_date_anchor']['start'] = value
            self.assertFalse(self.valid(e))

    def test_frame_capture_or_edition_drift_rejected(self):
        for key,value in [('capture_sha256','0'*64), ('source_metadata',dict(self.ch['source'],edition='武英殿本'))]:
            e,b = self.changed(); b['frame'][key] = value
            self.assertFalse(self.valid(e))

    def test_date_quote_cannot_be_changed_or_full_quote_substituted(self):
        for value in ('明年卒', self.ch['paragraphs'][4]['text']):
            e,b = self.changed(); e['normalized_date']['evidence'][2]['quote'] = value
            self.assertFalse(self.valid(e))

    def test_event_still_requires_the_full_physical_paragraph(self):
        e,b = self.changed(); e['evidence'][0]['quote'] = e['normalized_date']['original_quote']
        self.assertFalse(self.valid(e))

    def test_one_end_of_current_marker_cannot_change(self):
        ch = copy.deepcopy(self.ch); ch['paragraphs'][4]['mentions'][0]['person_id'] = 'wrong-current-owner'
        self.assertFalse(self.valid(self.base, {ch['id']:ch}))

    def test_reference_role_cannot_be_omitted_or_extra_mid_added(self):
        e,b = self.changed(); b['non_deceased_references'].pop()
        self.assertFalse(self.valid(e))
        e,b = self.changed(); b['non_deceased_references'].append(copy.deepcopy(b['non_deceased_references'][0]))
        self.assertFalse(self.valid(e))

    def test_wrong_year_or_event_kind_rejected(self):
        e,b = self.changed(); e['normalized_date']['year'] = 548
        self.assertFalse(self.valid(e))
        e,b = self.changed(); e['event_type'] = 'birth'
        self.assertFalse(self.valid(e))

    def test_acquisition_cannot_be_upgraded_to_fixed(self):
        e,b = self.changed(); b['frame']['capture_qualification']['captured_leaves']['/fixed_body_obtained'] = True
        self.assertFalse(self.valid(e))

    def test_unknown_event_metadata_does_not_change_source_binding(self):
        e,b = self.changed(); e['future_editorial_metadata'] = {'preserve': [False,0,'原值']}
        self.assertTrue(self.valid(e))


    def test_non_numeric_new_era_with_coherent_physical_frames_rejected(self):
        # Synthetic physical counterexample, not a claim about historical text.
        # All text/offset/capture/reverse endpoints remain coherent so this
        # exercises the new-era boundary rather than a stale SHA failure.
        e,b = self.changed(); ch = copy.deepcopy(self.ch); par = ch['paragraphs'][4]
        insert, added = 209, '大同初。'
        par['text'] = par['text'][:insert] + added + par['text'][insert:]
        for m in par['mentions']:
            for k in ('start','end'):
                if m[k] >= insert: m[k] += len(added)
        def move(a):
            if type(a) is dict:
                if a.get('paragraph_id') == par['id'] and all(k in a for k in ('start','end','surface')):
                    # End of preceding quote remains before inserted text.
                    if a['start'] >= insert: a['start'] += len(added); a['end'] += len(added)
                    elif a['end'] > insert: a['end'] += len(added)
                    a['surface'] = par['text'][a['start']:a['end']]
                for v in a.values(): move(v)
            elif type(a) is list:
                for v in a: move(v)
        move(e)
        e['evidence'][0]['quote'] = par['text']
        for ev in e['normalized_date']['evidence']: ev['quote'] = ev['source_quote_anchor']['surface']
        e['normalized_date']['original_quote'] = e['normalized_date']['evidence'][2]['quote']
        frame = b['frame']; cap = json.loads((ROOT / frame['capture_path']).read_text())
        cap['complete_units'][4]['observed_text'] = par['text']
        cap['complete_units'][4]['character_map'] = list(range(len(par['text'])))
        frame['character_positions'] = list(range(len(par['text'])))
        frame['paragraph_sha256'] = hashlib.sha256(par['text'].encode()).hexdigest()
        cap_bytes = (json.dumps(cap,ensure_ascii=False)+'\n').encode()
        frame['capture_sha256'] = hashlib.sha256(cap_bytes).hexdigest()
        registry = json.loads((ROOT / 'registry/persons.json').read_text())
        needed = {m.get('person_id') for m in par['mentions']}
        registry['persons'] = [r for r in registry['persons'] if r['id'] in needed]
        works = json.loads((ROOT / 'registry/works.json').read_text())
        works['works'] = [w for w in works['works'] if w['id'] == ch['work_id']]
        wp = json.loads((ROOT / 'registry/work-provenance.json').read_text())
        wp['text_bases'] = {ch['source_id']:wp['text_bases'][ch['source_id']]}
        with tempfile.TemporaryDirectory(prefix='death-era-boundary-') as tmp:
            root = Path(tmp)
            files = {frame['native_path']:ch,'registry/persons.json':registry,'registry/works.json':works,'registry/work-provenance.json':wp}
            for rel,value in files.items():
                q=root/rel; q.parent.mkdir(parents=True,exist_ok=True); q.write_text(json.dumps(value,ensure_ascii=False))
            q=root/frame['capture_path']; q.parent.mkdir(parents=True,exist_ok=True); q.write_bytes(cap_bytes)
            self.assertFalse(local_death_date_evidence_valid(e['normalized_date'],e,{ch['id']:ch},source_age_number,root=root))

if __name__ == '__main__':
    unittest.main()
