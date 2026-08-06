from __future__ import annotations

from urllib.parse import unquote, urlparse

from src.integrations.publishers.base import PublisherSupplementaryAdapter


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
