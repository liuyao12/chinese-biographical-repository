"""Opaque person identifiers; published legacy identifiers remain valid."""
import re
import secrets
import string

LEGACY = re.compile(r'cbr-p[0-9]{6}')
SUFFIX_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZΓΔΘΛΞΠΣΦΨΩБДЖЗИЙЦЧШЩЪЫЬЭЮЯÆÐÞØŒŁŊŦĦĐẞÅÄÖÜÑÇŠŽČĞİŞŴŶŸ'
FAMILY = re.compile(r'[a-z0-9]{3}_[a-z0-9]{3}_[a-z0-9]{3}(?:_[' + SUFFIX_CHARS + r'*]*[' + SUFFIX_CHARS + r'])?')
LEGACY_FAMILY = re.compile(r'[a-z0-9]{3}_[a-z0-9]{3}_[a-z0-9]{3}-[' + SUFFIX_CHARS + r']*')
OPAQUE = re.compile(r'cbr-p-[a-z0-9]{4}_[a-z0-9]{4}_[a-z0-9]{4}')


def valid_person_id(value):
    return isinstance(value, str) and bool(LEGACY.fullmatch(value) or OPAQUE.fullmatch(value) or FAMILY.fullmatch(value) or LEGACY_FAMILY.fullmatch(value))


def allocate_person_id(existing):
    used = set(existing)
    while True:
        token = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(9))
        candidate = '_'.join(token[n:n+3] for n in (0, 3, 6))
        if candidate not in used and not any(pid.startswith(candidate) for pid in used):
            return candidate


def allocate_child_id(parent_id, existing):
    return allocate_descendant_id(parent_id, 1, existing)


def allocate_descendant_id(ancestor_id, generations, existing):
    if not isinstance(ancestor_id, str) or not FAMILY.fullmatch(ancestor_id):
        raise ValueError('Ancestor must have a family-path ID')
    if type(generations) is not int or generations < 1:
        raise ValueError('Generation distance must be a positive integer')
    used = set(existing)
    for suffix in SUFFIX_CHARS:
        branch = ancestor_id + ('_' if len(ancestor_id) == 11 else '') + '*' * (generations - 1) + suffix
        # A missing generation reserves a branch; it does not register a person.
        if not any(pid.startswith(branch) for pid in used):
            return branch
    raise ValueError('No available child suffix')


def family_path_errors(person_id, path):
    errors = []
    connection = path.get('connection')
    ancestor = path.get('ancestor_person_id', path.get('parent_person_id'))
    distance = path.get('generation_distance', 1 if connection == 'father' else None)
    expected = {'father': 1, 'grandfather': 2, 'great_grandfather': 3}.get(connection)
    if type(distance) is not int or distance < 1 or connection not in ('father', 'grandfather', 'great_grandfather', 'ancestor') or expected is not None and distance != expected:
        errors.append('家族路徑世代距離與關係不符')
        return errors
    prefix = ancestor + ('_' if len(ancestor) == 11 else '') if isinstance(ancestor, str) else ''
    if not isinstance(ancestor, str) or not FAMILY.fullmatch(ancestor) or not FAMILY.fullmatch(person_id) or not person_id.startswith(prefix) or len(person_id) != len(prefix) + distance:
        errors.append('家族路徑格式與所記世代距離不符')
    if distance > 1:
        if path.get('parent_person_id') is not None or path.get('intermediate_person_ids') != [None] * (distance - 1):
            errors.append('缺名中間世代須留空，不得造出父親')
        if person_id[len(prefix):-1] != '*' * (distance - 1):
            errors.append('缺名世代須以星號標記')
    return errors
