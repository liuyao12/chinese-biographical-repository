"""Personless family-network overlays; these group people without inventing ancestry."""
import json
from pathlib import Path


def load_networks(root, catalog, source_map, assembled):
    """Validate network overlays and expand only cited branches and known descendants."""
    path = Path(root) / 'registry/family-networks.json'
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding='utf-8'))
    if set(data) != {'format_version', 'record_type', 'networks'} or data.get('record_type') != 'agnatic_family_network_set':
        raise ValueError('父系親族網絡索引格式無效')
    people, records = catalog
    assertions = {a['id']: a for r in records if r.get('record_type') == 'person_assertion_set' for a in r['assertions']}
    networks = []
    seen_network_ids = set()
    for network in data['networks']:
        required = {'id', 'type', 'status', 'human_reviewed', 'label', 'grouping_only',
                    'common_ancestor_person_id', 'generation_distance', 'branches',
                    'relation_assertion_ids', 'rationale'}
        if set(network) != required:
            raise ValueError('父系網絡欄位無效')
        if (not isinstance(network['id'], str) or not network['id'].startswith('fn-')
                or network['id'] in people or network['id'] in seen_network_ids
                or network['type'] != 'agnatic_cousin_network'
                or network['status'] != 'contextual_provisional'
                or network['human_reviewed'] is not False or network['grouping_only'] is not True
                or network['common_ancestor_person_id'] is not None
                or network['generation_distance'] is not None or not network['rationale']):
            raise ValueError('親族網絡必須是無人物身份、無共同祖先／世距的暫定分組')
        seen_network_ids.add(network['id'])
        branch_ids, branch_members, all_members = set(), {}, set()
        for branch in network['branches']:
            if set(branch) != {'id', 'label', 'entry_person_id', 'assembly_id', 'descendant_rule'}:
                raise ValueError('父系網絡分支欄位無效')
            if (branch['id'] in branch_ids or branch['entry_person_id'] not in people
                    or not branch['label']):
                raise ValueError('父系網絡分支身份無效')
            branch_ids.add(branch['id'])
            if branch['assembly_id']:
                members = {source for pid, row in assembled.items()
                           if row.get('assembly_id') == branch['assembly_id']
                           for source in row['source_person_ids']}
                if not members or branch['entry_person_id'] not in members:
                    raise ValueError('父系網絡引用的既有家族組裝不存在或未含分支人物')
                if branch['descendant_rule'] != 'existing_family_assembly':
                    raise ValueError('既有家族分支規則無效')
            else:
                if branch['descendant_rule'] != 'source_attested_paternal_father_assertions':
                    raise ValueError('人物分支只可沿用明示父系斷言')
                members = {branch['entry_person_id']}
                frontier = {branch['entry_person_id']}
                while frontier:
                    children = {a['subject_person_id'] for a in assertions.values()
                                if a.get('predicate') == 'father' and a.get('status') == 'source_attested'
                                and a.get('qualifiers', {}).get('lineage') == 'paternal'
                                and a.get('qualifiers', {}).get('adopted_for_family_tree') is not False
                                and a.get('object_person_id') in frontier}
                    frontier = children - members
                    if not frontier.issubset(people):
                        raise ValueError('父系網絡遇到未登錄的來源人物')
                    members.update(frontier)
            if not members.issubset(people) or all_members.intersection(members):
                raise ValueError('父系網絡分支重疊或含未登錄人物')
            all_members.update(members)
            branch_members[branch['id']] = members
        if len(branch_ids) < 2:
            raise ValueError('父系網絡需有多個分支')
        relations = []
        for assertion_id in network['relation_assertion_ids']:
            assertion = assertions.get(assertion_id)
            kinship = assertion.get('qualifiers', {}).get('kinship_structure', {}) if assertion else {}
            if (not assertion or assertion.get('predicate') != 'agnatic_cousin'
                    or assertion.get('status') != 'source_attested'
                    or kinship.get('lineage') != 'paternal'
                    or kinship.get('distance') is not None
                    or kinship.get('common_ancestor_person_id') is not None
                    or assertion['subject_person_id'] not in all_members
                    or assertion['object_person_id'] not in all_members):
                raise ValueError('父系網絡關係須指向分支中的來源已載父系親屬斷言')
            relations.append(assertion)
        if not relations:
            raise ValueError('父系網絡至少需要一條來源親屬斷言')
        network_out = {k: v for k, v in network.items() if k != 'branches'}
        network_out['branches'] = []
        for branch in network['branches']:
            network_out['branches'].append({**branch, 'person_ids': sorted(branch_members[branch['id']])})
        network_out['person_ids'] = sorted(all_members)
        network_out['relations'] = [
            {'assertion_id': a['id'], 'subject_person_id': a['subject_person_id'],
             'predicate': a['predicate'], 'object_person_id': a['object_person_id'],
             'source_term': a.get('qualifiers', {}).get('source_term'),
             'kinship_structure': a.get('qualifiers', {}).get('kinship_structure'),
             'evidence': a.get('evidence', [])}
            for a in relations]
        networks.append(network_out)
    return networks
