from __future__ import annotations

import re
from urllib.parse import unquote, urlparse

from src.integrations.publishers.base import (
    PublisherAttachment,
    PublisherSupplementaryAdapter,
)


class ACSSupplementaryAdapter(PublisherSupplementaryAdapter):
    publisher = "acs"
    domains = ("acs.org", "acs.figshare.com")
    doi_prefixes = ("10.1021/",)

    def article_url(self, *, doi, article_url):
        return f"https://pubs.acs.org/doi/{doi}" if doi else super().article_url(
            doi=doi, article_url=article_url
        )


class RSCSupplementaryAdapter(PublisherSupplementaryAdapter):
    publisher = "rsc"
    domains = ("rsc.org",)
    doi_prefixes = ("10.1039/",)

    def article_url(self, *, doi, article_url):
        value = str(doi or "").casefold()
        code = value.split("/", 1)[-1]
        decade = {"a": 1990, "b": 2000, "c": 2010, "d": 2020}.get(
            code[:1]
        )
        if len(code) >= 5 and decade is not None and code[1].isdigit():
            return (
                f"https://pubs.rsc.org/en/content/articlelanding/{decade + int(code[1])}/"
                f"{code[2:4]}/{code}"
            )
        return super().article_url(doi=doi, article_url=article_url)


class ElsevierSupplementaryAdapter(PublisherSupplementaryAdapter):
    publisher = "elsevier"
    domains = (
        "sciencedirect.com",
        "elsevier.com",
        "elseviercdn.com",
        "els-cdn.com",
    )
    doi_prefixes = ("10.1016/",)
    can_confirm_absence_from_page = False
    attachment_extensions = (
        "pdf",
        "docx",
        "zip",
        "xlsx",
        "csv",
        "txt",
        "pptx",
        "mp4",
        "mov",
        "avi",
    )

    def discover(self, client, *, doi, article_url):
        attachments, metadata = super().discover(
            client, doi=doi, article_url=article_url
        )
        if attachments:
            return attachments, metadata
        pii = _elsevier_pii(str(metadata.get("landing_url") or ""))
        if not pii:
            return attachments, metadata
        attachments, probes = self._discover_cdn_attachments(client, pii)
        return attachments, {
            **metadata,
            "status": "publisher_attachments_found" if attachments else "not_found",
            "absence_confirmed": bool(not attachments),
            "pii": pii,
            "cdn_probes": probes,
        }

    def _discover_cdn_attachments(self, client, pii):
        output: list[PublisherAttachment] = []
        probes = 0
        for index in range(1, 11):
            found_at_index = False
            for extension in self.attachment_extensions:
                probes += 1
                url = (
                    "https://ars.els-cdn.com/content/image/"
                    f"1-s2.0-{pii}-mmc{index}.{extension}"
                )
                response = client.head(url, headers={"Range": "bytes=0-0"})
                if response.status_code == 404:
                    continue
                if response.status_code in {401, 403, 429}:
                    response.raise_for_status()
                if response.status_code not in {200, 206}:
                    continue
                found_at_index = True
                output.append(
                    PublisherAttachment(
                        url=url,
                        file_name=f"{pii}-mmc{index}.{extension}",
                        publisher=self.publisher,
                        discovered_from=str(response.url),
                        label=f"Elsevier supplementary attachment mmc{index}",
                    )
                )
                break
            if not found_at_index:
                break
        return output, probes


class WileySupplementaryAdapter(PublisherSupplementaryAdapter):
    publisher = "wiley"
    domains = ("wiley.com", "onlinelibrary.wiley.com")
    doi_prefixes = ("10.1002/", "10.1111/")

    def article_url(self, *, doi, article_url):
        return (
            f"https://onlinelibrary.wiley.com/doi/{doi}"
            if doi
            else super().article_url(doi=doi, article_url=article_url)
        )


class NatureSupplementaryAdapter(PublisherSupplementaryAdapter):
    publisher = "nature"
    domains = (
        "nature.com",
        "springernature.com",
        "springer.com",
    )
    doi_prefixes = ("10.1038/",)

    def article_url(self, *, doi, article_url):
        if doi and "/" in doi:
            return f"https://www.nature.com/articles/{doi.split('/', 1)[1]}"
        return super().article_url(doi=doi, article_url=article_url)


class MDPISupplementaryAdapter(PublisherSupplementaryAdapter):
    publisher = "mdpi"
    domains = ("mdpi.com", "mdpi-res.com")
    doi_prefixes = ("10.3390/",)


PUBLISHER_ADAPTERS = (
    ACSSupplementaryAdapter(),
    RSCSupplementaryAdapter(),
    ElsevierSupplementaryAdapter(),
    WileySupplementaryAdapter(),
    NatureSupplementaryAdapter(),
    MDPISupplementaryAdapter(),
)


def _elsevier_pii(url: str) -> str | None:
    match = re.search(r"/pii/([A-Z0-9]+)", url, re.I)
    return match.group(1) if match else None


def publisher_adapter(
    *, doi: str | None, article_url: str | None, enabled: list[str] | None = None
) -> PublisherSupplementaryAdapter | None:
    if not doi and (urlparse(article_url or "").hostname or "").casefold() in {
        "doi.org",
        "www.doi.org",
    }:
        doi = unquote(urlparse(article_url or "").path.lstrip("/")) or None
    allowed = {item.casefold() for item in enabled} if enabled else None
    for adapter in PUBLISHER_ADAPTERS:
        if allowed is not None and adapter.publisher not in allowed:
            continue
        if adapter.matches(doi=doi, article_url=article_url):
            return adapter
    return None
