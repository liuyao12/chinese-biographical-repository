"""Actual received Song052 scopes; finite proof does not supply missing text."""
import copy,json,tempfile,unittest
from pathlib import Path
try:
    from scripts import received_life_year_scopes as model
    from scripts.validate_corpus import normalized_date_errors,direct_source_age_valid,source_age_number
    from scripts.local_death_date_evidence import local_death_date_evidence_valid
    from scripts.age_context import age_context_valid
except ImportError:
    import received_life_year_scopes as model
    from validate_corpus import normalized_date_errors,direct_source_age_valid,source_age_number
    from local_death_date_evidence import local_death_date_evidence_valid
    from age_context import age_context_valid
ROOT=Path(__file__).resolve().parents[1]
CH='corpus/songshu/052-xiejingren.json'
def read(p):return json.loads(Path(p).read_text())
class ReceivedLifeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c=read(ROOT/CH);cls.chs={cls.c['id']:cls.c};cls.want=model.expected(ROOT,cls.chs)
    def test_actual_dates_and_ages(self):
        for row,year,age in zip(self.want.values(),(416,435),(47,46)):
            e=row['event'];d=e['normalized_date']
            self.assertEqual((d['source_expression'],d['year'],row['age']['value']),('十二年',year,age))
            self.assertTrue(model.valid(d,e,self.chs,root=ROOT))
            self.assertEqual(normalized_date_errors(d,self.chs,root=ROOT,bound_record=e),[])
            self.assertTrue(local_death_date_evidence_valid(d,e,self.chs,source_age_number,root=ROOT))
            self.assertTrue(direct_source_age_valid(row['age']))
            self.assertTrue(age_context_valid(row['age'],{e['id']:e}))
            self.assertIsNone(row['age']['birth_year'])
    def test_wrong_actor_year_scope_and_source_expression(self):
        a,b=self.want.values()
        for edit in ('actor','year','expression','missing_context','later_year'):
            e=copy.deepcopy(a['event']);d=e['normalized_date']
            if edit=='actor':e['person_id']=b['event']['person_id'];d['event_evidence_binding']['person_id']=e['person_id']
            elif edit=='year':d['year']=d['era_year']=435
            elif edit=='expression':d['source_expression']='義熙十二年'
            elif edit=='missing_context':d['evidence'].pop(1)
            else:d['year']=d['era_year']=421
            self.assertFalse(model.valid(d,e,self.chs,root=ROOT),edit)
    def test_known_slot_cannot_drop_binding_or_age(self):
        c=copy.deepcopy(self.c);c['annotation']['age_assertions']=[r['age']for r in self.want.values()]
        ev=[copy.deepcopy(r['event'])for r in self.want.values()]
        origin=[r['origin']for r in self.want.values()if r['origin']]
        records=[c,{'record_type':'person_life_event_assertion_set','events':ev},{'record_type':'person_address_assertion_set','assertions':origin}]
        self.assertEqual(model.errors(ROOT,records),[])
        self.assertEqual(model.native_errors(ROOT,{c['id']:c}),[])
        del ev[0]['normalized_date']['event_evidence_binding']
        self.assertTrue(model.errors(ROOT,records))
        ev[0]=copy.deepcopy(next(iter(self.want.values()))['event']);c['annotation']['age_assertions'].pop()
        self.assertTrue(model.errors(ROOT,records))
    def test_changed_actual_source_role_or_layer_rejected(self):
        for kind in ('subject','layer','year'):
            c=copy.deepcopy(self.c);ps={p['id'].rsplit(':',1)[-1]:p for p in c['paragraphs']}
            if kind=='subject':ps['p017']['mentions'][0]['person_id']='unrelated_source_identity'
            elif kind=='layer':ps['p018']['text_layer']='received_quoted_document'
            else:ps['p018']['text']=ps['p018']['text'].replace('十二年','十七年',1)
            e=next(reversed(self.want.values()))['event']
            self.assertFalse(model.valid(e['normalized_date'],e,{c['id']:c},root=ROOT))
    def test_bad_type_fails_closed(self):
        e=next(iter(self.want.values()))['event']
        for bad in (None,[],1,'record'):
            self.assertFalse(model.valid(e['normalized_date'],bad,self.chs,root=ROOT))
            self.assertFalse(model.valid(e['normalized_date'],e,bad,root=ROOT))
    def test_raw_and_trusted_proof_are_real_files(self):
        entry=next(iter(model.slots(ROOT).values()));ref=entry['proof_ref'];proof=read(ROOT/ref['path'])
        with tempfile.TemporaryDirectory()as td:
            r=Path(td)
            for rel in (model.INDEX,ref['path'],proof['raw_file']['path']):
                dest=r/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((ROOT/rel).read_bytes())
            e=next(iter(self.want.values()))['event']
            self.assertTrue(model.valid(e['normalized_date'],e,self.chs,root=r))
            f=r/proof['raw_file']['path'];f.write_bytes(f.read_bytes()+b'\n')
            self.assertFalse(model.valid(e['normalized_date'],e,self.chs,root=r))
            f.write_bytes((ROOT/proof['raw_file']['path']).read_bytes())
            (r/ref['path']).write_text('{}')
            self.assertFalse(model.valid(e['normalized_date'],e,self.chs,root=r))
    def test_current_canonical_follows_source_mid(self):
        c=copy.deepcopy(self.c);old=next(iter(self.want.values()))['event']['person_id'];new='synthetic_current_canonical'
        for p in c['paragraphs']:
            for m in p['mentions']:
                if m.get('person_id')==old:m['person_id']=new
        want=model.expected(ROOT,{c['id']:c});e=next(iter(want.values()))['event']
        self.assertEqual(e['person_id'],new);self.assertTrue(model.valid(e['normalized_date'],e,{c['id']:c},root=ROOT))
    def test_origin_is_source_origin_only(self):
        a=next(iter(self.want.values()))['origin']
        self.assertEqual(a['relation'],'biographical_origin');self.assertEqual(a['place']['source_name'],'陳郡陽夏')
        self.assertIsNone(a['date_expression']);self.assertIsNone(next(reversed(self.want.values()))['origin'])
if __name__=='__main__':unittest.main()
