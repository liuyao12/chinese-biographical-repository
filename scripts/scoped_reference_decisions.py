"""Validate a published identity judgment whose cited tokens include contextual person references."""
def scoped_reference_decision_valid(decision, chapters):
    try:
        basis = decision['identification_basis']
        if decision['surface_usage'] != 'source_scoped_reference' or basis['kind'] != 'source_context':
            return False
        references = basis['target_reference_ids']
        named = basis.get('target_mention_ids', [])
        issued = basis['issued_target_ids']
        if not references or len(issued) != len(set(issued)) or set(issued) != set(named) | set(references) or set(named) & set(references):
            return False
        roles = basis['referent_roles_by_id']
        if set(roles) != set(references):
            return False
        selected = {}
        for cid in decision['chapter_ids']:
            chapter = chapters[cid]
            paragraphs = {p['id']: p for p in chapter['paragraphs']}
            local = {r['id']: r for r in chapter['annotation'].get('person_reference_occurrences', [])}
            for rid in references:
                if rid in local:
                    row = local[rid]
                    if row['referent_role'] != roles[rid]:
                        return False
                    selected[rid] = (cid, paragraphs[row['paragraph_id']], row)
            for p in paragraphs.values():
                for m in p['mentions']:
                    if m['id'] in named:
                        if m['kind'] != 'person':
                            return False
                        selected[m['id']] = (cid, p, m)
        if set(selected) != set(issued) or {x[2]['surface'] for x in selected.values()} != set(decision['surfaces']):
            return False
        for rid, (cid, p, row) in selected.items():
            if row['person_id'] != decision['person_id'] or p['text'][row['start']:row['end']] != row['surface']:
                return False
            local = [e for e in decision['evidence'] if e['chapter_id'] == cid and e['paragraph_id'] == p['id'] and e['source_id'] == chapters[cid]['source_id']]
            if not any(p['text'].startswith(e['quote'], i) and i <= row['start'] < row['end'] <= i + len(e['quote'])
                       for e in local for i in range(len(p['text']))):
                return False
        return True
    except (KeyError, TypeError, ValueError, IndexError):
        return False


def superseded_holdings_valid(chapter, table):
    try:
        active = {h['id'] for h in table['holdings']}
        proposals = {p['id']: p for p in chapter['annotation']['title_proposals']}
        records = table['superseded_holdings']
        if not records or len({r['id'] for r in records}) != len(records):
            return False
        for r in records:
            original, new = r['original_record'], proposals[r['replacement_id']]
            if (r['id'] in active or original['id'] != r['id'] or new['former_holding_id'] != r['id']
                    or r['replacement_type'] != 'unassumed_appointment' or new['outcome'] != 'not_assumed'
                    or new['supersedes'] != [dict(record_type='title_holding',id=r['id'],prior_mode=original['mode'],prior_status=original['status'])]
                    or not (r['person_id'] == original['person_id'] == new['person_id'])
                    or not (r['title'] == original['title'] == new['title'])
                    or not original['attestations'] or not original['effective_period'] or not original['evidence']
                    or r['source_frame'] != new['source_frame']):
                return False
            a=original['attestations'][0]
            if any(a[k] != new['role_anchor'][k] for k in ('paragraph_id','start','end','surface')):
                return False
            if not any(new['source_frame'] in e['quote'] for e in original['evidence']):
                return False
        return True
    except (KeyError, TypeError, ValueError, IndexError):
        return False
