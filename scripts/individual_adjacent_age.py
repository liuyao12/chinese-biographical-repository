"""Bind an adjacent-numeral approximate age to an immediately named child."""
def individual_adjacent_age_errors(age,paragraph):
    try:
        number=age['source_number'];digits='一二三四五六七八九'
        if not isinstance(number,str)or len(number)!=2 or any(x not in digits for x in number):return ['個人約齡數詞無效']
        values=[digits.index(x)+1 for x in number];scope=age['subject_scope'];text=paragraph['text'];term=age['source_term'];e,=age['evidence'];m=next(m for m in paragraph['mentions']if m['id']==e['person_mention_id']);start,end=scope['start'],scope['end'];interpretation=age['approximation_interpretation']
        valid=(values[1]==values[0]+1 and all(type(x)is int for x in age['approximation'].get('numbers',[]))
               and age['approximation']=={'kind':'adjacent_age_numbers','numbers':values}
               and age.get('value')is None and age.get('birth_year')is None
               and not any(k in age for k in ['bounds','source_number_bounds','group_reference','normalized_date'])
               and age.get('reporting_status')=='approximate_report' and age.get('status')=='source_attested'
               and age.get('unit')=='source_age_years' and age.get('counting')=='unspecified_source_age'
               and age.get('human_reviewed')is False and bool(age.get('reviewer'))
               and term in ['年'+number+unit for unit in ['歲','歳','嵗']]
               and set(scope)=={'kind','paragraph_id','start','end','source_term'} and scope['kind']=='immediate_child_age'
               and scope['paragraph_id']==paragraph['id'] and type(start)is int and type(end)is int
               and 0<=start<end<=len(text) and text[start:end]==scope['source_term']=='有一'+m['surface']+term
               and m.get('kind')=='person' and m.get('person_id')==age['person_id'] and m['surface']in ['男','子','女']
               and m['start']==start+2 and m['end']+len(term)==end and text[m['start']:m['end']]==m['surface']
               and e['paragraph_id']==paragraph['id'] and e['quote']==text
               and interpretation.get('status')=='editorial_provisional' and interpretation.get('human_reviewed')is False
               and bool(interpretation.get('reviewer')) and bool(interpretation.get('rationale')))
        return [] if valid else ['個人相鄰數詞約齡須綁同句子女及完整原詞，不得改為確歲上下界或出生年']
    except (KeyError,TypeError,ValueError,StopIteration,AttributeError):return ['個人約齡的來源或主體綁定不全']
