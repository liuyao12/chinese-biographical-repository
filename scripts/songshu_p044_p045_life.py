"""卷五十一 p044–p045 思考卒年資料的固定來源驗證。"""
from pathlib import Path
import json

CID = 'c-songshu-051-wyd1739-zongshi'
PID = 'zg6_7so_7t0'
MID = CID + ':p045:m0021'
EVENT_ID = 'le-song051-p044-p045-sikao-death'
ERA_URL = 'https://dict.revised.moe.edu.tw/appendix.jsp?ID=3&page=2'


def expected_event(root):
    root = Path(root)
    chapter = json.loads((root / 'corpus/songshu/051-wyd1739.json').read_text())
    paragraph = next(p for p in chapter['paragraphs'] if p['id'] == CID + ':p045')
    mention = next(m for m in paragraph['mentions'] if m['id'] == MID)
    text = paragraph['text']
    quote = text
    age = json.loads((root / 'source-evidence/song051-wyd1739-zongshi/yixin-complete-unit-contract.json').read_text())
    age = age['later_phase']['age_assertions']
    age, = [a for a in age if a['id'] == 'age-song051-p044-p045-sikao-death']
    normalized_date = age['normalized_date']
    return {
        'id': EVENT_ID,
        'person_id': PID,
        'event_type': 'death',
        'source_term': '卒',
        'date_expression': '泰始元年',
        'status': 'source_attested',
        'evidence': [{
            'work_id': chapter['work_id'], 'book_id': chapter['book_id'],
            'source_id': chapter['source_id'], 'chapter_id': CID,
            'paragraph_id': paragraph['id'], 'quote': quote,
            'person_mention_id': mention['id'],
        }],
        'source_anchor': {
            'paragraph_id': paragraph['id'],
            'start': text.index('泰始元年卒') + len('泰始元年'),
            'end': text.index('泰始元年卒') + len('泰始元年') + 1,
            'surface': '卒',
        },
        'normalized_date': normalized_date,
        'interpretation_note': '本傳明載泰始元年卒；按宋年號表換算為465年，死亡年已知而出生年未載。',
        'reviewer': 'Codex（AI代理）',
        'human_reviewed': False,
        'model': None,
    }


def valid_event(event, root):
    try:
        return event == expected_event(root)
    except (KeyError, TypeError, ValueError, StopIteration, OSError):
        return False
