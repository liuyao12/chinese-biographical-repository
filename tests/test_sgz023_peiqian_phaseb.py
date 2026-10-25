"""Permanent whole157/native semantics; no clone or generated profiles."""
import copy,json,unittest,ast,re
from pathlib import Path
from scripts.fixed_kanripo_fact_slots import records,valid,inherited_surface_valid,noble_replacement_valid
from scripts.fixed_peiqian_structural import recruitment_valid,prefix_surface_valid,bereavement_context_valid,wrongful_killing_valid,office_departure_valid,office_end_valid
from scripts.fixed_parallel_death_era_variant import valid as date_valid
from scripts.surname_from_father import validate as surname_valid
ROOT=Path(__file__).resolve().parents[1];CID='c-sanguozhi-023-peiqian';KEY='sgz023-peiqian-family-qian-finite'
class PeiqianPhaseB(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch=json.loads((ROOT/'corpus/sanguozhi/023-peiqian.json').read_text());cls.rs=records(cls.ch,ROOT);cls.by={r['id']:r for r in cls.rs};cls.new=[r for r in cls.rs if r['id'].startswith(('th-sgz023-peiqian-phaseb-','sd-sgz023-peiqian-phaseb-','le-sgz023-peiqian-phaseb-','pe-sgz023-peiqian-phaseb-','ev-sgz023-peiqian-phaseb-','age-sgz023-peiqian-phaseb-'))or r['id']in ['nc-sgz023-peiqian-phaseb-contextual-li','nc-sgz023-peiqian-phaseb-contextual-kang','nc-sgz023-peiqian-phaseb-contextual-chuo']];cls.hs={r['id']:r for r in cls.rs if 'attestations'in r};cls.aa=[r for r in cls.rs if 'predicate'in r];tree=ast.parse((ROOT/'scripts/validate_corpus.py').read_text());fs=[n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name in ['source_age_number','normalized_date_errors','named_office_end_valid']];cls.dispatchers={'ROOT':ROOT,'re':re};exec(compile(ast.Module(body=fs,type_ignores=[]),'actual-native-dispatchers','exec'),cls.dispatchers)
 def test_complete157_actual_native_not_subset_and_unknown_slot(self):
  self.assertEqual(len(self.rs),157);self.assertEqual(len(self.new),73);actual=[]
  for f in (ROOT/'corpus/sanguozhi').glob('*.json'):
   v=json.loads(f.read_text())
   if v.get('chapter_id')!=CID:continue
   for field in ['assertions','holdings','records','events']:actual.extend(r for r in v.get(field,[])if r.get('fixed_source_fact_binding',{}).get('key')==KEY)
  actual.extend(r for r in self.ch['annotation'].get('age_assertions',[])if r.get('fixed_source_fact_binding',{}).get('key')==KEY);self.assertEqual(len(actual),157);self.assertEqual({r['id']:r for r in actual},self.by)
  for r in self.new:
   self.assertTrue(valid(r,self.ch,ROOT));bad=copy.deepcopy(r);bad['fixed_source_fact_binding']['slot']='unreviewed';self.assertFalse(valid(bad,self.ch,ROOT))
 def test_all_unknown_tenures_and_specific_era_reports(self):
  for h in self.new:
   if 'attestations'not in h:continue
   for b in h['effective_period'].values():self.assertIsNone(b['date_expression']);self.assertNotIn('normalized_date',b)
  h=self.by['th-sgz023-peiqian-phaseb-008'];self.assertEqual(len(h['attestations']),2);self.assertEqual(h['attestations'][0]['date_expression'],'咸熙中');self.assertIsNone(h['attestations'][1]['date_expression']);self.assertNotIn('th-sgz023-peiqian-phaseb-016',self.by)
  h=self.by['th-sgz023-peiqian-phaseb-033'];self.assertEqual(h['attestations'][0]['date_expression'],'元康末');self.assertEqual(h['attestations'][0]['normalized_date_range']['earliest']['year'],291);self.assertEqual(h['attestations'][0]['normalized_date_range']['latest']['year'],299)
 def test_shared_rank_gate_both_raw_verbs_and_no_parent_posthumous(self):
  for suffix,raw,title in [('xiu-inherited-clear','嗣','清陽亭侯'),('wei-inherited-julu','襲封','鉅鹿公')]:
   h=self.by['th-sgz023-peiqian-phaseb-'+suffix];a=h['attestations'][0];self.assertEqual(a['surface'],raw);self.assertEqual(h['title'],title);self.assertTrue(inherited_surface_valid(h,a,self.ch,self.hs,self.aa,ROOT));bad=copy.deepcopy(h);bad['title']='元公';self.assertFalse(inherited_surface_valid(bad,a,self.ch,self.hs,self.aa,ROOT))
 def test_departure_events_have_only_qualified_unique_prior_office_end(self):
  for hid,eid,prior,following in [('th-sgz023-peiqian-pqt-049','pe-sgz023-peiqian-phaseb-005-office-departure','尚書令','拜光祿大夫'),('th-sgz023-peiqian-phaseb-013','pe-sgz023-peiqian-phaseb-021-office-departure','黄門侍郎','遷衛國相')]:
   h=self.by[hid];e=self.by[eid];self.assertTrue(office_departure_valid(e,self.ch,ROOT));self.assertTrue(office_end_valid(h,self.ch,ROOT));self.assertEqual(e['title_holding_id'],hid);self.assertEqual(e['office_title'],prior);self.assertEqual(h['end_basis']['prior_office_anchor']['surface'],prior);self.assertEqual(h['end_basis']['following_office_anchor']['surface'],following);self.assertIsNone(h['effective_period']['end']['date_expression']);self.assertEqual(h['end_basis']['interpretation_status'],'contextual_provisional');bad=copy.deepcopy(h);bad['end_basis']['following_office_anchor']['surface']='他職';self.assertFalse(office_end_valid(bad,self.ch,ROOT));bad=copy.deepcopy(e);bad['title_holding_id']='th-sgz023-peiqian-pqt-048';self.assertFalse(office_departure_valid(bad,self.ch,ROOT))
 def test_explicit_gaifeng_uses_shared_replacement_gate(self):
  h=self.by['th-sgz023-peiqian-phaseb-xiu-julu-gong'];self.assertTrue(noble_replacement_valid(h,self.hs,{}, {},{CID:self.ch},ROOT));self.assertEqual(h['transfer_basis']['source_term'],'改封鉅鹿公');previous=self.hs[h['previous_holding_id']];self.assertEqual(previous['title'],'廣川侯');self.assertEqual(previous['effective_period']['end']['evidence'],h['effective_period']['start']['evidence']);bad=copy.deepcopy(h);bad['previous_holding_id']='th-sgz023-peiqian-pqt-050';self.assertFalse(noble_replacement_valid(bad,self.hs,{}, {},{CID:self.ch},ROOT))
 def test_reported_ages_do_not_supply_birth_or_recruitment_age(self):
  ages=[r for r in self.new if r['id'].startswith('age-')];self.assertEqual({r['value']for r in ages},{8,25,48})
  for r in ages:self.assertIsNone(r['birth_year']);self.assertIsNone(r['date_expression']);self.assertEqual(r['counting'],'unspecified_source_age')
  self.assertEqual(self.by['age-sgz023-peiqian-phaseb-009']['source_event_scope'],'able_to_compose_text');event=self.by['pe-sgz023-peiqian-phaseb-xiu-recruitment'];self.assertIsNone(event['source_recruitment_binding']['age_assertion_id']);self.assertTrue(recruitment_valid(event,self.ch,ROOT))
 def test_source_era_variant271_keeps_qin_not_global_emendation(self):
  e=self.by['le-sgz023-peiqian-phaseb-death-xiu'];ref=json.loads((ROOT/'corpus/jinshu/035-peixiu.json').read_text());self.assertEqual(e['date_expression'],'秦始七年');self.assertEqual(e['normalized_date']['year'],271);self.assertTrue(date_valid(e['normalized_date'],e,{CID:self.ch,ref['id']:ref},ROOT));bad=copy.deepcopy(e);bad['normalized_date']['year']=272;self.assertFalse(date_valid(bad['normalized_date'],bad,{CID:self.ch,ref['id']:ref},ROOT));bad=copy.deepcopy(e);bad.pop('normalized_date');self.assertFalse(date_valid(e['normalized_date'],bad,{CID:self.ch,ref['id']:ref},ROOT))
 def test_mourning_parent_and_wrongful_killing_keep_roles_unknown_year(self):
  e=self.by['le-sgz023-peiqian-phaseb-mao-death'];ev=e['evidence'][0];self.assertTrue(bereavement_context_valid(ev['context'],e,self.ch,ev,ROOT,self.aa));bad=copy.deepcopy(e);bad['person_id']=self.by['a-sgz023-peiqian-pqt-001']['subject_person_id'];self.assertFalse(bereavement_context_valid(ev['context'],bad,self.ch,ev,ROOT,self.aa));e=self.by['le-sgz023-peiqian-phaseb-wei-killing'];self.assertTrue(wrongful_killing_valid(e,self.ch,ROOT));self.assertIsNone(e['date_expression'])
 def test_source_office_prefix_and_no_fake_rank_authority(self):
  h=self.by['th-sgz023-peiqian-phaseb-017'];self.assertEqual(h['title'],'尚書令');self.assertEqual(h['attestations'][0]['surface'],'令');self.assertTrue(prefix_surface_valid(h,h['attestations'][0],self.ch,ROOT));self.assertEqual(self.by['th-sgz023-peiqian-phaseb-037']['title'],'從事中郎');self.assertNotIn('開府儀同三司',[h.get('title')for h in self.new]);self.assertNotIn('監軍將軍',[h.get('title')for h in self.new])
 def test_work_project_qualifications_and_three_surnames(self):
  works=[r for r in self.new if r.get('kind')=='creative_work_or_project_report'];self.assertEqual(len(works),7)
  for r in works:self.assertIsNone(r['values']['composition_date']);self.assertIsNone(r['values']['earliest_extant_edition']);self.assertFalse(r['values']['primary_work_seen'])
  project=next(r for r in works if r['values']['source_title']=='典治官制');self.assertIsNone(project['values']['work_id']);self.assertEqual(project['values']['completion_status'],'not_completed')
  for ming in ['黎','康','綽']:
   r=next(r for r in self.new if r.get('ming')==ming);self.assertEqual(r['surname'],'裴');self.assertEqual(r['status'],'contextual_provisional');self.assertEqual(len(r['surname_basis']['steps']),2);surname_valid(r,self.rs,{CID:self.ch},self.aa,root=ROOT)
 def test_malformed_date_arguments_sources_and_actual_dispatcher_reject(self):
  event=self.by['le-sgz023-peiqian-phaseb-death-xiu'];date=event['normalized_date'];ref=json.loads((ROOT/'corpus/jinshu/035-peixiu.json').read_text());chs={CID:self.ch,ref['id']:ref};f=self.dispatchers['normalized_date_errors']
  for bad in [None,[], 'bad',7]:
   self.assertIs(date_valid(date,bad,chs,ROOT),False);self.assertTrue(f(date,chs,ROOT,bad,'life_event'));self.assertIs(date_valid(bad,event,chs,ROOT),False);self.assertTrue(f(bad,chs,ROOT,event,'life_event'))
  for cid in chs:
   for bad in [None,[], 'bad']:
    cs=copy.deepcopy(chs);cs[cid]['source']=bad;self.assertIs(date_valid(date,event,cs,ROOT),False);self.assertTrue(f(date,cs,ROOT,event,'life_event'))
   for field,bad in [('url',None),('permalink',[]),('permalink',7)]:
    cs=copy.deepcopy(chs);cs[cid]['source'][field]=bad;self.assertIs(date_valid(date,event,cs,ROOT),False);self.assertTrue(f(date,cs,ROOT,event,'life_event'))
   for field,bad in [('text',None),('text',[]),('mentions',None),('mentions',[None])]:
    cs=copy.deepcopy(chs);cs[cid]['paragraphs'][0 if cid==ref['id']and len(cs[cid]['paragraphs'])==1 else next(i for i,p in enumerate(cs[cid]['paragraphs'])if p['id']==('c-jinshu-035-peixiu:p011'if cid==ref['id']else'c-sanguozhi-023-peiqian:p006'))][field]=bad;self.assertIs(date_valid(date,event,cs,ROOT),False);self.assertTrue(f(date,cs,ROOT,event,'life_event'))
 def test_malformed_structural_records_and_named_office_dispatcher_reject(self):
  f=self.dispatchers['named_office_end_valid']
  for bad in [None,[], 'bad',7]:
   for helper in [recruitment_valid,wrongful_killing_valid,office_departure_valid,office_end_valid]:self.assertIs(helper(bad,self.ch,ROOT),False)
   self.assertIs(f(bad,{}, {},ROOT,{CID:self.ch}),False)
  for bad in [None,[],[None],['bad'],7,'bad']:
   h={'end_basis':{'kind':'fixed_named_prior_office_departure'},'evidence':bad};self.assertIs(f(h,{}, {},ROOT,{CID:self.ch}),False)
 def test_coherent_source_rekey_no_structural_pid_rule(self):
  ch=copy.deepcopy(self.ch);old=self.by['th-sgz023-peiqian-phaseb-033']['person_id'];new='q8x_v4n_9t2'
  for p in ch['paragraphs']:
   for m in p['mentions']:
    if m.get('person_id')==old:m['person_id']=new
  rs=records(ch,ROOT);r=next(r for r in rs if r['id']=='th-sgz023-peiqian-phaseb-033');self.assertEqual(r['person_id'],new);self.assertEqual(next(r for r in rs if r['id']=='le-sgz023-peiqian-phaseb-wei-killing')['person_id'],new)
if __name__=='__main__':unittest.main()
