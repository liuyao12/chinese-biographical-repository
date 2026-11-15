"""驗證《晉書》卷76王籍之依王彬叔姪關係接至缺名父代祖父。"""

JIZHI = "57l_v07_8z9"
WANG_BIN = "7r6_k52_qji_ABDB"
WANG_YI = "7r6_k52_qji_ABDA"
WANG_ZHENG = "7r6_k52_qji_ABD"
NEPHEW_ASSERTION = "a-jinshu076-jizhi-wangbin-paternal-uncle"
BROTHER_ASSERTION = "a-jinshu076-yi-bin-brother"
FATHER_ASSERTION = "a-jinshu076-wang-001"
CHAPTER = "c-jinshu-076-wangbin"
PARAGRAPH = "c-jinshu-076-wangbin:line052"
URL = "https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7076&oldid=2180533"


def _evidence_matches_reference(reference, assertion, chapters):
    if reference.get("assertion_id") != assertion.get("id"):
        return False
    if not reference.get("scope") or reference.get("url") != URL:
        return False
    chapter = chapters.get(reference.get("chapter_id"))
    if not chapter or reference.get("url") not in (
        chapter.get("source", {}).get("url"),
        chapter.get("source", {}).get("permalink"),
    ):
        return False
    paragraphs = {p.get("id"): p for p in chapter.get("paragraphs", [])}
    paragraph = paragraphs.get(reference.get("paragraph_id"))
    if not paragraph or paragraph.get("text") != reference.get("quote"):
        return False
    return any(
        all(e.get(k) == reference.get(k) for k in (
            "work_id", "book_id", "source_id", "chapter_id", "paragraph_id", "quote", "subject_person_mention_id", "object_person_mention_id"
        ))
        for e in assertion.get("evidence", [])
    )


def ancestor_valid(member, rows, assertions_by_id, chapters):
    """Only the one reviewed source path is accepted; no father person is created."""
    try:
        if (
            member.get("person_id") != "7r6_k52_qji_ABD*A"
            or member.get("representative_source_person_id") != JIZHI
            or member.get("source_person_ids") != [JIZHI]
            or member.get("parent_person_id") is not None
            or member.get("source_assertion_id") is not None
            or member.get("ancestor_person_id") != WANG_ZHENG
            or member.get("connection") != "grandfather"
            or member.get("generation_distance") != 2
            or member.get("intermediate_person_ids") != [None]
            or not member.get("interpretation_note")
        ):
            return False
        proof = member.get("ancestor_connection")
        if not isinstance(proof, dict) or (
            proof.get("type") != "jinshu076_paternal_nephew_to_uncle_grandfather"
            or proof.get("status") != "contextual_provisional"
            or proof.get("human_reviewed") is not False
            or proof.get("nephew_assertion_id") != NEPHEW_ASSERTION
            or proof.get("uncle_person_id") != WANG_BIN
            or proof.get("uncle_sibling_person_id") != WANG_YI
            or proof.get("uncle_sibling_assertion_id") != BROTHER_ASSERTION
            or proof.get("uncle_father_assertion_id") != FATHER_ASSERTION
            or not proof.get("rationale")
        ):
            return False

        nephew, brother, father = (assertions_by_id.get(i) for i in (
            NEPHEW_ASSERTION, BROTHER_ASSERTION, FATHER_ASSERTION
        ))
        uncle, sibling, ancestor = (rows.get(i) for i in (WANG_BIN, WANG_YI, WANG_ZHENG))
        if not all((nephew, brother, father, uncle, sibling, ancestor)):
            return False
        if (
            nephew.get("predicate") != "paternal_uncle"
            or nephew.get("status") != "source_attested"
            or nephew.get("subject_person_id") != JIZHI
            or nephew.get("object_person_id") != WANG_BIN
            or nephew.get("qualifiers", {}).get("source_term") != "兄子"
            or not any(
                e.get("chapter_id") == CHAPTER
                and e.get("paragraph_id") == PARAGRAPH
                and e.get("subject_person_mention_id") == CHAPTER + ":line052:m0014"
                and e.get("object_person_mention_id") == CHAPTER + ":line052:m0006"
                for e in nephew.get("evidence", [])
            )
        ):
            return False
        parent_proof = uncle.get("parent_connection")
        if (
            uncle.get("parent_person_id") != WANG_ZHENG
            or not isinstance(parent_proof, dict)
            or parent_proof.get("type") != "shared_father_through_sibling"
            or parent_proof.get("status") != "contextual_provisional"
            or parent_proof.get("sibling_person_id") != WANG_YI
            or parent_proof.get("sibling_assertion_id") != BROTHER_ASSERTION
            or parent_proof.get("sibling_father_assertion_id") != FATHER_ASSERTION
            or brother.get("predicate") != "brother"
            or {brother.get("subject_person_id"), brother.get("object_person_id")} != {WANG_BIN, WANG_YI}
            or father.get("predicate") != "father"
            or father.get("subject_person_id") != WANG_YI
            or father.get("object_person_id") != WANG_ZHENG
            or brother.get("qualifiers", {}).get("lineage") == "maternal"
            or father.get("qualifiers", {}).get("lineage") == "maternal"
        ):
            return False

        expected_refs = [
            (nephew, e, "《晉書》明言籍之為彬兄子；未指名籍之之父。")
            for e in nephew.get("evidence", [])
        ]
        expected_refs.extend(
            (assertions_by_id.get(r.get("assertion_id")), r, r.get("scope"))
            for r in parent_proof.get("references", [])
        )
        refs = proof.get("references")
        if not isinstance(refs, list) or len(refs) != len(expected_refs):
            return False
        unused = list(refs)
        for assertion, evidence, scope in expected_refs:
            if not assertion or not scope:
                return False
            matched = next((
                r for r in unused
                if r.get("assertion_id") == assertion.get("id")
                and all(r.get(k) == evidence.get(k) for k in (
                    "work_id", "book_id", "source_id", "chapter_id", "paragraph_id", "quote", "subject_person_mention_id", "object_person_mention_id"
                ))
                and r.get("url") == URL
                and r.get("scope") == scope
                and _evidence_matches_reference(r, assertion, chapters)
            ), None)
            if matched is None:
                return False
            unused.remove(matched)

        for assertion in assertions_by_id.values():
            if assertion.get("subject_person_id") == JIZHI and assertion.get("predicate") in (
                "father", "adoptive_father", "grandfather", "great_grandfather", "ancestor"
            ):
                if assertion.get("predicate") in ("father", "adoptive_father"):
                    return False
                if assertion.get("object_person_id") != WANG_ZHENG:
                    return False
        return True
    except (KeyError, TypeError, AttributeError):
        return False
