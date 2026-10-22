import copy,json,unittest
from pathlib import Path
from scripts.named_family_offices import valid,duty_valid,sibling_order_valid
from scripts.annal_named_death import valid as death_valid,project_layers
from scripts.validate_corpus import normalized_date_errors
R=Path(__file__).resolve().parents[1]
class Followup(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch=json.loads((R/'corpus/sanguozhi/009-caozhen.json').read_text());cls.cs={cls.ch['id']:cls.ch};cls.ps={p['id']:(cls.ch['id'],p)for p in cls.ch['paragraphs']};cls.hs={h['id']:h for h in json.loads((R/'corpus/sanguozhi/009-caozhen-titles.json').read_text())['holdings']};cls.new=[h for h in cls.hs.values()if'source_family_office_frame'in h];cls.d=json.loads((R/'corpus/sanguozhi/009-caozhen-close-family-details.json').read_text())['records'][0];cls.a=next(x for x in json.loads((R/'corpus/sanguozhi/009-caozhen-assertions.json').read_text())['assertions']if x['id']=='a-sgz009-caozhen-recovery-008');cls.e=next(x for x in json.loads((R/'corpus/sanguozhi/009-caozhen-life-events.json').read_text())['events']if x['id']=='le-sgz009-p006-m0345')
 def test_eight_roles(self):
  self.assertEqual(len(self.new),8)
  for h in self.new:self.assertTrue(valid(h,self.cs),h['id'])
 def test_duty_not_new_office(self):self.assertTrue(duty_valid(self.d,self.cs,self.hs));self.assertFalse(self.d['values']['independent_substantive_office'])
 def test_brother_order_no_ordinals(self):self.assertTrue(sibling_order_valid(self.a,self.ps));self.assertIsNone(self.a['qualifiers']['relative_birth_order']['older_ordinal'])
 def test_death_bridge(self):self.assertTrue(death_valid(self.e['normalized_date'],self.e,self.cs,R));self.assertEqual(normalized_date_errors(self.e['normalized_date'],self.cs,R,self.e,'life_event'),[])
 def test_wrong_child(self):
  h=copy.deepcopy(self.new[0]);h['person_id']=self.new[1]['person_id'];self.assertFalse(valid(h,self.cs))
 def test_list_not_absolute_birth_order(self):
  h=copy.deepcopy(self.new[0]);h['source_family_office_frame']['absolute_birth_order_inferred']=True;self.assertFalse(valid(h,self.cs))
 def test_unnamed_group_not_named_recipients(self):
  h=copy.deepcopy(self.new[0]);h['source_family_office_frame']['roles'].pop('child5');self.assertFalse(valid(h,self.cs))
 def test_five_not_six(self):
  h=copy.deepcopy(self.new[0]);h['source_family_office_frame']['fields']['count']['surface']='六';self.assertFalse(valid(h,self.cs))
 def test_offices_not_cross_assigned(self):
  h=copy.deepcopy(self.new[-1]);h['source_family_office_frame']['recipient_role']='younger1';self.assertFalse(valid(h,self.cs))
 def test_duty_not_independent_office(self):
  d=copy.deepcopy(self.d);d['values']['independent_substantive_office']=True;self.assertFalse(duty_valid(d,self.cs,self.hs))
 def test_wrong_order(self):
  a=copy.deepcopy(self.a);q=a['qualifiers']['relative_birth_order'];q['older_person_id'],q['younger_person_id']=q['younger_person_id'],q['older_person_id'];self.assertFalse(sibling_order_valid(a,self.ps))
 def test_wrong_year(self):
  e=copy.deepcopy(self.e);e['normalized_date']['year']=230;self.assertFalse(death_valid(e['normalized_date'],e,self.cs,R))
 def test_wrong_fullname(self):
  e=copy.deepcopy(self.e);e['normalized_date']['named_annal_death_binding']['reference']['actor']['quote']='曹爽';self.assertFalse(death_valid(e['normalized_date'],e,self.cs,R))
 def test_wrong_sha(self):
  e=copy.deepcopy(self.e);e['normalized_date']['named_annal_death_binding']['reference']['sha256']='0'*64;self.assertFalse(death_valid(e['normalized_date'],e,self.cs,R))
 def test_month_not_filled(self):
  e=copy.deepcopy(self.e);e['normalized_date']['month']=3;self.assertFalse(death_valid(e['normalized_date'],e,self.cs,R))
 def test_cut_context(self):
  e=copy.deepcopy(self.e);u=e['normalized_date']['named_annal_death_binding']['reference']['complete_unit'];u['quote']=u['quote'][1:];u['start']+=1;self.assertFalse(death_valid(e['normalized_date'],e,self.cs,R))
 def test_five_grants_after_father_death_not_after_execution(self):
  h=copy.deepcopy(self.new[0]);b=h['source_family_office_frame'];self.assertEqual(b['preceding_named_death']['relation'],'after');b['preceding_named_death']['person_mention_id']=b['roles']['child1'];self.assertFalse(valid(h,self.cs))
 def test_annal_event_not_in_ancient_note(self):
  text,layers=project_layers('五年春(三月大司馬某薨)三月大司馬某薨');i=text.index('三月');self.assertTrue(any(layers[i:i+8]));self.assertFalse(any(layers[i+8:]))
 def test_all_tenure_ends_unknown(self):
  for h in self.new:self.assertEqual(h['effective_period']['end']['status'],'unknown')
 def test_synthetic_ids_not_whitelist(self):
  cs=copy.deepcopy(self.cs);h=copy.deepcopy(self.new[0]);mapping={pid:'synthetic_'+str(i)for i,pid in enumerate(sorted({m['person_id']for p in cs[self.ch['id']]['paragraphs']for m in p['mentions']if m['kind']=='person'}))}
  for p in cs[self.ch['id']]['paragraphs']:
   for m in p['mentions']:
    if m['kind']=='person':m['person_id']=mapping[m['person_id']]
  h['person_id']=mapping[h['person_id']];self.assertTrue(valid(h,cs))
if __name__=='__main__':unittest.main()
