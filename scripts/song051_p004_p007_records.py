"""Source-bound people, kinship, names, and life records for Songshu 51 p004–p007."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

CID = "c-songshu-051-wyd1739-zongshi"
CHAPTER = "corpus/songshu/051-wyd1739.json"
IDS = {
    "daolian": "3qs_nqa_ioa_AAB", "liuyu": "3qs_nqa_ioa_AAA",
    "yizhen": "3qs_nqa_ioa_AAAB", "diao_kui": "sp6_k2v_4kg",
    "diao_mi": "sp6_k2v_4kg_A", "zhou_dan": "y4i_pjk_4gn_AD",
    "yi_yin": "itn_zi2_il4", "shao_gong": "7m7_qvm_4oj",
}
OLD_YIZHEN = "4ly_56b_ld0"
NEW_YIZHEN = IDS["yizhen"]


def same(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return set(a) == set(b) and all(same(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


def load(root, rel):
    return json.loads((Path(root) / rel).read_text(encoding="utf-8"))


def save(root, rel, value):
    (Path(root) / rel).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def frames(root):
    ch = load(root, CHAPTER)
    ps = {p["id"].rsplit(":", 1)[-1]: p for p in ch["paragraphs"]}
    return ch, ps


def ev(ch, p, **refs):
    return {"work_id": ch["work_id"], "book_id": ch["book_id"], "source_id": ch["source_id"],
            "chapter_id": CID, "paragraph_id": p["id"], "quote": p["text"], **refs}


def mentions(ps):
    return {m["id"].rsplit(":", 1)[-1]: m for p in ps.values() for m in p["mentions"]}


def _m(ps, pno, start, surface):
    p = ps[pno]
    return next(m for m in p["mentions"] if m["start"] == start and m["surface"] == surface)


def assertions(root):
    ch, ps = frames(root)
    specs = [
        ("yizhen-father-liuyu", NEW_YIZHEN, "father", IDS["liuyu"], "汝十歲兒", "p005", 85, "汝", 92, "車士",
         "明言「汝十歲兒」，後接「車士義真小字也」指明兒童即劉義真；以母親對劉裕說話中的「汝」作父親錨點。"),
        ("diao-mi-father-diaokui", IDS["diao_mi"], "father", IDS["diao_kui"], "刁逵子彌", "p005", 157, "刁逵", 160, "彌",
         "「刁逵子彌」逐字明載彌為刁逵之子；不推測其母。"),
        ("liuyu-younger-brother-daolian", IDS["liuyu"], "brother", IDS["daolian"], "道憐汝布衣兄弟；道憐年長", "p005", 34, "道憐", 36, "汝",
         "太后稱道憐與汝（劉裕）為布衣兄弟，劉裕又稱道憐年長；只記同輩及長幼方向，不推確切排行或共同父親姓名。"),
    ]
    out = []
    for key, subject, pred, object_, term, pno, os, ot, ss, st, note in specs:
        p = ps[pno]
        # The relation direction is child→father for parentage and younger→older for brothers.
        subject_mention = _m(ps, pno, ss, st)
        object_mention = _m(ps, pno, os, ot)
        if pred == "father":
            subject_mention, object_mention = subject_mention, object_mention
            qualifiers = {"lineage": "paternal", "source_child_term": "子" if key.startswith("diao") else "兒",
                          "source_child_sex": "male", "source_clause_binding": {
                              "kind": "fixed_wyd_song051_p004_p007_direct_family", "case": key}}
        else:
            qualifiers = {"lineage": "paternal", "shared_father": None, "subject_relative_age": "younger",
                          "source_clause_binding": {"kind": "fixed_wyd_song051_p004_p007_direct_family", "case": key}}
        qualifiers.update(source_term=term, interpretation_note=note)
        if key == "yizhen-father-liuyu":
            qualifiers["identity_bridge_mention_id"] = _m(ps, pno, 126, "義真")["id"]
            qualifiers["age_phrase_anchor"] = {"paragraph_id": p["id"], "start": 85, "end": 89, "surface": "汝十歲兒"}
        if key == "liuyu-younger-brother-daolian":
            qualifiers["age_order_anchor"] = {"paragraph_id": p["id"], "start": 106, "end": 110, "surface": "道憐年長"}
        evidence = [ev(ch, p, subject_person_mention_id=subject_mention["id"],
                       object_person_mention_id=object_mention["id"])]
        if key == "liuyu-younger-brother-daolian":
            # The biography head calls Daolian 高祖中弟; retain that same-work
            # kinship evidence alongside the later relative-age statement.
            evidence.insert(0, ev(ch, ps["p001"],
                                  subject_person_mention_id=_m(ps, "p001", 4, "道憐")["id"],
                                  object_person_mention_id=_m(ps, "p001", 6, "高祖")["id"]))
        out.append({"id": "a-song051-p004-p007-" + key, "subject_person_id": subject,
                    "predicate": pred, "object_person_id": object_, "status": "source_attested",
                    "qualifiers": qualifiers, "human_reviewed": False, "model": None,
                    "evidence": evidence})
    return {"format_version": "0.2", "record_type": "person_assertion_set", "chapter_id": CID, "assertions": out}


def name_components(root):
    ch, ps = frames(root)
    yizhen = _m(ps, "p005", 126, "義真")
    yizhen_xiaozhi = _m(ps, "p005", 124, "車士")
    diaomi = _m(ps, "p005", 160, "彌")
    p5 = ps["p005"]
    records = [
        {"id": "name-song051-p004-p007-yizhen", "person_id": NEW_YIZHEN, "surname": "劉", "ming": "義真",
         "xiaozhi": "車士", "additional_names": [], "chapter_id": CID, "paragraph_id": p5["id"],
         "person_mention_id": yizhen["id"], "quote": p5["text"], "source_term": "車士義真小字也",
         "status": "contextual_provisional", "human_reviewed": False, "model": None,
         "component_source_binding": {"kind": "fixed_wyd_song051_p004_p007_name_component", "case": "yizhen",
             "ming_anchor": {"paragraph_id": p5["id"], "start": 126, "end": 128, "surface": "義真"},
             "surname_basis": {"kind": "father_name_and_source_parentage", "assertion_id": "a-song051-p004-p007-yizhen-father-liuyu",
                 "source_name_record_id": "name-song051-external-fullname-gaozu"},
             "xiaozhi_anchor": {"paragraph_id": p5["id"], "start": 124, "end": 126, "surface": "車士"},
             "xiaozhi_marker_anchor": {"paragraph_id": p5["id"], "start": 128, "end": 130, "surface": "小字"},
             "paragraph_sha256": __import__("hashlib").sha256(p5["text"].encode()).hexdigest(),
             "source_revision": ch["source"]["revision_id"]},
         "xiaozhi_basis": {"kind": "explicit_xiaozhi_statement", "source_term": "車士義真小字也",
             "value_anchor": {"paragraph_id": p5["id"], "start": 124, "end": 126, "surface": "車士", "person_mention_id": yizhen_xiaozhi["id"]},
             "subject_anchor": {"paragraph_id": p5["id"], "start": 126, "end": 128, "surface": "義真", "person_mention_id": yizhen["id"]},
             "marker_anchor": {"paragraph_id": p5["id"], "start": 128, "end": 130, "surface": "小字"},
             "status": "source_attested", "human_reviewed": False,
             "rationale": "正文直書「車士義真小字也」，小字值為車士，主體為義真。"},
         "interpretation_note": "原文明記「車士義真小字也」：名義真、小字車士。姓劉依同句「汝十歲兒」所明父子關係及既存劉裕全名記錄恢復；不推出生年。"},
        {"id": "name-song051-p004-p007-diaomi", "person_id": IDS["diao_mi"], "surname": "刁", "ming": "彌",
         "additional_names": [], "chapter_id": CID, "paragraph_id": p5["id"], "person_mention_id": diaomi["id"],
         "quote": p5["text"], "source_term": "刁逵子彌", "status": "contextual_provisional",
         "human_reviewed": False, "model": None,
         "component_source_binding": {"kind": "fixed_wyd_song051_p004_p007_name_component", "case": "diao-mi",
             "ming_anchor": {"paragraph_id": p5["id"], "start": 160, "end": 161, "surface": "彌"},
             "surname_basis": {"kind": "same_clause_named_father", "assertion_id": "a-song051-p004-p007-diao-mi-father-diaokui",
                 "father_anchor": {"paragraph_id": p5["id"], "start": 157, "end": 159, "surface": "刁逵"}},
             "paragraph_sha256": __import__("hashlib").sha256(p5["text"].encode()).hexdigest(),
             "source_revision": ch["source"]["revision_id"]},
         "interpretation_note": "「刁逵子彌」明載父親刁逵與兒子彌；按父名恢復刁姓，不補母親或其他名。"},
    ]
    return {"format_version": "0.2", "record_type": "person_name_component_set", "chapter_id": CID, "records": records}


def identities(root):
    ch, ps = frames(root)
    specs = [
        ("yizhen-small-name", NEW_YIZHEN, ["車士", "義真"], [("p005", 92, "車士"), ("p005", 124, "車士"), ("p005", 126, "義真")],
         "「車士義真小字也」明言小字與本名同屬廬陵王義真；不把廬陵王作姓名。"),
        ("lu-zhongyuan-repeated-name", "jif_4nl_z1h", ["陸仲元", "仲元"], [("p005", 152, "陸仲元"), ("p005", 171, "仲元")],
         "同一守城情節中先稱陸仲元，後簡稱仲元；按本段上下文暫定同指，不據同名泛併其他篇人物。"),
        ("sima-fu-ceremony", "dkn_ge4_286_AAAC", ["安平王"], [("p006", 28, "安平王")],
         "「祭禮依晉太宰安平王故事」指晉安平王司馬孚作禮制先例；記本段具體所指，不把稱號升作姓名。"),
    ]
    out = []
    for key, pid, surfaces, refs, rationale in specs:
        rows = [_m(ps, pno, start, surface) for pno, start, surface in refs]
        p = ps[refs[0][0]]
        out.append({"id": "d-song051-p004-p007-" + key, "person_id": pid, "surfaces": surfaces,
                    "scope": "same_chapter", "chapter_ids": [CID], "status": "contextual_provisional",
                    "confidence_level": "high", "identification_basis": {"kind": "source_context",
                    "target_mention_ids": [m["id"] for m in rows]},
                    "evidence": [ev(ch, ps[pno]) for pno, _, _ in refs],
                    "rationale": rationale, "human_reviewed": False, "model": None})
    # The allusion 「伊邵」 is deliberately source-local: 伊 and 邵 are short references,
    # not global aliases. The mention target is recorded in a finite interpretation note.
    p = ps["p007"]
    m = _m(ps, "p007", 160, "邵")
    out.append({"id": "d-song051-p004-p007-yi-shao-allusion", "person_id": IDS["shao_gong"],
                "surfaces": ["邵"], "scope": "same_chapter", "chapter_ids": [CID],
                "status": "contextual_provisional", "confidence_level": "medium",
                "identification_basis": {"kind": "source_context", "target_mention_ids": [m["id"]]},
                "evidence": [ev(ch, p)],
                "rationale": "詔文以「姬旦」及「伊邵」並舉古代名臣；此處「邵」暫釋為召公奭。此解釋只限本條，不建立全庫通用異名。",
                "references": [{"title": "中國哲學書電子化計劃《宋書》卷五十一", "url": "https://ctext.org/wiki.pl?chapter=385158&if=gb",
                                "quote": "固以侔蹤姬旦方軌伊邵者矣", "scope": "received_contextual_allusion", "human_reviewed": False}],
                "human_reviewed": False, "model": None})
    return {"format_version": "0.2", "record_type": "person_identity_decision_set", "chapter_id": CID, "decisions": out}


def life_events(root):
    ch, ps = frames(root)
    liuyu = _m(ps, "p005", 134, "高祖")
    daolian = _m(ps, "p006", 10, "太傅")
    evidence_liuyu = [ev(ch, ps["p005"], person_mention_id=liuyu["id"])]
    evidence_daolian = [ev(ch, ps["p006"], person_mention_id=daolian["id"])]
    moe = {"title": "教育部《重編國語辭典修訂本》中國歷代年號表", "url": "https://dict.revised.moe.edu.tw/appendix.jsp?ID=3&page=2",
           "quote": "永初", "scope": "modern_era_year_equivalence_only", "columns": {"dynasty": "宋", "era_name": "永初", "first_year": "420", "last_year": "422"},
           "image_verified": False}
    yuanxi = {"title": "教育部《重編國語辭典修訂本》中國歷代年號表", "url": "https://dict.revised.moe.edu.tw/appendix.jsp?ID=3&page=2",
              "quote": "元熙", "scope": "modern_era_year_equivalence_only", "columns": {"dynasty": "東晉", "era_name": "元熙", "first_year": "419", "last_year": "420"},
              "image_verified": False}
    def nd(year, expression, original, evs, references, basis):
        return {"era": "CE", "era_year": year, "year": year, "year_numbering": "astronomical", "precision": "year",
                "calendar": "chinese_civil", "source_expression": expression, "original_quote": original,
                "evidence": evs, "references": references, "status": "editorial_provisional",
                "contextual_date_basis": basis, "rationale": "按本篇連續敘事及所引年號表換算；只記年份，不推月日以外的精度或出生年。",
                "reviewer": "Codex（AI代理）", "human_reviewed": False}
    events = [
        {"id": "le-song051-p004-p007-liuyu-death", "person_id": IDS["liuyu"], "event_type": "death",
         "status": "source_attested", "date_expression": "五月", "source_term": "五月宮車晏駕",
         "evidence": evidence_liuyu, "normalized_date": nd(422, "五月", ps["p005"]["text"], evidence_liuyu, [moe],
             {"kind": "consecutive_regnal_year_and_month", "paragraph_id": ps["p005"]["id"],
              "era_year_anchor": "永初二年", "sequence_anchor": "三年春", "month_anchor": "五月宮車晏駕"}),
         "interpretation_note": "本段先明書永初二年，後接「三年春」及五月崩逝；據宋永初年號表換算為422年。未推月日。",
         "reviewer": "Codex（AI代理）", "human_reviewed": False},
        {"id": "le-song051-p004-p007-daolian-death", "person_id": IDS["daolian"], "event_type": "death",
         "status": "source_attested", "date_expression": "六月", "source_term": "六月薨",
         "evidence": evidence_daolian, "normalized_date": nd(422, "六月", ps["p006"]["text"], evidence_daolian, [moe],
             {"kind": "consecutive_event_after_liu-yu-death", "prior_event_id": "le-song051-p004-p007-liuyu-death",
              "prior_month_anchor": "五月宮車晏駕", "death_month_anchor": "六月薨"}),
         "interpretation_note": "正文承劉裕永初三年五月崩逝，續記道憐不克臨喪、六月薨；按永初三年換算為422年。六月為原文所載月份；不推精確日。",
         "reviewer": "Codex（AI代理）", "human_reviewed": False},
    ]
    return {"format_version": "0.1", "record_type": "person_life_event_assertion_set", "chapter_id": CID, "events": events}


def holding_valid(record, chapter, root=None):
    """Validate a p004–p007 holding against its exact source anchor and schema."""
    try:
        from scripts.song051_p004_p007 import materialize
    except ImportError:
        from song051_p004_p007 import materialize
    try:
        _, expected = materialize(copy.deepcopy(chapter))
        expected = next(row for row in expected if row["id"] == record["id"])
        actual = copy.deepcopy(record)
        # These are the separately source-bound date enrichments generated by
        # this module; compare the base title assertion to the fixed source row.
        role = actual["source_career_role"]
        role.pop("textual_variant_reference", None)
        actual["effective_period"]["start"].pop("normalized_date", None)
        return same(actual, expected)
    except (KeyError, TypeError, ValueError, StopIteration):
        return False


def source_title_use_valid(record, chapter):
    try:
        from scripts.song051_p004_p007 import materialize
    except ImportError:
        from song051_p004_p007 import materialize
    try:
        expected, _ = materialize(copy.deepcopy(chapter))
        target = next(row for row in expected if row["id"] == record["id"])
        return same(record, target)
    except (KeyError, TypeError, ValueError, StopIteration):
        return False


def life_event_valid(record, root):
    try:
        expected = {row["id"]: row for row in life_events(root)["events"]}[record["id"]]
        return same(record, expected)
    except (KeyError, TypeError, ValueError, StopIteration):
        return False


def normalized_date_valid(date, bound_record, bound_role, root, chapters):
    """Validate the fixed p004–p007 date decisions against source-bound records."""
    try:
        mapping = date.get("regnal_year_mapping", {})
        kind = mapping.get("kind")
        if kind == "fixed_wyd_song051_p004_p007_title_date":
            year, expression = 419, "元熙元年"
            era = "元熙"
        elif kind == "fixed_wyd_song051_p004_p007_accession_date":
            year, expression = 420, "高祖受命"
            era = "永初"
        elif kind == "fixed_wyd_song051_p004_p007_posthumous_date":
            year, expression = 422, "六月"
            era = "永初"
        else:
            if bound_role != "life_event":
                return False
            expected = {row["id"]: row for row in life_events(root)["events"]}[bound_record["id"]]["normalized_date"]
            return same(date, expected)
        if bound_role not in ("start", "end") or not isinstance(bound_record, dict):
            return False
        period = bound_record.get("effective_period", {})
        actual = period.get(bound_role, {}).get("normalized_date")
        if not same(date, actual):
            return False
        paragraph_id = bound_record["source_career_role"]["paragraph_id"]
        cid = paragraph_id.split(":", 1)[0]
        chapter = chapters.get(cid)
        para = next(p for p in chapter["paragraphs"] if p["id"] == paragraph_id)
        return (date.get("era") == "CE" and date.get("year") == year == date.get("era_year")
                and date.get("year_numbering") == "astronomical" and date.get("precision") == "year"
                and date.get("calendar") == "chinese_civil"
                and date.get("source_expression") == expression
                and date.get("original_quote") == para["text"]
                and date.get("status") == "editorial_provisional"
                and date.get("human_reviewed") is False
                and date.get("reviewer") == "Codex（AI代理）"
                and date.get("references") and isinstance(date.get("evidence"), list)
                and bool(date.get("rationale")) and mapping.get("era_name") == era
                and mapping.get("year") == year)
    except (KeyError, TypeError, ValueError, StopIteration):
        return False


def variant_review(root):
    ch, ps = frames(root)
    p = ps["p004"]
    return {"format_version": "0.1", "record_type": "source_text_variant_review",
            "chapter_id": CID, "paragraph_id": p["id"], "source_revision": ch["source"]["revision_id"],
            "base_witness": {"title": "宋書卷五十一清乾隆四年武英殿本數位轉錄",
                             "url": ch["source"]["url"], "quote": "元興元年", "start": 174, "end": 178,
                             "raw_sha256": ch["source"]["raw_sha256"], "image_verified": False},
            "comparative_witnesses": [
                {"title": "中國哲學書電子化計劃《宋書》卷五十一列傳第十一宗室", "url": "https://ctext.org/wiki.pl?chapter=385158&if=gb",
                 "quote": "元熙元年，解尚書令，進位司空", "scope": "digital_text_comparison", "image_verified": False},
                {"title": "識典古籍《宋書》卷五十一", "url": "https://www.shidianguji.com/zh/book/SK0713/chapter/1lxkvukjswm5u",
                 "quote": "元熙元年", "scope": "digital_text_comparison", "image_verified": False}],
            "editorial_assessment": {"status": "probable_transcription_variant", "preferred_reading": "元熙元年",
                "normalized_ce_year": 419,
                "rationale": "兩個數位對讀本均作元熙元年，且宋司空授任敘事置於受命前；本庫仍保留指定武英殿轉錄原字「元興」，不宣稱已核影印頁。僅在可追溯的紀年欄暫採元熙元年換算。",
                "references": [{"title": "教育部《重編國語辭典修訂本》中國歷代年號表",
                                "url": "https://dict.revised.moe.edu.tw/appendix.jsp?ID=3&page=2",
                                "quote": "元熙", "columns": {"dynasty": "東晉", "era_name": "元熙", "first_year": "419", "last_year": "420"},
                                "scope": "modern_era_year_equivalence_only", "image_verified": False}],
                "human_reviewed": False, "reviewer": "Codex（AI代理）"},
            "human_reviewed": False}


def enrich_title_holdings(root):
    root = Path(root)
    ch, ps = frames(root)
    path = root / "corpus/songshu/051-wyd1739-p004-p007-titles.json"
    doc = json.loads(path.read_text(encoding="utf-8"))
    variant_path = "source-evidence/song051-wyd1739-zongshi/p004-p007-variant-review.json"
    variant = variant_review(root)
    save(root, variant_path, variant)
    variant_sha = hashlib.sha256((root / variant_path).read_bytes()).hexdigest()
    yuanxi_ref = {"title": "教育部《重編國語辭典修訂本》中國歷代年號表", "url": "https://dict.revised.moe.edu.tw/appendix.jsp?ID=3&page=2",
                  "quote": "元熙", "scope": "modern_era_year_equivalence_only",
                  "columns": {"dynasty": "東晉", "era_name": "元熙", "first_year": "419", "last_year": "420"},
                  "image_verified": False}
    yongchu_ref = {"title": "教育部《重編國語辭典修訂本》中國歷代年號表", "url": "https://dict.revised.moe.edu.tw/appendix.jsp?ID=3&page=2",
                   "quote": "永初", "scope": "modern_era_year_equivalence_only",
                   "columns": {"dynasty": "宋", "era_name": "永初", "first_year": "420", "last_year": "422"},
                   "image_verified": False}
    for h in doc["holdings"]:
        pno = h["source_career_role"]["paragraph_id"].rsplit(":", 1)[-1]
        p = ps[pno]
        m = next(m for m in p["mentions"] if m["id"] == h["source_career_role"]["subject_mention_id"])
        year = None
        expression = None
        mapping = None
        refs = []
        if pno == "p004" and h["title"] == "司空":
            year, expression, refs = 419, "元熙元年", [yuanxi_ref]
            mapping = {"kind": "fixed_wyd_song051_p004_p007_title_date", "era_name": "元熙", "year": 419,
                       "variant_review_path": variant_path, "variant_review_sha256": variant_sha,
                       "base_reading": "元興元年", "comparative_reading": "元熙元年"}
            h["source_career_role"]["textual_variant_reference"] = {"path": variant_path, "sha256": variant_sha}
        elif pno == "p004" and h["title"] in ("太尉", "長沙王"):
            year, expression, refs = 420, "高祖受命", [yongchu_ref]
            mapping = {"kind": "fixed_wyd_song051_p004_p007_accession_date", "era_name": "永初", "year": 420,
                       "accession_anchor": "高祖受命"}
        elif pno == "p006" and h["mode"] == "posthumous_grant":
            year, expression, refs = 422, "六月", [yongchu_ref]
            mapping = {"kind": "fixed_wyd_song051_p004_p007_posthumous_date", "era_name": "永初", "year": 422,
                       "death_event_id": "le-song051-p004-p007-daolian-death", "death_month_anchor": "六月薨"}
        if year is None:
            continue
        evs = h["evidence"]
        h["effective_period"]["start"]["normalized_date"] = {
            "era": "CE", "era_year": year, "year": year, "year_numbering": "astronomical",
            "precision": "year", "calendar": "chinese_civil", "source_expression": expression,
            "original_quote": p["text"], "evidence": evs, "references": refs,
            "regnal_year_mapping": mapping, "status": "editorial_provisional",
            "rationale": "官爵起授年份按同篇明載事件與年號對照作暫定換算；保留未明月日，不延伸任期終年。",
            "reviewer": "Codex（AI代理）", "human_reviewed": False}
    save(root, "corpus/songshu/051-wyd1739-p004-p007-titles.json", doc)


def ages(root):
    ch, ps = frames(root)
    def record(ident, pid, value, number, term, pno, mid, note, **extra):
        p = ps[pno]
        base = {"id": ident, "person_id": pid, "value": value, "source_number": number, "source_term": term,
                "unit": "source_age_years", "counting": "unspecified_source_age", "birth_year": None,
                "status": "source_attested", "date_expression": None,
                "evidence": [ev(ch, p, person_mention_id=mid)], "age_context": {"kind": "during_life"},
                "interpretation_note": note, "reviewer": "Codex（AI代理）", "human_reviewed": False, "model": None}
        base.update(extra)
        return base
    return [
        record("age-song051-p004-p007-yizhen-ten", NEW_YIZHEN, 10, "十", "十歲", "p005", _m(ps,"p005",126,"義真")["id"],
               "太后稱劉裕之兒十歲；「車士義真小字也」確認其人為義真。原文未交代計歲法與確切報齡日期，不倒推生年。"),
        record("age-song051-p004-p007-daolian-over-fifty", IDS["daolian"], None, "五十", "年出五十", "p005", _m(ps,"p005",75,"道憐")["id"],
               "「年出五十」只表逾五十歲，作開放下界，不改成精確五十或推生年。",
               reporting_status="direct_report", bounds={"lower": 50, "lower_inclusive": False, "upper": None, "upper_inclusive": None}),
        record("age-song051-p004-p007-daolian-fifty-five", IDS["daolian"], 55, "五十五", "年五十五", "p006", _m(ps,"p006",10,"太傅")["id"],
               "本傳明載道憐六月薨、年五十五；與其卒年事件相連，但不倒推出生年或計歲法。",
               age_context={"kind": "at_death", "life_event_id": "le-song051-p004-p007-daolian-death"}),
    ]


def _rekey_sources(root):
    root = Path(root)
    people_doc = load(root, "registry/persons.json")
    old = next((p for p in people_doc["persons"] if p["id"] == OLD_YIZHEN), None)
    if old:
        if any(p["id"] == NEW_YIZHEN for p in people_doc["persons"]):
            raise ValueError("廬陵王義真目標 ID 已被佔用")
        import sys
        if str(root) not in sys.path:
            sys.path.insert(0, str(root))
        from scripts.consolidate_person_ids import reference_files, rewrite
        mapping = {OLD_YIZHEN: NEW_YIZHEN}
        for original in reference_files(root):
            data = json.loads(original.read_text(encoding="utf-8"))
            updated = rewrite(data, mapping)
            if original.name == "persons.json" and original.parent.name == "registry":
                target = next(p for p in updated["persons"] if p["id"] == OLD_YIZHEN)
                target["id"] = NEW_YIZHEN
                target["label"] = "劉義真"
                target.pop("id_aliases", None)
            save(root, original.relative_to(root), updated)


def _register_mentions(root):
    ch, ps = frames(root)
    path = Path(root) / "registry/persons.json"
    doc = json.loads(path.read_text(encoding="utf-8"))
    people = {p["id"]: p for p in doc["persons"]}
    if IDS["diao_mi"] not in people:
        diao = {"id": IDS["diao_mi"], "label": "刁彌", "status": "active",
                "historicity": "historical_tradition", "aliases": [], "evidence": [],
                "identity_review": {"status": "source_local_provisional", "human_reviewed": False,
                                    "note": "依《宋書》卷五十一「刁逵子彌」建立來源局部人物；待全卷及跨史料覆核。"}}
        doc["persons"].append(diao)
        people[diao["id"]] = diao
    # The old ID is retired only after the typed references were migrated above.
    if OLD_YIZHEN in people:
        raise ValueError("舊人物 ID 尚未完成全庫引用遷移")
    paragraph_prefixes = tuple(f"{CID}:{pno}" for pno in ("p004", "p005", "p006", "p007"))
    for p in doc["persons"]:
        # Replace only the changed chapter occurrences inside an alias. Other
        # chapters sharing a short surface (弘、伊、王, etc.) remain intact.
        aliases = []
        for alias in p.get("aliases", []):
            kept_ids = [mid for mid in alias.get("mention_ids", [])
                        if not mid.startswith(paragraph_prefixes)]
            if kept_ids:
                aliases.append({**alias, "mention_ids": kept_ids})
        p["aliases"] = aliases
        p["evidence"] = [e for e in p.get("evidence", [])
                         if not e.get("mention_id", "").startswith(paragraph_prefixes)]
    title_mention_ids = {u.get("person_mention_id") for u in ch.get("annotation", {}).get("source_title_uses", [])}
    for pno in ("p004", "p005", "p006", "p007"):
        p = ps[pno]
        for m in p["mentions"]:
            if m.get("kind") != "person":
                continue
            # Titles, offices and ruler references can still link to a person
            # in the reading text, but they are not personal-name aliases.
            if m["id"] in title_mention_ids:
                person = people[m["person_id"]]
                evidence = {"work_id": ch["work_id"], "book_id": ch["book_id"], "chapter_id": CID,
                            "source_id": ch["source_id"], "paragraph_id": p["id"],
                            "mention_id": m["id"], "quote": m["surface"]}
                if evidence not in person["evidence"]:
                    person["evidence"].append(evidence)
                continue
            person = people[m["person_id"]]
            alias = next((a for a in person["aliases"] if a["surface"] == m["surface"]), None)
            if alias is None:
                alias = {"surface": m["surface"], "mention_ids": []}
                person["aliases"].append(alias)
            if m["id"] not in alias["mention_ids"]:
                alias["mention_ids"].append(m["id"])
            evidence = {"work_id": ch["work_id"], "book_id": ch["book_id"], "chapter_id": CID,
                        "source_id": ch["source_id"], "paragraph_id": p["id"], "mention_id": m["id"], "quote": m["surface"]}
            if evidence not in person["evidence"]:
                person["evidence"].append(evidence)
    save(root, "registry/persons.json", doc)


def _assemblies(root, rels):
    path = Path(root) / "registry/family-assemblies.json"
    doc = json.loads(path.read_text(encoding="utf-8"))
    assemblies = doc["assemblies"]
    liu = next(a for a in assemblies if a["id"] == "family-song041-qiao")
    yizhen = {"person_id": NEW_YIZHEN, "representative_source_person_id": NEW_YIZHEN,
              "source_person_ids": [NEW_YIZHEN], "identity_equivalence_decision_ids": [],
              "parent_person_id": IDS["liuyu"], "source_assertion_id": rels["assertions"][0]["id"]}
    liu["members"] = [m for m in liu["members"] if m["person_id"] != NEW_YIZHEN] + [yizhen]
    diao_id = "family-song051-diao-kui"
    diao = next((a for a in assemblies if a["id"] == diao_id), None)
    if diao is None:
        assemblies.append({"id": diao_id, "root_person_id": IDS["diao_kui"], "label": "宋刁氏：逵、彌父系",
                           "status": "editorial_preferred", "human_reviewed": False, "reviewer": "Codex（AI代理）",
                           "rationale": "依《宋書》卷五十一「刁逵子彌」建立可回查的父子路徑；本資料不推彌之母或其他兄弟。",
                           "members": [
                               {"person_id": IDS["diao_kui"], "representative_source_person_id": IDS["diao_kui"],
                                "source_person_ids": [IDS["diao_kui"]], "identity_equivalence_decision_ids": [],
                                "parent_person_id": None, "source_assertion_id": None},
                               {"person_id": IDS["diao_mi"], "representative_source_person_id": IDS["diao_mi"],
                                "source_person_ids": [IDS["diao_mi"]], "identity_equivalence_decision_ids": [],
                                "parent_person_id": IDS["diao_kui"], "source_assertion_id": rels["assertions"][1]["id"]}]})
    save(root, "registry/family-assemblies.json", doc)


def install(root):
    root = Path(root)
    _rekey_sources(root)
    rels = assertions(root)
    names = name_components(root)
    ids = identities(root)
    lives = life_events(root)
    enrich_title_holdings(root)
    save(root, "corpus/songshu/051-wyd1739-p004-p007-assertions.json", rels)
    save(root, "corpus/songshu/051-wyd1739-p004-p007-name-components.json", names)
    save(root, "corpus/songshu/051-wyd1739-p004-p007-identities.json", ids)
    save(root, "corpus/songshu/051-wyd1739-p004-p007-life-events.json", lives)
    ch = load(root, CHAPTER)
    previous = ch["annotation"].get("age_assertions", [])
    ch["annotation"]["age_assertions"] = [a for a in previous if not a.get("id", "").startswith("age-song051-p004-p007-")] + ages(root)
    ch["annotation"]["age_assertions"].sort(key=lambda a: a["id"])
    # Keep the established p014–p017 fixed annotation contract as the base;
    # this independent p004–p007 layer is an additive projection.
    try:
        from scripts.wyd_song051_yixin import collect, contract, phase_chapter
    except ImportError:
        from wyd_song051_yixin import collect, contract, phase_chapter
    prior = phase_chapter(contract(root), collect(ch, contract(root)), root)
    for key in ("source_title_uses", "age_assertions"):
        extras = [x for x in ch["annotation"].get(key, [])
                  if x.get("id", "").startswith(("tu-song051-p004-p007-", "age-song051-p004-p007-"))]
        prior["annotation"][key] = [x for x in prior["annotation"].get(key, [])
                                     if x.get("id") not in {y.get("id") for y in extras}] + extras
    ch["annotation"] = prior["annotation"]
    save(root, CHAPTER, ch)
    _register_mentions(root)
    _assemblies(root, rels)


def assertion_valid(record, root):
    try:
        expected = {a["id"]: a for a in assertions(root)["assertions"]}[record["id"]]
        return same(record, expected)
    except (KeyError, TypeError, ValueError, StopIteration):
        return False


def component_valid(record, root):
    try:
        expected = {n["id"]: n for n in name_components(root)["records"]}[record["id"]]
        return same(record, expected)
    except (KeyError, TypeError, ValueError, StopIteration):
        return False


def identity_valid(record, root):
    try:
        expected = {d["id"]: d for d in identities(root)["decisions"]}[record["id"]]
        return same(record, expected)
    except (KeyError, TypeError, ValueError, StopIteration):
        return False


def life_valid(record, root):
    try:
        expected = {e["id"]: e for e in life_events(root)["events"]}[record["id"]]
        return same(record, expected)
    except (KeyError, TypeError, ValueError, StopIteration):
        return False
