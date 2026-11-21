"""Bind the named nephew and uncle to the specific Cheng-Han source clause."""


def sent_uncle_valid(assertion, paragraphs):
    evidence = assertion.get("evidence", [])
    qualifiers = assertion.get("qualifiers", {})
    if len(evidence) != 1 or assertion.get("predicate") != "paternal_uncle":
        return False
    ev = evidence[0]
    hit = paragraphs.get(ev.get("paragraph_id"))
    if not hit or hit[0] != ev.get("chapter_id") or hit[0] != "c-jinshu-098-huanwen":
        return False
    paragraph = hit[1]
    term = "勢使其叔父福"
    if qualifiers.get("source_term") != term or paragraph["text"].count(term) != 1 or term not in ev.get("quote", ""):
        return False
    start = paragraph["text"].index(term)
    marks = {m["id"]: m for m in paragraph["mentions"] if m["kind"] == "person"}
    for side, surface, pos in (("subject", "勢", start), ("object", "福", start + len(term) - 1)):
        mark = marks.get(ev.get(side + "_person_mention_id"), {})
        if (mark.get("start"), mark.get("end"), mark.get("surface")) != (pos, pos + 1, surface):
            return False
        if mark.get("person_id") != assertion.get(side + "_person_id"):
            return False
    return assertion["subject_person_id"] != assertion["object_person_id"]
