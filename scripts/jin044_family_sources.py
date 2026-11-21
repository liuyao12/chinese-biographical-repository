"""Bind the wife of Liu Kun to her two relatives using each witness's wording."""
from hashlib import sha256
def valid(a,e,ch,chapters,root):
    try:
        b=a['qualifiers'];p,=[p for p in ch['paragraphs']if p['id']==e['paragraph_id']]
        t=p['text'];s=next(x for x in p['mentions']if x['id']==e['subject_person_mention_id'])
        ref=next(x for x in ch['annotation']['person_reference_occurrences']if x['id']==e['object_reference_id'])
        if (a['human_reviewed'] is not False or a['status']!='source_attested' or e['quote']!=t
                or e['source_id']!=ch['source_id'] or e['chapter_id']!=ch['id']
                or s['kind']!='person' or ref['paragraph_id']!=p['id'] or (s['person_id'],ref['person_id'])!=(a['subject_person_id'],a['object_person_id'])
                or t[s['start']:s['end']]!=s['surface'] or t[ref['start']:ref['end']]!=ref['surface']):return False
        prior=chapters['c-jinshu-067-wenqiao']; pp,=[p for p in prior['paragraphs'] if p['text'].startswith('平北大將軍劉琨妻，嶠之從母也。')]
        prior_ku,=[m for m in pp['mentions']if m['surface']=='劉琨' and m['start']==5]
        prior_wife,=[r for r in prior['annotation']['person_reference_occurrences']if r['paragraph_id']==pp['id'] and r['surface']=='妻'and r['start']==7]
        if prior_wife['person_id']!=ref['person_id']:return False
        rule=b['source_clause_binding']['rule']
        if rule=='registered_maternal_aunt':
            phrase='琨妻即諶之從母';i=t.index(phrase);ku,=[m for m in p['mentions']if m['start']==i]
            return (ch['source']['revision_id']==1775345 and t.count(phrase)==1 and s['surface']=='諶'and s['start']==i+3 and ref['surface']=='從母' and ref['start']==i+5 and ku['person_id']==prior_ku['person_id'] and b['source_term']==phrase and b['lineage']=='maternal'and b['generation_difference']==-1 and b['mother_person_id'] is None and a['predicate']=='maternal_aunt')
        if rule=='registered_wife':
            phrase='琨妻即諶之從母';i=t.index(phrase)
            return (ch['source']['revision_id']==1775345 and s['surface']=='琨' and s['start']==i and s['person_id']==prior_ku['person_id'] and ref['surface']=='妻'and ref['start']==i+1 and b['source_term']=='琨妻'and a['predicate']=='spouse')
        if rule=='printed_zhi':
            phrase='劉琨妻之姪也';i=t.index(phrase);ku,=[m for m in p['mentions']if m['start']==i]
            w=ch['source']['image_witnesses'][0];return (ch['source']['edition']=='清乾隆武英殿本，商務影印，第12冊。' and w['pdf_page']==76 and sha256((root/w['path']).read_bytes()).hexdigest()==w['sha256'] and ch['source']['revision_id'] is None and t.startswith('悅字道儒魏司空林曾孫') and t.count(phrase)==1 and s['surface']=='悅' and s['start']==0 and ku['surface']=='劉琨'and ku['person_id']==prior_ku['person_id'] and ref['surface']=='妻'and ref['start']==i+2 and a['predicate']=='kinship_unspecified' and b['kinship_basis']=='woman_calls_zhi'and b['source_term']==phrase and b['named_intermediate_parent'] is None)
    except (TypeError,KeyError,ValueError,StopIteration,OSError):return False
    return False
