import httpx

from src.integrations.publishers import publisher_adapter
from src.stages.stage04_supplementary_acquisition import acquire_supplementary_materials


class FailingClient:
    def get(self, _url):
        raise AssertionError("network must not be used when SI already exists")


class FakeStore:
    def __init__(self):
        self.copies = []

    def copy_to(self, uri, destination):
        self.copies.append(uri)
        destination.write_bytes(b"%PDF-1.7 support")
        return {"etag": "etag", "content_type": "application/pdf"}


def test_stage04_skips_network_for_existing_supplementary(tmp_path):
    paper = {
        "paper_id": "p1",
        "has_local_supplementary": True,
        "supplementary_documents": [{"document_id": "si"}],
    }
    record = acquire_supplementary_materials(
        [paper], tmp_path, {}, client=FailingClient()
    )[0]
    assert record["supplementary_acquisition"]["download_status"] == "skipped_existing_supplementary"


def test_stage04_retries_only_verified_remote_inventory_uri(tmp_path):
    store = FakeStore()
    paper = {
        "paper_id": "p1",
        "source_record": {"support_path": ["stale/si.pdf"]},
        "supplementary_discovery": {
            "matched_remote_uris": [
                "s3://private-cooperate-data/en-paper-hzzj/support/si.pdf"
            ]
        },
        "supplementary_documents": [],
    }
    record = acquire_supplementary_materials(
        [paper], tmp_path, {}, store=store, client=FailingClient()
    )[0]
    assert record["supplementary_acquisition"]["download_status"] == "downloaded"
    assert store.copies == [
        "s3://private-cooperate-data/en-paper-hzzj/support/si.pdf"
    ]


def test_stage04_does_not_guess_uri_from_unverified_metadata_hint(tmp_path):
    store = FakeStore()
    paper = {
        "paper_id": "p1",
        "source_dataset": "en-paper-hzzj",
        "source_record": {"support_path": ["support/si.pdf"]},
        "supplementary_documents": [],
    }
    record = acquire_supplementary_materials(
        [paper],
        tmp_path,
        {"enable_network": False},
        store=store,
        client=FailingClient(),
    )[0]
    assert record["supplementary_acquisition"]["download_status"] == "not_attempted"
    assert store.copies == []


def test_stage04_downloads_only_official_publisher_links(tmp_path):
    article = "https://pubs.acs.org/doi/10.1021/example"
    si = "https://acs.figshare.com/ndownloader/files/12345"

    def handler(request):
        if str(request.url) == article:
            return httpx.Response(
                200,
                text=(
                    '<a href="https://github.com/example/data.zip">Supporting data</a>'
                    f'<a href="{si}">Supporting Information PDF</a>'
                ),
                request=request,
            )
        if str(request.url) == si:
            return httpx.Response(
                200,
                content=b"%PDF-1.7 support",
                headers={"content-type": "application/pdf"},
                request=request,
            )
        raise AssertionError(str(request.url))

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        record = acquire_supplementary_materials(
            [{"paper_id": "p1", "doi": "10.1021/example", "article_url": article}],
            tmp_path,
            {"publisher_adapters": ["acs"]},
            client=client,
        )[0]
    attachments = record["supplementary_acquisition"]["attachments"]
    assert len(attachments) == 1
    assert attachments[0]["source_url"] == si


def test_publisher_adapter_can_recover_doi_from_doi_url():
    adapter = publisher_adapter(
        doi=None,
        article_url="https://doi.org/10.1002/anie.202310798",
        enabled=["wiley"],
    )
    assert adapter is not None
    assert adapter.publisher == "wiley"


def test_stage04_enforces_per_paper_deadline(tmp_path):
    article = "https://pubs.acs.org/doi/10.1021/example"

    def handler(request):
        return httpx.Response(200, text="<html></html>", request=request)

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        record = acquire_supplementary_materials(
            [{"paper_id": "p1", "doi": "10.1021/example", "article_url": article}],
            tmp_path,
            {"publisher_adapters": ["acs"], "paper_timeout_seconds": 0},
            client=client,
        )[0]
    assert record["supplementary_acquisition"]["download_status"] == "timeout"


def test_stage04_rejects_oversize_stream_without_partial_file(tmp_path):
    article = "https://pubs.acs.org/doi/10.1021/example"
    si = "https://acs.figshare.com/ndownloader/files/12345"

    def handler(request):
        if str(request.url) == article:
            return httpx.Response(
                200,
                text=f'<a href="{si}">Supporting Information PDF</a>',
                request=request,
            )
        return httpx.Response(
            200,
            content=b"%PDF-1.7 support",
            headers={"content-type": "application/pdf"},
            request=request,
        )

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        record = acquire_supplementary_materials(
            [{"paper_id": "p1", "doi": "10.1021/example", "article_url": article}],
            tmp_path,
            {"publisher_adapters": ["acs"], "max_file_bytes": 5},
            client=client,
        )[0]
    assert record["supplementary_acquisition"]["download_status"] == "oversize"
    assert list((tmp_path / "files" / "p1").iterdir()) == []


def test_nature_adapter_ignores_page_fragment_and_accepts_static_esm(tmp_path):
    article = "https://www.nature.com/articles/s41467-024-12345-6"
    si = "https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-024-12345-6/MediaObjects/41467_2024_12345_MOESM1_ESM.pdf"

    def handler(request):
        if str(request.url) == article:
            return httpx.Response(
                200,
                text=(
                    '<a href="#MOESM1">Supplementary information</a>'
                    f'<meta name="citation_supplementary_material" content="{si}">'
                ),
                request=request,
            )
        if str(request.url) == si:
            return httpx.Response(
                200,
                content=b"%PDF-1.7 support",
                headers={"content-type": "application/pdf"},
                request=request,
            )
        raise AssertionError(str(request.url))

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        record = acquire_supplementary_materials(
            [{"paper_id": "p1", "doi": "10.1038/s41467-024-12345-6"}],
            tmp_path,
            {"publisher_adapters": ["nature"]},
            client=client,
        )[0]
    attachments = record["supplementary_acquisition"]["attachments"]
    assert [item["source_url"] for item in attachments] == [si]


def test_publisher_adapters_build_direct_official_landing_urls():
    cases = {
        "acs": (
            "10.1021/jacs.4c00001",
            "https://pubs.acs.org/doi/10.1021/jacs.4c00001",
        ),
        "rsc": (
            "10.1039/D4SC00001A",
            "https://pubs.rsc.org/en/content/articlelanding/2024/sc/d4sc00001a",
        ),
        "wiley": (
            "10.1002/anie.202400001",
            "https://onlinelibrary.wiley.com/doi/10.1002/anie.202400001",
        ),
        "nature": (
            "10.1038/s41467-024-12345-6",
            "https://www.nature.com/articles/s41467-024-12345-6",
        ),
    }
    for publisher, (doi, expected) in cases.items():
        adapter = publisher_adapter(doi=doi, article_url=None, enabled=[publisher])
        assert adapter is not None
        assert adapter.article_url(doi=doi, article_url=None) == expected


def test_elsevier_adapter_discovers_official_cdn_attachments(tmp_path):
    doi = "10.1016/j.checat.2023.100826"
    doi_url = f"https://doi.org/{doi}"
    landing = "https://linkinghub.elsevier.com/retrieve/pii/S2667109323004062"
    si = (
        "https://ars.els-cdn.com/content/image/"
        "1-s2.0-S2667109323004062-mmc1.pdf"
    )

    def handler(request):
        url = str(request.url)
        if url == doi_url:
            return httpx.Response(302, headers={"location": landing}, request=request)
        if url == landing:
            return httpx.Response(200, text=f"Article DOI: {doi}", request=request)
        if request.method == "HEAD" and url == si:
            return httpx.Response(
                206,
                headers={
                    "content-type": "application/pdf",
                    "content-range": "bytes 0-0/17",
                },
                request=request,
            )
        if request.method == "HEAD" and "-mmc2." in url:
            return httpx.Response(404, request=request)
        if url == si:
            return httpx.Response(
                200,
                content=b"%PDF-1.7 support",
                headers={"content-type": "application/pdf"},
                request=request,
            )
        raise AssertionError(f"unexpected request: {request.method} {url}")

    with httpx.Client(
        transport=httpx.MockTransport(handler), follow_redirects=True
    ) as client:
        record = acquire_supplementary_materials(
            [{"paper_id": "p1", "doi": doi}],
            tmp_path,
            {"publisher_adapters": ["elsevier"]},
            client=client,
        )[0]
    acquisition = record["supplementary_acquisition"]
    assert acquisition["download_status"] == "downloaded"
    assert acquisition["presence_status"] == "available"
    assert [item["source_url"] for item in acquisition["attachments"]] == [si]


def test_successful_official_page_can_confirm_no_supplementary(tmp_path):
    doi = "10.1039/D4SC00001A"
    article = "https://pubs.rsc.org/en/content/articlelanding/2024/sc/d4sc00001a"

    def handler(request):
        assert str(request.url) == article
        return httpx.Response(200, text=f"Article DOI: {doi}", request=request)

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        record = acquire_supplementary_materials(
            [{"paper_id": "p1", "doi": doi}],
            tmp_path,
            {"publisher_adapters": ["rsc"]},
            client=client,
        )[0]
    acquisition = record["supplementary_acquisition"]
    assert acquisition["download_status"] == "not_attempted"
    assert acquisition["presence_status"] == "absent_confirmed"


def test_stage04_accepts_official_zip_without_url_extension(tmp_path):
    article = "https://pubs.acs.org/doi/10.1021/example"
    si = "https://acs.figshare.com/ndownloader/files/12345"

    def handler(request):
        if str(request.url) == article:
            return httpx.Response(
                200,
                text=f'<a href="{si}">Supporting Information ZIP</a>',
                request=request,
            )
        if str(request.url) == si:
            return httpx.Response(
                200,
                content=b"PK\x03\x04archive",
                headers={"content-type": "application/zip"},
                request=request,
            )
        raise AssertionError(str(request.url))

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        record = acquire_supplementary_materials(
            [{"paper_id": "p1", "doi": "10.1021/example"}],
            tmp_path,
            {"publisher_adapters": ["acs"]},
            client=client,
        )[0]
    attachment = record["supplementary_acquisition"]["attachments"][0]
    assert attachment["path"].endswith(".zip")
