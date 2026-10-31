# Optional Docling extraction adapter

The base OpenFX runtime remains dependency-free. The optional adapter is read-only
and accepts local PDF, Office, HTML and image files only. It never fetches URLs,
runs macros/scripts, or upgrades extracted text into a verified claim.

## Isolated CPU installation

Use a disposable virtual environment and inspect the dependency plan before
installing. Docling downloads model artifacts on first use; this can consume
substantial disk space and network bandwidth. Do not install it on the small
project VPS or in the base environment by default.

```bash
python -m venv .venv-docling
. .venv-docling/bin/activate
python -m pip install --dry-run -r requirements-docling.txt
# Proceed only after reviewing package versions, disk use and licenses:
python -m pip install -r requirements-docling.txt
```

The pinned version is a reproducibility starting point, not a security guarantee.
Record the resolved transitive dependency lock and model revisions before a
benchmark. The package's MIT license does not automatically license its model
weights or optional dependencies.

## API

```python
from openfx.docling_adapter import extract_local_document

artifact = extract_local_document(
    "fixtures/my-authorized-file.pdf",
    rights_review_state="owner_created",
    max_file_bytes=25 * 1024 * 1024,
    max_pages=100,
)
```

The returned envelope contains source and artifact SHA-256, tool version,
configuration hash, status/errors, Markdown, structured Docling output and the
rights state supplied by the caller. It always says
`verification_state=unverified_extraction`. The adapter does not infer rights.

## Limits and next validation gate

The adapter enforces local-file type, size and Docling page-count limits. It
does not itself provide a hard CPU/RAM/wall-clock sandbox; run it in an outer
process/container with OS limits and no network. Audio/video ASR is intentionally
not wired into this first adapter because it needs separate optional extras,
FFmpeg, model downloads and Persian/English accuracy validation.

CI tests use a fake converter and do not install Docling or download models.
A real CPU run on a rights-clear, labelled fixture corpus is still required
before claiming extraction quality, speedup, Persian accuracy or operational
readiness.
