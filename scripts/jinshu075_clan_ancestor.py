"""Validate the source-bound clan-ancestor appellation in Jinshu 075."""


PARAGRAPH_ID = "c-jinshu-075-xunsong-families:xunsong-intro:p001"
SOURCE_TERM = "族曾祖顗"
SUBJECT_ID = "yoo_ox0_545_BABAAA"  # 荀崧
OBJECT_ID = "yoo_ox0_545_BAA"  # 荀顗


def valid(assertion, paragraphs):
    """Keep the appellation explicit without asserting direct ancestry."""
    try:
        e, = assertion["evidence"]
        chapter_id, paragraph = paragraphs[e["paragraph_id"]]
        q = assertion["qualifiers"]
        binding = q["source_clause_binding"]
        text = paragraph["text"]
        mentions = {m["id"]: m for m in paragraph["mentions"]}
        subject = mentions[e["subject_person_mention_id"]]
        object_ = mentions[e["object_person_mention_id"]]
        start, end = binding["start"], binding["end"]
        return (
            assertion["id"] == "a-jinshu075-xunsong-clan-ancestor"
            and assertion["predicate"] == "kinship_unspecified"
            and assertion["status"] == "source_attested"
            and assertion.get("human_reviewed") is False
            and assertion["subject_person_id"] == SUBJECT_ID
            and assertion["object_person_id"] == OBJECT_ID
            and set(q) == {
                "source_term", "kinship_basis", "lineage",
                "generation_difference", "exact_distance",
                "common_ancestor_person_id", "connecting_person_ids",
                "source_clause_binding",
            }
            and q["source_term"] == SOURCE_TERM
            and q["kinship_basis"] == "paternal_clan_ancestor_appellation"
            and q["lineage"] == "unspecified"
            and all(q[key] is None for key in (
                "generation_difference", "exact_distance",
                "common_ancestor_person_id", "connecting_person_ids",
            ))
            and binding == {
                "kind": "named_biographical_subject_clan_ancestor_appellation",
                "start": 62,
                "end": 66,
            }
            and e["work_id"] == "w-jinshu"
            and e["book_id"] == "b-jinshu-075"
            and e["chapter_id"] == chapter_id == "c-jinshu-075-xunsong-families"
            and e["paragraph_id"] == PARAGRAPH_ID
            and e["source_id"] == "s-jinshu-075-xunsong-families"
            and e["quote"] == text
            and subject["kind"] == object_["kind"] == "person"
            and subject["person_id"] == SUBJECT_ID
            and object_["person_id"] == OBJECT_ID
            and subject["surface"] == "荀崧"
            and object_["surface"] == "顗"
            and text[subject["start"]:subject["end"]] == subject["surface"]
            and text[object_["start"]:object_["end"]] == object_["surface"]
            and 0 <= start < end <= len(text)
            and text[start:end] == SOURCE_TERM
            and text[start - 4:start] == "齠齔時，"
        )
    except (KeyError, TypeError, ValueError, StopIteration):
        return False
