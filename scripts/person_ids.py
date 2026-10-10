"""Opaque person identifiers; published legacy identifiers remain valid."""
import re
import secrets
import string

LEGACY = re.compile(r'cbr-p[0-9]{6}')
SUFFIX_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZΓΔΘΛΞΠΣΦΨΩБДЖЗИЙЦЧШЩЪЫЬЭЮЯÆÐÞØŒŁŊŦĦĐẞÅÄÖÜÑÇŠŽČĞİŞŴŶŸ'
FAMILY = re.compile(r'[a-z0-9]{3}_[a-z0-9]{3}_[a-z0-9]{3}-[' + SUFFIX_CHARS + r']*')
OPAQUE = re.compile(r'cbr-p-[a-z0-9]{4}_[a-z0-9]{4}_[a-z0-9]{4}')


def valid_person_id(value):
    return isinstance(value, str) and bool(LEGACY.fullmatch(value) or OPAQUE.fullmatch(value) or FAMILY.fullmatch(value))


def allocate_person_id(existing):
    used = set(existing)
    while True:
        token = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(9))
        candidate = '_'.join(token[n:n+3] for n in (0, 3, 6)) + '-'
        if candidate not in used and not any(pid.startswith(candidate) for pid in used):
            return candidate


def allocate_child_id(parent_id, existing):
    if not isinstance(parent_id, str) or not FAMILY.fullmatch(parent_id):
        raise ValueError('Parent must have a family-path ID')
    used = set(existing)
    for suffix in SUFFIX_CHARS:
        candidate = parent_id + suffix
        if candidate not in used and not any(pid.startswith(candidate) for pid in used):
            return candidate
    raise ValueError('No available child suffix')
