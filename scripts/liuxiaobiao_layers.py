# coding: utf-8
"""核本次世說選錄的注本、正文和引書，保存古注歸屬與原字位置。"""
import hashlib
import re


def valid(p, chapter, root):
    try:
        if chapter['work_id'] != 'w-shishuoxinyu' or p['text_layer'] != 'witness_appended_liuxiaobiao_note':
            return False
        q, source, attribution = p['source_quote'], chapter['source'], p['attribution']
        fixed = (root / source['raw_path']).read_bytes()
        t = fixed.decode('utf-8')
        a, b = q['raw_start'], q['raw_end']
        if (hashlib.sha256(fixed).hexdigest() != source['raw_file_sha256'] or not (0 <= a < b <= len(t))
                or t[a:b] != q['quote'] or t[:a].count('\n') + 1 != q['raw_line']
                or attribution['annotator'] != '劉孝標' or not q['source_layer'].startswith('劉注引')):
            return False
        quotation = q['source_layer'][3:]
        if quotation != attribution['quoted_work'] or not quotation:
            return False
        left = t[:a].splitlines()[-1]
        start = left.rfind('{{*|')
        if start < 0:
            return False
        introductory = left[start:]
        marker = re.sub(r'-\{([^{}]+)\}-', r'\1', introductory)
        if quotation not in marker or '曰：' not in marker:
            return False
        rendered = re.sub(r'\{\{ProperNoun\|([^{}]+)\}\}', r'\1', q['quote'])
        rendered = re.sub(r'-\{([^{}]+)\}-', r'\1', rendered)
        return p['text'] == rendered
    except (KeyError, ValueError, TypeError, OSError, IndexError):
        return False
