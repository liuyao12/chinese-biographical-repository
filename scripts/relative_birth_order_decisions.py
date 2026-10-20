"""Keep conflicting witnessed sibling order separate from preferred ordering."""
from pathlib import Path
import copy
import hashlib
import re


def decision_errors(root, chapters, assertions, person_ids):
    errors = []
    seen = set()
    targets = set()
    for chapter in chapters.values():
        paragraphs = {p['id']: p for p in chapter['paragraphs']}
        for decision in chapter.get('annotation', {}).get('relative_birth_order_decisions', []):
            try:
                assert set(decision) == {'id', 'assertion_id', 'person_ids', 'source_mention_ids', 'source_term', 'claims', 'preferred_claim_id', 'rationale', 'reviewer', 'human_reviewed', 'status'}
                assert decision['id'] not in seen and decision['assertion_id'] not in targets
                seen.add(decision['id']); targets.add(decision['assertion_id'])
                a = assertions[decision['assertion_id']]
                pair = {a['subject_person_id'], a['object_person_id']}
                assert a['predicate'] == 'brother' and len(pair) == 2
                assert set(decision['person_ids']) == pair and len(decision['person_ids']) == 2 and pair <= person_ids
                assert decision['status'] == 'interpretation_disputed' and decision['human_reviewed'] is False
                assert decision['preferred_claim_id'] is None and decision['rationale'] and decision['reviewer'] and decision['source_term']
                assert len(decision['claims']) == 2 and len({c['id'] for c in decision['claims']}) == 2
                local = {m['id']: (p, m) for p in paragraphs.values() for m in p['mentions']}
                assert len(decision['source_mention_ids']) == 2
                hits = [local[mid] for mid in decision['source_mention_ids']]
                assert len({p['id'] for p, _ in hits}) == 1 and {m['person_id'] for _, m in hits} == pair
                assert decision['source_term'] in hits[0][0]['text']
                assert {c['witness']['syntax'] for c in decision['claims']} == {'older_cidi_younger', 'younger_older_zhidiye'}
                directions = []
                for claim in decision['claims']:
                    assert set(claim) == {'id', 'older_person_id', 'younger_person_id', 'witness'}
                    assert {claim['older_person_id'], claim['younger_person_id']} == pair
                    directions.append((claim['older_person_id'], claim['younger_person_id']))
                    witness = claim['witness']
                    assert set(witness) == {'path', 'sha256', 'fixed_url', 'revision_id', 'raw_line_range', 'quote', 'start', 'end', 'older_span', 'younger_span', 'syntax'}
                    assert len(witness['revision_id']) == 40 and witness['revision_id'] in witness['fixed_url']
                    assert witness['fixed_url'].startswith('https://')
                    path = Path(witness['path'])
                    assert not path.is_absolute() and '..' not in path.parts and path.parts[0] in ('sources', 'source-evidence')
                    raw = (Path(root) / path).read_bytes()
                    assert hashlib.sha256(raw).hexdigest() == witness['sha256']
                    lines = raw.decode('utf-8').splitlines()
                    first, last = witness['raw_line_range']
                    assert type(first) is int and type(last) is int and 1 <= first <= last <= len(lines)
                    line = re.sub(r'<pb:[^>]*>|[\s¶]', '', '\n'.join(lines[first - 1:last]))
                    assert type(witness['start']) is int and 0 <= witness['start'] < witness['end'] <= len(line)
                    assert line[witness['start']:witness['end']] == witness['quote']
                    for key in ('older_span', 'younger_span'):
                        s = witness[key]
                        assert set(s) == {'start', 'end', 'surface'}
                        assert 0 <= s['start'] < s['end'] <= len(witness['quote'])
                        assert witness['quote'][s['start']:s['end']] == s['surface']
                    assert witness['older_span'] != witness['younger_span']
                    older = witness['older_span']['surface']; younger = witness['younger_span']['surface']
                    if witness['syntax'] == 'older_cidi_younger':
                        assert witness['quote'] == older + '次弟' + younger
                        assert witness['older_span']['start'] == 0 and witness['younger_span']['start'] == len(older) + 2
                        assert witness['path'] == chapter['source']['raw_path'] and witness['sha256'] == chapter['source']['raw_file_sha256']
                        assert [(m['person_id'], m['surface']) for _, m in hits] == [(claim['older_person_id'], older), (claim['younger_person_id'], younger)]
                        assert witness['quote'] == decision['source_term']
                    elif witness['syntax'] == 'younger_older_zhidiye':
                        assert witness['quote'] == younger + older + '之弟也'
                        assert witness['younger_span']['start'] == 0 and witness['older_span']['start'] == len(younger)
                    else:
                        raise ValueError('Unsupported witnessed order syntax')
                assert directions[0] == directions[1][::-1]
                order = a['qualifiers']['relative_birth_order']
                assert order['scope'] == 'siblings' and order['operator'] == 'lt'
                assert (order['older_person_id'], order['younger_person_id']) in directions
                assert any(e['chapter_id'] == chapter['id'] and e['paragraph_id'] == hits[0][0]['id'] and e['quote'] == hits[0][0]['text'] for e in a['evidence'])
            except (AssertionError, KeyError, IndexError, TypeError, ValueError, OSError):
                errors.append('長幼分歧判讀須匹配兄弟原斷言、雙端錨點及兩份相反固定原證：' + str(decision.get('id')))
    return errors


def relevant_decisions(chapters, person_ids):
    return [dict(copy.deepcopy(d), chapter_id=c['id'], source_id=c['source_id'])
            for c in chapters.values() for d in c.get('annotation', {}).get('relative_birth_order_decisions', [])
            if person_ids.intersection(d['person_ids'])]


def preferred_relation(assertion, decisions):
    result = copy.deepcopy(assertion)
    d = next((d for d in decisions if d['assertion_id'] == assertion['id']), None)
    if d is not None:
        if d['preferred_claim_id'] is not None:
            raise ValueError('This narrow model supports only unresolved witnessed sibling order')
        result['qualifiers'].pop('relative_birth_order', None)
        result['relative_birth_order_decision_id'] = d['id']
    return result
