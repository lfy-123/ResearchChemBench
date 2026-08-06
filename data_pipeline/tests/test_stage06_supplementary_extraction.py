from src.stages.stage06_supplementary_extraction import extract_supplementary_materials


def test_stage06_reuses_stage02_si_without_reparsing(tmp_path):
    text = tmp_path / "existing.txt"
    text.write_text("ORCA calculations used a def2 basis set and produced an energy.")

    def fail_extractor(*_args):
        raise AssertionError("Stage 00 SI must not be parsed again in Stage 06")

    paper = {
        "paper_id": "p1",
        "supplementary_documents": [
            {
                "document_id": "si-existing",
                "document_role": "supplementary",
                "source_path": "si.pdf",
                "text_path": str(text),
            }
        ],
        "supplementary_acquisition": {
            "download_status": "skipped_existing_supplementary",
            "attachments": [],
        },
    }
    record = extract_supplementary_materials(
        [paper], tmp_path / "out", {}, fast_extractor=fail_extractor
    )[0]
    assert record["supplementary_extraction"]["status"] == "reused_stage02"
    assert record["supplementary_extraction"]["software_evidence"]


def test_stage06_parses_only_new_stage04_attachments(tmp_path):
    pdf = tmp_path / "downloaded.pdf"
    pdf.write_bytes(b"pdf")

    def extractor(_source, destination, _config):
        value = "Computational details used VASP with a plane-wave cutoff. Table S1 reports energy."
        destination.write_text(value, encoding="utf-8")
        return value

    paper = {
        "paper_id": "p1",
        "supplementary_documents": [],
        "supplementary_acquisition": {
            "download_status": "downloaded",
            "attachments": [{"path": str(pdf), "sha256": "abc", "newly_downloaded": True}],
        },
    }
    record = extract_supplementary_materials(
        [paper], tmp_path / "out", {}, fast_extractor=extractor
    )[0]
    result = record["supplementary_extraction"]
    assert result["status"] == "success"
    assert result["documents"][0]["parser"] == "pdftotext"
    assert result["parameter_evidence"]
    assert result["result_evidence"]


def test_stage06_keeps_confirmed_no_supplementary_without_parsing(tmp_path):
    def fail_extractor(*_args):
        raise AssertionError("confirmed absence must not invoke a parser")

    paper = {
        "paper_id": "p1",
        "supplementary_documents": [],
        "supplementary_acquisition": {
            "presence_status": "absent_confirmed",
            "download_status": "not_attempted",
            "attachments": [],
        },
        "pipeline_routing": {"continue": True},
    }
    record = extract_supplementary_materials(
        [paper], tmp_path / "out", {}, fast_extractor=fail_extractor
    )[0]
    assert record["supplementary_extraction"]["status"] == (
        "confirmed_no_supplementary"
    )
    assert record["pipeline_routing"]["continue"] is True


def test_stage06_rejects_unavailable_supplementary(tmp_path):
    def fail_extractor(*_args):
        raise AssertionError("unavailable supplementary must not invoke a parser")

    paper = {
        "paper_id": "p1",
        "supplementary_documents": [],
        "supplementary_acquisition": {
            "presence_status": "present_unavailable",
            "download_status": "access_blocked",
            "attachments": [],
        },
        "pipeline_routing": {"continue": True},
    }
    record = extract_supplementary_materials(
        [paper], tmp_path / "out", {}, fast_extractor=fail_extractor
    )[0]
    assert record["supplementary_extraction"]["status"] == "supplementary_unavailable"
    assert record["pipeline_routing"]["continue"] is False


def test_stage06_preserves_non_pdf_supplement_without_pdftotext(tmp_path):
    archive = tmp_path / "support.zip"
    archive.write_bytes(b"PK\x03\x04archive")

    def fail_extractor(*_args):
        raise AssertionError("non-PDF SI must not be passed to pdftotext")

    paper = {
        "paper_id": "p1",
        "supplementary_documents": [],
        "supplementary_acquisition": {
            "presence_status": "available",
            "download_status": "downloaded",
            "attachments": [
                {"path": str(archive), "sha256": "abc", "newly_downloaded": True}
            ],
        },
        "pipeline_routing": {"continue": True},
    }
    record = extract_supplementary_materials(
        [paper], tmp_path / "out", {}, fast_extractor=fail_extractor
    )[0]
    result = record["supplementary_extraction"]
    assert result["status"] == "success"
    assert result["documents"][0]["parser"] == "not_extracted"
    assert result["documents"][0]["extraction_status"] == "non_pdf_asset_preserved"
