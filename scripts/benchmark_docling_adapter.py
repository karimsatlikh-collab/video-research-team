"""Run a reproducible CPU Docling benchmark over a rights-cleared manifest.

Manifest schema: {"schema_version":1,"fixtures":[{"fixture_id":"...","path":"...","rights_review_state":"...","critical_tokens":["..."],"expected_locators":["..."]}]}
Paths are resolved under --root; paths escaping root are rejected.
"""
from __future__ import annotations

import argparse
import json
import platform
import sys
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

from openfx.docling_adapter import extract_local_document


def _norm(value: str) -> str:
    return unicodedata.normalize("NFC", value).casefold()


def score_artifact(artifact: dict, critical_tokens: list[str],
                   expected_locators: list[str]) -> dict:
    text = _norm(artifact["markdown"] + "\n" +
                 json.dumps(artifact["structured_document"], ensure_ascii=False))
    tokens = [_norm(token) for token in critical_tokens]
    locators_text = json.dumps(artifact["structured_document"],
                               ensure_ascii=False, sort_keys=True)
    locator_hits = [loc for loc in expected_locators if loc in locators_text]
    token_hits = [token for token in tokens if token in text]
    return {
        "critical_token_hits": len(token_hits),
        "critical_token_total": len(tokens),
        "critical_token_recall": (len(token_hits) / len(tokens) if tokens else None),
        "missing_critical_tokens": [critical_tokens[i] for i, token in enumerate(tokens)
                                    if token not in text],
        "locator_hits": len(locator_hits),
        "locator_total": len(expected_locators),
        "locator_recall": (len(locator_hits) / len(expected_locators)
                           if expected_locators else None),
        "missing_locators": [loc for loc in expected_locators if loc not in locators_text],
    }


def run(manifest_path: Path, root: Path, output_path: Path,
        max_file_bytes: int, max_pages: int) -> dict:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("schema_version") != 1 or not isinstance(manifest.get("fixtures"), list):
        raise ValueError("unsupported benchmark manifest")
    root = root.resolve(strict=True)
    rows = []
    for fixture in manifest["fixtures"]:
        fid = fixture["fixture_id"]
        candidate = (root / fixture["path"]).resolve(strict=True)
        if not candidate.is_relative_to(root):
            raise ValueError(f"fixture escapes root: {fid}")
        started = time.perf_counter()
        try:
            artifact = extract_local_document(
                candidate,
                rights_review_state=fixture["rights_review_state"],
                max_file_bytes=max_file_bytes,
                max_pages=max_pages,
            )
            elapsed = time.perf_counter() - started
            row = {
                "fixture_id": fid,
                "status": "success",
                "elapsed_seconds": elapsed,
                "source_sha256": artifact["source"]["sha256"],
                "artifact_sha256": artifact["artifact_sha256"],
                **score_artifact(artifact, fixture.get("critical_tokens", []),
                                 fixture.get("expected_locators", [])),
            }
        except Exception as exc:  # retain and classify per-file failures
            row = {
                "fixture_id": fid,
                "status": "failed",
                "elapsed_seconds": time.perf_counter() - started,
                "failure_type": type(exc).__name__,
                "failure": str(exc),
            }
        rows.append(row)

    result = {
        "schema_version": 1,
        "benchmark": "time-openfx-docling-cpu",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "manifest_sha256": __import__("hashlib").sha256(
            manifest_path.read_bytes()).hexdigest(),
        "limits": {"max_file_bytes": max_file_bytes, "max_pages": max_pages},
        "fixture_count": len(rows),
        "success_count": sum(row["status"] == "success" for row in rows),
        "failure_count": sum(row["status"] == "failed" for row in rows),
        "rows": rows,
        "limitations": [
            "No manual-time baseline is measured by this script.",
            "Critical-token recall is not precision and does not replace human review.",
            "Wall time includes cold/warm state as encountered; run repeated rounds separately.",
            "No hard CPU/RAM/wall-clock sandbox is provided by the adapter.",
        ],
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-file-bytes", type=int, default=25 * 1024 * 1024)
    parser.add_argument("--max-pages", type=int, default=100)
    args = parser.parse_args()
    result = run(args.manifest, args.root, args.output,
                 args.max_file_bytes, args.max_pages)
    print(json.dumps({k: result[k] for k in
                      ("fixture_count", "success_count", "failure_count")},
                     ensure_ascii=False))
    return 0 if result["failure_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
