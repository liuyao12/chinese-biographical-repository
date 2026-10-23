import unittest,copy,hashlib
from scripts.epitaph_named_lifecycle import valid,KIND

def fixture():
 t='故將軍沈君墓誌銘。君姓沈，諱寧，字子安，廣陵人也。春秋卅有二，以延昌四年九月九日，於南城里第瘠甚而卒。詔贈將軍。粵以熙平二年九月二日，卜窆於本縣之舊塋焉。'
 pid='synthetic-paragraph';cid='synthetic-chapter';person='synthetic-person'
 def a(s):i=t.index(s);return dict(paragraph_id=pid,start=i,end=i+len(s),surface=s)
 head=dict(id='name-mention',kind='person',person_id=person,**{k:v for k,v in a('寧').items()if k!='paragraph_id'})
 b=dict(kind=KIND,paragraph_id=pid,paragraph_sha256=hashlib.sha256(t.encode()).hexdigest(),head_mention_id=head['id'],death_scope=a('春秋卅有二，以延昌四年九月九日，於南城里第瘠甚而卒。'),burial_scope=a('粵以熙平二年九月二日，卜窆於本縣之舊塋焉。'),origin_anchor=a('廣陵'))
 c=dict(id=cid,work_id='synthetic-work',book_id='synthetic-book',source_id='synthetic-source',paragraphs=[dict(id=pid,text=t,text_layer='epitaph_as_modernly_transcribed',mentions=[head])],annotation=dict(epitaph_life_binding=b,epitaph_fact_binding=dict(paragraph_sha256=b['paragraph_sha256'],roles=dict(head=head['id']))))
 e={k:c[k]for k in ['work_id','book_id','source_id']};e.update(chapter_id=cid,paragraph_id=pid,quote=t,person_mention_id=head['id'])
 n=dict(person_id=person,surname='沈',ming='寧',zi='子安',additional_names=[],chapter_id=cid,paragraph_id=pid,quote=t,human_reviewed=False)
 ads=[dict(person_id=person,relation=rel,place=dict(source_name=place,place_id=None,modern_identification=None),source_term=place,date_expression=None,evidence=[copy.deepcopy(e)],human_reviewed=False)for rel,place in [('biographical_origin','廣陵'),('death_place','南城里第'),('burial_place','本縣之舊塋')]]
 records=[dict(record_type='person_name_component_set',chapter_id=cid,records=[n]),dict(record_type='person_address_assertion_set',chapter_id=cid,assertions=ads)]
 for typ,era,num,year,first,last in [('death','延昌','四',515,512,515),('burial','熙平','二',517,516,518)]:
  expr=era+num+'年';day='九日'if typ=='death'else'二日';term='卒'if typ=='death'else'卜窆'
  norm=dict(era='CE',era_year=year,year=year,year_numbering='astronomical',precision='year',calendar='chinese_civil',source_expression=expr,status='editorial_provisional',original_quote=t,evidence=[copy.deepcopy(e)],references=[dict(title='Synthetic fixed equivalence table',scope='modern_era_year_equivalence_only',url='https://example.org/era-table',quote=era,columns=dict(dynasty='北魏',era_name=era,first_year=str(first),last_year=str(last)))],regnal_year_mapping=dict(kind='ce_regnal_era_span',reference_index=0,start_ce_year=first,end_ce_year=last,regnal_year=4 if typ=='death'else 2,source_number=num,era_name=era),rationale='synthetic explicit era arithmetic',reviewer='AI',human_reviewed=False)
  # Month occurs twice: use the selected event's own dated scope.
  sc=b['death_scope'if typ=='death'else'burial_scope']
  def local(s):i=sc['start']+sc['surface'].index(s);return dict(paragraph_id=pid,start=i,end=i+len(s),surface=s)
  event=dict(id='synthetic-'+typ,status='source_attested',person_id=person,event_type=typ,date_expression=expr+'九月'+day,source_term=term,source_anchor=local(term),human_reviewed=False,evidence=[copy.deepcopy(e)],normalized_date=norm,epitaph_date_parts=dict(calendar='chinese_lunisolar',month=9,day=9 if typ=='death'else 2,month_anchor=local('九月'),day_anchor=local(day),precision='source_month_day_no_gregorian_conversion'))
  records.append(dict(record_type='person_life_event_assertion_set'if typ=='death'else'person_event_assertion_set',chapter_id=cid,events=[event]))
 c['annotation']['age_assertions']=[dict(person_id=person,source_term='春秋卅有二',source_number='卅有二',value=32,age_context=dict(kind='at_death',life_event_id='synthetic-death'),birth_year=None,counting='unspecified_source_age',date_expression=None,human_reviewed=False,evidence=[copy.deepcopy(e)])]
 return c,records

class LifecycleContract(unittest.TestCase):
 def test_positive(self):valid(*fixture())
 def bad(self,fn):
  c,r=fixture();fn(c,r)
  with self.assertRaises((AssertionError,KeyError,ValueError,StopIteration,TypeError)):valid(c,r)
 def test_other_person(self):self.bad(lambda c,r:r[2]['events'][0].update(person_id='another'))
 def test_birth_not_inferred(self):self.bad(lambda c,r:c['annotation']['age_assertions'][0].update(birth_year=484))
 def test_age_number(self):self.bad(lambda c,r:c['annotation']['age_assertions'][0].update(value=46))
 def test_age_counting(self):self.bad(lambda c,r:c['annotation']['age_assertions'][0].update(counting='nominal_age'))
 def test_burial_death_date_swap(self):self.bad(lambda c,r:r[3]['events'][0].update(normalized_date=copy.deepcopy(r[2]['events'][0]['normalized_date'])))
 def test_burial_date_expression(self):self.bad(lambda c,r:r[3]['events'][0].update(date_expression=r[2]['events'][0]['date_expression']))
 def test_burial_monthday(self):self.bad(lambda c,r:r[3]['events'][0]['epitaph_date_parts'].update(day=9))
 def test_burial_wrong_day_anchor(self):self.bad(lambda c,r:r[3]['events'][0]['epitaph_date_parts'].update(day_anchor=r[2]['events'][0]['epitaph_date_parts']['day_anchor']))
 def test_death_wrong_year(self):self.bad(lambda c,r:r[2]['events'][0]['normalized_date'].update(year=516,era_year=516))
 def test_burial_county_guess(self):self.bad(lambda c,r:r[1]['assertions'][2]['place'].update(source_name='南城舊塋'))
 def test_modern_place_guess(self):self.bad(lambda c,r:r[1]['assertions'][0]['place'].update(modern_identification='modern county'))
 def test_origin_as_birth_place(self):self.bad(lambda c,r:r[1]['assertions'][0].update(relation='birth_place'))
 def test_wrong_ming(self):self.bad(lambda c,r:r[0]['records'][0].update(ming='安'))
 def test_inferred_surname(self):self.bad(lambda c,r:r[0]['records'][0].update(surname_basis={'kind':'family_guess'}))
 def test_wrong_evidence_subject(self):self.bad(lambda c,r:r[2]['events'][0]['evidence'][0].update(person_mention_id='other'))
 def test_short_quote(self):self.bad(lambda c,r:r[2]['events'][0]['evidence'][0].update(quote='瘠甚而卒'))
 def test_wrong_offset(self):self.bad(lambda c,r:c['annotation']['epitaph_life_binding']['death_scope'].update(start=0))
 def test_wrong_source(self):self.bad(lambda c,r:r[2]['events'][0]['evidence'][0].update(source_id='another'))
 def test_extra_birth_event(self):self.bad(lambda c,r:r[2]['events'].append(dict(event_type='birth')))
class SourceNumerals(unittest.TestCase):
 def test_age_forms(self):
  from scripts.validate_corpus import source_age_number,direct_source_age_valid
  for s,v in [('卌',40),('卌有六',46),('卅有二',32),('廿三',23),('廿有三',23)]:
   self.assertEqual(source_age_number(s),v);self.assertTrue(direct_source_age_valid(dict(source_number=s,value=v,source_term='年'+s)))
  self.assertFalse(direct_source_age_valid(dict(source_number='三',value=3,source_term='春秋三')))
  for s in ['卌有','卌有十','卅有有二','有六','卌六六']:self.assertIsNone(source_age_number(s))
if __name__=='__main__':unittest.main()
