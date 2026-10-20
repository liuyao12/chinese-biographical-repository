"""Exact, portable fixed-raw projections; no inferred similarity."""
import hashlib
import json
from pathlib import Path


def need(value, message):
    if not value:
        raise ValueError('固定見證投影：' + message)


def body_positions(chapter, paragraph, lines):
    matches = [e for e in chapter['source']['normalization']['excerpts']
               if e['proposed_paragraph_id'] == paragraph['id']]
    need(len(matches) == 1, '節引單元須唯一')
    e = matches[0]; first, last = e['source_lines']
    need(type(first) is int and type(last) is int and 1 <= first <= last <= len(lines), '原行越界')
    raw = '\n'.join(lines[first-1:last]); quote = e['raw_quote']
    need(quote in (raw, raw+'\n') and hashlib.sha256(quote.encode()).hexdigest() == e['raw_quote_sha256'], '原引或SHA不符')
    points, chars, depth = [], [], 0
    for n in range(first, last+1):
        line = lines[n-1]; i = 0
        while i < len(line):
            if line.startswith('<pb:', i):
                end = line.find('>', i); need(end >= 0, '頁標未閉合'); i = end+1; continue
            ch = line[i]
            if ch == '(': depth += 1
            elif ch == ')': depth -= 1; need(depth >= 0, '括注不平衡')
            elif depth == 0 and ch not in '¶\n\r': chars.append(ch); points.append((n, i))
            i += 1
    need(depth == 0, '括注不平衡')
    text = ''.join(chars)
    if 'body_selection' in e:
        selection = e['body_selection']; a, b = selection['start'], selection['end']
        need(type(a) is int and type(b) is int and 0 <= a < b <= len(text), '選段越界')
        text, points = text[a:b], points[a:b]
        need(bool(selection['begin_anchor']) and bool(selection['end_anchor']) and text.startswith(selection['begin_anchor']) and text.endswith(selection['end_anchor']), '選段錨點不符')
    need(text == paragraph['text'], '正文投影不符')
    return points


def repository_positions(root, paragraph, lines):
    position = paragraph['source_position']; rel = Path(position['raw_projection_ref']); root = Path(root).resolve()
    need(not rel.is_absolute() and rel.parts[:1] == ('source-evidence',) and '..' not in rel.parts, '投影路徑不安全')
    path = (root/rel).resolve(); evidence = root/'source-evidence'
    need(path.is_relative_to(root) and path.is_relative_to(evidence), '投影路徑越界source-evidence')
    data = json.loads(path.read_text())
    # Hash the actual fixed witness, including its original terminal newline.
    raw = position.get('raw_file_sha256')
    # Caller supplies the full raw digest; splitlines alone cannot recover terminal newline.
    need(raw is None or raw == data['raw_sha256'], '段落raw SHA不符')
    units = data['units']
    def unit_key(u):
        key = u.get('candidate_id',u.get('key'))
        need(isinstance(key,str) and bool(key), '缺少unit key')
        need('candidate_id' not in u or 'key' not in u or u['candidate_id'] == u['key'], 'mixed key不一致')
        return key
    keys = [unit_key(u) for u in units]
    need(len(keys) == len(set(keys)), '重複unit_key')
    matches = [u for u in units if unit_key(u) == position['unit_key']]
    need(len(matches) == 1, '未知unit_key')
    unit = matches[0]; need(unit['layer'] == position['source_layer'], '來源層不符')
    window = unit.get('raw_window')
    if window is not None:
        need(isinstance(window,list) and len(window)==2 and all(type(x)is int for x in window) and 1 <= window[0] <= window[1] <= len(lines), 'raw_window越界')
        if 'first_line' in position or 'last_line' in position:
            need([position.get('first_line'),position.get('last_line')] == window, 'raw_window與段落不符')
    points, parts, cursor, seen = [], [], 0, set()
    for run in unit['raw_runs']:
        n, a, b, s, e = [run[k] for k in ('raw_line','raw_start','raw_end','start','end')]
        need(all(type(x) is int for x in (n,a,b,s,e)) and 1 <= n <= len(lines) and 0 <= a < b <= len(lines[n-1]) and s == cursor and e-s == b-a, 'raw_runs越界／offset不連續')
        need(window is None or window[0] <= n <= window[1], 'raw_runs越出raw_window')
        text = lines[n-1][a:b]; pts = [(n,i) for i in range(a,b)]
        need(text == run['surface'] and not seen.intersection(pts), 'raw_runs錯字／重疊')
        need(not points or points[-1] < pts[0], 'raw_runs順序錯誤')
        seen.update(pts); points.extend(pts); parts.append(text); cursor = e
    text = ''.join(parts)
    need('text' not in unit or unit['text'] == text, 'unit.text與實算正文不符')
    need('text_sha256' in unit or isinstance(unit.get('text'),str), '缺少text及text SHA')
    need(text == paragraph['text'] and cursor == len(text), '單元正文不符')
    if 'text_sha256' in unit:
        need(hashlib.sha256(text.encode()).hexdigest() == unit['text_sha256'], '單元SHA不符')
    return points, data['raw_sha256']
