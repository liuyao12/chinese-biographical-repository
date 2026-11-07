"""核對完整連續傳文中的子嗣承接；不以遠段或補字代替證據。"""
import hashlib
import re


def digital_paratext_errors(chapter):
    """只允許另存的空行與數位節題；不能藉此略去傳文。"""
    errors = []
    records = chapter.get('source', {}).get('normalization', {}).get('omitted_digital_paratext', [])
    if not isinstance(records, list):
        return ['數位節題記錄須為列表']
    occupied = set()
    for record in records:
        if not isinstance(record, dict):
            errors.append('數位節題記錄須為物件'); continue
        span, raw = record.get('source_lines'), record.get('raw_quote')
        valid = (isinstance(span, list) and len(span) == 2
                 and all(type(n) is int and n > 0 for n in span)
                 and span[0] <= span[1] and isinstance(raw, str)
                 and record.get('kind') == 'digital_section_heading'
                 and record.get('not_received_text') is True
                 and record.get('source_revision') == chapter.get('source', {}).get('revision_id'))
        if valid:
            lines = raw.split('\n')
            nonblank = [line.strip() for line in lines if line.strip()]
            valid = (len(lines) == span[1] - span[0] + 1 and bool(nonblank)
                     and all(re.fullmatch(r'(?P<marks>={2,6})[^=\n]+(?P=marks)', line) for line in nonblank)
                     and hashlib.sha256(raw.encode()).hexdigest() == record.get('raw_quote_sha256')
                     and not occupied.intersection(range(span[0], span[1] + 1)))
            if valid:
                for para in chapter.get('paragraphs', []):
                    position = para.get('source_position', {})
                    first, last = position.get('first_line'), position.get('last_line')
                    if type(first) is int and type(last) is int and first <= span[1] and span[0] <= last:
                        valid = False
                occupied.update(range(span[0], span[1] + 1))
        if not valid:
            errors.append('數位節題須有相符固定版本、原行雜湊與純節題文字，不得混入或略去正文')
    return errors


def received_paragraphs_contiguous(chapter, first, second):
    a, b = first.get('source_position', {}), second.get('source_position', {})
    end, start = a.get('last_line'), b.get('first_line')
    if type(end) is not int or type(start) is not int or start <= end:
        return False
    if end + 1 == start:
        return True
    if digital_paratext_errors(chapter):
        return False
    try:
        from .subject_continuation import verified_blank_gap
    except ImportError:
        from subject_continuation import verified_blank_gap
    if verified_blank_gap(chapter, a, b):
        return True
    records = chapter.get('source', {}).get('normalization', {}).get('omitted_digital_paratext', [])
    spans = sorted(record['source_lines'] for record in records
                   if end < record['source_lines'][0] and record['source_lines'][1] < start)
    cursor = end + 1
    for left, right in spans:
        if left != cursor:
            return False
        cursor = right + 1
    return cursor == start

def child_continuation_errors(assertion, chapter, root=None):
    if isinstance(assertion, dict) and isinstance(assertion.get('context'), dict) and isinstance(assertion['context'].get('source_continuity'), dict) and assertion['context']['source_continuity'].get('kind') == 'editorial_received_subject_parentage':
        return editorial_received_parentage_errors(assertion, chapter, root)
    if isinstance(assertion, dict) and isinstance(assertion.get("context"), dict) and isinstance(assertion["context"].get("source_continuity"), dict) and assertion["context"]["source_continuity"].get("kind") == "fixed_received_raw_natural_paragraphs":
        return natural_parentage_errors(assertion, chapter, root)
    if 'secondary_child_clause' in assertion.get('context', {}):
        try:
            from scripts.continued_biography_family import children_errors
        except ImportError:
            from continued_biography_family import children_errors
        return children_errors(assertion, chapter)

    errors = []
    context = assertion.get('context', {})
    ids = context.get('paragraph_ids')
    paras = chapter.get('paragraphs', [])
    order = [p['id'] for p in paras]
    byid = {p['id']: p for p in paras}
    evidence = assertion.get('evidence', [])
    valid = (context.get('kind') == 'biographical_child_continuation'
             and assertion.get('predicate') == 'father'
             and isinstance(ids, list) and len(ids) >= 2
             and all(isinstance(i, str) and i in order for i in ids)
             and len(set(ids)) == len(ids)
             and bool(context.get('rationale'))
             and context.get('status') == 'contextual_provisional'
             and context.get('human_reviewed') is False
             and ids == [e.get('paragraph_id') for e in evidence])
    if valid:
        valid = ids == order[order.index(ids[0]):order.index(ids[-1]) + 1]
    if valid:
        for pid, e in zip(ids, evidence):
            p = byid[pid]
            position = p.get('source_position', {})
            valid &= (e.get('chapter_id') == chapter.get('id')
                      and e.get('source_id') == chapter.get('source_id')
                      and e.get('quote') == p.get('text')
                      and p.get('text_layer') == 'received_chapter'
                      and position.get('editorial_excerpt_boundary') is True
                      and type(position.get('first_line')) is int
                      and type(position.get('last_line')) is int
                      and position['first_line'] <= position['last_line']
                      and position.get('revision_id') == chapter.get('source', {}).get('revision_id'))
        if valid:
            for a, b in zip(ids, ids[1:]):
                valid &= received_paragraphs_contiguous(chapter, byid[a], byid[b])
    if not valid:
        return ['傳主子嗣承接須保留同一固定見證的完整連續原段、原行與判讀']
    anchor = next((m for m in byid[ids[0]].get('mentions', [])
                   if m.get('id') == context.get('parent_mention_id')), None)
    child = next((m for m in byid[ids[-1]].get('mentions', [])
                  if m.get('id') == context.get('child_mention_id')), None)
    if (not anchor or anchor.get('kind') != 'person'
            or anchor.get('person_id') != assertion.get('object_person_id')
            or not child or child.get('kind') != 'person'
            or child.get('person_id') != assertion.get('subject_person_id')
            or child.get('start') != 1 or not byid[ids[-1]]['text'].startswith('子')
            or assertion.get('qualifiers', {}).get('source_term') != '子'
            or assertion.get('qualifiers', {}).get('lineage') != 'paternal'):
        errors.append('傳主子嗣承接的父名錨點或段首子某錨點不符')
    return errors

# Opt-in natural received paragraphs; older excerpt contracts remain unchanged.
def natural_parentage_context(assertion, chapter, root):
    from pathlib import Path
    import json, hashlib
    if not isinstance(assertion, dict) or not isinstance(chapter, dict) or root is None:
        raise ValueError('Natural parentage needs a fixed physical source root')
    q=assertion['qualifiers'];ctx=assertion.get('context',{});binding=q.get('source_clause_binding',{})
    ref=(ctx.get('source_continuity',{}).get('fixed_witness_reference')
         if ctx.get('kind')=='biographical_child_continuation' else binding.get('fixed_witness_reference'))
    if not isinstance(ref,dict)or set(ref)!={'path','sha256'} or ref.get('path')!='source-evidence/jin043-wangyan-family/fixed-natural-units.json' or ref.get('sha256')!='ccb8afd52371a3a5c129c44eedf5c6fbe83d0f2e27a1f7639a22d4d222677f54':raise ValueError('Natural parentage source reference')
    root=Path(root).resolve();rel=Path(ref['path']);path=root/rel
    if rel.is_absolute()or '..'in rel.parts or rel.parts[0]!='source-evidence'or path.resolve()!=path:raise ValueError('Natural source path boundary')
    rb=path.read_bytes()
    if hashlib.sha256(rb).hexdigest()!=ref['sha256']:raise ValueError('Natural source contract drift')
    spec=json.loads(rb);c=chapter;s=c['source']
    if any(spec[k]!=c[k]for k in ('chapter_id','work_id','book_id','source_id')if k!='chapter_id')or spec['chapter_id']!=c['id']or spec['source_revision']!=s['revision_id']:raise ValueError('Natural source identity')
    rawrel=Path(spec['raw_file']);rawpath=root/rawrel
    if rawrel.is_absolute()or '..'in rawrel.parts or rawrel.parts[0]!='sources'or rawpath.resolve()!=rawpath:raise ValueError('Natural raw path boundary')
    raw=rawpath.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=spec['raw_sha256']or spec['raw_sha256']!=s['wikitext_sha256']or spec['raw_file']!=s['raw_file']:raise ValueError('Natural raw drift')
    lines=raw.decode().splitlines();units=[dict(paragraph_id=p['id'],text=p['text'],text_layer=p['text_layer'],source_position=p['source_position'])for p in c['paragraphs']]
    if units!=spec['units']:raise ValueError('Natural complete unit changed')
    last=None
    for p in c['paragraphs']:
        pos=p['source_position'];lo,hi=pos['first_line'],pos['last_line']
        if type(lo)is not int or lo!=hi or pos['revision_id']!=s['revision_id']or p['text_layer']!='received_chapter':raise ValueError('Not a complete received natural paragraph')
        if last is not None and(any(x.strip()for x in lines[last:lo-1])or lo<=last):raise ValueError('Prose/title omitted between natural paragraphs')
        last=hi
    roles={}
    for key,loc in spec['roles'].items():
        p=next(p for p in c['paragraphs']if p['id']==loc['paragraph_id']);m,=[m for m in p['mentions']if m['id']==loc['mention_id']]
        if lines[p['source_position']['first_line']-1].strip()!=p['text']:raise ValueError('Role paragraph must be literal raw')
        if m['kind']!='person'or any(m[k]!=loc[k]for k in ('start','end','surface'))or p['text'][m['start']:m['end']]!=m['surface']:raise ValueError('Natural source role drift')
        people=json.loads((root/'registry/persons.json').read_text())['persons']
        person,=[x for x in people if x['id']==m['person_id']]
        if not any(e.get('mention_id')==m['id'] and e.get('paragraph_id')==p['id'] for e in person['evidence']):raise ValueError('Natural inverse role mismatch')
        roles[key]=(p,m)
    return spec,roles


def natural_parentage_errors(a,ch,root):
    try:
        spec,r=natural_parentage_context(a,ch,root);q=a['qualifiers'];ctx=a.get('context',{});b=q.get('source_clause_binding',{})
        hp,head=r['head'];fp,father=r['father'];rp,resumed=r['resumed'];cp,child=r['child']
        if(len({head['person_id'],father['person_id'],child['person_id']})!=3 or a['predicate']!='father'or a['status']!='source_attested'or a['human_reviewed']is not False or head['start']!=0 or not hp['text'].startswith(head['surface']+'字')or hp['id']!=ch['paragraphs'][0]['id']or head['person_id']!=resumed['person_id']):raise ValueError('Natural biography topic')
        def ev(p):return dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=ch['id'],paragraph_id=p['id'],quote=p['text'])
        if b.get('rule')=='natural_received_head_father':
            if set(q)!={'source_term','lineage','source_clause_binding'}or q['lineage']!='paternal'or q['source_term']!='父'+father['surface']or set(b)!={'kind','rule','head_mention_id','father_mention_id','fixed_witness_reference'}or b['kind']!='biography_family_clause'or b['head_mention_id']!=head['id']or b['father_mention_id']!=father['id']or fp['id']!=hp['id']or a['subject_person_id']!=head['person_id']or a['object_person_id']!=father['person_id']:raise ValueError('Natural named father endpoints')
            text=hp['text'];prefix=text[:father['start']-1]
            if text[father['start']-1:father['end']]!=q['source_term']or prefix.count('「')!=prefix.count('」')or prefix.count('『')!=prefix.count('』'):raise ValueError('Father term is quoted or absent')
            e=ev(hp);e.update(subject_person_mention_id=head['id'],object_person_mention_id=father['id'])
            if a['evidence']!=[e]:raise ValueError('Natural father full evidence')
        else:
            if set(q)!={'source_term','lineage'}or q!={'source_term':'子','lineage':'paternal'}or ctx.get('kind')!='biographical_child_continuation'or set(ctx)!={'kind','paragraph_ids','parent_mention_id','child_mention_id','status','human_reviewed','rationale','source_continuity'}or ctx['source_continuity'].get('kind')!='fixed_received_raw_natural_paragraphs'or set(ctx['source_continuity'])!={'kind','fixed_witness_reference'}or ctx['status']!='contextual_provisional'or ctx['human_reviewed']is not False or not ctx['rationale']:raise ValueError('Natural adjacent child format')
            order=[p['id']for p in ch['paragraphs']]
            if(order.index(cp['id'])!=order.index(rp['id'])+1 or ctx['paragraph_ids']!=[rp['id'],cp['id']]or ctx['parent_mention_id']!=resumed['id']or ctx['child_mention_id']!=child['id']or resumed['start']!=0 or child['start']!=1 or not cp['text'].startswith('子'+child['surface']+'，字')or a['subject_person_id']!=child['person_id']or a['object_person_id']!=head['person_id']):raise ValueError('Natural child topic/son position')
            e1,e2=ev(rp),ev(cp);e1['object_person_mention_id']=resumed['id'];e2['subject_person_mention_id']=child['id']
            if a['evidence']!=[e1,e2]:raise ValueError('Natural child evidence')
        return []
    except(KeyError,TypeError,ValueError,IndexError,StopIteration,AttributeError,OSError):
        return ['自然段父子須綁完整固定raw、真空行、傳首及續述同父錨、段首子錨；不借旁人或換題']


def editorial_received_parentage_errors(assertion, chapter, root):
    """Validate an explicit editor's subject continuation, not historical NLU.

    Entire intervening paragraphs and their observed acquisition frames remain
    physical inputs. The parent marker is never manufactured in the child list.
    """
    try:
        from scripts.surname_source_frames import source_view, same, read, at
    except ImportError:
        from surname_source_frames import source_view, same, read, at
    try:
        ctx = assertion['context']; binding = ctx['source_continuity']
        ids = ctx['paragraph_ids']; evidence = assertion['evidence']
        if (root is None or ctx.get('kind') != 'biographical_child_continuation'
                or ctx.get('status') != 'contextual_provisional'
                or ctx.get('human_reviewed') is not False
                or not isinstance(ctx.get('rationale'), str) or not ctx['rationale'].strip()
                or assertion.get('predicate') != 'father'
                or assertion.get('status') != 'source_attested'
                or assertion.get('human_reviewed') is not False
                or set(binding) not in ({'kind', 'frames', 'parentage_clause', 'source_positions'},
                                        {'kind', 'frames', 'parentage_list', 'source_positions'})
                or binding['kind'] != 'editorial_received_subject_parentage'
                or type(ids) is not list or len(ids) < 2 or len(set(ids)) != len(ids)
                or ids != [e.get('paragraph_id') for e in evidence]):
            raise ValueError('Explicit editor/context/evidence shape')
        order = [p['id'] for p in chapter['paragraphs']]
        if ids != order[order.index(ids[0]):order.index(ids[-1]) + 1]:
            raise ValueError('All intervening paragraphs are required')
        frames = binding['frames']
        if type(frames) is not list or [f['paragraph_id'] for f in frames] != ids:
            raise ValueError('One exact source frame per paragraph')
        ps, cs, people, marker, anchor, existing = source_view(
            frames, {chapter['id']: chapter}, [], root)
        selected = [ps[i][1] for i in ids]
        revision = chapter['source']['revision_id']
        positions = binding['source_positions']
        if type(positions) is not list or [p['paragraph_id'] for p in positions] != ids:
            raise ValueError('Capture-bound source positions')
        import json
        for p, e, f, position_ref in zip(selected, evidence, frames, positions):
            if set(position_ref) != {'paragraph_id','first_line_pointer','last_line_pointer'}:
                raise ValueError('Capture position pointer shape')
            captured = json.loads(read(root, f['capture_path']))
            pos = p.get('source_position', {})
            if (p.get('text_layer') != 'received_chapter'
                    or pos.get('editorial_excerpt_boundary') is not True
                    or not same(at(captured, position_ref['first_line_pointer']), pos.get('first_line'))
                    or not same(at(captured, position_ref['last_line_pointer']), pos.get('last_line'))
                    or not same(pos.get('revision_id'), revision)
                    or type(pos.get('first_line')) is not int
                    or type(pos.get('last_line')) is not int
                    or not 0 < pos['first_line'] <= pos['last_line']
                    or any(e.get(k) != chapter[k] for k in ('work_id','book_id','source_id'))
                    or e.get('chapter_id') != chapter['id']
                    or e.get('quote') != p['text']):
                raise ValueError('Whole received paragraph/source identity')
        if any(not received_paragraphs_contiguous(chapter, a, b)
               for a, b in zip(selected, selected[1:])):
            raise ValueError('Observed source continuity may not omit prose')
        _, first, parent = marker(ids[0], ctx['parent_mention_id'])
        _, last, child = marker(ids[-1], ctx['child_mention_id'])
        if (parent['person_id'] != assertion['object_person_id']
                or child['person_id'] != assertion['subject_person_id']
                or parent['person_id'] == child['person_id']):
            raise ValueError('Actual distinct parent/child roles')
        if 'parentage_list' in binding:
            return editorial_parentage_list_errors(assertion, last, parent, child, marker, anchor)
        clause = binding['parentage_clause']; anchor(clause)
        term = assertion['qualifiers'].get('source_term')
        if (clause['paragraph_id'] != last['id']
                or term not in ('子', '長子', '次子', '少子')
                or assertion['qualifiers'].get('lineage') != 'paternal'
                or clause['surface'] != term + child['surface']
                or clause['start'] + len(term) != child['start']
                or clause['end'] != child['end']
                or clause['start'] > 0 and last['text'][clause['start']-1] not in '。；，：'):
            raise ValueError('Exact selected kin term and named child')
        birth = assertion['qualifiers'].get('birth_order')
        if birth is not None:
            ordinal = {'長子': 1, '次子': 2}.get(term)
            if (ordinal is None or type(birth) is not dict
                    or type(birth.get('ordinal')) is not int or birth['ordinal'] != ordinal
                    or birth.get('parent_person_id') != parent['person_id']
                    or birth.get('scope') != 'sons_of_parent'
                    or birth.get('position') != ('eldest' if ordinal == 1 else 'unspecified')
                    or birth.get('interpretation_status') != 'source_attested'):
                raise ValueError('Source-reported ordinal, not list order')
        return []
    except (AssertionError, KeyError, TypeError, ValueError, IndexError, StopIteration, OSError):
        return ['編者傳主親屬承接須有完整連續原段、取得資格、真實父子錨與反查及所選親屬詞；不以schema證明歷史同指']


def editorial_parentage_list_errors(assertion, paragraph, parent, child, marker, anchor):
    """Check source-bound list membership; AI, not this function, reads the list."""
    try:
        listing = assertion['context']['source_continuity']['parentage_list']
        if set(listing) != {'kind','scope_anchor','members'} or listing['kind'] != 'editorial_source_named_children_list':
            raise ValueError('Explicit list binding')
        scope = listing['scope_anchor']; anchor(scope)
        members = listing['members']
        if (scope['paragraph_id'] != paragraph['id'] or type(members) is not list
                or not members or len({m['child_mention_id'] for m in members}) != len(members)):
            raise ValueError('One complete scoped list')
        selected = None; prior_end = scope['start']; child_ids = set(); explicit = 0
        for member in members:
            if set(member) != {'child_mention_id','kinship_term_anchor','intervening_office_anchor'}:
                raise ValueError('Typed list member')
            _, _, m = marker(paragraph['id'], member['child_mention_id'])
            if (not prior_end <= m['start'] < m['end'] <= scope['end']
                    or m['person_id'] in child_ids or m['person_id'] == parent['person_id']):
                raise ValueError('Distinct ordered source children')
            prior_end = m['end']; child_ids.add(m['person_id'])
            term, office = member['kinship_term_anchor'], member['intervening_office_anchor']
            if term is not None:
                anchor(term)
                if (term['paragraph_id'] != paragraph['id']
                        or term['surface'] not in ('子','長子','次子','少子')
                        or not scope['start'] <= term['start'] < term['end'] <= m['start']):
                    raise ValueError('Literal selected parentage term')
                explicit += 1
                if office is None:
                    if term['end'] != m['start']:raise ValueError('No omitted office gap')
                else:
                    anchor(office)
                    if (office['paragraph_id'] != paragraph['id'] or office['start'] != term['end']
                            or office['end'] != m['start']
                            or any(c in office['surface'] for c in '。；，：「」『』')):
                        raise ValueError('Exact intervening office, not a fabricated name')
            elif office is not None or not explicit:
                raise ValueError('Implicit members follow an explicit source child expression')
            if m['id'] == child['id']:selected = member
        if selected is None or not explicit:
            raise ValueError('Selected child belongs to this list')
        # A title/name may occur more than once, but no unaccounted person may
        # be silently converted into a child by the list's broad text span.
        for m in paragraph['mentions']:
            if m.get('kind') == 'person' and m['start'] < scope['end'] and scope['start'] < m['end']:
                marker(paragraph['id'], m['id'])
                if m['person_id'] not in child_ids or not scope['start'] <= m['start'] < m['end'] <= scope['end']:
                    raise ValueError('Foreign person in selected children list')
        q = assertion['qualifiers']; term = selected['kinship_term_anchor']
        if q.get('lineage') != 'paternal' or q.get('source_term') != (term['surface'] if term else scope['surface']):
            raise ValueError('Preserve original term or complete implicit list, never invented 子')
        birth = q.get('birth_order')
        if birth is not None:
            ordinal = {'長子':1,'次子':2}.get(term['surface']) if term else None
            if (ordinal is None or type(birth) is not dict or type(birth.get('ordinal')) is not int
                    or birth['ordinal'] != ordinal or birth.get('parent_person_id') != parent['person_id']
                    or birth.get('scope') != 'sons_of_parent'
                    or birth.get('position') != ('eldest' if ordinal == 1 else 'unspecified')
                    or birth.get('interpretation_status') != 'source_attested'):
                raise ValueError('No ordinal inferred from remaining list position')
        return []
    except (AssertionError,KeyError,TypeError,ValueError,IndexError,StopIteration,OSError):
        return ['編者子名單承接須保存真子名錨、原有子詞／官職間隔及完整名單範圍；省略子詞者不補字或排行']
