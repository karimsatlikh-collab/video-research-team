# TIME-OPENFX benchmark protocol and manual baseline

## Freeze before measurement
- Freeze fixture manifest and all fixture SHA-256 values.
- Record Git commit, Python version, OS/CPU, Docling and transitive package versions,
  OCR/ASR model IDs/revisions, model cache state and all resource limits.
- Use the same files and ground truth for every candidate.
- Run at least 3 CPU rounds: first/cold start separately, then two warm rounds.
- Retain raw JSON output, stdout/stderr, failures and reviewer corrections.

## Human/manual baseline
The current metadata-only collector is not a content-extraction baseline. A valid
manual comparison requires a human operator to complete the same pre-defined task
for each fixture: open source, locate required passages, transcribe/copy critical
tokens, record page/time locators, and submit a structured result.

Record per fixture:
- operator pseudonym (no personal details), task start/end UTC, active seconds;
- interruption/idle seconds separately;
- exact critical-token and locator results against the same ground truth;
- corrections and review seconds;
- tool/software used and whether the operator had seen the fixture before.

Do not invent or backfill times. At least 10 representative fixtures and 2 operators
are preferred before generalizing; report individual results and median/p90, not
only a pooled mean. Keep human review time separate from machine runtime.

## Metrics and interpretation
The benchmark script reports extraction success, elapsed time, critical-token recall
and locator recall. These are not precision, semantic correctness, or proof that
the source supports a claim. Compare exact numbers, signs, units, percentages,
dates and negations separately. A missing or changed critical token is a blocking
failure even if average OCR/ASR quality is high.

The adapter's process memory and hard runtime limits are not enforced internally.
Use an OS/container sandbox with network disabled, read-only input, bounded temp
storage, CPU/RAM/time quotas, and no script/macro execution for any real corpus run.
Keep source files and model downloads out of public fixtures unless rights permit.

## Decision gate
- Keep the deterministic workflow kernel as default unless a matched-budget
  experiment shows specialist-agent handoffs improve quality enough to justify
  added latency, token cost and human review.
- Do not fine-tune models until a labelled benchmark identifies a stable failure
  mode that a pretrained tool cannot address.
- Do not claim project-level time savings until the manual baseline and automated
  runs use the same corpus and acceptance criteria.
- Do not enable paid APIs, VPS, cloud GPU, remote workers, MT5 or broker access
  without explicit authorization.
