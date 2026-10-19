"""年號中之後直接接年序；核同篇相鄰原段、同人錨點與年號，不把中定為元年。"""
def valid(date,parse,chapters):
 try:
  m=date['regnal_year_mapping'];c=date['era_only_context'];es=date['evidence'];ref=date['references'][m['reference_index']]
  if m['kind']!='era_only_antecedent_ce_span' or len(es)!=1 or not chapters:return False
  a,b=c['antecedent_evidence'],es[0];ch=chapters[a['chapter_id']];ps=ch['paragraphs'];ia=next(i for i,p in enumerate(ps)if p['id']==a['paragraph_id']);ib=next(i for i,p in enumerate(ps)if p['id']==b['paragraph_id']);p,q=ps[ia],ps[ib]
  n=parse(m['source_number']);first,last=m['start_ce_year'],m['end_ce_year'];term=m['era_name']+'中';subject=c['subject_person_id']
  exact=(ia+1==ib and a['chapter_id']==b['chapter_id']==ch['id'] and a['source_id']==b['source_id']==ch['source_id'] and a['quote']==p['text'] and b['quote']==q['text'] and date['original_quote']==q['text'] and p['source_position']['first_line']+2==q['source_position']['first_line'] and p['source_position']['revision_id']==q['source_position']['revision_id'])
  if not exact:return False
  for e,para in [(a,p),(b,q)]:
   if not any(z['id']==e['person_mention_id'] and z.get('person_id')==subject for z in para['mentions']):return False
  return (term in p['text'] and c['era_expression']==term and c['antecedent_paragraph_id']==p['id'] and c['event_paragraph_id']==q['id'] and c['same_biographical_unit']is True and date['source_expression']==m['source_number']+'年' and q['text'].startswith(date['source_expression']+'，卒') and type(n)is int and 1<=n and m['regnal_year']==n and date['year']==date['era_year']==first+n-1 and first<=date['year']<=last and date['calendar']=='chinese_civil' and date['precision']=='year' and ref['scope']=='modern_era_year_equivalence_only' and ref['quote']==m['era_name'] and ref['columns']['era_name']==m['era_name'] and ref['columns']['first_year']==str(first) and ref['columns']['last_year']==str(last))
 except (KeyError,TypeError,IndexError,StopIteration,ValueError):return False
