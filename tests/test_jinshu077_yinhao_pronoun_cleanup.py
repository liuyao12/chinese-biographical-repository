import hashlib
import json
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRONOUN_SURFACES = {"其", "足下", "君", "我"}

# Existing source anchors whose function is pronominal or a direct form of
# address.  Their IDs and referents are retained; none is a personal-name alias.
EXPECTED = {
    "corpus/jinshu/077-yinhao.json": {
        "c-jinshu-077-yinhao:p001:m0032": "djo_u3b_i9w",
        "c-jinshu-077-yinhao:p001:m0074": "djo_u3b_i9w",
        "c-jinshu-077-yinhao:p003:m0080": "djo_u3b_i9w_A",
        "c-jinshu-077-yinhao:p003:m0172": "djo_u3b_i9w_A",
        "c-jinshu-077-yinhao:p004:m0097": "djo_u3b_i9w_A",
        "c-jinshu-077-yinhao:p004:m0168": "djo_u3b_i9w_A",
        "c-jinshu-077-yinhao:p004:m0189": "djo_u3b_i9w_A",
        "c-jinshu-077-yinhao:p006:m0163": "5jb_986_aop",
        "c-jinshu-077-yinhao:p007:m0008": "djo_u3b_i9w_A",
        "c-jinshu-077-yinhao:p008:m0294": "nzw_thb_ddp",
        "c-jinshu-077-yinhao:p010:m0018": "djo_u3b_i9w_A",
        "c-jinshu-077-yinhao:p010:m0021": "u9s_w6j_8mc_AA",
        "c-jinshu-077-yinhao:p010:m0028": "djo_u3b_i9w_A",
        "c-jinshu-077-yinhao:p010:m0030": "u9s_w6j_8mc_AA",
        "c-jinshu-077-yinhao:p010:m0037": "djo_u3b_i9w_A",
        "c-jinshu-077-yinhao:p010:m0078": "u9s_w6j_8mc_AA",
        "c-jinshu-077-yinhao:p010:m0090": "u9s_w6j_8mc_AA",
        "c-jinshu-077-yinhao:p010:m0125": "djo_u3b_i9w_A",
        "c-jinshu-077-yinhao:p011:m0026": "djo_u3b_i9w_A",
        "c-jinshu-077-yinhao:p013:m0006": "djo_u3b_i9w_A",
        "c-jinshu-077-yinhao:p014:m0207": "djo_u3b_i9w_A",
        "c-jinshu-077-yinhao:p014:m0217": "djo_u3b_i9w_A",
    },
    "corpus/jinshu/079.json": {
        "c-jinshu-079-xielang-family:phase6-line031:m0105": "u9s_w6j_8mc_AA",
        "c-jinshu-079-xielang-family:phase6-line047:m0248": "u9s_w6j_8mc_AA",
        "c-jinshu-079-xielang-family:exp-xieyi-p001:m0095": "u9s_w6j_8mc_AA",
        "c-jinshu-079-xielang-family:exp-xieyi-p001:m0132": "u9s_w6j_8mc_AA",
    },
    "corpus/jinshu/098-huanwen.json": {
        "c-jinshu-098-huanwen:p027:m0015": "u9s_w6j_8mc_AA",
    },
}


class Jinshu077YinhaoPronounCleanupTests(unittest.TestCase):
    def test_exact_source_mentions_remain_linked_as_pronouns(self):
        for relative_path, expected in EXPECTED.items():
            with self.subTest(path=relative_path):
                chapter = json.loads((ROOT / relative_path).read_text(encoding="utf-8"))
                found = {
                    mention["id"]: mention
                    for paragraph in chapter["paragraphs"]
                    for mention in paragraph.get("mentions", [])
                    if mention["id"] in expected
                }
                self.assertEqual(set(found), set(expected))
                for mention_id, person_id in expected.items():
                    mention = found[mention_id]
                    self.assertEqual(mention["kind"], "pronoun")
                    self.assertEqual(mention.get("person_id"), person_id)
                    self.assertIn(mention["surface"], PRONOUN_SURFACES)

    def test_pronoun_surfaces_are_not_person_name_aliases(self):
        registry = json.loads((ROOT / "registry/persons.json").read_text(encoding="utf-8"))
        compact = json.loads((ROOT / "data/corpus/persons.json").read_text(encoding="utf-8"))
        affected = {"djo_u3b_i9w_A", "djo_u3b_i9w", "u9s_w6j_8mc_AA", "5jb_986_aop", "nzw_thb_ddp"}
        registry_people = {person["id"]: person for person in registry["persons"]}
        changed_ids = {mention_id for mentions in EXPECTED.values() for mention_id in mentions}
        for person_id in affected:
            with self.subTest(person_id=person_id):
                self.assertFalse(
                    PRONOUN_SURFACES.intersection(alias["surface"] for alias in registry_people[person_id]["aliases"])
                )
                self.assertFalse(PRONOUN_SURFACES.intersection(compact[person_id]["aliases"]))
                self.assertFalse(
                    changed_ids.intersection(evidence.get("mention_id") for evidence in registry_people[person_id]["evidence"])
                )

                bundle = json.loads((ROOT / f"exports/persons/{person_id}.json").read_text(encoding="utf-8"))
                for source_person in bundle["persons"]:
                    if source_person["id"] == person_id:
                        self.assertFalse(
                            PRONOUN_SURFACES.intersection(alias["surface"] for alias in source_person["aliases"])
                        )
                    self.assertFalse(
                        changed_ids.intersection(evidence.get("mention_id") for evidence in source_person["evidence"])
                    )

    def test_reader_markup_uses_pronoun_elements(self):
        for relative_path, expected in EXPECTED.items():
            xml_path = ROOT / relative_path.replace("corpus/", "corpus/").replace(".json", ".xml")
            root = ET.parse(xml_path).getroot()
            elements = {element.attrib.get("id"): element for element in root.iter() if element.attrib.get("id")}
            for mention_id, person_id in expected.items():
                with self.subTest(path=relative_path, mention_id=mention_id):
                    element = elements[mention_id]
                    self.assertEqual(element.tag, "rs")
                    self.assertEqual(element.attrib.get("type"), "pronoun")
                    if person_id:
                        self.assertEqual(element.attrib.get("ref"), person_id)

    def test_identity_surface_inventory_excludes_pronouns(self):
        chapter = json.loads((ROOT / "corpus/jinshu/079-identities.json").read_text(encoding="utf-8"))
        decision = next(
            item for item in chapter["decisions"]
            if item["id"] == "d-phase6-079-u9s_w6j_8mc_AA"
        )
        self.assertFalse(PRONOUN_SURFACES.intersection(decision["surfaces"]))

    def test_source_text_is_unchanged(self):
        for relative_path in EXPECTED:
            with self.subTest(path=relative_path):
                chapter = json.loads((ROOT / relative_path).read_text(encoding="utf-8"))
                received_text = "\n\n".join(paragraph["text"] for paragraph in chapter["paragraphs"])
                self.assertEqual(
                    hashlib.sha256(received_text.encode("utf-8")).hexdigest(),
                    chapter["text_sha256"],
                )


if __name__ == "__main__":
    unittest.main()
