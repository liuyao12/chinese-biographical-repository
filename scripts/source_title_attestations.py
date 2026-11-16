"""Validate person-linked titles attested in a received chapter heading.

A heading is a source locus in its own right. It must never be represented by a
fabricated paragraph mention or a made-up body-text offset.
"""

def source_title_attestation_valid(holding, chapter):
    try:
        a = holding["source_title_attestation"]
        if set(a) != {
            "kind", "source_title", "source_revision_id", "source_id",
            "title_anchor", "person_anchor"
        }:
            return False
        if a["kind"] != "chapter_heading_title":
            return False
        source = chapter["source"]
        if a["source_revision_id"] != source["revision_id"] or a["source_id"] != chapter["source_id"]:
            return False
        quote = a["source_title"]
        if not isinstance(quote, str) or not quote or quote not in source["title"]:
            return False
        anchor = a["title_anchor"]
        if set(anchor) != {"start", "end", "surface"}:
            return False
        if type(anchor["start"]) is not int or type(anchor["end"]) is not int:
            return False
        if not (0 <= anchor["start"] < anchor["end"] <= len(quote)):
            return False
        if quote[anchor["start"]:anchor["end"]] != anchor["surface"] or anchor["surface"] != holding["title"]:
            return False
        person_anchor = a["person_anchor"]
        if set(person_anchor) != {"paragraph_id", "person_mention_id"}:
            return False
        paragraph = next(p for p in chapter["paragraphs"] if p["id"] == person_anchor["paragraph_id"])
        mention = next(m for m in paragraph["mentions"] if m["id"] == person_anchor["person_mention_id"])
        return (
            mention.get("kind") == "person"
            and mention.get("person_id") == holding["person_id"]
            and paragraph["text"][mention["start"]:mention["end"]] == mention["surface"]
        )
    except (KeyError, TypeError, ValueError, StopIteration):
        return False
