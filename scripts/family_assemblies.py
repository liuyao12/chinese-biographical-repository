"""核對並讀取有明示證據的父系組裝；不按姓名猜測。"""
import json
from pathlib import Path
try:
    from .person_ids import family_path_errors
    from .ancestry_chain import consecutive_ancestor_parent_valid
except ImportError:
    from person_ids import family_path_errors
    from ancestry_chain import consecutive_ancestor_parent_valid


def brother_connects(assertion, first, second):
    """兄弟端點可反向核對；原斷言方向及長幼限定不改寫。"""
    a, b = assertion['subject_person_id'], assertion['object_person_id']
    return (assertion['predicate'] == 'brother'
            and assertion.get('qualifiers', {}).get('shared_father') is not False
            and not set(first).intersection(second)
            and ((a in first and b in second) or (b in first and a in second)))


def load_assemblies(root, catalog):
    path = Path(root) / 'registry/family-assemblies.json'
    if not path.exists():
        return {}, {}
    people, records = catalog
    assertions = {a['id']: a for r in records if r.get('record_type') == 'person_assertion_set' for a in r['assertions']}
    equivalences = {d['id']: d for r in records if r.get('record_type') == 'person_equivalence_set' for d in r['decisions']}
    chapters = {r['id']: r for r in records if r.get('record_type') == 'marked_chapter'}
    source_map, assembled = {}, {}
    for assembly in json.loads(path.read_text())['assemblies']:
        rows = {m['person_id']: m for m in assembly['members']}
        root_id = assembly['root_person_id']
        if root_id not in rows or rows[root_id]['parent_person_id'] is not None:
            raise ValueError('組裝家族根無效')
        for pid, member in rows.items():
            ids = set(member['source_person_ids'])
            representative = member['representative_source_person_id']
            if not ids or not ids.issubset(people) or representative not in ids:
                raise ValueError('組裝來源人物無效')
            reached = {representative}
            decisions = [equivalences[eid] for eid in member['identity_equivalence_decision_ids']]
            if any(not set(d['person_ids']).issubset(ids) for d in decisions):
                raise ValueError('組裝同指決定超出人物範圍')
            while True:
                expanded = reached | {p for d in decisions if reached.intersection(d['person_ids']) for p in d['person_ids']}
                if expanded == reached:
                    break
                reached = expanded
            if reached != ids:
                raise ValueError('組裝來源候選缺少同指證據')
            parent = member['parent_person_id']
            ancestor = member.get('ancestor_person_id')
            if ancestor is not None:
                if parent is not None or ancestor not in rows or ancestor == pid:
                    raise ValueError('缺代組裝祖先或父親欄位無效')
                connection = member.get('ancestor_connection')
                if connection:
                    if not isinstance(connection, dict):
                        raise ValueError('同父兄弟祖先組裝格式無效')
                    sibling = rows.get(connection.get('sibling_person_id'))
                    brother = assertions.get(connection.get('sibling_assertion_id'))
                    source = assertions.get(connection.get('sibling_ancestor_assertion_id'))
                    valid = (connection.get('type') == 'shared_ancestor_through_sibling'
                             and connection.get('status') == 'contextual_provisional'
                             and bool(connection.get('rationale'))
                             and member['source_assertion_id'] is None
                             and member.get('connection') in ('grandfather', 'great_grandfather')
                             and bool(sibling) and bool(brother) and bool(source)
                             and sibling.get('ancestor_person_id') == ancestor
                             and sibling.get('connection') == member.get('connection')
                             and sibling.get('generation_distance') == member.get('generation_distance')
                             and sibling.get('source_assertion_id') == source['id']
                             and brother_connects(brother, ids, sibling['source_person_ids'])
                             and source['predicate'] == member.get('connection')
                             and source['subject_person_id'] in sibling['source_person_ids']
                             and source['object_person_id'] in rows[ancestor]['source_person_ids'])
                    proofs = {a['id']: a for a in (brother, source) if a}
                    refs = connection.get('references', [])
                    valid = (valid and isinstance(refs, list) and bool(refs)
                             and all(isinstance(ref, dict) for ref in refs)
                             and {ref.get('assertion_id') for ref in refs} == set(proofs)
                             and all(ref.get('scope') and ref.get('url', '').startswith(('https://', 'http://'))
                                     and any(ref.get('quote') == e['quote']
                                             and ref.get('paragraph_id') == e['paragraph_id']
                                             and ref.get('chapter_id') == e['chapter_id']
                                             and ref.get('source_id') == e['source_id']
                                             and ref.get('url') in [chapters.get(e['chapter_id'], {}).get('source', {}).get('url'),
                                                                    chapters.get(e['chapter_id'], {}).get('source', {}).get('permalink')]
                                             for e in proofs.get(ref.get('assertion_id'), {}).get('evidence', []))
                                     for ref in refs))
                    if not valid:
                        raise ValueError('同父兄弟祖先組裝缺少有效兄弟及祖孫證據')
                else:
                    assertion = assertions.get(member['source_assertion_id'])
                    if (not assertion or assertion.get('qualifiers', {}).get('adopted_for_family_tree') is False
                        or assertion['predicate'] != member.get('connection')
                        or assertion['subject_person_id'] not in ids
                        or assertion['object_person_id'] not in rows[ancestor]['source_person_ids']):
                        raise ValueError('缺代組裝祖孫端點與來源不符')
                if family_path_errors(pid, member):
                    raise ValueError('缺代組裝 ID 與所記世代距離不符')
                if not member.get('interpretation_note'):
                    raise ValueError('缺代組裝須記明未補父親的判讀')
            elif parent is None and pid != root_id:
                raise ValueError('非根組裝人物缺少父系連接')
            if parent is not None:
                if parent not in rows or not pid.startswith(root_id + '_'):
                    raise ValueError('組裝父親不在同族')
                connection = member.get('parent_connection')
                if connection:
                    if connection.get('type') == 'parent_between_consecutive_ancestors':
                        if not consecutive_ancestor_parent_valid(member, rows, assertions, chapters):
                            raise ValueError('連續具名祖先組裝缺少相符世次及同段證據')
                    elif connection['type'] == 'shared_father_through_sibling_chain':
                        sibling_ids = connection.get('sibling_person_ids')
                        brother_ids = connection.get('sibling_assertion_ids')
                        valid = (isinstance(sibling_ids, list) and isinstance(brother_ids, list)
                                 and len(sibling_ids) >= 2 and len(sibling_ids) == len(brother_ids)
                                 and all(isinstance(x, str) for x in sibling_ids + brother_ids)
                                 and len(set([pid] + sibling_ids)) == len(sibling_ids) + 1
                                 and connection.get('status') == 'contextual_provisional'
                                 and bool(connection.get('rationale'))
                                 and member['source_assertion_id'] is None)
                        current_ids = ids
                        if valid:
                            for sibling_id, brother_id in zip(sibling_ids, brother_ids):
                                sibling = rows.get(sibling_id)
                                brother = assertions.get(brother_id)
                                valid = bool(sibling and brother
                                             and sibling.get('parent_person_id') == parent
                                             and brother_connects(brother, current_ids, sibling['source_person_ids']))
                                if not valid:
                                    break
                                current_ids = set(sibling['source_person_ids'])
                        father = assertions.get(connection.get('sibling_father_assertion_id'))
                        valid = (valid and bool(father) and father['predicate'] == 'father'
                                 and father['subject_person_id'] in current_ids
                                 and father['object_person_id'] in rows[parent]['source_person_ids'])
                        if not valid:
                            raise ValueError('同父兄弟鏈組裝缺少有效逐步證據')
                    else:
                        sibling = rows.get(connection['sibling_person_id'])
                        brother = assertions[connection['sibling_assertion_id']]
                        father = assertions[connection['sibling_father_assertion_id']]
                        if (connection['type'] != 'shared_father_through_sibling' or not sibling
                            or connection['status'] != 'contextual_provisional' or not connection['rationale']
                            or not brother_connects(brother, ids, sibling['source_person_ids'])
                            or father['predicate'] != 'father' or father['subject_person_id'] not in sibling['source_person_ids']
                            or father['object_person_id'] not in rows[parent]['source_person_ids']
                            or member['source_assertion_id'] is not None):
                            raise ValueError('同父兄弟組裝缺少有效兄弟及父親證據')
                    if not connection.get('references') or any(not ref.get('quote') or not ref.get('scope')
                        or not ref.get('url', '').startswith(('https://', 'http://')) for ref in connection['references']):
                        raise ValueError('同父兄弟組裝缺少限定及補證')
                else:
                    assertion = assertions[member['source_assertion_id']]
                    if assertion['predicate'] != 'father' or assertion['subject_person_id'] not in ids or assertion['object_person_id'] not in rows[parent]['source_person_ids']:
                        raise ValueError('組裝父子端點與來源不符')
                if family_path_errors(pid, {'connection': 'father', 'parent_person_id': parent}):
                    raise ValueError('組裝 ID 與父系世代不符')
            if pid in assembled or any(source in source_map for source in ids):
                raise ValueError('組裝人物重複')
            if pid in people and pid not in ids:
                raise ValueError('組裝 ID 與另一來源人物碰撞')
            row = dict(member, assembly_id=assembly['id'], root_person_id=root_id,
                       status=assembly['status'], human_reviewed=assembly['human_reviewed'])
            assembled[pid] = row
            for source in ids:
                source_map[source] = row
    return source_map, assembled
