"""Guard the unaccepted Sanguozhi 058 witness from becoming graph data."""


def comparison_only_valid(reading, identities, boundary, excerpts):
    witness = reading.get("witness", {})
    return (
        reading.get("record_type") == "source_witness_assessment"
        and reading.get("scope") == "comparison_only_not_adopted_as_CBR_text_base"
        and witness.get("fixed_revision") == 2131313
        and witness.get("print_edition") == "unknown"
        and witness.get("image_verified") is False
        and "revision_author" not in witness
        and reading.get("excerpt_sha256")
        and identities.get("record_type") == "unadopted_comparison_observation"
        and identities.get("status") == "not_materialized"
        and "不納入 CBR 通行正文" in boundary
        and "不供人物圖譜使用" in "".join(reading.get("editorial_limits", []))
        and "[陳壽正文]" in excerpts
        and "[裴松之注；引《陸氏世頌》]" in excerpts
        and "[來源見證原行" in excerpts
    )


def no_materialized_relations(assertion_record):
    return (
        assertion_record.get("record_type") == "unadopted_comparison_disposition"
        and assertion_record.get("status") == "not_adopted"
        and assertion_record.get("assertions") == []
    )
