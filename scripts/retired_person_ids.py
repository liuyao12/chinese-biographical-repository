"""Known retired ID reservations. This is never alias or redirect resolution."""
import json
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
        family_form = 'retired_person_ids' in data
        if namespace_form == family_form:
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
        else:
            owner = data.get('family_id')
            ids = data['retired_person_ids']
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
