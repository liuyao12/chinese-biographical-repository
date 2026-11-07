"""Bind a local death quotation to an independently retained fixed narrative year chain.

The binding is an explicit source reading, not a claim to infer an event from NLU.
The existing relative-year and biography-scope validators remain mandatory.
"""
def local_death_date_evidence_valid(date, event, chapters, parse_number, root=None):
    if isinstance(date, dict) and isinstance(date.get('event_evidence_binding'), dict) and date['event_evidence_binding'].get('kind') == 'source_bound_same_paragraph_death_year_chain':
        return _same_paragraph_death_year_valid(date, event, chapters, parse_number, root)
    if isinstance(date,dict)and isinstance(date.get('event_evidence_binding'),dict)and date['event_evidence_binding'].get('kind')=='fixed_wyd063_death_local_year':
        try:from scripts.wyd_song063_basics import date_valid
        except ImportError:from wyd_song063_basics import date_valid
        return date_valid(date,event,chapters,root)
    if isinstance(date, dict) and date.get('event_evidence_binding', {}).get('kind') == 'wyd_song044_execution_narrative_year':
        try:from scripts.wyd_song044_life import date_valid
        except ImportError:from wyd_song044_life import date_valid
        return date_valid(date,event,chapters,root)
    if isinstance(date, dict) and date.get('event_evidence_binding', {}).get('kind') == 'biographical_subject_ordinal_chain_death':
        try:
            from scripts.biographical_death_year_chain import valid
        except ImportError:
            from biographical_death_year_chain import valid
        return valid(date, event, chapters, parse_number, root=root)
    if isinstance(date, dict) and date.get('event_evidence_binding', {}).get('kind') == 'named_group_execution_after_biographical_year_chain':
        try:
            from scripts.group_execution_year import valid
        except ImportError:
            from group_execution_year import valid
        return valid(date, event, chapters, parse_number)
    if isinstance(date, dict) and 'cross_chapter_event_binding' in date:
        try:
            from scripts.cross_chapter_annal_date import cross_chapter_annal_date_valid
        except ImportError:
            from cross_chapter_annal_date import cross_chapter_annal_date_valid
        return cross_chapter_annal_date_valid(date, event, 'life_event', chapters)
    # fixed-wyd045-life-date
    if isinstance(date,dict)and date.get('event_evidence_binding',{}).get('kind')=='fixed_wyd045_death_local_year':
        try:from scripts.wyd_song045_lifecycle import date_valid
        except ImportError:from wyd_song045_lifecycle import date_valid
        return date_valid(date,event,chapters,root)
    try:
        from scripts.relative_regnal_year import relative_regnal_year_valid
        from scripts.relative_biography_scope import valid as biography_scope_valid
    except ImportError:
        from relative_regnal_year import relative_regnal_year_valid
        from relative_biography_scope import valid as biography_scope_valid
    try:
        b=date.get('event_evidence_binding');scope=date.get('narrative_era_scope')
        if (not isinstance(b,dict) or set(b)!={'kind','life_event_id','person_id','source_term','source_fingerprint','event_evidence_index','date_evidence_index','event_quote_anchor','event_term_anchor','event_person_mention_id','event_date_expression_anchor','death_subject_scope'}
                or b['kind']!='local_death_in_fixed_narrative_year_chain'
                or event.get('event_type')!='death' or event.get('status')!='source_attested'
                or b['life_event_id']!=event.get('id') or b['person_id']!=event.get('person_id')
                or b['source_term']!=event.get('source_term') or not b['source_term']
                or not (any(t in b['source_term'] for t in ('死','卒','薨')) or b.get('death_subject_scope',{}).get('kind')=='named_victim_in_execution_term' and b['source_term'][:1]in('斬','梟'))
                or not isinstance(scope,dict) or scope.get('kind')!='same_biographical_timeline_with_embedded_quotations'
                or not relative_regnal_year_valid(date,parse_number,chapters)
                or not biography_scope_valid(date,chapters)):
            return False
        ch=chapters[scope['chapter_id']];ps={p['id']:p for p in ch['paragraphs']};source=ch['source'];es=date['evidence'];locals_=event['evidence'];ids=scope['paragraph_ids']
        if (not isinstance(es,list) or not isinstance(locals_,list) or len(locals_)!=1
                or type(b['event_evidence_index'])is not int or b['event_evidence_index']!=0
                or type(b['date_evidence_index'])is not int or b['date_evidence_index']!=len(es)-1
                or [e['paragraph_id']for e in es]!=ids or len(set(ids))!=len(ids)):
            return False
        expected={'source_id':ch['source_id'],'source_commit':source.get('source_commit',source.get('revision_id')),'source_blob_sha':source.get('source_blob_sha',source.get('source_blob')),'response_sha256':source.get('response_sha256',source.get('raw_file_sha256'))}
        execution_scope=b.get('death_subject_scope',{}).get('kind')=='named_victim_in_execution_term'
        if execution_scope:
            if date.get('era_year')!=date.get('year'):
                return False
            # This scope uses the existing fixed raw witness revision/SHA256;
            # no locally computed object ID is claimed to verify a remote blob.
            expected={'source_id':ch['source_id'],'source_revision':source.get('revision_id',source.get('source_commit')),'raw_file_sha256':source.get('raw_file_sha256',source.get('response_sha256'))}
        if (b['source_fingerprint']!=expected or not all(isinstance(v,str)and v for v in expected.values())):
            return False
        for e in es:
            p=ps[e['paragraph_id']]
            if (e.get('quote')!=p['text'] or any(e.get(k)!=ch[k]for k in ('work_id','book_id','source_id'))
                    or e.get('chapter_id')!=ch['id'] or p['source_position'].get('source_commit',p['source_position'].get('revision_id',p['source_position'].get('source_revision')if execution_scope else None))!=(expected['source_revision']if execution_scope else expected['source_commit'])):
                return False
        e=locals_[0];full=es[b['date_evidence_index']];p=ps[full['paragraph_id']]
        if (e.get('paragraph_id')!=p['id'] or any(e.get(k)!=full.get(k)for k in ('work_id','book_id','chapter_id','source_id'))
                or date.get('original_quote')!=p['text'] or e.get('person_mention_id')!=b['event_person_mention_id']
                or full.get('person_mention_id')!=b['event_person_mention_id']):
            return False
        def exact(a):
            return (isinstance(a,dict)and set(a)=={'paragraph_id','start','end','surface'}
                    and a['paragraph_id']==p['id'] and type(a['start'])is int and type(a['end'])is int
                    and 0<=a['start']<a['end']<=len(p['text'])and p['text'][a['start']:a['end']]==a['surface'])
        qa,ta,da=b['event_quote_anchor'],b['event_term_anchor'],b['event_date_expression_anchor']
        if (not all(exact(a)for a in (qa,ta,da)) or qa['surface']!=e.get('quote')or ta['surface']!=event.get('source_term')
                or not qa['start']<=ta['start']<ta['end']<=qa['end']
                or da['surface']!=event.get('date_expression')or not da['surface'].startswith(date['source_expression'])
                or da['start']!=scope['event_date_anchor']['start']
                or scope['event_date_anchor']['paragraph_id']!=p['id'] or da['end']>ta['end']):
            return False
        m=next(m for m in p['mentions']if m['id']==b['event_person_mention_id'])
        subject=b['death_subject_scope']
        if not isinstance(subject,dict)or set(subject)!=({'kind','clause_anchor','actor_person_mention_id'}if execution_scope else {'kind','clause_anchor'})or not exact(subject['clause_anchor']):
            return False
        ca=subject['clause_anchor']
        named=(subject['kind']=='named_subject_in_death_term'and ca==ta
               and ta['start']<=m['start']<m['end']<=ta['end']and m['start']==ta['start'])
        ill=(subject['kind']=='illness_clause_ending_in_death'
             and ca['start']==m['start']and ca['end']==ta['end']
             and ca['surface'].startswith(m['surface']+'有疾')
             and ta['surface']in('遂薨','薨','遂卒','卒','遂死','死'))
        execution=False
        if execution_scope:
            import re
            actor=next((a for a in p['mentions']if a['id']==subject['actor_person_mention_id']),None)
            before=p['text'][max(0,ca['start']-2):ca['start']]
            direct=(actor is not None and actor.get('kind')=='person'and actor.get('person_id')!=m.get('person_id')
                    and actor['start']==ca['start']and actor['end']<=ta['start'])
            if direct:
                prefix=p['text'][actor['end']:ta['start']]
                # A reusable positive battle/execution clause, not a free NLU
                # claim: named actor [advances and routs at named place] kills victim.
                battle=re.fullmatch(r'進[擊撃]大破之於[^曰云言詔非未不欲將當議請免可宜應令命遣使若如恐斬梟。；！？：「」『』\s]{1,8}',prefix)
                suffix=p['text'][m['end']:ca['end']]
                execution=(ta['surface']in('斬'+m['surface'],'梟'+m['surface'])
                    and m['start']==ta['start']+1 and m['end']==ta['end']
                    and (prefix==''or battle is not None)
                    and re.fullmatch(r'(?:[并並][一二三四五六七八九十百千萬兩零〇餘]+級)?',suffix)is not None
                    and not any(x in before for x in ('未','不','非','欲','將','當','議','請','免','可','宜','應','令','命','遣','使','若','如','恐'))
                    and not any(x in p['text'][da['end']:ca['start']]for x in ('曰','云','詔','「','」','『','』'))
                    and re.search(r'(?:元|[一二三四五六七八九十百]+)年|明年|翌年|其年',p['text'][da['end']:ta['start']])is None
                    and not any(era!=date['regnal_year_mapping']['era_name']and era in p['text'][da['end']:ta['start']]for era in scope['known_era_names'])
                    and not any(a.get('kind')=='person'and ca['start']<=a['start']<ca['end']and a['id']not in(actor['id'],m['id'])for a in p['mentions']))
        return (m.get('kind')=='person'and m.get('person_id')==event.get('person_id')
                and qa['start']<=m['start']<m['end']<=qa['end']and m['end']<=ta['end']
                and qa['start']<=ca['start']<ca['end']<=qa['end']and(named or ill or execution))
    except(KeyError,ValueError,TypeError,IndexError,StopIteration,AttributeError):
        return False


def _same_paragraph_death_year_valid(date, event, chapters, parse_number, root):
    """Validate an offline reading's exact source/recipient/date binding, not NLU.

    Full event evidence and smaller date evidence remain distinct. Reference
    roles declare the editor's reading; source_view verifies their physical
    markers and reciprocal ownership, not their historical interpretation.
    """
    try:
        try:
            from scripts.relative_regnal_year import relative_regnal_year_valid
            from scripts.surname_source_frames import source_view, same
            from scripts.quotation_boundaries import unquoted_span
            from scripts.era_stage_dates import KNOWN_ERAS
        except ImportError:
            from relative_regnal_year import relative_regnal_year_valid
            from surname_source_frames import source_view, same
            from quotation_boundaries import unquoted_span
            from era_stage_dates import KNOWN_ERAS
        import re
        b = date['event_evidence_binding']
        assert root is not None and set(b) == {
            'kind', 'life_event_id', 'person_id', 'source_term', 'frame',
            'era_anchor', 'antecedent_anchor', 'event_date_anchor',
            'event_term_anchor', 'death_subject_reference', 'non_deceased_references'}
        assert event.get('event_type') == 'death' and event.get('status') == 'source_attested'
        assert b['life_event_id'] == event['id'] and b['person_id'] == event['person_id']
        assert type(b['source_term']) is str and b['source_term'] == event['source_term']
        assert any(t in b['source_term'] for t in ('死', '卒', '薨'))
        assert date.get('status') == 'editorial_provisional' and date.get('human_reviewed') is False
        assert relative_regnal_year_valid(date, parse_number, chapters)
        ps, _, _, marker, anchor, _ = source_view([b['frame']], chapters, [], root)
        par = b['frame']['paragraph_id']; ch, p = ps[par]; text = p['text']
        def bound(a):
            anchor(a)
            assert a['paragraph_id'] == par
            return a
        era, prior, da, term = [bound(b[k]) for k in (
            'era_anchor', 'antecedent_anchor', 'event_date_anchor', 'event_term_anchor')]
        context = date['relative_year_reference']
        assert era['surface'] == context['era_expression']
        assert prior['surface'] == context['antecedent_expression']
        assert da['surface'] == date['source_expression'] == event['date_expression']
        assert term['surface'] == event['source_term']
        assert era['start'] <= prior['start'] and prior['end'] <= da['start'] < da['end'] <= term['start']
        assert unquoted_span(text, era['start'], term['end'])
        assert not any(name in text[prior['end']:term['end']] for name in KNOWN_ERAS)
        # A new local year expression would invalidate the selected sequence.
        assert re.search(r'(?:元|[一二三四五六七八九十百]+)年|明年|翌年|其年', text[prior['end']:da['start']]) is None
        assert re.search(r'(?:元|[一二三四五六七八九十百]+)年|明年|翌年|其年', text[da['end']:term['end']]) is None
        local = event['evidence']; es = date['evidence']
        assert type(local) is list and len(local) == 1 and type(es) is list and len(es) == 3
        dims = dict(work_id=ch['work_id'], book_id=ch['book_id'], source_id=ch['source_id'], chapter_id=ch['id'], paragraph_id=par)
        def evidence(e):
            assert all(same(e.get(k), v) for k, v in dims.items())
            _, _, m = marker(par, e['person_mention_id'])
            assert m['person_id'] == event['person_id']
        evidence(local[0]); assert local[0]['quote'] == text
        indices = [context[k] for k in ('era_evidence_index', 'antecedent_evidence_index', 'event_evidence_index')]
        assert indices == [0, 1, 2]
        for e, a in zip(es, (era, prior, da)):
            evidence(e); q = bound(e['source_quote_anchor'])
            assert e['quote'] == q['surface'] and q['start'] <= a['start'] < a['end'] <= q['end']
        last = es[2]['source_quote_anchor']
        assert date['original_quote'] == es[2]['quote'] and last['start'] == da['start'] and term['end'] <= last['end']
        subject = b['death_subject_reference']
        assert set(subject) == {'person_mention_id', 'clause_anchor', 'status', 'human_reviewed', 'rationale'}
        assert subject['status'] == 'contextual_provisional' and subject['human_reviewed'] is False
        assert type(subject['rationale']) is str and subject['rationale'].strip()
        _, _, m = marker(par, subject['person_mention_id']); ca = bound(subject['clause_anchor'])
        assert m['person_id'] == event['person_id'] and ca['start'] == m['start'] and ca['end'] == term['end']
        assert da['end'] <= ca['start'] < m['end'] <= term['start']
        assert ca['start'] == 0 or text[ca['start'] - 1] in '。；！？'
        assert not any(c in text[m['end']:term['end']] for c in '。；！？')
        refs = b['non_deceased_references']; assert type(refs) is list
        foreign = [a for a in p['mentions'] if a.get('kind') == 'person' and era['start'] <= a['start'] < term['end'] and a.get('person_id') != event['person_id']]
        assert [r['person_mention_id'] for r in refs] == [a['id'] for a in foreign]
        for r in refs:
            assert set(r) == {'person_mention_id', 'status', 'human_reviewed', 'rationale'}
            assert r['status'] == 'contextual_provisional' and r['human_reviewed'] is False
            assert type(r['rationale']) is str and r['rationale'].strip()
            marker(par, r['person_mention_id'])
        return True
    except (AssertionError, KeyError, ValueError, TypeError, IndexError, StopIteration, AttributeError, OSError):
        return False
