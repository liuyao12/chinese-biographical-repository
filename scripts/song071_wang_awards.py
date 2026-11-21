"""Verify the recipient of coordinated gifts after several servants are also killed."""
from hashlib import sha256

CHAPTER = "c-songshu-071-wangsengchuo"
SOURCE = "s-songshu-071-wangsengchuo"
PARAGRAPH = CHAPTER + ":p004"
TEXT_SHA = "0fc0186cb601b04bd7d59995c40908154847dcf8efe37f16e7e27241e531e09b"
WANG = "7r6_k52_qji_ABAAAAEA"
EMPEROR = "hx8_st4_jdd"
TERMS = {
    "散騎常侍": ("posthumous_grant", "office", "追贈散騎常侍金紫光禄大夫"),
    "金紫光禄大夫": ("posthumous_grant", "office", "追贈散騎常侍金紫光禄大夫"),
    "愍侯": ("posthumous_naming", "honorific", "謚曰愍侯"),
}


def valid(h, paragraphs, mentions, events):
    try:
        mode, kind, wording = TERMS[h["title"]]
        b = h["naming_basis" if mode == "posthumous_naming" else "posthumous_basis"]
        e, = h["evidence"]
        t, = h["attestations"]
        cid, p = paragraphs[e["paragraph_id"]]
        text = p["text"]
        death = events[b["death_event_id"]]
        ev, = death["evidence"]
        if (cid != CHAPTER or p["id"] != PARAGRAPH or sha256(text.encode()).hexdigest() != TEXT_SHA
                or (e["work_id"], e["book_id"], e["chapter_id"], e["source_id"]) !=
                ("w-songshu", "b-songshu-071", CHAPTER, SOURCE)
                or e["quote"] != text or ev != e or b["evidence"] != [e]
                or h["effective_period"]["start"] != {"status":"source_event", "event_type":mode,
                                                      "date_expression":None, "evidence":[e]}
                or (h["person_id"], h["mode"], h["kind"], h["status"]) !=
                (WANG, mode, kind, "source_attested")
                or death["id"] != "le-song071-wyg-sengchuo" or death["event_type"] != "death"
                or death["person_id"] != WANG or death["status"] != "source_attested"
                or b["kind"] != "song071_wang_posthumous_awards" or b["source_term"] != wording
                or b["death_term"] != death["source_term"] or death["source_term"] != "收害"):
            return False

        def anchor(word):
            start = text.index(word)
            return {"paragraph_id": PARAGRAPH, "start": start, "end": start+len(word), "surface": word}

        if death["source_anchor"] != anchor("收害") or b["source_anchor"] != anchor(wording):
            return False
        expected_recipient = text.index("得僧綽所啓") + 1
        for key, pid, surface, offset in [
                ("recipient_person_mention_id", WANG, "僧綽", expected_recipient),
                ("issuer_person_mention_id", EMPEROR, "世祖", text.index("世祖即位"))]:
            chapter, para, marked = mentions[b[key]]
            if ((chapter, para, marked["person_id"], marked["start"], marked["surface"]) !=
                    (CHAPTER, PARAGRAPH, pid, offset, surface)):
                return False
        return (e["person_mention_id"] == b["recipient_person_mention_id"] == t["person_mention_id"]
                and t["usage"] == "posthumous_usage"
                and all(t[k] == v for k,v in anchor(h["title"]).items()))
    except (KeyError, ValueError, TypeError):
        return False
