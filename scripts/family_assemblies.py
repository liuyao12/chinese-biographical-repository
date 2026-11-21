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
    """兄弟姊妹端點可反向核對；父系仍為明示可撤回的編輯推導。"""
    a, b = assertion['subject_person_id'], assertion['object_person_id']
    return (assertion['predicate'] in ('brother', 'sister')
            and assertion.get('qualifiers', {}).get('shared_father') is not False
            and not set(first).intersection(second)
            and ((a in first and b in second) or (b in first and a in second)))


def registry_sibling_path_valid(person_id, path, assertions):
    """現役 ID 的暫定父系可由具名兄弟與其中一人的明父逐步繫證。"""
    proof = path.get('parent_connection', {})
    if not isinstance(proof, dict):
        return False
    siblings = proof.get('sibling_assertion_ids')
    if (proof.get('type') != 'shared_father_through_siblings'
            or path.get('connection') != 'father' or path.get('source_assertion_id') is not None
            or not isinstance(siblings, list) or not siblings
            or not all(isinstance(a, str) for a in siblings)
            or len(set(siblings)) != len(siblings)):
        return False
    current = person_id
    seen = {current}
    for aid in siblings:
        a = assertions.get(aid)
        if not a or a.get('qualifiers', {}).get('adopted_for_family_tree') is False:
            return False
        other = a['object_person_id'] if a['subject_person_id'] == current else a['subject_person_id']
        if other in seen or not brother_connects(a, {current}, {other}):
            return False
        seen.add(other)
        current = other
    father_id = proof.get('sibling_father_assertion_id')
    if not isinstance(father_id, str):
        return False
    father = assertions.get(father_id)
    if (not father or father['predicate'] != 'father' or father['subject_person_id'] != current
            or father['object_person_id'] != path['parent_person_id'] or father['object_person_id'] in seen
            or father.get('qualifiers', {}).get('adopted_for_family_tree') is False
            or father.get('qualifiers', {}).get('lineage') == 'maternal'):
        return False
    needed = set(siblings + [father_id])
    cited = set()
    for e in path.get('evidence', []):
        aid = e.get('source_assertion_id')
        if aid not in needed:
            return False
        a = assertions[aid]
        if (e.get('source_term') != a['qualifiers'].get('source_term')
                or not any(all(ref.get(k) == e.get(k) for k in ('chapter_id', 'source_id', 'paragraph_id'))
                           and ref['quote'] in e['quote'] for ref in a['evidence'])):
            return False
        cited.add(aid)
    return cited == needed


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
        if assembly.get('schema_mode') == 'personless_namespace':
            try:
                from .personless_namespace import namespace_members
            except ImportError:
                from personless_namespace import namespace_members
            if any(row.get('namespace_id') == assembly.get('namespace_id') for row in assembled.values()):
                raise ValueError('Namespace reused by another assembly')
            namespace_rows = namespace_members(assembly, people, assertions, chapters)
            if any(pid in assembled or source in source_map for pid, row in namespace_rows.items() for source in row['source_person_ids']):
                raise ValueError('Namespace member already assembled')
            for pid, row in namespace_rows.items():
                assembled[pid] = row
                for source in row['source_person_ids']: source_map[source] = row
            continue
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
                if isinstance(connection, dict) and connection.get('type') == 'wyd_song044_paternal_nephew_to_uncle_father':
                    try:
                        from scripts.wyd_song044_nephew import ancestor_valid as wyd_nephew_ancestor_valid
                    except ImportError:
                        from wyd_song044_nephew import ancestor_valid as wyd_nephew_ancestor_valid
                    if not wyd_nephew_ancestor_valid(member, rows, assertions, chapters, root):
                        raise ValueError('宋044兄子缺父祖連須有固定叔侄與明父來源；不得造父、倒向或改母嗣系')
                elif connection:
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
                             and source.get('qualifiers', {}).get('lineage') != 'maternal'
                             and source.get('qualifiers', {}).get('adopted_for_family_tree') is not False
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
                        or assertion.get('qualifiers', {}).get('lineage') == 'maternal'
                        or assertion['predicate'] != member.get('connection')
                        or (assertion['predicate'] == 'ancestor'
                            and assertion.get('qualifiers', {}).get('generation_distance') != member.get('generation_distance'))
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
                        if not consecutive_ancestor_parent_valid(member, rows, assertions, chapters, root=root):
                            raise ValueError('連續具名祖先組裝缺少相符世次及同段證據')
                    elif connection.get('type') == 'parent_between_body_and_attached_note_ancestors':
                        try:
                            from .body_note_ancestry import body_note_ancestor_parent_valid
                        except ImportError:
                            from body_note_ancestry import body_note_ancestor_parent_valid
                        if not body_note_ancestor_parent_valid(member, rows, assertions, chapters, root):
                            raise ValueError('正文與所附裴注祖先接合須有同一人物單元及逐字雙來源，不能補造明父')
                    elif connection.get('type') == 'parent_through_paternal_uncle':
                        try:
                            from .uncle_parentage import parent_through_paternal_uncle_valid
                        except ImportError:
                            from uncle_parentage import parent_through_paternal_uncle_valid
                        if not parent_through_paternal_uncle_valid(member, rows, assertions, chapters):
                            raise ValueError('叔父接合須有侄之父、叔父及叔父之父的具名正文，不得拿數位標題補父系')
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
