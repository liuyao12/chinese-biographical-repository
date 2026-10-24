"""Complete received subsection role contracts, with synthetic endpoint controls."""
from pathlib import Path
import unittest,json,copy,hashlib
from scripts import attached_biography_frames as f
ROOT=Path(__file__).resolve().parents[1]
class LimitedAttachedRoles(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch=json.loads((ROOT/'corpus/jinshu/044-luchen-cuiyue.json').read_text());cls.ps={p['id']:(cls.ch['id'],p)for p in cls.ch['paragraphs']};cls.chs={cls.ch['id']:cls.ch}
  cls.kin=json.loads((ROOT/'corpus/jinshu/044-luchen-cuiyue-assertions.json').read_text())['assertions'];cls.h=json.loads((ROOT/'corpus/jinshu/044-luchen-cuiyue-titles.json').read_text())['holdings'];cls.life=json.loads((ROOT/'corpus/jinshu/044-luchen-cuiyue-life-events.json').read_text())['events'][0];cls.ad=json.loads((ROOT/'corpus/jinshu/044-luchen-cuiyue-addresses.json').read_text())['assertions'];cls.age=cls.ch['annotation']['age_assertions'][-1];cls.names=json.loads((ROOT/'corpus/jinshu/044-luchen-cuiyue-name-components.json').read_text())['records']
 def test_all_production_slots(self):
  for a in self.kin:self.assertTrue(f.kinship_valid(a,self.ps,self.chs),a['id'])
  for h in self.h:self.assertTrue(f.holding_valid(h,self.ch),h['id'])
  for a in self.ad:self.assertTrue(f.address_valid(a,self.ch),a['id'])
  for n in self.names:self.assertTrue(f.name_valid(n,self.ch),n['id'])
  self.assertTrue(f.life_valid(self.life,self.ch));self.assertTrue(f.age_valid(self.age,self.ch))
 def test_reverse_and_wrong_endpoint(self):
  for old in self.kin:
   a=copy.deepcopy(old);a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id'];self.assertFalse(f.kinship_valid(a,self.ps,self.chs))
   a=copy.deepcopy(old);a['object_person_id']='synthetic_unrelated_person';self.assertFalse(f.kinship_valid(a,self.ps,self.chs))
 def test_mother_not_bio_and_aunt_not_intermediate(self):
  for old in self.kin:
   if old['predicate']not in('maternal_role','maternal_aunt'):continue
   for key,val in [('biological_mother',True),('mother_person_id','synthetic_known_mother'),('father_person_id','synthetic_father')]:
    a=copy.deepcopy(old);a['qualifiers'][key]=val;self.assertFalse(f.kinship_valid(a,self.ps,self.chs))
 def test_no_marriage_from_uncompleted_rite(self):
  a=copy.deepcopy(next(x for x in self.kin if x['id'].endswith('princess_father')));a['predicate']='spouse';self.assertFalse(f.kinship_valid(a,self.ps,self.chs))
 def test_ancestor_missing_links_not_filled(self):
  a=copy.deepcopy(next(x for x in self.kin if x['predicate']=='great_grandfather'))
  for k,v in [('generation_distance',6),('intermediate_person_ids',['synthetic_father',None])]:
   b=copy.deepcopy(a);b['qualifiers'][k]=v;self.assertFalse(f.kinship_valid(b,self.ps,self.chs))
 def test_relative_age_not_ordinal(self):
  a=copy.deepcopy(next(x for x in self.kin if x['predicate']=='brother'));b=copy.deepcopy(a);q=b['qualifiers']['relative_birth_order'];q['older_person_id'],q['younger_person_id']=q['younger_person_id'],q['older_person_id'];self.assertFalse(f.kinship_valid(b,self.ps,self.chs));a['qualifiers']['relative_birth_order']['younger_ordinal']=2;self.assertFalse(f.kinship_valid(a,self.ps,self.chs))
 def test_no_partial_quote_or_wrong_offset(self):
  a=copy.deepcopy(self.kin[0]);a['evidence'][0]['quote']=a['evidence'][0]['quote'][:35];self.assertFalse(f.kinship_valid(a,self.ps,self.chs))
  a=copy.deepcopy(self.kin[0]);a['qualifiers']['source_clause_binding']['roles']['r0']=a['qualifiers']['source_clause_binding']['roles']['r1'];self.assertFalse(f.kinship_valid(a,self.ps,self.chs))
 def test_coordinated_negation_rehash_rejected(self):
  a=copy.deepcopy(self.kin[0]);c=copy.deepcopy(self.ch);p=c['paragraphs'][0];p['text']=p['text'].replace('未成禮','已成禮');a['qualifiers']['source_clause_binding']['paragraph_sha256']=hashlib.sha256(p['text'].encode()).hexdigest();a['evidence'][0]['quote']=p['text'];ps={p['id']:(c['id'],p)for p in c['paragraphs']};self.assertFalse(f.kinship_valid(a,ps,{c['id']:c}))
 def test_office_co_recipients_and_later_slot(self):
  for old in self.h:
   a=copy.deepcopy(old);a['person_id']='synthetic_other_recipient';self.assertFalse(f.holding_valid(a,self.ch))
   a=copy.deepcopy(old);a['title']='大官';self.assertFalse(f.holding_valid(a,self.ch))
   a=copy.deepcopy(old);a['effective_period']['end']=dict(status='source_event',date_expression='永和六年',evidence=a['evidence']);self.assertFalse(f.holding_valid(a,self.ch))
 def test_death_year_age_place_guards(self):
  for k,v in [('year',351),('era_year',351)]:
   a=copy.deepcopy(self.life);a['normalized_date'][k]=v;self.assertFalse(f.life_valid(a,self.ch))
  a=copy.deepcopy(self.life);a['person_id']='synthetic_killer';self.assertFalse(f.life_valid(a,self.ch))
  a=copy.deepcopy(self.age);a['birth_year']=284;self.assertFalse(f.age_valid(a,self.ch));a=copy.deepcopy(self.age);a['age_context']['life_event_id']='synthetic_other_death';self.assertFalse(f.age_valid(a,self.ch))
  for old in self.ad:
   a=copy.deepcopy(old);a['relation']='birth_place';self.assertFalse(f.address_valid(a,self.ch))
 def test_name_roles_not_source_normalization(self):
  for old in self.names:
   a=copy.deepcopy(old);a['surname']='synthetic_surname';self.assertFalse(f.name_valid(a,self.ch))
  a=copy.deepcopy(self.names[0]);a['zi']='道儒';self.assertFalse(f.name_valid(a,self.ch))
 def test_unframed_aunt_does_not_bypass_legacy_guard(self):
  from scripts.song047_collateral_care import valid
  a=copy.deepcopy(next(x for x in self.kin if x['predicate']=='maternal_aunt'));a['qualifiers'].pop('source_clause_binding');self.assertFalse(valid(a,self.ps));self.assertFalse(f.kinship_valid(a,self.ps,self.chs))
 def test_generic_office_words_not_formal_offices(self):
  for word in ('大官','少與','居大官','善屬文'):
   h=copy.deepcopy(self.h[-1]);h['title']=word;self.assertFalse(f.holding_valid(h,self.ch))
 def test_synthetic_ids_no_person_whitelist(self):
  # Rebind all person endpoints coherently to an unrelated synthetic universe.
  c=copy.deepcopy(self.ch);mappings={m['person_id']:'synthetic_person_'+str(i)for i,m in enumerate([m for p in c['paragraphs']for m in p['mentions']if m['kind']=='person'])}
  for p in c['paragraphs']:
   for m in p['mentions']:
    if m['kind']=='person':m['person_id']=mappings[m['person_id']]
  def rewrite(v):
   if isinstance(v,str):return mappings.get(v,v)
   if isinstance(v,list):return[rewrite(x)for x in v]
   if isinstance(v,dict):return{k:rewrite(x)for k,x in v.items()}
   return v
  ps={p['id']:(c['id'],p)for p in c['paragraphs']}
  for a in self.kin:self.assertTrue(f.kinship_valid(rewrite(a),ps,{c['id']:c}))
  for h in self.h:self.assertTrue(f.holding_valid(rewrite(h),c))
if __name__=='__main__':unittest.main()
