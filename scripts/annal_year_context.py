"""Bind an annal entry to its fixed witness's explicit yearly section.

The section is provenance, not a fabricated continuous biography paragraph.
No Gregorian day or birth year is inferred from the recorded month/day.
"""
import hashlib
import re


def annal_regnal_year_valid(date, parse_number):
    if date.get('annal_year_reference', {}).get('format') == 'rendered_single_year_annal':
        return _rendered_year_arithmetic(date, parse_number)
    if date.get('annal_year_reference', {}).get('format') == 'kanripo_continuous_year':
        try:
            from .jin_facts_boundaries import continuous_annal_valid
        except ImportError:
            from jin_facts_boundaries import continuous_annal_valid
        return continuous_annal_valid(date, parse_number)
    mapping = date.get('regnal_year_mapping', {})
    context = date.get('annal_year_reference', {})
    refs = date.get('references', [])
    if not isinstance(mapping, dict) or not isinstance(context, dict) or not isinstance(refs, list):
        return False
    ri, ci = mapping.get('reference_index'), mapping.get('context_reference_index')
    if (mapping.get('kind') != 'annal_ce_regnal_era_span'
            or any(type(i) is not int or not 0 <= i < len(refs) for i in (ri, ci))
            or ri == ci):
        return False
    modern, primary = refs[ri], refs[ci]
    if not isinstance(modern, dict) or not isinstance(primary, dict):
        return False
    section = primary.get('section', {})
    if not isinstance(section, dict):
        return False
    raw = section.get('raw_quote')
    bounds = section.get('source_lines')
    first, last, n = (mapping.get(k) for k in ('start_ce_year', 'end_ce_year', 'regnal_year'))
    number, name = mapping.get('source_number'), mapping.get('era_name')
    if (not isinstance(raw, str) or not isinstance(bounds, list) or len(bounds) != 2
            or any(type(i) is not int for i in bounds) or not 0 < bounds[0] < bounds[1]
            or not isinstance(name, str) or not name or (1 if number == '元' else parse_number(number)) != n
            or type(n) is not int or n < 1 or mapping.get('target_regnal_year') != n
            or type(first) is not int or type(last) is not int or not 0 < first <= last
            or date.get('era') != 'CE' or date.get('year') != first + n - 1
            or not first <= date['year'] <= last):
        return False
    lines = raw.splitlines()
    term = name + str(number) + '年'
    next_heading = section.get('next_heading', '')
    if not isinstance(next_heading, str):
        return False
    match = re.fullmatch(r'==(.+?)([元一二三四五六七八九十百]+)年==', next_heading)
    line = context.get('event_source_line')
    expression = date.get('source_expression')
    if (len(lines) != bounds[1] - bounds[0] + 1
            or not lines or lines[0] != '==' + term + '=='
            or lines[-1] != next_heading or not match or match[1] != name
            or parse_number(match[2]) != n + 1
            or any(re.fullmatch(r'==.*==', text) for text in lines[1:-1])
            or not next((text for text in lines[1:-1] if text.strip()), '').startswith(str(number) + '年')
            or section.get('year_expression') != term
            or section.get('raw_quote_sha256') != hashlib.sha256(raw.encode()).hexdigest()
            or type(line) is not int or not bounds[0] < line < bounds[1]
            or lines[line - bounds[0]] != date.get('original_quote')
            or not isinstance(expression, str) or not expression or expression not in date['original_quote']
            or context.get('section_id') != section.get('id')):
        return False
    evidence = date.get('evidence', [])
    if (not isinstance(evidence, list) or len(evidence) != 1 or not isinstance(evidence[0], dict)
            or context.get('event_paragraph_id') != evidence[0].get('paragraph_id')
            or date['original_quote'] != evidence[0].get('quote')
            or any(primary.get(k) != evidence[0].get(k) for k in ('work_id', 'book_id', 'chapter_id', 'source_id'))
            or primary.get('quote') != raw or primary.get('scope') != 'primary_annal_year_section_context'
            or primary.get('image_verified') is not False
            or not str(primary.get('url', '')).startswith('https://')
            or primary.get('source_revision') != section.get('source_revision')):
        return False
    return (modern.get('scope') == 'modern_era_year_equivalence_only'
            and modern.get('quote') == name and str(modern.get('url', '')).startswith('https://')
            and isinstance(modern.get('columns'), dict)
            and modern.get('columns', {}).get('era_name') == name
            and modern.get('columns', {}).get('first_year') == str(first)
            and modern.get('columns', {}).get('last_year') == str(last))


def life_event_year_context_valid(event, chapters, root=None):
    """A verified year frame can date an event whose own sentence has no date."""
    try:
        date = event['normalized_date']
        reference = date.get('annal_year_reference') if isinstance(date, dict) else None
        if (event.get('date_expression') is not None
                or not isinstance(date, dict)
                or not isinstance(reference, dict)
                or reference.get('format') != 'rendered_single_year_annal'):
            return False
        chapter = chapters[date['evidence'][0]['chapter_id']]
        return annal_year_binding_valid(date, chapter, root=root,
                                        bound_record=event, bound_role='life_event')
    except (KeyError, TypeError, IndexError):
        return False


def annal_year_binding_valid(date, chapter, root=None, bound_record=None, bound_role=None):
    """The arithmetic check also needs this binding to the marked source file."""
    if not isinstance(chapter, dict):
        return False
    if date.get('annal_year_reference', {}).get('format') == 'rendered_single_year_annal':
        return _rendered_year_binding(date, chapter, root, bound_record, bound_role)
    if date.get('annal_year_reference', {}).get('format') == 'kanripo_continuous_year':
        try:
            from .jin_facts_boundaries import continuous_annal_binding_valid
        except ImportError:
            from jin_facts_boundaries import continuous_annal_binding_valid
        return continuous_annal_binding_valid(date, chapter)
    mapping = date.get('regnal_year_mapping', {})
    refs = date.get('references', [])
    if not isinstance(mapping, dict) or not isinstance(refs, list):
        return False
    ci = mapping.get('context_reference_index')
    if type(ci) is not int or not 0 <= ci < len(refs):
        return False
    ref = refs[ci]
    context = date.get('annal_year_reference', {})
    if not isinstance(ref, dict) or not isinstance(context, dict):
        return False
    section = ref.get('section')
    source = chapter.get('source', {})
    paragraph = next((p for p in chapter.get('paragraphs', [])
                      if p['id'] == context.get('event_paragraph_id')), {})
    position = paragraph.get('source_position', {})
    excerpt = next((e for e in source.get('normalization', {}).get('excerpts', [])
                    if e['proposed_paragraph_id'] == paragraph.get('id')), {})
    return (isinstance(section, dict)
            and section in source.get('annal_year_sections', [])
            and source.get('revision_id') == ref.get('source_revision') == section.get('source_revision')
            and all(ref.get(k) == chapter.get(k if k != 'chapter_id' else 'id')
                    for k in ('work_id', 'book_id', 'chapter_id', 'source_id'))
            and position.get('first_line') == position.get('last_line') == context.get('event_source_line')
            and paragraph.get('text') == excerpt.get('raw_quote') == date.get('original_quote')
            and excerpt.get('source_lines') == [context.get('event_source_line')] * 2)


def _same(a,b):
    if type(a)is not type(b):return False
    if type(a)is dict:return a.keys()==b.keys()and all(_same(a[k],b[k])for k in a)
    if type(a)is list:return len(a)==len(b)and all(_same(x,y)for x,y in zip(a,b))
    return a==b


def _rendered_year_arithmetic(date,parse):
    """Year equivalence only. Association with the selected event is separate."""
    try:
        m=date['regnal_year_mapping'];refs=date['references'];ri=m['reference_index'];ci=m['context_reference_index']
        assert type(ri)is type(ci)is int and 0<=ri<len(refs)and 0<=ci<len(refs)and ri!=ci
        modern=refs[ri];primary=refs[ci];n=m['regnal_year'];first=m['start_ce_year'];last=m['end_ce_year'];num=m['source_number'];name=m['era_name']
        assert m['kind']=='annal_ce_regnal_era_span'and all(type(x)is int for x in(n,first,last,date['year'],date['era_year']))and n==(1 if num=='元'else parse(num))and m['target_regnal_year']==n
        assert 0<first<=date['year']<=last and date['era']=='CE'and date['year']==date['era_year']==first+n-1
        assert date['calendar']=='chinese_civil'and date['precision']=='year'and date['status']=='editorial_provisional'and date['human_reviewed']is False
        assert all(date.get(k)is None for k in('month','day','month_expression','day_expression','day_ganzhi','sexagenary_day'))
        assert date['source_expression']==name+num+'年'and modern['scope']=='modern_era_year_equivalence_only'and modern['quote']==name
        assert modern['columns']==dict(dynasty=modern['columns']['dynasty'],era_name=name,first_year=str(first),last_year=str(last))and modern['url'].startswith('https://')
        assert primary['scope']=='primary_rendered_single_year_annal_context'and primary['image_verified']is False
        return True
    except(AssertionError,KeyError,TypeError,ValueError,IndexError,AttributeError):return False


def _rendered_year_binding(date,chapter,root,event,role):
    """Validate an offline editorial association, never infer all events' years."""
    from pathlib import Path
    import json
    from html.parser import HTMLParser
    try:
        assert root is not None and role=='life_event'and type(event)is dict and event['event_type']=='death'and event['status']=='source_attested'and event['human_reviewed']is False and event['date_expression']is None
        base=Path(root).resolve()
        def raw(rel):
            p=Path(rel);assert not p.is_absolute()and '..'not in p.parts and p.parts[0]in('corpus','registry','source-evidence','sources')
            q=base
            for part in p.parts:q=q/part;assert not q.is_symlink()
            assert q.resolve().is_relative_to(base);return q.read_bytes()
        def read(rel):return json.loads(raw(rel))
        ctx=date['annal_year_reference'];ref=date['references'][date['regnal_year_mapping']['context_reference_index']];section=ref['section']
        assert ctx['format']=='rendered_single_year_annal'and section['id']==ctx['section_id']and section in chapter['source']['annal_year_sections']
        assert chapter['record_type']=='marked_chapter'and Path(section['chapter_path']).parts[0]=='corpus'and Path(section['observation_path']).parts[0]=='source-evidence'
        assert _same(read(section['chapter_path']),chapter)
        for key in('work_id','book_id','source_id'):assert ref[key]==chapter[key]
        assert ref['chapter_id']==chapter['id']and ref['source_revision']==chapter['source']['revision_id']
        b=raw(section['observation_path']);assert hashlib.sha256(b).hexdigest()==section['observation_sha256'];ob=json.loads(b)
        assert ob['kind']=='current_rendered_single_year_annal_observation'and all(ob[k]==chapter[k]for k in('work_id','book_id','source_id'))and ob['chapter_id']==chapter['id']
        src=chapter['source'];assert _same(ob['reported_revision'],src['revision_id'])and ob['url']==src['url']==ref['url']
        assert src['observation_kind']=='current_rendered_observation'and ob['human_reviewed']is src['human_reviewed']is False
        assert ob['fixed_body_obtained']is src['fixed_body_obtained']is False and ob['raw_capture_obtained']is src['raw_capture_obtained']is False and ob['image_verified']is src['image_verified']is False
        assert all(src.get(k)is None for k in('actual_print_edition','actual_print_edition_id','printed_base_edition','printed_base_edition_id'))
        assert all(src.get(k,False)is False for k in('original_wikitext_obtained','raw_wikitext_obtained','fixed_permalink_body_read'))
        assert type(src['edition'])is str and '未知'in src['edition']and '未核'in src['edition']
        observed=ob['observed_text'];assert type(observed)is str
        def unit(key,layer):
            u=ob['units'][section[key]];assert u['layer']==layer and type(u['text'])is str;mp=u['character_map']
            assert type(mp)is list and len(mp)==len(u['text'])and mp and all(type(i)is int and 0<=i<len(observed)for i in mp)and mp==list(range(mp[0],mp[0]+len(mp)))
            assert ''.join(observed[i]for i in mp)==u['text']and hashlib.sha256(u['text'].encode()).hexdigest()==u['text_sha256'];return u
        total=unit('total_unit','received_chapter_summary');heading=unit('year_unit','digital_editorial_heading_with_modern_ce_gloss');eu=unit('event_unit','received_chapter');wu=unit('work_unit','digital_work_heading');bu=unit('book_unit','digital_book_heading')
        assert re.search(r'(?:^|[，、；： ])一年(?:。|$)',total['text'])and total['character_map'][-1]<eu['character_map'][0]and heading['character_map'][-1]<eu['character_map'][0]
        ya=section['year_anchor'];assert set(ya)=={'start','end','surface'}and type(ya['start'])is type(ya['end'])is int and 0<=ya['start']<ya['end']<=len(heading['text'])and heading['text'][ya['start']:ya['end']]==ya['surface']==date['source_expression']
        assert '公元'not in ya['surface']and ref['quote']==heading['text']
        between=observed[heading['character_map'][-1]+1:eu['character_map'][0]]
        assert not re.search(r'(?m)^(?:L[0-9]+:)?\s*(?:==.*?年==|[^\n]{0,12}'+re.escape(date['regnal_year_mapping']['era_name'])+r'[元一二三四五六七八九十百]+年)',between)
        work,=[w for w in read('registry/works.json')['works']if w['id']==chapter['work_id']];book,=[x for x in work['books']if x['id']==chapter['book_id']]
        assert wu['text']==work['title']and book['chapter_ids'].count(chapter['id'])==1 and book['work_id']==work['id']and type(book['number'])is int
        bn=section['book_number_anchor'];assert set(bn)=={'start','end','surface'}and type(bn['start'])is type(bn['end'])is int and 0<=bn['start']<bn['end']<=len(bu['text'])and bu['text'][bn['start']:bn['end']]==bn['surface']and bn['surface']==section['book_number_source']
        from_number=section['book_number_value'];assert type(from_number)is int and from_number==book['number']
        # The Chinese numeral is checked independently; never infer a book from a filename.
        try:from scripts.validate_corpus import source_age_number
        except ImportError:from validate_corpus import source_age_number
        assert source_age_number(bn['surface'])==from_number
        tb=read('registry/work-provenance.json')['text_bases'][chapter['source_id']];assert tb['source_id']==chapter['source_id']and tb['work_id']==work['id']
        p,=[p for p in chapter['paragraphs']if p['id']==ctx['event_paragraph_id']];assert p['text_layer']=='received_chapter'and p['text']==eu['text']==date['original_quote']
        association,=[a for a in chapter['annotation']['annal_event_year_associations']if a['id']==ctx['event_association_id']]
        assert set(association)=={'id','kind','section_id','event_id','life_events_path','paragraph_id','person_mention_id','event_anchor','temporal_scope','status','rationale','reviewer','human_reviewed'}
        assert association['kind']=='offline_editorial_annal_event_year_association'and association['section_id']==section['id']and association['event_id']==event['id']and association['paragraph_id']==p['id']
        assert association['temporal_scope']=='current_annal_year_for_selected_event_only'and association['status']=='editorial_provisional'and association['human_reviewed']is False and association['rationale'].strip()and association['reviewer'].strip()
        assert Path(association['life_events_path']).parts[0]=='corpus'
        doc=read(association['life_events_path']);assert doc['record_type']=='person_life_event_assertion_set'and doc['chapter_id']==chapter['id'];stored,=[e for e in doc['events']if e['id']==event['id']];assert _same(stored,event)and _same(event['normalized_date'],date)
        mid=association['person_mention_id'];m,=[m for m in p['mentions']if m['id']==mid];assert m['kind']=='person'and m['person_id']==event['person_id']and type(m['start'])is type(m['end'])is int and 0<=m['start']<m['end']<=len(p['text'])and p['text'][m['start']:m['end']]==m['surface']
        anchor=association['event_anchor'];assert set(anchor)=={'paragraph_id','start','end','surface'}and type(anchor['start'])is type(anchor['end'])is int and 0<=anchor['start']<anchor['end']<=len(p['text'])and anchor['paragraph_id']==p['id']and p['text'][anchor['start']:anchor['end']]==anchor['surface']
        term=event['source_term'];assert re.fullmatch(r'(?:遂|乃|因)?(?:死獄中|死|卒|薨|崩)',term)and anchor['start']==m['start']and anchor['surface']==m['surface']+term+'。'and anchor['end']==m['end']+len(term)+1
        before=p['text'][:m['start']];assert before.count('「')==before.count('」')and before.count('『')==before.count('』')
        assert not p['text'].startswith(('初，','先是，','昔，','曩者'))
        e,=event['evidence'];assert _same(date['evidence'],event['evidence'])and e==dict(work_id=chapter['work_id'],book_id=chapter['book_id'],source_id=chapter['source_id'],chapter_id=chapter['id'],paragraph_id=p['id'],person_mention_id=mid,quote=p['text'])
        persons=read('registry/persons.json')['persons'];reverse=[(r['id'],x)for r in persons for x in r.get('evidence',[])if x.get('mention_id')==mid];aliases=[(r['id'],a)for r in persons for a in r.get('aliases',[])for am in a.get('mention_ids',[])if am==mid]
        expected=dict(work_id=chapter['work_id'],book_id=chapter['book_id'],source_id=chapter['source_id'],chapter_id=chapter['id'],paragraph_id=p['id'],mention_id=mid,quote=m['surface'])
        assert len(reverse)==len(aliases)==1 and reverse[0][0]==aliases[0][0]==m['person_id']and _same(reverse[0][1],expected)and aliases[0][1]['surface']==m['surface']
        modern=date['references'][date['regnal_year_mapping']['reference_index']];lc=modern['local_capture'];assert Path(lc['path']).parts[0]=='sources'and Path(lc['path']).suffix=='.html';html=raw(lc['path']);assert hashlib.sha256(html).hexdigest()==lc['sha256']
        match=re.search(r'<tr\b[^>]*id=[\"\']'+re.escape(lc['row_id'])+r'[\"\'][^>]*>.*?</tr>',html.decode(),re.S);assert match
        class Text(HTMLParser):
            def __init__(self):super().__init__();self.parts=[]
            def handle_data(self,data):
                if data.strip():self.parts.append(data.strip())
        parser=Text();parser.feed(match[0]);cols=modern['columns'];assert parser.parts[-4:]==[cols['dynasty'],cols['era_name'],cols['first_year'],cols['last_year']]
        return True
    except(AssertionError,KeyError,TypeError,ValueError,IndexError,StopIteration,AttributeError,OSError):return False
