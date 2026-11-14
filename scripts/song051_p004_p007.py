"""Materialize the first-pass personal references in Songshu 51, p004–p007.

All positions are Unicode code-point offsets in the fixed Wuyingdian digital
transcription.  This does not claim the transcription has been image-verified.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

CID = "c-songshu-051-wyd1739-zongshi"
CHAPTER = "corpus/songshu/051-wyd1739.json"
IDS = {
    "daolian": "3qs_nqa_ioa_AAB",
    "liuyu": "3qs_nqa_ioa_AAA",
    "yizhen": "3qs_nqa_ioa_AAAB",
    "yilong": "3qs_nqa_ioa_AAAA",
    "wen_shou": "ph1_ms8_hyq_AA",
    "xiuzhi": "pcf_gg0_ena",
    "lu_zhongyuan": "jif_4nl_z1h",
    "diao_kui": "sp6_k2v_4kg",
    "diao_mi": "sp6_k2v_4kg_A",
    "sima_fu": "dkn_ge4_286_AAAC",
    "daogui": "3qs_nqa_ioa_AAC",
    "muzhi": "255_233_b52",
    "wang_hong": "7r6_k52_qji_ABAAAAA",
    "daoji": "w8z_nph_trk",
    "zhene": "quq_d6y_akf",
    "zhou_dan": "y4i_pjk_4gn_AD",
    "yi_yin": "itn_zi2_il4",
    "shao_gong": "7m7_qvm_4oj",
}

# (paragraph, start, surface, person key or None, usage)
# usage: name, title, office, rank, pronoun, unresolved
SPECS = [
    ("p004", 9, "司馬休之", "xiuzhi", "name"),
    ("p004", 13, "道憐", "daolian", "name"),
    ("p004", 76, "道憐", "daolian", "name"),
    ("p004", 15, "監留府事", "daolian", "office"),
    ("p004", 30, "都督荆湘益秦寧梁雍七州諸軍", "daolian", "office"),
    ("p004", 43, "驃騎將軍", "daolian", "office"),
    ("p004", 47, "開府儀同三司", "daolian", "office"),
    ("p004", 53, "鎮護南蠻校尉", "daolian", "office"),
    ("p004", 59, "荆州刺史", "daolian", "office"),
    ("p004", 63, "持節", "daolian", "office"),
    ("p004", 65, "常侍", "daolian", "office"),
    ("p004", 94, "高祖", "liuyu", "title"),
    ("p004", 102, "之", "daolian", "pronoun"),
    ("p004", 126, "高祖", "liuyu", "title"),
    ("p004", 137, "道憐", "daolian", "name"),
    ("p004", 141, "侍中", "daolian", "office"),
    ("p004", 143, "都督徐兗青三州揚州之晉陵諸軍事", "daolian", "office"),
    ("p004", 158, "守尚書令", "daolian", "office"),
    ("p004", 162, "徐兗二州刺史", "daolian", "office"),
    ("p004", 168, "持節", "daolian", "office"),
    ("p004", 170, "將軍", "daolian", "office"),
    ("p004", 179, "尚書令", "daolian", "office"),
    ("p004", 184, "司空", "daolian", "office"),
    ("p004", 190, "高祖", "liuyu", "title"),
    ("p004", 196, "太尉", "daolian", "office"),
    ("p004", 199, "長沙王", "daolian", "rank"),
    ("p004", 207, "持節", "daolian", "office"),
    ("p004", 209, "侍", "daolian", "office"),
    ("p005", 0, "中", "daolian", "office"),
    ("p005", 19, "廬陵王", "yizhen", "rank"),
    ("p005", 22, "義真", "yizhen", "name"),
    ("p005", 25, "揚州刺史", "yizhen", "office"),
    ("p005", 29, "太后", "wen_shou", "title"),
    ("p005", 32, "上", "liuyu", "title"),
    ("p005", 34, "道憐", "daolian", "name"),
    ("p005", 36, "汝", "liuyu", "pronoun"),
    ("p005", 46, "上", "liuyu", "title"),
    ("p005", 48, "寄奴", "liuyu", "name"),
    ("p005", 51, "道憐", "daolian", "name"),
    ("p005", 68, "道憐", "daolian", "name"),
    ("p005", 72, "太后", "wen_shou", "title"),
    ("p005", 75, "道憐", "daolian", "name"),
    ("p005", 85, "汝", "liuyu", "pronoun"),
    ("p005", 90, "上", "liuyu", "title"),
    ("p005", 92, "車士", "yizhen", "name"),
    ("p005", 104, "寄奴", "liuyu", "name"),
    ("p005", 106, "道憐", "daolian", "name"),
    ("p005", 119, "太后", "wen_shou", "title"),
    ("p005", 124, "車士", "yizhen", "name"),
    ("p005", 126, "義真", "yizhen", "name"),
    ("p005", 134, "高祖", "liuyu", "title"),
    ("p005", 145, "道憐", "daolian", "name"),
    ("p005", 150, "司馬", "lu_zhongyuan", "office"),
    ("p005", 152, "陸仲元", "lu_zhongyuan", "name"),
    ("p005", 157, "刁逵", "diao_kui", "name"),
    ("p005", 160, "彌", "diao_mi", "name"),
    ("p005", 171, "仲元", "lu_zhongyuan", "name"),
    ("p005", 175, "之", "diao_mi", "pronoun"),
    ("p005", 180, "陳豔", None, "unresolved"),
    ("p005", 183, "彌", "diao_mi", "name"),
    ("p005", 203, "道憐", "daolian", "name"),
    ("p006", 10, "太傅", "daolian", "office"),
    ("p006", 12, "持節", "daolian", "office"),
    ("p006", 14, "侍中", "daolian", "office"),
    ("p006", 16, "都督", "daolian", "office"),
    ("p006", 18, "刺史", "daolian", "office"),
    ("p006", 26, "太宰", "sima_fu", "office"),
    ("p006", 28, "安平王", "sima_fu", "rank"),
    ("p006", 60, "太祖", "yilong", "title"),
    ("p006", 136, "先皇", "liuyu", "title"),
    ("p006", 155, "聖明", "yilong", "title"),
    ("p006", 178, "使持節", "daolian", "office"),
    ("p006", 181, "侍中", "daolian", "office"),
    ("p006", 183, "都督南徐兗二州揚州之晉陵京口諸軍事", "daolian", "office"),
    ("p006", 200, "太傅", "daolian", "office"),
    ("p006", 202, "南徐兗二州刺史", "daolian", "office"),
    ("p006", 209, "長", "daolian", "rank"),
    ("p007", 0, "沙景王", "daolian", "rank"),
    ("p007", 4, "侍中", "daogui", "office"),
    ("p007", 6, "大司馬", "daogui", "office"),
    ("p007", 9, "臨川烈武王", "daogui", "rank"),
    ("p007", 15, "司徒", "muzhi", "office"),
    ("p007", 17, "南康文宣公", "muzhi", "rank"),
    ("p007", 22, "穆之", "muzhi", "name"),
    ("p007", 24, "侍中", "wang_hong", "office"),
    ("p007", 26, "衞將軍", "wang_hong", "office"),
    ("p007", 29, "開府儀同三司", "wang_hong", "office"),
    ("p007", 35, "錄尚書事", "wang_hong", "office"),
    ("p007", 39, "揚州刺史", "wang_hong", "office"),
    ("p007", 43, "華容縣開國公", "wang_hong", "rank"),
    ("p007", 49, "弘", "wang_hong", "name"),
    ("p007", 50, "使持節", "daoji", "office"),
    ("p007", 53, "散騎常侍", "daoji", "office"),
    ("p007", 57, "都督江州豫州西陽新蔡晉熙四郡軍事", "daoji", "office"),
    ("p007", 73, "征南大將軍", "daoji", "office"),
    ("p007", 78, "開府儀同三司", "daoji", "office"),
    ("p007", 84, "江州刺史", "daoji", "office"),
    ("p007", 88, "永修縣開國公", "daoji", "rank"),
    ("p007", 94, "道濟", "daoji", "name"),
    ("p007", 97, "將軍", "zhene", "office"),
    ("p007", 99, "青州刺史", "zhene", "office"),
    ("p007", 103, "龍陽縣開國侯", "zhene", "rank"),
    ("p007", 109, "鎮惡", "zhene", "name"),
    ("p007", 155, "姬旦", "zhou_dan", "name"),
    ("p007", 159, "伊", "yi_yin", "name"),
    ("p007", 160, "邵", "shao_gong", "name"),
]

def _paragraphs(chapter):
    return {p["id"].rsplit(":", 1)[-1]: p for p in chapter["paragraphs"]}

def _evidence(chapter, p, mention_id):
    return {
        "work_id": chapter["work_id"], "book_id": chapter["book_id"],
        "source_id": chapter["source_id"], "chapter_id": CID,
        "paragraph_id": p["id"], "quote": p["text"],
        "person_mention_id": mention_id,
    }

def materialize(chapter):
    """Return fresh mention lists and title-use rows without changing text."""
    ps = _paragraphs(chapter)
    grouped = {p: [] for p in ("p004", "p005", "p006", "p007")}
    for pno, start, surface, person_key, usage in SPECS:
        p = ps[pno]
        end = start + len(surface)
        if p["text"][start:end] != surface:
            raise ValueError(f"固定人物錨與底文不符：{pno} {start} {surface}")
        mention = {"start": start, "end": end, "surface": surface}
        if usage == "pronoun":
            mention.update(kind="pronoun", person_id=IDS[person_key], status="contextual_provisional",
                           interpretation_note="依本段發言對象與敘事語境辨其所指；保留代詞類型，不列入姓名異稱。")
        elif usage == "unresolved":
            mention.update(kind="unresolved", person_id=None, status="unresolved",
                           interpretation_note="武英殿數位轉錄作「陳豔」，識典古籍數位文本作「陳㹠」；字形及其是否能與已知人物同一，均待核，不接人物 ID。")
        else:
            mention.update(kind="person", person_id=IDS[person_key])
        grouped[pno].append((start, mention, usage))

    title_uses = []
    title_records = []
    for pno, rows in grouped.items():
        rows.sort(key=lambda row: row[0])
        cursor = 0
        p = ps[pno]
        p["mentions"] = []
        for i, (start, mention, usage) in enumerate(rows):
            if start < cursor:
                raise ValueError(f"人物錨重疊：{pno} {start}")
            cursor = mention["end"]
            mention["id"] = f"{p['id']}:m{i:04d}"
            p["mentions"].append(mention)
            compound_id = None
            if (pno, start, mention["surface"]) in (("p004", 209, "侍"), ("p005", 0, "中")):
                compound_id = "th-song051-p004-p007-composite-shizhong"
            elif (pno, start, mention["surface"]) in (("p006", 209, "長"), ("p007", 0, "沙景王")):
                compound_id = "th-song051-p004-p007-composite-changsha"
            if usage in ("office", "rank"):
                holding_id = f"th-song051-p004-p007-{pno}-{i:04d}"
                if compound_id:
                    title_uses.append(_title_use(chapter, p, mention, compound_id, usage))
                else:
                    title_records.append(_holding(chapter, p, mention, holding_id, usage))
                    title_uses.append(_title_use(chapter, p, mention, holding_id, usage))
            elif usage == "title":
                title_uses.append(_title_use(chapter, p, mention, None, usage))
        p["annotation_status"] = "named_mentions_first_pass"
    title_records.extend((_composite_holding(chapter, ps, "th-song051-p004-p007-composite-shizhong"),
                          _composite_holding(chapter, ps, "th-song051-p004-p007-composite-changsha")))
    return title_uses, title_records

def _composite_holding(chapter, paragraphs, ident):
    if ident.endswith("shizhong"):
        title = "侍中"
        parts = [("p004", 209, "侍"), ("p005", 0, "中")]
    else:
        title = "長沙景王"
        parts = [("p006", 209, "長"), ("p007", 0, "沙景王")]
    anchors, evidence, attestations = [], [], []
    for pno, start, surface in parts:
        p = paragraphs[pno]
        m = next(m for m in p["mentions"] if m["start"] == start and m["surface"] == surface)
        anchors.append({"paragraph_id": p["id"], "start": start, "end": start + len(surface), "surface": surface,
                        "person_mention_id": m["id"]})
        evidence.append(_evidence(chapter, p, m["id"]))
        attestations.append({"id": f"att-{ident}-{pno}", "paragraph_id": p["id"], "start": start,
                             "end": start + len(surface), "surface": surface, "person_mention_id": m["id"],
                             "usage": "narrative", "date_expression": None})
    start = {"status": "unknown", "date_expression": None, "evidence": []}
    end = copy.deepcopy(start)
    return {"id": ident, "person_id": IDS["daolian"], "title": title,
            "kind": "noble_rank" if title == "長沙景王" else "office", "mode": "attestation",
            "status": "source_attested", "appointment_role": "source_report",
            "source_career_role": {"kind": "fixed_wyd_song051_p004_p007_composite_title",
                "record_id": ident, "paragraph_id": anchors[0]["paragraph_id"],
                "subject_mention_id": anchors[0]["person_mention_id"], "source_anchors": anchors,
                "source_revision": chapter["source"]["revision_id"], "human_reviewed": False},
            "evidence": evidence, "attestations": attestations,
            "effective_period": {"start": start, "end": end},
            "interpretation_note": "稱號跨篇章段界，依前段末字與後段首字連讀；底文及兩處人物提及各自保留原位。",
            "reviewer": "Codex（AI代理）", "human_reviewed": False, "model": None}

def _title_use(chapter, p, m, holding_id, usage):
    basis = {"office": "source_attested_office_reference", "rank": "source_attested_rank_reference",
             "title": "contextual_person_title_reference"}[usage]
    return {
        "id": f"tu-song051-p004-p007-{m['id'].rsplit(':',1)[-1]}-{p['id'].rsplit(':',1)[-1]}",
        "person_id": m["person_id"], "person_mention_id": m["id"],
        "source_term": m["surface"],
        "source_anchor": {"paragraph_id": p["id"], "start": m["start"], "end": m["end"], "surface": m["surface"]},
        "usage_kind": "title_reference", "holding_ids": [holding_id] if holding_id else [],
        "evidence": [_evidence(chapter, p, m["id"])],
        "source_use_binding": {
            "kind": "fixed_wyd_song051_p004_p007_title_reference",
            "basis": basis,
            "interpretation_note": "本次標註依局部敘事／詔文所指具體人物；原詞保留為稱謂或職爵，不作姓名別名。",
        },
        "human_reviewed": False,
    }

def _holding(chapter, p, m, hid, usage):
    title = m["surface"]
    kind = "noble_rank" if usage == "rank" else ("honorific" if title in ("持節", "使持節") else "office")
    mode = "attestation"
    date = None
    context_start = max(0, m["start"] - 14)
    context_end = min(len(p["text"]), m["end"] + 14)
    context = p["text"][context_start:context_end]
    if p["id"].endswith(":p004"):
        text = p["text"]
        milestones = [(text.find(term), term) for term in ("江陵平以為", "徵道憐還為", "元興元年", "高祖受命")]
        prior = [(pos, term) for pos, term in milestones if 0 <= pos < m["start"]]
        nearest = max(prior, default=(-1, None))[1]
        if nearest == "江陵平以為":
            mode, date = "grant", "江陵平"
        elif nearest == "徵道憐還為":
            mode, date = "grant", "徵道憐還"
        elif nearest == "元興元年":
            mode, date = ("grant" if title == "司空" else "attestation"), "元興元年"
        elif nearest == "高祖受命":
            mode, date = "grant", "高祖受命"
    elif p["id"].endswith(":p006") and "追贈" in p["text"][max(0,m["start"]-8):m["start"]]:
        mode = "posthumous_grant" if title == "太傅" else "attestation"
        date = "六月"
    evidence = [_evidence(chapter, p, m["id"])]
    if mode == "attestation": start = {"status": "unknown", "date_expression": None, "evidence": []}
    else: start = {"status": "source_event", "event_type": mode, "date_expression": date, "evidence": evidence}
    unknown = {"status": "unknown", "date_expression": None, "evidence": []}
    return {
        "id": hid, "person_id": m["person_id"], "title": title, "kind": kind, "mode": mode,
        "status": "source_attested", "appointment_role": "source_report",
        "source_career_role": {
            "kind": "fixed_wyd_song051_p004_p007_title",
            "record_id": hid, "paragraph_id": p["id"], "subject_mention_id": m["id"],
            "source_anchor": {"paragraph_id": p["id"], "start": m["start"], "end": m["end"], "surface": title},
            "context_anchor": {"paragraph_id": p["id"], "start": context_start, "end": context_end, "surface": context},
            "source_revision": chapter["source"]["revision_id"], "human_reviewed": False,
        },
        "evidence": evidence,
        "attestations": [{"id": "att-" + hid, "paragraph_id": p["id"], "start": m["start"], "end": m["end"],
                          "surface": title, "person_mention_id": m["id"], "usage": "narrative", "date_expression": date}],
        "effective_period": {"start": start, "end": copy.deepcopy(unknown)},
        "interpretation_note": "保存此處明載的官爵／職稱；無明確起訖年者留未知，不由卒年推終期。跨段斷字各存原位，不改寫底文。",
        "reviewer": "Codex（AI代理）", "human_reviewed": False, "model": None,
    }

def install(root):
    root = Path(root)
    path = root / CHAPTER
    chapter = json.loads(path.read_text(encoding="utf-8"))
    uses, holdings = materialize(chapter)
    chapter.setdefault("annotation", {})["source_title_uses"] = [
        u for u in chapter["annotation"].get("source_title_uses", [])
        if not u.get("id", "").startswith("tu-song051-p004-p007-")
    ] + uses
    path.write_text(json.dumps(chapter, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    title_path = root / "corpus/songshu/051-wyd1739-p004-p007-titles.json"
    title_path.write_text(json.dumps({"format_version":"0.2","record_type":"title_holding_assertion_set","chapter_id":CID,"holdings":holdings},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    try:
        from scripts.song051_p004_p007_records import install as install_records
    except ImportError:
        from song051_p004_p007_records import install as install_records
    install_records(root)
    return chapter

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    install(root)
