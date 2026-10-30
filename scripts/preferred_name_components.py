"""Source-scoped display reading; never rewrites source names or merges identities."""
def locator(name):
    return {k:name.get(k) for k in ('id','person_id','chapter_id','paragraph_id','surname','ming','quote')}

def reading_errors(reading, names, chapters, *, root=None):
    if isinstance(reading,dict)and isinstance(reading.get('basis'),dict)and reading['basis'].get('kind')=='cross_chapter_same_person_source_variant':
        try:from scripts.cross_chapter_name_reading import reading_errors as cross_errors
        except ImportError:from cross_chapter_name_reading import reading_errors as cross_errors
        return cross_errors(reading,names,chapters)
    if isinstance(reading,dict)and isinstance(reading.get('basis'),dict)and reading['basis'].get('kind')=='source_bound_wyd_song051_adjacent_name_variant':
        try:from scripts.wyd_song051_yixin import preferred_name_reading_errors
        except ImportError:from wyd_song051_yixin import preferred_name_reading_errors
        return preferred_name_reading_errors(reading,names,chapters,root)
    errors=[]
    if (not isinstance(reading,dict) or set(reading)!={'id','person_id','field','preferred_value','source_values','records','status','human_reviewed','rationale','coverage','basis'}
        or reading.get('field')!='ming' or reading.get('status')!='editorial_provisional'
        or not isinstance(reading.get('human_reviewed'),bool) or reading.get('coverage')!='listed_records_only'
        or not reading.get('rationale') or not isinstance(reading.get('id'),str)or not reading['id']
        or not isinstance(reading.get('person_id'),str)or not reading['person_id']):
        return ['姓名顯示選讀契約無效']
    values=reading['source_values'];refs=reading['records'];person=reading['person_id']
    if (not isinstance(values,list)or any(not isinstance(v,str)or len(v)!=1 for v in values)or len(set(values))!=2
        or reading['preferred_value']not in values or not isinstance(refs,list)or len(refs)<2):return ['姓名顯示選讀字形範圍無效']
    seen=[]
    for ref in refs:
        if not isinstance(ref,dict)or set(ref)!={'record','anchor','source_id'}:errors.append('姓名選讀來源鍵無效');continue
        n=ref['record'];a=ref['anchor']
        if not isinstance(n,dict)or set(n)!={'id','person_id','chapter_id','paragraph_id','surname','ming','quote'}:errors.append('姓名選讀record鍵無效');continue
        hit=[x for x in names if locator(x)==n]
        if len(hit)!=1 or n.get('person_id')!=person or n.get('ming')not in values:errors.append('姓名選讀未精確綁同人原始record');continue
        c=chapters.get(n['chapter_id']);p=next((p for p in c['paragraphs']if p['id']==n['paragraph_id']),None)if c else None
        m=next((m for m in p['mentions']if m['id']==a.get('id')),None)if p and isinstance(a,dict)else None
        if (not p or ref['source_id']!=c['source_id']or n['quote']not in p['text']or not m or a!=m or m.get('person_id')!=person
            or p['text'][m['start']:m['end']]!=m['surface']or n['ming']not in m['surface']):errors.append('姓名選讀人名錨或引句無效')
        seen.append(n)
    if len({str(x)for x in seen})!=len(refs):errors.append('姓名選讀重複來源')
    if {x['ming']for x in seen}!=set(values):errors.append('姓名選讀未列每個原字形')
    # Every presently-known record bearing either declared spelling must be listed.
    # A genuinely new third spelling is NOT normalized by this decision.
    relevant=[locator(n)for n in names if n.get('person_id')==person and n.get('ming')in values]
    if any(n not in seen for n in relevant):errors.append('姓名選讀遺漏已知同字形來源record')
    basis=reading['basis']
    if not isinstance(basis,dict)or set(basis)!={'kind','source_id','chapter_id','paragraph_id','quote','anchors'}:
        errors.append('姓名選讀缺同段混用依據')
    else:
        c=chapters.get(basis['chapter_id']);p=next((p for p in c['paragraphs']if p['id']==basis['paragraph_id']),None)if c else None
        aa=basis['anchors'];observed=set()
        if (not p or c['source_id']!=basis['source_id']or basis['kind']!='same_paragraph_mixed_name_spellings'
            or not isinstance(aa,list)or len(aa)<2 or basis['quote']!=p['text']):errors.append('姓名選讀同段依據無效')
        else:
            for a in aa:
                m=next((m for m in p['mentions']if isinstance(a,dict)and m['id']==a.get('id')),None)
                if not m or a!=m or m.get('person_id')!=person:errors.append('姓名選讀混用錨不同人或非原錨');continue
                observed.update(v for v in values if v in m['surface'])
            if observed!=set(values):errors.append('姓名選讀同段未見兩原字形')
    return errors

def validated_readings(records, names, chapters, person_ids=None, *, root=None):
    sets=[r for r in records if r.get('record_type')=='preferred_name_component_reading_set']
    for r in sets:
        if set(r)!={'format_version','record_type','readings'}or r.get('format_version')!='0.1'or not isinstance(r.get('readings'),list)or not r['readings']:raise ValueError('姓名顯示選讀集契約無效')
    readings=[d for r in sets for d in r['readings']]
    ids=set();scopes=set()
    for r in readings:
        errors=reading_errors(r,names,chapters,root=root)
        if errors:raise ValueError('；'.join(errors))
        if r.get('id')in ids:raise ValueError('姓名顯示選讀ID重複')
        scope=(r.get('person_id'),r.get('field'))
        if scope in scopes:raise ValueError('同一姓名構件有重複顯示選讀')
        scopes.add(scope)
        ids.add(r.get('id'))
    return [r for r in readings if person_ids is None or r['person_id']in person_ids]
