#!/usr/bin/env python3
"""Generate the source-bound address, age, life-event, and title records for 宋書071 王僧綽."""
from __future__ import annotations
import copy, hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_ID = "c-songshu-071-wangsengchuo"
PERSON_ID = "7r6_k52_qji_ABAAAAEA"
CHAPTER_PATH = ROOT / "corpus/songshu/071-wangsengchuo.json"
SOURCE_PATH = "corpus/songshu/071-wangsengchuo.json"
CALENDAR_PATH = "source-evidence/song045-wyd1739-liucui/life-moe-yuanjia-row.json"
UNKNOWN = {"status": "unknown", "date_expression": None, "evidence": []}

def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def dump(path, value):
    (ROOT / path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def main():
    chapter = load(SOURCE_PATH)
    if chapter["id"] != CHAPTER_ID or chapter["source"]["image_verified"] is not False:
        raise SystemExit("來源篇或圖像核讀狀態與本批預期不同")
    paragraphs = {p["id"].rsplit(":", 1)[-1]: p for p in chapter["paragraphs"]}
    def p(key): return paragraphs[key]
    def mention(pid, mid):
        found = [m for m in p(pid)["mentions"] if m["id"] == mid and m.get("person_id") == PERSON_ID]
        if len(found) != 1: raise ValueError(f"人物錨點不唯一或人物端不符：{mid}")
        return found[0]
    def anchor(pid, text, within=None):
        body = p(pid)["text"]
        area = body if within is None else within
        if area not in body or area.count(text) != 1: raise ValueError(f"來源詞需在限定上下文恰好出現一次：{pid} {text}")
        start = body.index(area) + area.index(text)
        return {"paragraph_id": p(pid)["id"], "start": start, "end": start + len(text), "surface": text}
    def evidence(pid, mid):
        m = mention(pid, mid)
        return {"work_id": chapter["work_id"], "book_id": chapter["book_id"],
                "source_id": chapter["source_id"], "chapter_id": CHAPTER_ID,
                "paragraph_id": p(pid)["id"], "quote": p(pid)["text"],
                "person_mention_id": m["id"]}

    # Origin is explicitly stated at the head of the biography. Do not map it to a modern county.
    addresses = {"format_version": "0.2", "record_type": "person_address_assertion_set",
                 "chapter_id": CHAPTER_ID, "assertions": [{
        "id": "ad-song071-sengchuo-origin", "person_id": PERSON_ID,
        "relation": "biographical_origin", "source_term": "琅邪臨沂人",
        "place": {"source_name": "琅邪臨沂", "modern_place_id": None},
        "date_expression": None, "status": "source_attested",
        "evidence": [{**evidence("p001", "c-songshu-071-wangsengchuo:p001:m0000"),
                       "place_anchor": anchor("p001", "琅邪臨沂")}],
        "interpretation_note": "傳首所記籍貫；不作出生、居住、死亡或葬地，不定位現代行政區。",
        "human_reviewed": False, "model": None}]}

    death_id = "le-song071-sengchuo-death"
    death_e = evidence("p004", "c-songshu-071-wangsengchuo:p004:m0088")
    death = {"format_version": "0.2", "record_type": "person_life_event_assertion_set",
             "chapter_id": CHAPTER_ID, "events": [{
        "id": death_id, "person_id": PERSON_ID, "event_type": "death",
        "source_term": "乃收害焉", "date_expression": None,
        "status": "source_attested", "evidence": [death_e],
        "interpretation_note": "劭弒逆後被收害；本傳未在本事件句明記年次，先不補公元卒年。報齡另記，不倒推生年。",
        "reviewer": "Codex（AI代理）", "human_reviewed": False, "model": None}]}

    ages = []
    for suffix, value, number, term, pid, mid, context in [
        ("13", 13, "十三", "年十三", "p001", "c-songshu-071-wangsengchuo:p001:m0000", {"kind": "during_life"}),
        ("29", 29, "二十九", "時年二十九", "p001", "c-songshu-071-wangsengchuo:p001:m0242", {"kind": "during_life"}),
        ("31", 31, "三十一", "時年三十一", "p004", "c-songshu-071-wangsengchuo:p004:m0088", {"kind": "at_death", "life_event_id": death_id}),
    ]:
        ages.append({"id": f"age-song071-sengchuo-{suffix}", "person_id": PERSON_ID,
                     "value": value, "source_number": number, "source_term": term,
                     "unit": "source_age_years", "counting": "unspecified_source_age",
                     "birth_year": None, "status": "source_attested", "date_expression": None,
                     "evidence": [evidence(pid, mid)], "age_context": context,
                     "interpretation_note": "保留本傳報齡與原數；計歲方式未明，不倒算出生年。",
                     "reviewer": "Codex（AI代理）", "human_reviewed": False, "model": None})
    chapter.setdefault("annotation", {})["age_assertions"] = ages
    dump(SOURCE_PATH, chapter)

    calendar = load(CALENDAR_PATH)
    calendar_sha = hashlib.sha256((ROOT / CALENDAR_PATH).read_bytes()).hexdigest()
    if calendar["columns"] != {"dynasty": "宋", "era_name": "元嘉", "first_year": "424", "last_year": "453"}:
        raise ValueError("教育部元嘉年表列與預期不符")
    date_ref = {"title": "教育部《重編國語辭典修訂本》中國歷代年號表",
                "url": calendar["url"], "scope": "modern_era_year_equivalence_only",
                "quote": "元嘉", "columns": copy.deepcopy(calendar["columns"]),
                "fixed_row_reference": {"path": CALENDAR_PATH, "sha256": calendar_sha},
                "image_verified": False}
    p1 = p("p001")
    base_evidence = evidence("p001", "c-songshu-071-wangsengchuo:p001:m0000")
    def grant_date():
        return {"era": "CE", "year": 449, "era_year": 449, "year_numbering": "astronomical",
                "precision": "year", "calendar": "chinese_civil", "source_expression": "元嘉二十六年",
                "status": "editorial_provisional", "original_quote": p1["text"],
                "evidence": [base_evidence], "references": [copy.deepcopy(date_ref)],
                "rationale": "元嘉始於424年；元嘉二十六年按年號序數換算為449年。只記年，不換算月日。",
                "regnal_year_mapping": {"kind": "ce_regnal_era_span", "era_name": "元嘉",
                    "source_number": "二十六", "regnal_year": 26, "start_ce_year": 424,
                    "end_ce_year": 453, "reference_index": 0},
                "reviewer": "Codex（AI代理）", "human_reviewed": False, "model": None}

    holdings = []
    def add_holding(key, title, kind, mode, pid, mid, phrase, usage="narrative",
                    start_kind=None, date_expression=None, normalized_date=None,
                    transfer=None, note=None):
        ev = evidence(pid, mid)
        a = anchor(pid, phrase if len(phrase) < len(title) else title, within=phrase if len(phrase) > len(title) else None)
        start = ({"status": "unknown", "date_expression": None, "evidence": []}
                 if mode == "attestation" else
                 {"status": "source_event", "event_type": start_kind or mode,
                  "date_expression": date_expression, "evidence": [ev]})
        if normalized_date is not None: start["normalized_date"] = normalized_date
        h = {"id": f"th-song071-sengchuo-{key}", "person_id": PERSON_ID,
             "title": title, "kind": kind, "mode": mode, "status": "source_attested",
             "evidence": [ev], "attestations": [{"id": f"att-song071-sengchuo-{key}",
                "paragraph_id": p(pid)["id"], "person_mention_id": mid,
                "start": a["start"], "end": a["end"], "surface": a["surface"],
                "usage": usage, "date_expression": date_expression}],
             "effective_period": {"start": start, "end": copy.deepcopy(UNKNOWN)},
             "interpretation_note": note or "只記本傳明載的用稱／任官事件；未載的月日及終點不推定。",
             "reviewer": "Codex（AI代理）", "human_reviewed": False, "model": None}
        if transfer:
            h["office_transfer_basis"] = {"kind": "explicit_office_transfer", **transfer, "evidence": [ev]}
        holdings.append(h)

    m1 = "c-songshu-071-wangsengchuo:p001:m0000"
    m4 = "c-songshu-071-wangsengchuo:p004:m0088"
    add_holding("yuzhang-hou", "豫章縣侯", "noble_rank", "accession", "p001", m1,
                "豫章縣侯", usage="narrative", start_kind="accession",
                note="本傳明言襲封豫章縣侯；《宋書》卷六十三父曇首爵名作豫寧縣侯，兩處原文保留，不替來源消平異名。")
    add_holding("sima-can-jun", "司徒參軍", "office", "grant", "p001", m1,
                "司徒參軍", usage="narrative", start_kind="grant",
                note="傳文稱初為江夏王義恭司徒參軍；任始及終年均未載。")
    for key, title, phrase in [("wenxue", "文學", "文學"), ("mishu-cheng", "袐書丞", "袐書丞"),
                               ("zuo-zhangshi", "司徒左長史", "司徒左長史"),
                               ("taizi-zhongshuzi", "太子中庶子", "太子中庶子")]:
        add_holding(key, title, "office", "attestation", "p001", m1, phrase,
                    note="只記傳文所列官稱；「轉」後連列數職而未逐職標明授任年月，不補造各職起訖。")
    transfer_phrase = "徙尚書吏部郎"
    add_holding("shangshu-libulang", "尚書吏部郎", "office", "transfer", "p001", m1,
                "尚書吏部郎", usage="narrative", start_kind="transfer",
                date_expression="元嘉二十六年", normalized_date=grant_date(),
                transfer={"verb": "徙", "titles": ["尚書吏部郎"], "source_term": transfer_phrase},
                note="元嘉二十六年徙尚書吏部郎，換算449年；只確定授任年，離任年不詳。")
    add_holding("shizhong", "侍中", "office", "transfer", "p001", "c-songshu-071-wangsengchuo:p001:m0149",
                "遷侍中", usage="narrative", start_kind="transfer", date_expression="二十八年",
                transfer={"verb": "遷", "titles": ["侍中"], "source_term": "遷侍中"},
                note="本段承前元嘉二十六年而記二十八年遷侍中；保留原紀年，終止年未載。")
    add_holding("libu-shangshu", "吏部尚書", "office", "transfer", "p004", m4,
                "吏部尚書", usage="narrative", start_kind="transfer",
                transfer={"verb": "轉為", "titles": ["吏部尚書"], "source_term": "轉為吏部尚書"},
                note="劭即位後本傳稱轉為吏部尚書；本段未明紀年，任期終點不另推定。")
    add_holding("sanjichangshi-posthumous", "散騎常侍", "office", "attestation", "p004", m4,
                "散騎常侍", usage="narrative",
                note="本傳明言世祖即位後追贈散騎常侍；以追贈用稱保存，不作生前實任。")
    add_holding("jinzi-guanglu-posthumous", "金紫光禄大夫", "office", "attestation", "p004", m4,
                "金紫光禄大夫", usage="narrative",
                note="本傳與散騎常侍並列於追贈語中；保存追贈性質，不作生前實任。")
    add_holding("min-hou-posthumous", "愍侯", "honorific", "attestation", "p004", m4,
                "愍侯", usage="narrative",
                note="本傳明言謚曰愍侯；記為死後諡號，不與生前豫章縣侯混同。")
    title_set = {"format_version": "0.2", "record_type": "title_holding_assertion_set",
                 "chapter_id": CHAPTER_ID, "holdings": holdings}
    dump("corpus/songshu/071-wangsengchuo-addresses.json", addresses)
    dump("corpus/songshu/071-wangsengchuo-life-events.json", death)
    dump("corpus/songshu/071-wangsengchuo-titles.json", title_set)
    print(f"generated origin=1, death=1, ages={len(ages)}, titles={len(holdings)}")

if __name__ == "__main__":
    main()
