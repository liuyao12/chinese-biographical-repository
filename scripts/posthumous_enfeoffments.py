"""Explicit 追封 is an event distinct from lifetime granting and 追贈."""

def valid(h,paragraphs,mentions,events):
    if isinstance(h.get('enfeoffment_basis'), dict) and h['enfeoffment_basis'].get('kind') == 'explicit_posthumous_enfeoffment_after_named_subject_death_previous_paragraph':
        b=h['enfeoffment_basis']; ctx=b.get('death_context',{}); event=events.get(b.get('death_event_id'))
        if (h.get('mode')!='posthumous_enfeoffment' or h.get('kind')!='royal_rank'
                or b.get('source_term')!='追封'+h.get('title','') or h.get('title')!='臨川王'
                or b.get('evidence')!=h.get('evidence')
                or b.get('evidence')!=h.get('effective_period',{}).get('start',{}).get('evidence')
                or not event or event.get('event_type')!='death' or event.get('person_id')!=h.get('person_id')
                or not event.get('evidence') or len(b['evidence'])!=1):return False
        e=b['evidence'][0];hit=paragraphs.get(e.get('paragraph_id'));prev=paragraphs.get(ctx.get('paragraph_id'))
        if (not hit or not prev or hit[0]!=prev[0] or not hit[1]['id'].endswith(':p028')
                or not prev[1]['id'].endswith(':p027') or e.get('quote')!=hit[1]['text']
                or ctx.get('quote')!=prev[1]['text'] or ctx.get('source_revision')!='cbr-ai-transcription-sha256:aa7b16d610871f77b747adbe0edb84f8775e1d404140a1e3f6284dccd11aaa45'
                or ctx.get('paragraph_sha256')!=__import__('hashlib').sha256(prev[1]['text'].encode()).hexdigest()
                or b['source_term'] not in hit[1]['text'] or hit[1]['text'].count(b['source_term'])!=1):return False
        m=mentions.get(e.get('person_mention_id'));dm=mentions.get(ctx.get('person_mention_id'))
        if (not m or m[2].get('person_id')!=h.get('person_id') or not dm
                or dm[2].get('person_id')!=h.get('person_id') or dm[1]!=ctx.get('paragraph_id')):return False
        death_quote=next((x for x in event['evidence'] if x.get('paragraph_id')==ctx['paragraph_id'] and x.get('quote')==ctx['quote']),None)
        return bool(death_quote and event.get('source_term') in ctx.get('quote','') and death_quote.get('person_mention_id')==ctx.get('person_mention_id'))
    if isinstance(h.get('enfeoffment_basis'), dict) and h['enfeoffment_basis'].get('kind') == 'explicit_named_or_continued_posthumous_enfeoffment':
        try:
            from scripts.song041_title_semantics import enfeoffment_valid
        except ImportError:
            from song041_title_semantics import enfeoffment_valid
        return enfeoffment_valid(h, paragraphs)
    b=h.get('enfeoffment_basis',{})
    if not isinstance(b,dict):return False
    if (set(b)!={'kind','source_term','death_event_id','evidence'} or b.get('kind')!='explicit_posthumous_enfeoffment'
            or h.get('mode')!='posthumous_enfeoffment' or h.get('kind')!='noble_rank'
            or b.get('source_term')!='追封'+h.get('title','') or not b.get('evidence')
            or b['evidence']!=h.get('evidence') or b['evidence']!=h.get('effective_period',{}).get('start',{}).get('evidence')):return False
    event=events.get(b['death_event_id'])
    if not event or event.get('event_type')!='death' or event.get('person_id')!=h.get('person_id'):return False
    for e in b['evidence']:
        hit=paragraphs.get(e.get('paragraph_id'))
        if not hit or e.get('quote')!=hit[1].get('text'):return False
        p=hit[1];text=p['text'];term=b['source_term']
        if text.count(term)!=1:return False
        at=text.index(term);m=mentions.get(e.get('person_mention_id'))
        local=(m and m[1]==p['id'] and m[2].get('person_id')==h['person_id'])
        carried=e.get('context',{})
        if not local:
            # The corpus validator separately verifies this adjacent named subject.
            previous=paragraphs.get(carried.get('paragraph_id'));prior=mentions.get(carried.get('person_mention_id'))
            if (not previous or previous[0]!=hit[0] or not prior or prior[1]!=carried.get('paragraph_id')
                    or prior[2].get('person_id')!=h['person_id'] or carried.get('kind')!='previous_paragraph_subject'
                    or carried.get('quote')!=previous[1].get('text') or carried.get('person_mention_id')!=e.get('person_mention_id')):return False
        death_quotes=[x for x in event.get('evidence',[])if x.get('paragraph_id')==p['id'] and x.get('quote')==text]
        if not death_quotes or not event.get('source_term') or text.index(event['source_term'])>=at or not any(x.get('person_mention_id')==e.get('person_mention_id')for x in death_quotes):return False
        if any(x.get('kind')=='person' and x.get('person_id')!=h['person_id'] and at<=x['start']<at+len(term) for x in p.get('mentions',[])):return False
        if not any(a.get('paragraph_id')==p['id'] and a.get('surface')==h['title'] and a.get('start')==at+2 and a.get('end')==at+len(term) for a in h.get('attestations',[])):return False
    return True
