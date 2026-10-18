# coding: utf-8
import copy,json,unittest
from pathlib import Path
from scripts.royal_transfers import royal_transfer_errors,chronology_choice_errors
from scripts.table_evidence import load_tables,table_regnal_range_errors
ROOT=Path(__file__).resolve().parents[1]
class XiTransfers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapters={}
        for number in ['052','118']:
            c=json.loads((ROOT/f'corpus/shiji/{number}.json').read_text());cls.chapters[c['id']]=c
        cls.ps={p['id']:(c['id'],p)for c in cls.chapters.values()for p in c['paragraphs']};cls.ms={m['id']:(c['id'],p['id'],m)for c in cls.chapters.values()for p in c['paragraphs']for m in p['mentions']};cls.hs={h['id']:h for h in json.loads((ROOT/'corpus/shiji/118-titles.json').read_text())['holdings']};cls.tables=load_tables(ROOT)
    def test_three_periods_are_connected_by_two_explicit_transfers(self):
        a,b,c=[self.hs['th-shiji118-xi-'+s]for s in ['chengyang-before','huainan-transfer','chengyang-return']];self.assertEqual(a['effective_period']['start']['status'],'unknown');self.assertEqual(c['effective_period']['end']['status'],'unknown')
        for old,new in [(a,b),(b,c)]:
            self.assertEqual(royal_transfer_errors(new,self.hs,self.ps,self.ms),[]);x=old['effective_period']['end'];y=new['effective_period']['start'];self.assertEqual(x['event_type'],'explicit_end');self.assertEqual(y['event_type'],'transfer');self.assertEqual(x['evidence'],y['evidence']);self.assertEqual(x['normalized_date_range'],y['normalized_date_range'])
    def test_elliptical_return_never_fabricates_a_destination_title_span(self):
        h=self.hs['th-shiji118-xi-chengyang-return'];a=h['attestations'][0];p=self.ps[a['paragraph_id']][1];self.assertNotIn('城陽王',p['text']);self.assertEqual(p['text'][a['start']:a['end']],'王');self.assertEqual(a['context_role'],'pre_transfer_rank');self.assertEqual(h['jurisdictions'][0]['source_name'],'城陽');self.assertEqual(h['resumption_basis']['return_source_term'],'復故城陽')
    def test_return_requires_same_person_earlier_kingdom_and_actual_prior_rank(self):
        base=self.hs['th-shiji118-xi-chengyang-return']
        for change in ['wrong_person','posthumous','wrong_origin','wrong_destination','wrong_rank_context','wrong_return_phrase','wrong_earlier']:
            h=copy.deepcopy(base);hs=copy.deepcopy(self.hs);prior=hs[h['resumption_basis']['earlier_holding_id']]
            if change=='wrong_person':prior['person_id']='synthetic-person'
            if change=='posthumous':prior['mode']='posthumous_naming'
            if change=='wrong_origin':h['resumption_basis']['previous_source_title']='濟北王'
            if change=='wrong_destination':h['jurisdictions'][0]['source_name']='濟北'
            if change=='wrong_rank_context':h['attestations'][0]['context_role']='destination_title'
            if change=='wrong_return_phrase':h['resumption_basis']['return_source_term']='新封城陽'
            if change=='wrong_earlier':h['resumption_basis']['earlier_holding_id']='th-shiji118-025'
            self.assertTrue(royal_transfer_errors(h,hs,self.ps,self.ms),change)
    def test_months_of_other_grants_are_not_borrowed_for_xi(self):
        for suffix,years in [('huainan-transfer',(169,168)),('chengyang-return',(165,164))]:
            h=self.hs['th-shiji118-xi-'+suffix];p=h['effective_period']['start'];d=p['normalized_date_range'];self.assertEqual((d['earliest']['era_year'],d['latest']['era_year']),years);self.assertNotIn('normalized_date',p);self.assertNotIn('month',d['earliest']);self.assertEqual(table_regnal_range_errors(d,p['date_expression'],self.tables,self.ms),[])
    def test_source_choice_preserves_eight_four_and_parallel_five(self):
        for suffix,term in [('huainan-transfer','共王八年，徙王淮南'),('chengyang-return','四年，復還王城陽')]:
            h=self.hs['th-shiji118-xi-'+suffix];self.assertEqual(chronology_choice_errors(h,self.ps,self.chapters),[]);c=h['chronology_source_choice'];self.assertEqual(c['alternative_source_term'],term);self.assertEqual(c['alternative_chapter_id'],'c-shiji-052-qidaohui');self.assertTrue(any('五年復還王城' in ref['quote'].replace('¶','').replace('\n','')for ref in c['references']));self.assertFalse(c['human_reviewed'])
    def test_chronology_choice_rejects_mismatched_or_empty_source_claims(self):
        base=self.hs['th-shiji118-xi-chengyang-return']
        for change in ['wrong_chapter','empty_quote','empty_term','wrong_preferred','human','unfixed','altered_display']:
            h=copy.deepcopy(base);c=h['chronology_source_choice']
            if change=='wrong_chapter':c['alternative_chapter_id']='c-shiji-118-huainan'
            if change=='empty_quote':c['alternative_evidence']['quote']=''
            if change=='empty_term':c['alternative_source_term']=''
            if change=='wrong_preferred':c['preferred_source_expression']='孝文十二年'
            if change=='human':c['human_reviewed']=True
            if change=='unfixed':
                for ref in c['references']:ref['source_commit']=''
            if change=='altered_display':c['references'][0]['display_quote']='合成錯字'
            self.assertTrue(chronology_choice_errors(h,self.ps,self.chapters),change)
    def test_native_table_marks_names_not_unnamed_year_or_whole_cells(self):
        t=self.tables['shiji-017'];cells={c['id']:c for f in t['fragments']for row in f['rows']for c in row['cells']}
        person=next(p for p in json.loads((ROOT/'registry/persons.json').read_text())['persons']if p['id']=='yqp_nlb_p1p_ABFA');self.assertEqual(person['evidence_scope'],'corpus_and_native_table_mentions')
        for cid,term in [('shiji-017-t1-r031-c06','共王喜'),('shiji-017-t1-r039-c13','城陽王喜'),('shiji-017-t1-r043-c06','淮南王喜')]:
            c=cells[cid];self.assertEqual(len(c['person_mentions']),1);m=c['person_mentions'][0];self.assertEqual(m['surface'],term);self.assertEqual(m['person_id'],'yqp_nlb_p1p_ABFA');self.assertEqual(c['text'][m['start']:m['end']],term);self.assertLess(m['end'],len(c['text']));self.assertEqual({e['book_id']for e in m['identity_evidence']},{'b-shiji-052','b-shiji-118'})
        self.assertEqual(cells['shiji-017-t1-r038-c06']['person_mentions'],[])

if __name__=='__main__':unittest.main()
