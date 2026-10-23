"""Full-source epitaph personal introduction and distinct dated death/burial frames."""
import re,hashlib
KIND='epitaph_named_head_dated_death_and_burial'
def valid(c,records):
 b=c['annotation']['epitaph_life_binding'];p,=c['paragraphs'];t=p['text'];near=c['annotation']['epitaph_fact_binding']
 assert set(b)=={'kind','paragraph_id','paragraph_sha256','head_mention_id','death_scope','burial_scope','origin_anchor'}and b['kind']==KIND
 assert b['paragraph_id']==p['id']and b['paragraph_sha256']==hashlib.sha256(t.encode()).hexdigest()and b['paragraph_sha256']==near['paragraph_sha256']
 ms={m['id']:m for m in p['mentions']};head=ms[b['head_mention_id']];assert head['id']==near['roles']['head']and head['kind']=='person';person=head['person_id']
 def exact(a):assert set(a)=={'paragraph_id','start','end','surface'}and a['paragraph_id']==p['id']and t[a['start']:a['end']]==a['surface'];return a['surface']
 intro=re.search(r'君姓(?P<surname>[^，。非不未無]+)，諱(?P<ming>[^，。非不未無]+)，字(?P<zi>[^，。非不未無]+)，(?P<origin>[^，。非不未無]+)人也。',t);assert intro
 assert head['start']==intro.start('ming')and head['surface']==intro['ming'];assert exact(b['origin_anchor'])==intro['origin']and b['origin_anchor']['start']==intro.start('origin')
 death=re.fullmatch(r'春秋(?P<age>[一二三四五六七八九十廿卅卌有]+)，以(?P<date>(?P<era>[^一二三四五六七八九十元年月日，。非不未無]+)(?P<year>[一二三四五六七八九十元]+)年(?P<month>[一二三四五六七八九十]+)月(?P<day>[一二三四五六七八九十]+)日)，於(?P<place>[^，。非不未無]+)瘠甚而卒。',exact(b['death_scope']));assert death
 burial=re.fullmatch(r'粵以(?P<date>(?P<era>[^一二三四五六七八九十元年月日，。非不未無]+)(?P<year>[一二三四五六七八九十元]+)年(?P<month>[一二三四五六七八九十]+)月(?P<day>[一二三四五六七八九十]+)日)，卜窆於(?P<place>[^，。非不未無]+)焉。',exact(b['burial_scope']));assert burial
 assert head['end']<b['death_scope']['start']<b['death_scope']['end']<=b['burial_scope']['start']
 def evidence(e):assert e==dict(work_id=c['work_id'],book_id=c['book_id'],source_id=c['source_id'],chapter_id=c['id'],paragraph_id=p['id'],quote=t,person_mention_id=head['id'])
 def anchor(a,scope,hit,group):
  assert exact(a)==hit[group]and a['start']==scope['start']+hit.start(group)
 try:from scripts.validate_corpus import source_age_number,normalized_date_errors
 except ImportError:from validate_corpus import source_age_number,normalized_date_errors
 other=[r for r in records if r['record_type']!='person_assertion_set'];assert len(other)==4
 for r in other:assert r['chapter_id']==c['id']
 names,=[r for r in other if r['record_type']=='person_name_component_set'];n,=names['records']
 assert n['person_id']==person and n['surname']==intro['surname']and n['ming']==intro['ming']and n['zi']==intro['zi']and n['additional_names']==[]and 'surname_basis'not in n and n['human_reviewed'] is False and n['quote']==t and n['paragraph_id']==p['id']
 addresses,=[r for r in other if r['record_type']=='person_address_assertion_set'];assert len(addresses['assertions'])==3
 expected={'biographical_origin':intro['origin'],'death_place':death['place'],'burial_place':burial['place']}
 for a in addresses['assertions']:
  assert a['person_id']==person and a['place']==dict(source_name=expected.pop(a['relation']),place_id=None,modern_identification=None)and a['source_term']==a['place']['source_name']and a['date_expression']is None and 'normalized_date'not in a and a['human_reviewed']is False
  e,=a['evidence'];evidence(e)
 # No birth, inferred age convention, or transfer of death day/place to burial.
 for kind,hit,scope,typ in [('person_life_event_assertion_set',death,b['death_scope'],'death'),('person_event_assertion_set',burial,b['burial_scope'],'burial')]:
  r,=[r for r in other if r['record_type']==kind];event,=r['events'];assert event['event_type']==typ and event['person_id']==person and event['date_expression']==hit['date']and event['source_term']==('卒'if typ=='death'else'卜窆')and event['human_reviewed']is False
  e,=event['evidence'];evidence(e);a=event['source_anchor'];assert exact(a)==event['source_term']and a['start']==scope['start']+scope['surface'].index(event['source_term'])
  norm=event['normalized_date'];assert norm['source_expression']==hit['era']+hit['year']+'年'and norm['original_quote']==t and norm['evidence']==event['evidence']and not normalized_date_errors(norm,{c['id']:c})
  parts=event['epitaph_date_parts'];assert set(parts)=={'calendar','month','day','month_anchor','day_anchor','precision'}and parts['calendar']=='chinese_lunisolar'and parts['precision']=='source_month_day_no_gregorian_conversion'
  assert parts['month']==source_age_number(hit['month'])and parts['day']==source_age_number(hit['day'])and 1<=parts['month']<=12 and 1<=parts['day']<=30
  for group in ['month','day']:
   a=parts[group+'_anchor'];assert exact(a)==hit[group]+('月'if group=='month'else'日')and a['start']==scope['start']+hit.start(group)
 age,=c['annotation']['age_assertions'];assert age['person_id']==person and age['source_term']=='春秋'+death['age']and age['source_number']==death['age']and age['value']==source_age_number(death['age'])and age['birth_year']is None and age['counting']=='unspecified_source_age'and age['date_expression']is None and 'normalized_date'not in age and age['human_reviewed']is False
 e,=age['evidence'];evidence(e)
 death_record,=[r for r in other if r['record_type']=='person_life_event_assertion_set'];death_event,=death_record['events']
 assert age.get('age_context')==dict(kind='at_death',life_event_id=death_event['id'])
 try:from scripts.age_context import age_context_valid
 except ImportError:from age_context import age_context_valid
 assert age_context_valid(age,{death_event['id']:death_event})
