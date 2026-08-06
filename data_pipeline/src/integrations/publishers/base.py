from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from urllib.parse import parse_qs, unquote, urldefrag, urljoin, urlparse

import httpx


@dataclass(frozen=True)
class PublisherAttachment:
    url: str
    file_name: str
    publisher: str
    discovered_from: str
    label: str

    def as_dict(self) -> dict[str, str]:
        return asdict(self)


class PublisherSupplementaryAdapter:
    publisher = "unknown"
    domains: tuple[str, ...] = ()
    doi_prefixes: tuple[str, ...] = ()
    can_confirm_absence_from_page = True
    supplementary_pattern = re.compile(
        r"supp(?:lement|orting|info)|supporting.?information|electronic.?supplement|esm|mmc",
        re.I,
    )

    def matches(self, *, doi: str | None, article_url: str | None) -> bool:
        host = urlparse(article_url or "").hostname or ""
        return self._official_host(host) or any(
            str(doi or "").casefold().startswith(prefix.casefold())
            for prefix in self.doi_prefixes
        )

    def article_url(self, *, doi: str | None, article_url: str | None) -> str | None:
        return article_url or (f"https://doi.org/{doi}" if doi else None)

    def discover(
        self,
        client: httpx.Client,
        *,
        doi: str | None,
        article_url: str | None,
    ) -> tuple[list[PublisherAttachment], dict[str, str | int | None]]:
        target = self.article_url(doi=doi, article_url=article_url)
        if not target:
            return [], {"publisher": self.publisher, "status": "missing_article_identifier"}
        response = client.get(target)
        response.raise_for_status()
        final_url = str(response.url)
        if not self._official_host(urlparse(final_url).hostname or ""):
            raise PermissionError(
                f"publisher landing page redirected outside official domains: {final_url}"
            )
        parser = _LinkParser()
        parser.feed(response.text)
        output: dict[str, PublisherAttachment] = {}
        for href, label in parser.links:
            if not href.strip() or href.lstrip().startswith("#"):
                continue
            url, _fragment = urldefrag(urljoin(final_url, href))
            host = urlparse(url).hostname or ""
            if not self._official_host(host):
                continue
            if not self.supplementary_pattern.search(f"{href} {label}"):
                continue
            name = _attachment_name(url, len(output) + 1)
            output.setdefault(
                url,
                PublisherAttachment(
                    url=url,
                    file_name=name,
                    publisher=self.publisher,
                    discovered_from=final_url,
                    label=" ".join(label.split())[:500],
                ),
            )
        doi_present = bool(
            doi and str(doi).casefold() in unquote(response.text).casefold()
        )
        return list(output.values()), {
            "publisher": self.publisher,
            "status": "publisher_attachments_found" if output else "not_found",
            "landing_url": final_url,
            "http_status": response.status_code,
            "absence_confirmed": bool(
                not output and doi_present and self.can_confirm_absence_from_page
            ),
        }

    def official_attachment_url(self, url: str) -> bool:
        return self._official_host(urlparse(url).hostname or "")

    def _official_host(self, host: str) -> bool:
        value = host.casefold().rstrip(".")
        return any(value == domain or value.endswith(f".{domain}") for domain in self.domains)


class _LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self._href: str | None = None
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs):
        values = dict(attrs)
        if tag.casefold() == "meta":
            name = str(values.get("name") or values.get("property") or "")
            content = str(values.get("content") or "")
            if content and re.search(r"supplement|supporting", name, re.I):
                self.links.append((content, name))
            return
        if tag.casefold() == "link":
            relation = str(values.get("rel") or "")
            href = str(values.get("href") or "")
            if href and re.search(r"supplement|supporting", relation, re.I):
                self.links.append((href, relation))
            return
        if tag.casefold() != "a":
            return
        self._href = values.get("href")
        self._text = [values.get("title") or "", values.get("aria-label") or ""]

    def handle_data(self, data: str):
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag: str):
        if tag.casefold() == "a" and self._href:
            self.links.append((self._href, " ".join(self._text)))
            self._href = None
            self._text = []


def _attachment_name(url: str, index: int) -> str:
    parsed = urlparse(url)
    query_name = (parse_qs(parsed.query).get("file") or [""])[0]
    name = unquote(query_name or parsed.path.rsplit("/", 1)[-1]).strip()
    name = re.sub(r"[^A-Za-z0-9._()-]+", "_", name).strip("._")
    return (name or f"supplementary-{index}")[:220]
