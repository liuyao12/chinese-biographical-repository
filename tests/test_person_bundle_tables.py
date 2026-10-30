import unittest
import tempfile
from pathlib import Path
from scripts.person_bundle import bundle

def fixture():
    people={pid:{'id':pid,'label':pid} for pid in ['aaa_bbb_111','ccc_ddd_222']}
    records=[]
    for n in [1,2]:
        tid=f'test-table-{n}'
        cell={'id':tid+'-cell','column':0,'rowspan':1,'colspan':1,'text':'甲乙甲','person_mentions':[
            {'id':tid+'-m1','start':0,'end':1,'surface':'甲','person_id':'aaa_bbb_111','status':'contextual_provisional'},
            {'id':tid+'-m2','start':1,'end':2,'surface':'乙','person_id':'ccc_ddd_222','status':'contextual_provisional'},
            {'id':tid+'-m3','start':2,'end':3,'surface':'甲','person_id':'aaa_bbb_111','status':'contextual_provisional'}]}
        table={'id':tid,'source':{'id':tid+'-witness','work_id':'w-test','book_id':'b-'+str(n),'chapter_id':'c-'+str(n),'revision':str(n),'revision_url':'https://example.org/revision/'+str(n),'image_verified':False},'fragments':[{'id':tid+'-fragment','source_header':['人名'],'rows':[{'id':tid+'-row','year':{'era':'BCE','value':100,'status':'digital_editorial_equivalence'},'cells':[cell]}]}]}
        records.append({'record_type':'historical_table_source','table':table})
    return people,records

class PersonBundleTableTests(unittest.TestCase):
    def setUp(self):
        # A synthetic table catalog belongs to a synthetic source root, never the
        # live repository whose source-owned sidecars require their full catalog.
        self.root_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.root_dir.cleanup)
        self.synthetic_root = Path(self.root_dir.name)
    def table_bundle(self, person_id, **kwargs):
        return bundle(person_id, root=self.synthetic_root, **kwargs)
    def test_table_only_person_has_readable_source_and_exact_cell(self):
        result=self.table_bundle('aaa_bbb_111',catalog=fixture())
        self.assertEqual(result['mentions'],[]);self.assertEqual(result['passages'],[])
        self.assertEqual(len(result['table_occurrences']),4);self.assertEqual(len(result['table_passages']),2);self.assertEqual(len(result['sources']),2)
        cells={c['id']:c for c in result['table_passages']}
        for m in result['table_occurrences']:
            c=cells[m['table_cell_id']];self.assertEqual(c['text'][m['start']:m['end']],m['surface']);self.assertEqual(m['quote'],c['text']);self.assertEqual(c['source_header'],['人名']);self.assertNotIn('paragraph_id',m)
            self.assertEqual(c['table_row_id'],m['table_row_id']);self.assertEqual(m['source_revision'],m['table_id'][-1])
    def test_frequency_counts_individual_focus_mentions_with_ties(self):
        r=self.table_bundle('aaa_bbb_111',catalog=fixture());self.assertEqual(set(r['most_mentioned_source_ids']),{'test-table-1-witness','test-table-2-witness'})
        for row in r['source_mention_summary']:
            self.assertEqual(row['mention_count'],2);self.assertEqual(row['passage_count'],1);self.assertEqual(row['paragraph_ids'],[]);self.assertEqual(len(row['table_cell_ids']),1)
        self.assertTrue(r['mention_count_policy']['frequency_is_not_authority'])
    def test_row_editorial_year_is_not_a_life_or_office_date(self):
        r=self.table_bundle('aaa_bbb_111',catalog=fixture());self.assertEqual(r['table_passages'][0]['row_year']['status'],'digital_editorial_equivalence');self.assertFalse(r.get('life_events'));self.assertEqual(r['date_normalizations'],[]);self.assertEqual(r['title_holdings'],[])
    def test_invalid_person_anchor_is_refused(self):
        catalog=fixture();catalog[1][0]['table']['fragments'][0]['rows'][0]['cells'][0]['person_mentions'][0]['surface']='乙'
        with self.assertRaisesRegex(ValueError,'年表人物提及'):self.table_bundle('aaa_bbb_111',catalog=catalog)
    def test_provisional_identity_is_explicit_and_keeps_each_original_person(self):
        catalog=fixture();catalog[1].append({'record_type':'person_equivalence_set','decisions':[{'id':'test-eq','person_ids':['aaa_bbb_111','ccc_ddd_222'],'evidence':[]}]})
        exact=self.table_bundle('aaa_bbb_111',catalog=catalog);merged=self.table_bundle('aaa_bbb_111',catalog=catalog,include_provisional=True)
        self.assertEqual(len(exact['table_occurrences']),4);self.assertEqual(len(merged['table_occurrences']),6);self.assertEqual({m['person_id'] for m in merged['table_occurrences']},{'aaa_bbb_111','ccc_ddd_222'})
    def test_luan_bu_short_forms_include_hou_row_without_qing_bu(self):
        r=bundle('jx9_cov_qe0',include_provisional=True);ms=[m for m in r['table_occurrences'] if m['table_cell_id'].startswith('shiji-019-t4-r008')]
        self.assertEqual(len(ms),6);self.assertFalse(any(m['surface']=='黥布' for m in ms));self.assertEqual(len({c['id'] for c in r['table_passages']}),len(r['table_passages']))
        source=next(s for s in r['sources'] if s['source_id']=='table-witness-shiji-019');self.assertEqual(source['source']['revision'],'6359260');self.assertFalse(source['source']['image_verified'])
