"""Tie the declined appointment to the biography's named subject."""


def valid(row, chapter):
    if chapter.get("id") != "c-jinshu-098-huanwen":
        return False
    paras = chapter.get("paragraphs", [])
    if len(paras) < 8:
        return False
    opening, para = paras[0], paras[7]
    text = para["text"]
    phrase = "進位太尉，固讓不拜。"
    if not text.startswith(phrase) or not opening["text"].startswith("桓溫，字元子"):
        return False
    if (row.get("title"), row.get("non_assumption_kind"), row.get("outcome")) != ("太尉", "declined", "not_assumed"):
        return False
    evidence = row.get("evidence", [])
    if len(evidence) != 1 or evidence[0].get("quote") != text or evidence[0].get("paragraph_id") != para["id"]:
        return False
    subject = next((m for m in opening["mentions"] if m["start"] == 0 and m["surface"] == "桓溫"), {})
    if row.get("person_id") != subject.get("person_id") or text.count("溫復進督司州") != 1:
        return False
    resumed = next((m for m in para["mentions"] if m["start"] == text.index("溫復進督司州") and m["surface"] == "溫"), {})
    if row.get("person_mention_id") != resumed.get("id") or resumed.get("person_id") != subject.get("person_id"):
        return False
    for key, form in (("role_anchor","太尉"),("appointment_anchor","進位"),("non_assumption_anchor","固讓不拜")):
        start = phrase.index(form)
        if row.get(key) != dict(paragraph_id=para["id"],start=start,end=start+len(form),surface=form):
            return False
    return True
