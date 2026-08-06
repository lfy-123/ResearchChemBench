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
