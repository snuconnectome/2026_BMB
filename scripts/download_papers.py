#!/usr/bin/env python3
"""
Paper PDF Batch Downloader
--------------------------
Multi-source academic paper downloader with parallel execution.
Sources: Unpaywall, Semantic Scholar, PubMed Central, CrossRef, arXiv.
Falls back to saving abstracts when PDFs are unavailable.
"""

import re
import os
import csv
import time
import logging
import argparse
import threading
import unicodedata
from pathlib import Path
from typing import Optional
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from tqdm import tqdm

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

USER_EMAIL = "researcher@example.com"
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3

HEADERS = {
    "User-Agent": (
        "PaperDownloader/1.0 "
        f"(mailto:{USER_EMAIL}; academic research use)"
    )
}

# ---------------------------------------------------------------------------
# Thread-safe Rate Limiter
# ---------------------------------------------------------------------------

class RateLimiter:
    """Token-bucket style rate limiter. Thread-safe."""
    def __init__(self, calls_per_second: float):
        self._min_interval = 1.0 / calls_per_second
        self._lock = threading.Lock()
        self._last_call = 0.0

    def wait(self):
        with self._lock:
            now = time.monotonic()
            elapsed = now - self._last_call
            if elapsed < self._min_interval:
                time.sleep(self._min_interval - elapsed)
            self._last_call = time.monotonic()

# One limiter per API endpoint
_semantic_scholar_limiter = RateLimiter(0.3)   # ~18 req/min (conservative)
_unpaywall_limiter = RateLimiter(5.0)          # generous
_pmc_limiter = RateLimiter(2.5)               # NCBI: 3/sec, be polite
_crossref_limiter = RateLimiter(3.0)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Data Model
# ---------------------------------------------------------------------------

@dataclass
class Reference:
    num: int
    raw: str
    authors: str = ""
    title: str = ""
    journal: str = ""
    year: str = ""
    doi: str = ""
    arxiv_id: str = ""
    is_book: bool = False

@dataclass
class DownloadResult:
    ref: Reference
    status: str = "pending"       # pdf_downloaded | abstract_saved | metadata_only | failed
    source: str = ""
    file_path: str = ""
    abstract: str = ""
    pdf_url: str = ""

# ---------------------------------------------------------------------------
# Reference Parser
# ---------------------------------------------------------------------------

def parse_references(text: str) -> list[Reference]:
    """Parse numbered reference list into structured Reference objects."""
    refs: list[Reference] = []
    lines = text.strip().split("\n")

    buffer = ""
    current_num = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        match = re.match(r"^(\d{1,3})\s+(.+)$", line) or re.match(r"^(\d{1,3})\t(.+)$", line)
        if match:
            if current_num is not None and buffer:
                refs.append(_parse_single_ref(current_num, buffer))
            current_num = int(match.group(1))
            buffer = match.group(2).strip()
        else:
            buffer += " " + line

    if current_num is not None and buffer:
        refs.append(_parse_single_ref(current_num, buffer))

    return refs


def _split_author_title(text: str) -> tuple[str, str, str]:
    """Split 'Authors. Title. Journal/Rest' handling initials and 'et al.' correctly.
    Returns (authors, title, rest).
    """
    in_match = re.search(r"(?:^|\.\s+)in\s+", text)
    if in_match:
        authors = text[:in_match.start()].strip().rstrip(".")
        rest = text[in_match.end():]
        return authors, rest.strip(), ""

    et_al_match = re.search(r"et al\.\s+", text)
    if et_al_match:
        authors = text[:et_al_match.end()].strip()
        rest = text[et_al_match.end():]
        title, journal_rest = _split_title_journal(rest)
        return authors, title, journal_rest

    last_initial_pos = -1
    for m in re.finditer(r"(?<=[A-Z])\.\s+", text):
        before = text[:m.start() + 1]
        prefix = before[-3:].lstrip()
        if re.match(r"^[A-Z]{1,2}\.$", prefix) or re.match(r"^[A-Z]\.$", before[-2:]):
            last_initial_pos = m.end()

    if last_initial_pos > 0:
        authors = text[:last_initial_pos].strip()
        rest = text[last_initial_pos:]
        title, journal_rest = _split_title_journal(rest)
        return authors, title, journal_rest

    candidates = list(re.finditer(r"\.\s+(?=[A-Z])", text))
    if candidates:
        m = candidates[0]
        authors = text[:m.start() + 1].strip()
        rest = text[m.end():]
        title, journal_rest = _split_title_journal(rest)
        return authors, title, journal_rest

    return "", text, ""


def _split_title_journal(text: str) -> tuple[str, str]:
    """Split 'Title. Journal Volume, Pages (Year)...' into (title, rest)."""
    match = re.search(
        r"[.?!]\s+"
        r"(?="
        r"(?:Nature|Science|Neuron|PNAS|JAMA|eLife|Cell|IEEE|Proceedings|Journal|"
        r"Trends|Brain|Progress|NeuroImage|Psychol|Behavioral|Child|Current|"
        r"American|Annual|Frontiers|PLOS|Econometrica|World|Social|Political|"
        r"BMC|Scientific|Digital|Academy|Personality|Review|Neuropsychopharmacology|"
        r"The\s+(?:Lancet|Quarterly|American|Annals|Asia)|"
        r"Curr\s+Biol|Psychol\s+Sci|Am\s+Econ|Annu\s+Rev|"
        r"Developmental|NEJM|Patterns|Technovation|European|"
        r"National\s+Bureau|Research\s+Square|IMF|AI\s+and\s+Ethics)"
        r")",
        text,
    )
    if match:
        return text[:match.start() + 1].strip(), text[match.end():].strip()

    match = re.search(r"[.?!]\s+(?=[A-Z][a-z])", text)
    if match:
        after = text[match.end():]
        if re.search(r"\d+[,\s]+\d+", after[:80]):
            return text[:match.start() + 1].strip(), text[match.end():].strip()

    year_match = re.search(r"\(\d{4}\)", text)
    if year_match:
        before_year = text[:year_match.start()]
        last_dot = before_year.rfind(". ")
        if last_dot > 0:
            return text[:last_dot + 1].strip(), text[last_dot + 2:].strip()

    return text.strip(), ""


def _parse_single_ref(num: int, raw: str) -> Reference:
    ref = Reference(num=num, raw=raw)

    doi_match = re.search(
        r"(?:DOI:\s*(?:https?://(?:dx\.)?doi\.org/)?|https?://(?:dx\.)?doi\.org/)"
        r"(10\.\d{4,}/[^\s,;]+)",
        raw,
    )
    if doi_match:
        ref.doi = doi_match.group(1).rstrip(".)")

    arxiv_match = re.search(r"arXiv[:\s]*(\d{4}\.\d{4,5})", raw)
    if arxiv_match:
        ref.arxiv_id = arxiv_match.group(1)

    year_matches = re.findall(r"\((\d{4})\)", raw)
    if year_matches:
        ref.year = year_matches[-1]

    clean = re.sub(r"DOI:\s*\S*", "", raw).strip()
    clean = re.sub(r"https?://\S+", "", clean).strip()
    clean = re.sub(r"<[^>]+>", "", clean).strip()

    ref.authors, ref.title, _ = _split_author_title(clean)
    ref.title = ref.title.rstrip(".")

    book_indicators = [
        "University Press", "Penguin", "Avon Books", "Harper & Row",
        "Crown Currency", "CRC Press", "Broadview Press", "Oxford and IBH",
        "Johns Hopkins",
    ]
    if any(ind in raw for ind in book_indicators):
        ref.is_book = True

    return ref


# ---------------------------------------------------------------------------
# API Resolvers
# ---------------------------------------------------------------------------

def _get_with_retry(
    url: str,
    params: dict = None,
    limiter: Optional[RateLimiter] = None,
    **kwargs,
) -> Optional[requests.Response]:
    timeout = kwargs.pop("timeout", REQUEST_TIMEOUT)
    for attempt in range(MAX_RETRIES + 1):
        if limiter:
            limiter.wait()
        try:
            resp = requests.get(url, params=params, headers=HEADERS, timeout=timeout, **kwargs)
            if resp.status_code == 429:
                wait = min(int(resp.headers.get("Retry-After", 3 * (attempt + 1))), 30)
                time.sleep(wait)
                continue
            return resp
        except requests.RequestException as e:
            if attempt < MAX_RETRIES:
                time.sleep(2 ** attempt)
            else:
                log.debug("Request failed after retries: %s", e)
    return None


def resolve_unpaywall(doi: str) -> tuple[Optional[str], str]:
    if not doi:
        return None, ""
    url = f"https://api.unpaywall.org/v2/{doi}"
    resp = _get_with_retry(url, params={"email": USER_EMAIL}, limiter=_unpaywall_limiter)
    if resp and resp.status_code == 200:
        data = resp.json()
        best = data.get("best_oa_location") or {}
        pdf_url = best.get("url_for_pdf") or best.get("url")
        if not pdf_url:
            for loc in data.get("oa_locations", []):
                pdf_url = loc.get("url_for_pdf") or loc.get("url")
                if pdf_url:
                    break
        return pdf_url, ""
    return None, ""


def resolve_semantic_scholar(doi: str = "", title: str = "") -> tuple[Optional[str], str]:
    base = "https://api.semanticscholar.org/graph/v1/paper"
    fields = "title,abstract,openAccessPdf,externalIds,url"

    if doi:
        url = f"{base}/DOI:{doi}"
        resp = _get_with_retry(url, params={"fields": fields}, limiter=_semantic_scholar_limiter)
    elif title:
        resp = _get_with_retry(
            f"{base}/search",
            params={"query": title[:200], "fields": fields, "limit": 1},
            limiter=_semantic_scholar_limiter,
        )
    else:
        return None, ""

    if resp and resp.status_code == 200:
        data = resp.json()
        if "data" in data:
            data = data["data"][0] if data["data"] else {}
        abstract = data.get("abstract", "") or ""
        oa_pdf = data.get("openAccessPdf") or {}
        pdf_url = oa_pdf.get("url")
        return pdf_url, abstract
    return None, ""


def resolve_pmc(doi: str) -> tuple[Optional[str], str]:
    if not doi:
        return None, ""
    url = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/"
    resp = _get_with_retry(
        url,
        params={"ids": doi, "format": "json", "tool": "paper_dl", "email": USER_EMAIL},
        limiter=_pmc_limiter,
    )
    if resp and resp.status_code == 200:
        data = resp.json()
        records = data.get("records", [])
        if records and records[0].get("pmcid"):
            pmcid = records[0]["pmcid"]
            pdf_url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmcid}/pdf/"
            return pdf_url, ""
    return None, ""


def resolve_crossref(doi: str) -> tuple[Optional[str], str]:
    if not doi:
        return None, ""
    url = f"https://api.crossref.org/works/{doi}"
    resp = _get_with_retry(url, params={"mailto": USER_EMAIL}, limiter=_crossref_limiter)
    if resp and resp.status_code == 200:
        data = resp.json().get("message", {})
        for link in data.get("link", []):
            if "pdf" in link.get("content-type", "").lower():
                return link.get("URL"), ""
        abstract = data.get("abstract", "")
        if abstract:
            abstract = re.sub(r"<[^>]+>", "", abstract)
        return None, abstract
    return None, ""


def resolve_arxiv(arxiv_id: str) -> tuple[Optional[str], str]:
    if not arxiv_id:
        return None, ""
    return f"https://arxiv.org/pdf/{arxiv_id}.pdf", ""


def resolve_doi_content_negotiation(doi: str) -> tuple[Optional[str], str]:
    if not doi:
        return None, ""
    url = f"https://doi.org/{doi}"
    try:
        resp = requests.head(
            url,
            headers={**HEADERS, "Accept": "application/pdf"},
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True,
        )
        if resp.status_code == 200 and "pdf" in resp.headers.get("Content-Type", "").lower():
            return resp.url, ""
    except requests.RequestException:
        pass
    return None, ""


def _sanitize_filename(name: str, max_len: int = 60) -> str:
    name = unicodedata.normalize("NFKD", name)
    name = re.sub(r"[^\w\s\-]", "", name)
    name = re.sub(r"\s+", "_", name).strip("_")
    return name[:max_len]


def download_pdf(url: str, dest_path: Path) -> bool:
    try:
        resp = requests.get(
            url,
            headers={**HEADERS, "Accept": "application/pdf"},
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True,
        )
        if resp.status_code != 200:
            return False
        content = resp.content
        if len(content) < 1000:
            return False
        if not content[:5] == b"%PDF-" and b"%PDF" not in content[:1024]:
            return False
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dest_path, "wb") as f:
            f.write(content)
        return True
    except Exception as e:
        log.debug("Download error for %s: %s", url, e)
        dest_path.unlink(missing_ok=True)
        return False


def process_single_paper(ref: Reference, pdf_dir: Path, abs_dir: Path) -> DownloadResult:
    result = DownloadResult(ref=ref)
    first_author = ref.authors.split(",")[0].split("&")[0].strip().split()[-1] if ref.authors else "Unknown"
    base_name = f"{ref.num:03d}_{_sanitize_filename(first_author)}_{ref.year}"
    pdf_path = pdf_dir / f"{base_name}.pdf"
    abs_path = abs_dir / f"{base_name}.txt"

    abstract_collected = ""
    resolvers = []

    if ref.arxiv_id:
        resolvers.append(("arXiv", lambda aid=ref.arxiv_id: resolve_arxiv(aid)))

    if ref.doi:
        resolvers.extend([
            ("Unpaywall", lambda d=ref.doi: resolve_unpaywall(d)),
            ("SemanticScholar", lambda d=ref.doi: resolve_semantic_scholar(doi=d)),
            ("PMC", lambda d=ref.doi: resolve_pmc(d)),
            ("CrossRef", lambda d=ref.doi: resolve_crossref(d)),
            ("DOI-Negotiation", lambda d=ref.doi: resolve_doi_content_negotiation(d)),
        ])
    else:
        resolvers.append(
            ("SemanticScholar", lambda t=ref.title: resolve_semantic_scholar(title=t))
        )

    for source_name, resolver_fn in resolvers:
        try:
            pdf_url, abstract = resolver_fn()
            if abstract:
                abstract_collected = abstract
            if pdf_url:
                log.info("[%03d] Trying %s: %s", ref.num, source_name, pdf_url[:80])
                if download_pdf(pdf_url, pdf_path):
                    result.status = "pdf_downloaded"
                    result.source = source_name
                    result.file_path = str(pdf_path)
                    result.pdf_url = pdf_url
                    log.info("[%03d] OK — %s via %s", ref.num, ref.title[:50], source_name)
                    return result
        except Exception as e:
            log.debug("[%03d] %s failed: %s", ref.num, source_name, e)

    if not abstract_collected and not ref.doi and ref.title:
        try:
            _, abstract_collected = resolve_semantic_scholar(title=ref.title)
        except Exception:
            pass

    if abstract_collected:
        abs_path.parent.mkdir(parents=True, exist_ok=True)
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write(f"Title: {ref.title}\n")
            f.write(f"Authors: {ref.authors}\n")
            f.write(f"Year: {ref.year}\n")
            f.write(f"DOI: {ref.doi}\n")
            f.write(f"Journal: {ref.journal}\n")
            f.write(f"\n--- Abstract ---\n\n{abstract_collected}\n")
        result.status = "abstract_saved"
        result.file_path = str(abs_path)
        result.abstract = abstract_collected[:200]
        log.info("[%03d] Abstract saved — %s", ref.num, ref.title[:50])
    elif ref.is_book:
        abs_path.parent.mkdir(parents=True, exist_ok=True)
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write(f"Title: {ref.title}\nAuthors: {ref.authors}\nYear: {ref.year}\nType: Book\n")
        result.status = "metadata_only"
        result.file_path = str(abs_path)
        log.info("[%03d] Book metadata saved — %s", ref.num, ref.title[:50])
    else:
        result.status = "failed"
        log.warning("[%03d] FAILED — %s", ref.num, ref.title[:50])

    return result


def run_batch_download(
    refs: list[Reference],
    output_dir: Path,
    max_workers: int = 8,
) -> list[DownloadResult]:
    pdf_dir = output_dir / "papers"
    abs_dir = output_dir / "abstracts"
    pdf_dir.mkdir(parents=True, exist_ok=True)
    abs_dir.mkdir(parents=True, exist_ok=True)

    results: list[DownloadResult] = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {
            executor.submit(process_single_paper, ref, pdf_dir, abs_dir): ref
            for ref in refs
        }
        with tqdm(total=len(refs), desc="Downloading papers", unit="paper") as pbar:
            for future in as_completed(future_map):
                ref = future_map[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    log.error("[%03d] Exception: %s", ref.num, e)
                    results.append(DownloadResult(ref=ref, status="failed"))
                pbar.update(1)

    results.sort(key=lambda r: r.ref.num)
    return results


def generate_report(results: list[DownloadResult], output_dir: Path) -> Path:
    report_path = output_dir / "download_report.csv"
    with open(report_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["num", "authors", "title", "year", "doi", "status", "source", "file_path", "pdf_url"])
        for r in results:
            writer.writerow([
                r.ref.num,
                r.ref.authors[:60],
                r.ref.title[:100],
                r.ref.year,
                r.ref.doi,
                r.status,
                r.source,
                r.file_path,
                r.pdf_url,
            ])

    total = len(results)
    pdfs = sum(1 for r in results if r.status == "pdf_downloaded")
    abstracts = sum(1 for r in results if r.status == "abstract_saved")
    metadata = sum(1 for r in results if r.status == "metadata_only")
    failed = sum(1 for r in results if r.status == "failed")

    log.info("=" * 60)
    log.info("DOWNLOAD COMPLETE  Total: %d  PDFs: %d  Abstracts: %d  Metadata: %d  Failed: %d",
             total, pdfs, abstracts, metadata, failed)
    log.info("Report: %s", report_path)
    log.info("=" * 60)

    return report_path


def main():
    parser = argparse.ArgumentParser(description="Batch download academic paper PDFs")
    parser.add_argument("--input", "-i", type=str, required=True,
                        help="Path to a text file containing numbered references")
    parser.add_argument("--output", "-o", type=str, default=".",
                        help="Output directory for papers/ and abstracts/")
    parser.add_argument("--workers", "-w", type=int, default=8,
                        help="Number of parallel download threads (default: 8)")
    parser.add_argument("--email", "-e", type=str, default=USER_EMAIL,
                        help="Email for API polite pool (Unpaywall, CrossRef)")
    args = parser.parse_args()

    HEADERS["User-Agent"] = f"PaperDownloader/1.0 (mailto:{args.email}; academic research use)"

    with open(args.input, "r", encoding="utf-8") as f:
        ref_text = f.read()

    output_dir = Path(args.output).resolve()
    log.info("Parsing references...")
    refs = parse_references(ref_text)
    log.info("Found %d references", len(refs))

    for r in refs:
        log.info("  [%03d] %s | DOI: %s | arXiv: %s | book: %s",
                 r.num, r.title[:50], r.doi or "-", r.arxiv_id or "-", r.is_book)

    log.info("Starting download with %d workers...", args.workers)
    results = run_batch_download(refs, output_dir, max_workers=args.workers)
    report_path = generate_report(results, output_dir)
    print(f"\nReport saved to: {report_path}")


if __name__ == "__main__":
    main()
