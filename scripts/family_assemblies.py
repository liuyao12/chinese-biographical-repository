"""核對並讀取有明示證據的父系組裝；不按姓名猜測。"""
import json
from pathlib import Path
try:
    from .person_ids import family_path_errors
except ImportError:
    from person_ids import family_path_errors


def load_assemblies(root, catalog):
    path = Path(root) / 'registry/family-assemblies.json'
    if not path.exists():
        return {}, {}
    people, records = catalog
    assertions = {a['id']: a for r in records if r.get('record_type') == 'person_assertion_set' for a in r['assertions']}
    equivalences = {d['id']: d for r in records if r.get('record_type') == 'person_equivalence_set' for d in r['decisions']}
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
            if parent is not None:
                if parent not in rows or not pid.startswith(root_id + '_'):
                    raise ValueError('組裝父親不在同族')
                connection = member.get('parent_connection')
                if connection:
                    sibling = rows.get(connection['sibling_person_id'])
                    brother = assertions[connection['sibling_assertion_id']]
                    father = assertions[connection['sibling_father_assertion_id']]
                    if (connection['type'] != 'shared_father_through_sibling' or not sibling
                        or connection['status'] != 'contextual_provisional' or not connection['rationale']
                        or brother['predicate'] != 'brother' or brother['subject_person_id'] not in ids
                        or brother['object_person_id'] not in sibling['source_person_ids']
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
