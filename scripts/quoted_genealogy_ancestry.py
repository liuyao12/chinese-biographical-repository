"""Validate a parent edge implied by explicit father/grandfather roles.

This narrow assembly rule preserves the source's two attested relations and
does not invent a separate source-attested parent assertion.
"""
import hashlib


BASIS = "quoted_genealogy_named_father_grandfather_roles"
CHAPTER_ID = "c-sanguozhi-026-guohuai"
PARAGRAPH_ID = "c-sanguozhi-026-guohuai:unit002"
SOURCE_ID = "s-sanguozhi-026-guohuai"
SOURCE_REVISION = "214fcafa79894355909c9d8c2c1533089e7791c6"
SOURCE_LAYER = "witness_appended_pei_songzhi_note"
QUOTE = "按郭氏譜淮祖全大司農父緼鴈門太守"
PROJECTION_PATH = "source-evidence/sanguozhi026-guohuai-typed/fixed-source-projection.json"
PROJECTION_SHA256 = "2796dc7b6322ca065601ffd677044654a37d1b91c87819cb21bcd1afd69554f8"


def valid(member, rows, assertions, chapters):
    try:
        c = member["parent_connection"]
        near = assertions[c["nearer_ancestor_assertion_id"]]
        far = assertions[c["farther_ancestor_assertion_id"]]
        subject_id = c["chain_subject_person_id"]
        witness = next(row for row in rows.values() if subject_id in row["source_person_ids"])
        parent = rows[member["parent_person_id"]]
        near_q, far_q = near["qualifiers"], far["qualifiers"]
        frame = near_q["source_kinship_frame"]
        if (c.get("type") != "parent_between_consecutive_ancestors"
                or c.get("interpretation_basis") != BASIS
                or c.get("status") != "contextual_provisional"
                or c.get("human_reviewed") is not False
                or not c.get("rationale")
                or member.get("source_assertion_id") is not None
                or near.get("status") != "source_attested"
                or far.get("status") != "source_attested"
                or near.get("predicate") != "father"
                or far.get("predicate") != "grandfather"
                or near.get("subject_person_id") != subject_id
                or far.get("subject_person_id") != subject_id
                or near_q.get("lineage") != "paternal"
                or far_q.get("lineage") != "paternal"
                or near.get("object_person_id") not in member["source_person_ids"]
                or far.get("object_person_id") not in parent["source_person_ids"]
                or subject_id not in witness["source_person_ids"]):
            return False
        far_frame = far_q.get("source_kinship_frame")
        if (frame.get("kind") != "received_quoted_family_frame"
                or frame.get("rule") != "annotated_head_ancestor_offices"
                or frame != far_frame
                or frame.get("human_reviewed") is not False
                or frame.get("source_layer") != SOURCE_LAYER
                or frame.get("source_revision") != SOURCE_REVISION
                or frame.get("fixed_witness_reference") != {"path": PROJECTION_PATH,
                                                              "sha256": PROJECTION_SHA256}
                or frame.get("scope_anchor") != {"paragraph_id": PARAGRAPH_ID,
                                                  "start": 0, "end": 16, "surface": QUOTE}):
            return False
        evidence_near = near.get("evidence", [])
        evidence_far = far.get("evidence", [])
        shared = {(e.get("chapter_id"), e.get("paragraph_id"), e.get("source_id"), e.get("quote"))
                  for e in evidence_near} & {
                  (e.get("chapter_id"), e.get("paragraph_id"), e.get("source_id"), e.get("quote"))
                  for e in evidence_far}
        if len(shared) != 1:
            return False
        chapter_id, paragraph_id, source_id, quote = next(iter(shared))
        if (chapter_id != CHAPTER_ID or paragraph_id != PARAGRAPH_ID
                or source_id != SOURCE_ID or quote != QUOTE
                or near_q.get("source_term") != "父緼"
                or far_q.get("source_term") != "祖全"):
            return False
        chapter = chapters[chapter_id]
        paragraph = next(p for p in chapter["paragraphs"] if p["id"] == paragraph_id)
        if (paragraph.get("text_layer") != SOURCE_LAYER
                or paragraph.get("text") != quote
                or chapter.get("source_id") != source_id
                or hashlib.sha256(quote.encode()).hexdigest() != frame.get("paragraph_sha256")
                or chapter.get("source", {}).get("revision_id") != SOURCE_REVISION):
            return False
        mentions = {m["id"]: m for m in paragraph.get("mentions", []) if m.get("kind") == "person"}
        roles = frame.get("roles", {})
        near_e = next(e for e in near["evidence"] if e.get("chapter_id") == chapter_id
                      and e.get("paragraph_id") == paragraph_id and e.get("source_id") == source_id
                      and e.get("quote") == quote)
        far_e = next(e for e in far["evidence"] if e.get("chapter_id") == chapter_id
                     and e.get("paragraph_id") == paragraph_id and e.get("source_id") == source_id
                     and e.get("quote") == quote)
        role_people = {
            "head": (subject_id, near_e.get("subject_person_mention_id")),
            "father": (near.get("object_person_id"), near_e.get("object_person_mention_id")),
            "grandfather": (far.get("object_person_id"), far_e.get("object_person_mention_id")),
        }
        if set(roles) != set(role_people):
            return False
        for role, (person_id, evidence_mention) in role_people.items():
            mid = roles[role]
            mention = mentions.get(mid)
            if (not mention or mid != evidence_mention or mention.get("person_id") != person_id
                    or quote[mention["start"]:mention["end"]] != mention["surface"]):
                return False
        refs = c.get("references")
        if (not isinstance(refs, list) or len(refs) != 2
                or {r.get("assertion_id") for r in refs} != {near["id"], far["id"]}
                or any(r.get("chapter_id") != chapter_id or r.get("paragraph_id") != paragraph_id
                       or r.get("source_id") != source_id or r.get("quote") != quote
                       or not r.get("scope")
                       or r.get("url") not in (chapter.get("source", {}).get("url"),
                                                chapter.get("source", {}).get("permalink"))
                       for r in refs)):
            return False
        # A conflicting explicit father for the proposed parent invalidates the
        # inferred edge rather than silently choosing this genealogy.
        if any(a.get("predicate") == "father"
               and a.get("subject_person_id") in member["source_person_ids"]
               and a.get("object_person_id") not in parent["source_person_ids"]
               for a in assertions.values()):
            return False
        return True
    except (KeyError, TypeError, ValueError, StopIteration, AttributeError):
        return False
