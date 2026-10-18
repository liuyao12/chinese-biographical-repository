# coding: utf-8
"""Corruption tests of a primary-source-backed draft, never published fixtures."""
import copy,json,unittest
from pathlib import Path
from scripts.chinese_civil_years import civil_year_errors
ROOT=Path(__file__).resolve().parents[1]
EVENT=json.loads((ROOT/'tests/fixtures/chu-wu-chinese-civil-year.json').read_text())
C=json.loads((ROOT/'corpus/shiji/106.json').read_text());T=json.loads((ROOT/'data/historical-tables/shiji-022.json').read_text())
class CivilYearTests(unittest.TestCase):
    def test_formal_corpus_validator_rejects_wrong_editorial_year(self):
        from unittest.mock import patch
        from scripts.validate_corpus import validate
        target=ROOT/'corpus/shiji/106-life-events.json'
        original=Path.read_text
        record=json.loads(original(target))
        event=next(e for e in record['events'] if e['id']==EVENT['id'])
        event['chinese_civil_year'].update(era_year=155,year=-154)
        def read(path,*args,**kwargs):
            return json.dumps(record,ensure_ascii=False) if path==target else original(path,*args,**kwargs)
        with patch.object(Path,'read_text',read):errors=validate(ROOT)
        self.assertTrue(any('紀年' in error or '曆年' in error for error in errors),errors)
    def test_source_bundle_exports_civil_year_without_counting_context_as_mentions(self):
        from scripts.person_bundle import bundle,load_catalog
        people,records=load_catalog(ROOT)
        current=bundle(EVENT['person_id'],catalog=(people,records))
        baseline=copy.deepcopy(records)
        for record in baseline:
            for event in record.get('events',[]):
                if event.get('id')==EVENT['id']:event.pop('chinese_civil_year',None)
        old=bundle(EVENT['person_id'],catalog=(people,baseline))
        self.assertEqual(current['source_mention_summary'],old['source_mention_summary'])
        self.assertEqual(current['mentions'],old['mentions'])
        normalized=next(e for e in current['chinese_civil_year_normalizations'] if e['record_id']==EVENT['id'])
        self.assertEqual(normalized['year'],-153)
        exported=next(e for e in current['life_events'] if e['id']==EVENT['id'])
        self.assertEqual(exported['normalized_date_range'],EVENT['normalized_date_range'])
        self.assertIn('c-shiji-106-wuwang:p009',{p['id'] for p in current['passages']})
        self.assertTrue(any(s['book_id']==EVENT['chinese_civil_year']['year_equivalence']['book_id'] for s in current['sources']))
    def errors(self,event):return civil_year_errors(event,{C['id']:C},{T['id']:T})
    def test_year_label_can_coexist_with_a_different_calendar_window(self):
        self.assertEqual(self.errors(EVENT),[])
        self.assertEqual(EVENT['chinese_civil_year']['year'],-153)
        self.assertEqual(EVENT['normalized_date_range']['earliest']['year'],-154)
    def test_neither_window_endpoint_can_override_the_sourced_label(self):
        e=copy.deepcopy(EVENT);e['chinese_civil_year'].update(era_year=155,year=-154)
        self.assertTrue(self.errors(e))
    def test_ce_bce_encoding_rejects_missing_year_and_wrong_sign(self):
        for values in [{'era_year':0,'year':1},{'era_year':154,'year':154},{'year':True}]:
            e=copy.deepcopy(EVENT);e['chinese_civil_year'].update(values);self.assertTrue(self.errors(e))
    def test_civil_label_is_not_an_exact_gregorian_date(self):
        for values in [{'calendar':'gregorian'},{'precision':'day'},{'human_reviewed':True}]:
            e=copy.deepcopy(EVENT);e['chinese_civil_year'].update(values);self.assertTrue(self.errors(e))
    def test_context_quote_and_book_identity_must_match(self):
        for key,value in [('quote','孝景帝四年'),('book_id','b-hanshu-106')]:
            e=copy.deepcopy(EVENT);e['chinese_civil_year']['context_evidence'][0][key]=value;self.assertTrue(self.errors(e))
    def test_table_row_and_fixed_witness_are_required(self):
        for key,value in [('editorial_year_cell_id','shiji-022-t1-r054-c00'),('source_revision','invented-revision'),('regnal_year_quote','四')]:
            e=copy.deepcopy(EVENT);e['chinese_civil_year']['year_equivalence'][key]=value;self.assertTrue(self.errors(e))
    def test_malformed_new_fields_fail_without_executing_or_crashing(self):
        for key,value in [('context_evidence','text'),('year_equivalence','text')]:
            e=copy.deepcopy(EVENT);e['chinese_civil_year'][key]=value;self.assertTrue(self.errors(e))
        e=copy.deepcopy(EVENT);e['evidence']='synthetic-invalid-base';self.assertTrue(self.errors(e))
    def test_synthetic_other_regnal_era_cannot_share_a_year_number(self):
        e=copy.deepcopy(EVENT);table=copy.deepcopy(T)
        for f in table['fragments']:
            for row in f['rows']:
                for cell in row['cells']:
                    if cell['id']=='shiji-022-t1-r051-c01':cell['text']='孝文元年'
        e['chinese_civil_year']['year_equivalence']['regnal_era_quote']='孝文元年'
        self.assertTrue(civil_year_errors(e,{C['id']:C},{T['id']:table}))
    def test_synthetic_later_context_is_not_earlier_event_evidence(self):
        e=copy.deepcopy(EVENT);chapter=copy.deepcopy(C);context=e['chinese_civil_year']['context_evidence'][0]
        paragraph=copy.deepcopy(next(p for p in chapter['paragraphs'] if p['id']==context['paragraph_id']));paragraph['id']='synthetic-later-context';chapter['paragraphs'].append(paragraph);context['paragraph_id']=paragraph['id']
        self.assertTrue(civil_year_errors(e,{C['id']:chapter},{T['id']:T}))
if __name__=='__main__':unittest.main()
