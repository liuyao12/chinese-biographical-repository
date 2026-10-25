"""Direct regnal-year labels in verified finite complete-source slots only."""
def valid(date,record,chapter,root):
 try:
  assert isinstance(date,dict)and isinstance(record,dict)and isinstance(chapter,dict)and root is not None
  try:from scripts.fixed_kanripo_fact_slots import valid as bound
  except ImportError:from fixed_kanripo_fact_slots import valid as bound
  assert record.get('fixed_source_fact_binding',{}).get('kind')=='fixed_kanripo_person_fact_slots'and bound(record,chapter,root)
  assert record.get('normalized_date')==date and record['event_type']=='death'
  m=date['regnal_year_mapping'];assert m['kind']=='fixed_kanripo_direct_slot_regnal_year'
  ref=date['references'][m['reference_index']];c=ref['columns'];n=m['regnal_year'];first=m['start_ce_year'];last=m['end_ce_year']
  try:from scripts.chinese_civil_years import numeral
  except ImportError:from chinese_civil_years import numeral
  assert type(n)is int and n==numeral(m['source_number'])and 0<n<=last-first+1
  assert date['year']==date['era_year']==first+n-1 and date['calendar']=='chinese_civil'and date['precision']=='year'and date['era']=='CE'
  assert c['first_year']==str(first)and c['last_year']==str(last)and c['era_name']==ref['quote']==m['era_name']
  assert date['source_expression']==record['date_expression']==m['source_era_name']+m['source_number']+'年'
  assert ref['scope']=='modern_era_year_equivalence_only'and ref['url']=='https://dict.revised.moe.edu.tw/appendix.jsp?ID=3&page=1'
  assert date['source_expression']in record['evidence'][0]['quote']and date['evidence']==record['evidence']
  return True
 except(AssertionError,KeyError,TypeError,ValueError,IndexError,OSError):return False
