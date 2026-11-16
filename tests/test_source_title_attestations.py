import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from source_title_attestations import source_title_attestation_valid


def test_chapter_heading_title_is_anchored_to_real_person_mention():
    chapter = {
        "id": "chapter-1",
        "source_id": "source-1",
        "source": {
            "title": "《文集》卷一〈唐故昭武校尉守左金吾衛將軍李公墓誌銘〉",
            "revision_id": 1614621,
        },
        "paragraphs": [{
            "id": "chapter-1:p001",
            "text": "公諱道古。",
            "mentions": [{
                "id": "chapter-1:p001:m0000",
                "kind": "person",
                "person_id": "person-1",
                "start": 2,
                "end": 4,
                "surface": "道古",
            }],
        }],
    }
    holding = {
        "person_id": "person-1",
        "title": "守左金吾衛將軍",
        "source_title_attestation": {
            "kind": "chapter_heading_title",
            "source_title": "唐故昭武校尉守左金吾衛將軍李公墓誌銘",
            "source_revision_id": 1614621,
            "source_id": "source-1",
            "title_anchor": {"start": 6, "end": 13, "surface": "守左金吾衛將軍"},
            "person_anchor": {
                "paragraph_id": "chapter-1:p001",
                "person_mention_id": "chapter-1:p001:m0000",
            },
        },
    }
    assert source_title_attestation_valid(holding, chapter)


def test_chapter_heading_title_rejects_a_fabricated_person_or_wrong_title_offset():
    chapter = {
        "id": "chapter-1",
        "source_id": "source-1",
        "source": {"title": "篇題：唐故昭武校尉守左金吾衛將軍李公墓誌銘", "revision_id": 1},
        "paragraphs": [{
            "id": "chapter-1:p001",
            "text": "公諱道古。",
            "mentions": [{
                "id": "chapter-1:p001:m0000", "kind": "person",
                "person_id": "person-1", "start": 2, "end": 4, "surface": "道古",
            }],
        }],
    }
    holding = {
        "person_id": "person-1", "title": "守左金吾衛將軍",
        "source_title_attestation": {
            "kind": "chapter_heading_title", "source_title": "唐故昭武校尉守左金吾衛將軍李公墓誌銘",
            "source_revision_id": 1, "source_id": "source-1",
            "title_anchor": {"start": 5, "end": 12, "surface": "守左金吾衛將軍"},
            "person_anchor": {"paragraph_id": "chapter-1:p001", "person_mention_id": "missing-mid"},
        },
    }
    assert not source_title_attestation_valid(holding, chapter)
    holding["source_title_attestation"]["person_anchor"]["person_mention_id"] = "chapter-1:p001:m0000"
    assert not source_title_attestation_valid(holding, chapter)
