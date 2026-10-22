"""Known retired ID reservations. This is never alias or redirect resolution."""
import json
import re
from pathlib import Path
try:
    from .person_ids import valid_person_id, FAMILY
except ImportError:
    from person_ids import valid_person_id, FAMILY


def retired_person_ids(root):
    result = set()
    for path in sorted((Path(root) / 'source-evidence').glob('*/annotation-chain.json')):
        data = json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(data, dict):
            raise ValueError('Malformed annotation receipt: ' + str(path))
        if data.get('record_type') != 'editorial_annotation_rekey_receipt':
            continue
        if data.get('person_aliases_created') is not False:
            raise ValueError('Retirement receipt cannot create aliases: ' + str(path))
        namespace_form = 'historical_rekey_mapping' in data
        family_form = 'family_id' in data
        identity_form = 'identity_decision_id' in data
        if sum((namespace_form, family_form, identity_form)) != 1 or (namespace_form and 'retired_person_ids' in data) or (not namespace_form and 'namespace_id' in data):
            raise ValueError('Unknown or ambiguous retirement receipt: ' + str(path))
        if namespace_form:
            owner = data.get('namespace_id')
            mapping = data['historical_rekey_mapping']
            if (not isinstance(owner, str) or not FAMILY.fullmatch(owner) or len(owner) != 11
                    or data.get('mapping_role') != 'audit_only_not_alias_or_current_person_endpoint'
                    or not isinstance(mapping, dict) or not mapping
                    or any(not valid_person_id(k) or not valid_person_id(v) or k == v
                           or not v.startswith(owner + '_') for k, v in mapping.items())):
                raise ValueError('Malformed namespace retirement receipt: ' + str(path))
            ids = list(mapping)
        elif identity_form:
            owner = data.get('identity_decision_id')
            ids = data.get('retired_person_ids')
            if (set(data) != {'record_type', 'identity_decision_id', 'retired_person_ids', 'retirement_policy', 'person_aliases_created'}
                    or not isinstance(owner, str) or re.fullmatch(r'd-[A-Za-z0-9][A-Za-z0-9_-]*', owner) is None
                    or data.get('retirement_policy') != 'audit_only_not_canonical_not_alias_not_reusable'
                    or not isinstance(ids, list) or not ids
                    or any(not valid_person_id(pid) for pid in ids) or len(ids) != len(set(ids))):
                raise ValueError('Malformed identity retirement receipt: ' + str(path))
            decisions = []
            for decision_path in sorted((Path(root) / 'corpus').glob('*/*-identities.json')):
                record = json.loads(decision_path.read_text(encoding='utf-8'))
                matching = [d for d in record.get('decisions', []) if d.get('id') == owner]
                if matching and record.get('record_type') not in ('person_identity_decision_set', 'identity_decision_set'):
                    raise ValueError('Identity retirement needs an identity decision set: ' + str(path))
                decisions.extend(matching)
            people_path = Path(root) / 'registry/persons.json'
            if not people_path.is_file():
                raise ValueError('Identity retirement needs current person registry: ' + str(path))
            current_people = {p['id'] for p in json.loads(people_path.read_text(encoding='utf-8'))['persons']}
            if (len(decisions) != 1
                    or not valid_person_id(decisions[0].get('person_id'))
                    or decisions[0]['person_id'] in ids
                    or decisions[0]['person_id'] not in current_people
                    or current_people.intersection(ids)
                    or decisions[0].get('scope') != 'cross_chapter'
                    or decisions[0].get('status') not in ('contextual_provisional', 'source_explicit')
                    or not decisions[0].get('evidence') or not decisions[0].get('rationale')):
                raise ValueError('Identity retirement must bind one supported current identity decision: ' + str(path))
        else:
            owner = data.get('family_id')
            ids = data.get('retired_person_ids')
            if (not isinstance(owner, str) or not owner.startswith('family-') or len(owner) <= 7
                    or any(not (c.isascii() and (c.isalnum() or c == '-')) for c in owner)
                    or data.get('retirement_policy') != 'audit_only_not_canonical_not_alias_not_reusable'
                    or not isinstance(ids, list) or not ids
                    or any(not valid_person_id(pid) for pid in ids) or len(ids) != len(set(ids))):
                raise ValueError('Malformed family retirement receipt: ' + str(path))
        result.update(ids)
    return frozenset(result)


def allocation_conflicts(candidate, retired):
    return any(candidate.startswith(pid) or pid.startswith(candidate) for pid in retired)


def assert_not_retired(person_id, root):
    if person_id in retired_person_ids(root):
        raise ValueError('Retired person ID cannot be registered: ' + person_id)
    return person_id
