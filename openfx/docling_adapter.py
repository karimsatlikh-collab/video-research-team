"""Optional, read-only Docling adapter with provenance metadata.

Docling is imported lazily. The core OpenFX install remains dependency-free.
Only local files are accepted; this adapter never fetches URLs or executes
source content. Extraction output is unverified evidence, never a verified claim.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any, Callable

SUPPORTED_EXTENSIONS = {
    ".pdf", ".docx", ".xlsx", ".pptx", ".html", ".htm",
    ".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp",
}
DEFAULT_MAX_FILE_BYTES = 25 * 1024 * 1024
DEFAULT_MAX_PAGES = 100


class ExtractionError(RuntimeError):
    """Raised when a local extraction cannot safely complete."""


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, ensure_ascii=False,
                         separators=(",", ":"), default=str).encode("utf-8")
    return _sha256_bytes(payload)


def _docling_converter() -> Any:
    try:
        from docling.document_converter import DocumentConverter
    except ImportError as exc:
        raise ExtractionError(
            "Docling is optional and is not installed. Install the pinned "
            "requirements-docling.txt in an isolated environment."
        ) from exc
    return DocumentConverter()


def extract_local_document(
    source_path: str | Path,
    *,
    rights_review_state: str = "unknown",
    max_file_bytes: int = DEFAULT_MAX_FILE_BYTES,
    max_pages: int = DEFAULT_MAX_PAGES,
    converter_factory: Callable[[], Any] | None = None,
) -> dict[str, Any]:
    """Extract one bounded local document and return a provenance envelope.

    max_pages and max_file_bytes are passed/enforced at the adapter boundary.
    A hard wall-clock/CPU/RAM sandbox is an outer-runner responsibility and is
    deliberately not claimed by this in-process adapter.
    """
    if max_file_bytes <= 0 or max_pages <= 0:
        raise ValueError("resource limits must be positive")
    if not rights_review_state or not isinstance(rights_review_state, str):
        raise ValueError("rights_review_state must be an explicit string")

    path = Path(source_path).expanduser().resolve(strict=True)
    if not path.is_file():
        raise ExtractionError("source must be a local regular file")
    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ExtractionError(f"unsupported document type: {path.suffix.lower()}")
    size = path.stat().st_size
    if size > max_file_bytes:
        raise ExtractionError("source exceeds max_file_bytes")

    source_hash_before = _sha256_file(path)
    config = {
        "adapter": "openfx.docling_adapter",
        "max_file_bytes": max_file_bytes,
        "max_pages": max_pages,
        "rights_review_state": rights_review_state,
    }
    converter = (converter_factory or _docling_converter)()
    result = converter.convert(
        path, raises_on_error=False, max_num_pages=max_pages,
        max_file_size=max_file_bytes,
    )
    source_hash_after = _sha256_file(path)
    if source_hash_before != source_hash_after:
        raise ExtractionError("source changed during extraction")

    document = getattr(result, "document", None)
    if document is None:
        errors = [str(item) for item in (getattr(result, "errors", None) or [])]
        raise ExtractionError("Docling returned no document: " + "; ".join(errors))

    markdown = document.export_to_markdown()
    if not isinstance(markdown, str):
        raise ExtractionError("Docling returned non-text Markdown output")
    structured = document.export_to_dict()
    artifact = {
        "schema_version": 1,
        "source": {
            "file_name": path.name,
            "file_size_bytes": size,
            "sha256": source_hash_before,
        },
        "extraction": {
            "tool": "docling",
            "tool_version": _docling_version(),
            "config": config,
            "config_sha256": _canonical_hash(config),
            "completed_at_utc": datetime.now(timezone.utc).isoformat(),
            "status": str(getattr(getattr(result, "status", None), "value",
                                  getattr(result, "status", "unknown"))),
            "errors": [str(item) for item in (getattr(result, "errors", None) or [])],
        },
        "rights_review_state": rights_review_state,
        "verification_state": "unverified_extraction",
        "markdown": markdown,
        "structured_document": structured,
    }
    artifact["artifact_sha256"] = _canonical_hash(artifact)
    return artifact


def _docling_version() -> str:
    try:
        return version("docling")
    except PackageNotFoundError:
        return "unknown"
