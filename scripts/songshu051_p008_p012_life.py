"""Fixed source-bound death and date records for Songshu 51 p008–p012."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

CID = "c-songshu-051-wyd1739-zongshi"
CH = "data/corpus/songshu/051-wyd1739.json"
OUT = "corpus/songshu/051-wyd1739-p008-p012-life-events.json"
KIND = "fixed_wyd_song051_p008_p012_life_date"
MOE = "教育部《重編國語辭典修訂本》中國歷代年號表"
ROWS = {
    "元嘉": "source-evidence/song045-wyd1739-liucui/life-moe-yuanjia-row.json",
    "元徽": "source-evidence/song051-wyd1739-zongshi/p014-p017-yuanhui-calendar-row.json",
    "昇明": "source-evidence/song051-wyd1739-zongshi/p008-p012-shengming-calendar-row.json",
}

SPECS = [
    ("yixin-death", "3qs_nqa_ioa_AABA", "p010", "成王", "十六年薨時年三十六", "十六年", "元嘉", 16, 439,
     "same_biography_omitted_era_year", "元嘉年序見同一傳中「元嘉元年」、「三年」、「七年」及後續十年、十二年；本處「十六年」依此連續年序換算。來源另明記時年三十六，不反推生年。"),
    ("jin-death", "3qs_nqa_ioa_AABAA", "p010", "瑾", "三十年為元凶所殺", "三十年", "元嘉", 30, 453,
     "same_biography_omitted_era_year", "本傳在父義欣元嘉十六年卒後連敘三十年；按同一傳記紀年脈絡解為元嘉三十年。保留上下文換算，不補月份日期。"),
    ("can-death", "3qs_nqa_ioa_AABAAA", "p010", "粲", "子粲早夭", None, None, None, None, None,
     "原文只記早夭，未給紀年或年齡，不推定。"),
    ("zuan-death", "3qs_nqa_ioa_AABAAB", "p010", "纂", "順帝昇明三年薨", "昇明三年", "昇明", 3, 479,
     "explicit_era_year", "原文直書順帝昇明三年。"),
    ("kai-death", "3qs_nqa_ioa_AABAC", "p010", "楷", "楷祕書郎為元凶所殺", None, None, None, None, None,
     "原文記為元凶所殺，未在本句給年；不僅憑元凶稱號補日期。"),
    ("yun-death", "3qs_nqa_ioa_AABAE", "p011", "韞", "昇明二年謀反伏誅", "昇明二年", "昇明", 2, 478,
     "explicit_era_year", "原文直書昇明二年。"),
    ("bi-death", "3qs_nqa_ioa_AABAF", "p012", "弼", "韞弟弼武昌太守亦與子勛同逆伏誅", None, None, None, None, None,
     "原文明記與子勛同逆伏誅，未在本句給年。"),
    ("jian-death", "3qs_nqa_ioa_AABAG", "p012", "鑒", "弟鑒員外散騎侍郎蚤卒", None, None, None, None, None,
     "原文只記蚤卒，未給紀年或年齡，不推定。"),
    ("xie-death", "3qs_nqa_ioa_AABAH", "p012", "勰", "鑒弟勰字彥麟侍中吳興太守後廢帝元徽元年卒", "元徽元年", "元徽", 1, 473,
     "explicit_era_year", "原文直書後廢帝元徽元年。"),
    ("hao-death", "3qs_nqa_ioa_AABAI", "p012", "顥", "勰弟顥字彥明侍中左衞將軍冠軍將軍吳興太守未拜元徽四年卒", "元徽四年", "元徽", 4, 476,
     "explicit_era_year", "原文直書元徽四年。"),
    ("yirong-death", "3qs_nqa_ioa_AABC", "p012", "義融", "元嘉十八年卒", "元嘉十八年", "元嘉", 18, 441,
     "explicit_era_year", "原文直書元嘉十八年。"),
    ("shu-death", "3qs_nqa_ioa_AABAJ", "p012", "述", "顥弟述東陽太守黃門郎與從弟秉同逆事敗走白山追禽伏誅", None, None, None, None, None,
     "原文明記事敗被追獲伏誅，未在本句給年。"),
]


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _reference(root: Path, era: str) -> dict:
    rel = ROWS[era]
    raw = (root / rel).read_bytes()
    row = json.loads(raw)
    return {
        "title": MOE,
        "url": row["url"],
        "quote": era,
        "scope": "modern_era_year_equivalence_only",
        "columns": copy.deepcopy(row["columns"]),
        "fixed_row_reference": {"path": rel, "sha256": _sha(raw)},
        "image_verified": False,
    }


def records(root: str | Path) -> dict:
    root = Path(root)
    chapter = json.loads((root / CH).read_bytes())
    paragraphs = {p["id"].rsplit(":", 1)[-1]: p for p in chapter["paragraphs"]}
    events = []
    for slug, pid, pno, surface, term, expression, era, era_year, year, context, note in SPECS:
        p = paragraphs[pno]
        text = p["text"]
        start = text.find(term)
        if start < 0 or text.find(term, start + 1) >= 0:
            raise ValueError(f"固定句須唯一出現：{pno} {term}")
        mention = next(m for m in p["mentions"]
                       if m.get("person_id") == pid and text[m["start"]:m["end"]] == surface)
        evidence = [{"work_id": chapter["work_id"], "book_id": chapter["book_id"],
                     "source_id": chapter["source_id"], "chapter_id": CID,
                     "paragraph_id": p["id"], "quote": text,
                     "person_mention_id": mention["id"]}]
        event = {
            "id": f"le-song051-p008-p012-{slug}", "person_id": pid, "event_type": "death",
            "status": "source_attested", "date_expression": expression, "source_term": term,
            "evidence": evidence,
            "source_anchor": {"paragraph_id": p["id"], "start": start,
                              "end": start + len(term), "surface": term},
            "interpretation_note": note, "reviewer": "Codex（AI代理）",
            "human_reviewed": False,
        }
        if year is not None:
            date = {
                "era": "CE", "era_year": year, "year": year,
                "year_numbering": "astronomical", "precision": "year",
                "calendar": "chinese_civil", "source_expression": expression,
                "original_quote": text, "evidence": evidence,
                "references": [_reference(root, era)],
                "regnal_year_mapping": {"kind": KIND, "era_name": era,
                                        "year": year, "source_expression": expression,
                                        "context_kind": context},
                "status": "editorial_provisional",
                "rationale": note, "reviewer": "Codex（AI代理）", "human_reviewed": False,
            }
            if context == "same_biography_omitted_era_year":
                date["contextual_date_basis"] = {
                    "kind": context, "paragraph_id": p["id"],
                    "sequence_anchor": expression, "prior_explicit_era_name": "元嘉",
                    "prior_sequence_markers": ["元嘉元年", "三年", "七年", "十年", "十二年", "十六年"],
                }
            event["normalized_date"] = date
        events.append(event)
    return {"format_version": "0.1", "record_type": "person_life_event_assertion_set",
            "chapter_id": CID, "events": events}


def date_valid(date: dict, event: dict, root: str | Path) -> bool:
    try:
        expected = next(e for e in records(root)["events"] if e["id"] == event["id"])
        return event == expected and date == expected["normalized_date"]
    except (KeyError, TypeError, ValueError, StopIteration, OSError):
        return False


def event_valid(event: dict, root: str | Path) -> bool:
    try:
        expected = next(e for e in records(root)["events"] if e["id"] == event["id"])
        return event == expected
    except (KeyError, TypeError, ValueError, StopIteration, OSError):
        return False


def record_valid(record: dict, root: str | Path) -> bool:
    try:
        return record == records(root)
    except (KeyError, TypeError, ValueError, StopIteration, OSError):
        return False
