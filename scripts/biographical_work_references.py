# coding: utf-8
"""Typed, narrowly delimited digressions in an otherwise retained biography topic."""
import hashlib
import json
import re
from pathlib import Path


def _inside(root, value, prefix):
    p = Path(value)
    if p.is_absolute() or not p.parts or p.parts[0] != prefix or '..' in p.parts:
        raise ValueError('unsafe relative path')
    root = Path(root).resolve()
    current = root
    for part in p.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError('symlink')
    if not current.resolve().is_relative_to(root):
        raise ValueError('outside root')
    return current


def projection_valid(chapter, paragraphs, binding, root):
    """Validate real retained bytes, not only an internally coherent fragment."""
    try:
        if root is None:
            return False
        spec = binding['received_text_projection']
        if set(spec) != {'path', 'sha256', 'source_layer', 'text_layer'} or any(spec[k] != 'received_text' for k in ('source_layer','text_layer')):
            return False
        source = chapter['source']
        raw_bytes = _inside(root, source['raw_path'], 'sources').read_bytes()
        if source.get('raw_sha256', source['raw_file_sha256']) != source['raw_file_sha256'] or hashlib.sha256(raw_bytes).hexdigest() != source['raw_file_sha256']:
            return False
        raw = raw_bytes.decode('utf-8')
        projection_bytes = _inside(root, spec['path'], 'source-evidence').read_bytes()
        if hashlib.sha256(projection_bytes).hexdigest() != spec['sha256']:
            return False
        projection = json.loads(projection_bytes.decode('utf-8'))
        if projection['source_id'] != chapter['source_id'] or projection['source']['revision_id'] != source['revision_id'] or projection['source']['raw_sha256'] != source['raw_file_sha256']:
            return False
        for item in [chapter,source,projection,projection['source']]:
            if any(item.get(k, 'received_text') != 'received_text' for k in ('source_layer','text_layer')) or 'annotator' in item or 'attached_note_to_paragraph_id' in item:
                return False
        by_suffix = {p['id'].rsplit(':',1)[1]:p for p in projection['paragraphs']}
        if len(by_suffix) != len(projection['paragraphs']):
            return False
        for p in paragraphs:
            pp = by_suffix[p['id'].rsplit(':',1)[1]]
            pos = p['source_position']
            for item in (p,pos,pp,pp['source_position']):
                if any(item.get(k,'received_text') != 'received_text' for k in ('source_layer','text_layer')) or 'annotator' in item or 'attached_note_to_paragraph_id' in item:
                    return False
            if {k:v for k,v in pos.items() if k != 'raw_path'} != pp['source_position'] or pp['text'] != p['text'] or pos['raw_path'] != source['raw_path']:
                return False
            start,end = pos['start'],pos['end']
            if type(start) is not int or type(end) is not int or not 0 <= start < end <= len(raw) or raw[start:end] != pos['raw']:
                return False
            coords = pp['raw_positions']
            if len(coords) != len(p['text']) or any(type(i) is not int for i in coords) or coords != sorted(set(coords)):
                return False
            if any(not start <= i < end for i in coords) or ''.join(raw[i] for i in coords) != p['text']:
                return False
        return True
    except (OSError,UnicodeError,ValueError,KeyError,TypeError,IndexError,AttributeError):
        return False


def references_valid(binding, paragraph, subject, death_anchor):
    """Only quoted praise returning to office narrative, and a continued work's author."""
    try:
        refs = binding['non_subject_references']
        others = [m for m in paragraph['mentions'] if m.get('kind') == 'person' and subject['end'] <= m['start'] < death_anchor['end'] and m.get('person_id') != subject['person_id']]
        if not isinstance(refs,list) or not refs or len(refs) != len(others):
            return False
        by_id = {m['id']:m for m in others}
        if len(by_id) != len(others) or {r['person_mention_id'] for r in refs} != set(by_id):
            return False
        text = paragraph['text']
        def outside_quote(position):
            stack = []
            for char in text[:position]:
                if char in '「『': stack.append(char)
                elif char in '」』':
                    if not stack or (stack.pop(),char) not in [('「','」'),('『','』')]: return False
            return not stack
        if not outside_quote(subject['start']) or not outside_quote(death_anchor['start']):
            return False
        for r in refs:
            if set(r) != {'kind','person_mention_id','anchor'}:
                return False
            m = by_id[r['person_mention_id']];a = r['anchor']
            if set(a) != {'paragraph_id','start','end','surface'} or a['paragraph_id'] != paragraph['id'] or type(a['start']) is not int or type(a['end']) is not int:
                return False
            lo,hi = a['start'],a['end']
            if not subject['end'] <= lo <= m['start'] < m['end'] <= hi <= death_anchor['start'] or text[lo:hi] != a['surface']:
                return False
            if not outside_quote(lo) or lo > 0 and text[lo-1] not in '。！？':
                return False
            # This grammar never treats a bare emperor mention as an ignorable name.
            if r['kind'] == 'quoted_praise_then_return_to_office':
                if m['start'] != lo or m['surface'] != '上' or not re.fullmatch(r'上善之，曰：「[^「」『』曰卒薨死]{1,24}」出[爲為]',a['surface']):
                    return False
            elif r['kind'] == 'author_of_continued_history':
                if text[lo:m['start']] != '續' or text[m['end']:hi] != '國史，未及撰述，':
                    return False
                year = binding['year_chain'][-1]['anchor']
                if hi != year['start'] or year['end'] >= death_anchor['start'] or text[year['end']:death_anchor['start']] != '，':
                    return False
            else:
                return False
            # A role anchor cannot silently contain additional named people.
            if any(x.get('kind') == 'person' and lo <= x['start'] < hi and x['id'] != m['id'] for x in paragraph['mentions']):
                return False
        return True
    except (KeyError,TypeError,ValueError,IndexError):
        return False
