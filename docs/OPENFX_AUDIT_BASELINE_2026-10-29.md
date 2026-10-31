# OpenFX Independent Audit — Baseline and Initial Findings

**Date:** 2026-10-29  
**Status:** Initial evidence-backed baseline; full audit remains in progress  
**Repository:** `karimsatlikh-collab/openfx-research-lab`  
**Default branch inspected:** `main` at `25c1366097c2ddf3a7951111ca9e9a1e6e4928b6`  
**Method:** GitHub repository/branch/PR/file inspection plus review of recorded GitHub Actions run statuses. No local clone was possible in this execution environment, so no local Python test command is claimed to have run.

## 1. Executive summary

**OpenFX is currently a research/engineering scaffold, not an end-to-end autonomous research system and not a trading validation platform.** The default `main` branch contains local-file metadata collection, basic metadata checks, an experiment scaffold, a mock worker, schemas, documentation, and CI. It does not contain the source/evidence research modules currently present in the open PR branch chain, and it has no real MT5 execution adapter.

A substantial feature set exists on non-main branches: source registry validation, transcript import and heuristic quality checks, evidence-linked claims, YouTube metadata search, MT5 HTML summary parsing, and stricter experiment/worker validation. These are meaningful prototypes, but they are not part of `main` and do not establish autonomous video extraction, semantic verification, real Strategy Tester execution, or profitable strategy performance.

The most important immediate risk is **branch/release ambiguity**: several capabilities described in the feature-branch roadmap and tests are not yet in the default branch. A report or user must identify the exact branch and commit for every capability claim.

## 2. Evidence and confidence labels

- **Observed:** directly read from the current repository tree, file, branch, PR metadata, or Actions API response.
- **CI-confirmed:** a named GitHub Actions run completed successfully for the stated commit. This confirms only the checks that workflow actually executes.
- **Code-reviewed:** inferred from inspected source code; no separate runtime test was performed here.
- **Not established:** no evidence was found in the inspected repository/status to support the capability.

No live trading, MT5 Strategy Tester execution, VPS deployment, or end-to-end source-to-experiment run is established by this audit.

## 3. Branch and pull-request baseline

| Item | Observed state | Implication |
|---|---|---|
| `main` | Commit `25c1366097c2ddf3a7951111ca9e9a1e6e4928b6`; 62 tracked tree entries observed | This remains the default-branch baseline; none of this audit's PRs has been merged. |
| PR #11 `openfx-audit-fixes` | Open; head `28161cb4622e4bd92ba356508b97409f6149a1af`; base `main` | Broad research/evidence/result-validation feature set and stricter experiment/worker validation; not in main. |
| PR #12 `openfx-transcript-adversarial-checks` | Open; head `649631de5f3a08be1ca0941ede4ff3646b346063`; base `openfx-audit-fixes` | Percentage-symbol fidelity checks; depends on PR #11 branch. |
| PR #13 mission/state/audit docs | Open; current head `6bd0e1b67849ca29aa3fa81071163ea0afbe171e`; base `main` | Holds the mission charter, continuity ledger, and evolving audit report. |
| PR #14 numeric glyph normalization | Open; head `61047b9a45ea556799a4d4c1c15073dc45e9025e`; base `openfx-transcript-adversarial-checks` | Normalizes equivalent numeric glyphs; exact-head CI passed. |
| PR #15 schema validation | Open; head `dc3e665efb95c93f0d55fddbd2fb1a7075b60b58`; base `openfx-audit-round1` | Adds executable JSON Schema validation and fixtures; exact-head CI passed. |
| PR #16 transcript import strictness | Open; head `5b6ad0b910b2501a67293f8fe5b4451a2b89192e`; base `openfx-audit-round1` | Fails closed on malformed subtitle blocks and preserves cue IDs resembling metadata; exact-head CI passed. |
| PR #17 rights gate | Open; head `5cd514fc3659a381f9070702d30a23c7fa725602`; base `openfx-audit-round1` | Blocks transcript import until rights are explicitly reviewed; exact-head CI passed. |
| PR #18 local scan scope/provenance | Open; head `29f7fcf061bf8c274bda79787dc3c0eb0749d2ec`; base `main` | Skips symlinks and records root-relative file paths; tests and CodeQL passed. |
| PR #19 CI least privilege | Open; head `65a76be37f999a7c15fada2cd8f762749efb2441`; base `main` | Adds read-only token permissions and timeouts; tests and CodeQL passed. |
| PR #20 transcript conditions/units/corpus | Open; current head `2ef5f2a323314164491cec6cdc92303264fd724a`; base `openfx-audit-round1` | Adds condition/unit warnings and a 24-case synthetic corpus; exact-head CI passed. |
| PR #21 YouTube API-key header | Open; head `822d0881a432548bdb51e3220d5f24984dc2e086`; base `openfx-audit-fixes` | Moves API key out of the URL query; exact-head CI passed. |
| PR #22 backtest verification-claim labels | Open; head `b4cc92860d3df7a64d4a3cfebb30626e5ab87a8b`; base `openfx-audit-round1` | Separates CLI-verified report parsing from self-declared journal/data/cost/split checks; exact-head CI passed. |

### CI evidence for current PR heads

- PR #11: OpenFX CI run `40921215811` and CodeQL run `40921215571` passed.
- PR #12: OpenFX CI run `40921649710` passed.
- PR #13: Unit tests run `40926703802` and project tests run `40926703827` passed on the current docs head; CodeQL run `40926711364` was still in progress at the last check.
- PR #14: CI run `40924158772` passed (109 repository tests, 15 worker tests).
- PR #15: CI run `40924445011` passed (8 schema-contract tests, 117 repository tests, 15 worker tests).
- PR #16: current-head CI run `40925335092` passed (112 repository tests, 15 worker tests).
- PR #17: CI run `40924903871` passed (111 repository tests, 15 worker tests).
- PR #18: current-head project/unit tests `40925208557` and `40925208133`, plus CodeQL `40925208196`, passed.
- PR #19: project/unit tests `40925003699` and `40925003750`, plus CodeQL `40925003707`, passed.
- PR #20: current-head CI run `40925975774` passed (115 repository tests, 15 worker tests, and 24-case corpus evaluation; curated matrix TP=18, FN=0, FP=0, TN=6).
- PR #21: CI run `40926204432` passed (104 repository tests, 15 worker tests).
- PR #22: CI run `40926577896` passed (109 repository tests, 15 worker tests).

Intermediate failures were retained rather than hidden: PR #16 run `40925250131` exposed a VTT cue-ID parsing issue; PR #17 run `40924728291` exposed a CLI fixture relying on unknown rights; PR #20 run `40925884008` exposed a corpus-script import-path issue. Each was corrected on its branch and followed by a successful exact-head run. These results validate only the checks named above, not end-to-end research correctness or MT5 execution.

## 3A. PR dependency and merge-order risk

The open PRs do not form one flat queue. Their declared bases are:

```text
main
├── PR #11 (openfx-audit-fixes)
│   ├── PR #12 (openfx-transcript-adversarial-checks)
│   │   └── PR #14 (openfx-audit-round1)
│   │       ├── PR #15 (schema validation)
│   │       ├── PR #16 (transcript import strictness)
│   │       ├── PR #17 (rights gate)
│   │       ├── PR #20 (condition/unit fidelity + corpus)
│       └── PR #22 (backtest verification-claim labeling)
│   └── PR #21 (YouTube API key header)
├── PR #13 (mission/state/audit docs)
├── PR #18 (local scan scope/provenance)
└── PR #19 (CI least privilege)
```

This graph is based on the current declared PR base branches, not a merge recommendation. PR #16 and PR #17 both change `openfx/transcript_import.py` and `tests/test_transcript_import.py`; each currently reports mergeable against its own base, but that does **not** prove they can be merged one after another without conflicts. PR #15 and PR #20 also depend on PR #14's branch contents. Before any owner-approved merge, consolidate overlapping transcript-import changes or rebase/retarget them in a deliberate sequence. No PR has been merged by this audit.

## 4. Architecture map

### Default branch (`main`)

```text
local files/directories
        |
        v
data_collection.py
  - authorized local file discovery
  - metadata + SHA-256
        |
        v
evaluation.py
  - basic metadata/duplicate checks
        |
        +----> main.py (environment/startup summary)
        |
        +----> create_experiment.py / openfx/experiment.py
                     |
                     v
               openfx/mock_worker.py
               - simulated lifecycle only
                     |
                     v
               experiment JSON manifest

worker/openfx_worker.py
  - validates declarative worker jobs
  - local audit/state prototype
  - does NOT invoke MT5 or execute a strategy

schemas/ + tests/ + .github/workflows/
  - structural validation and automated checks
```

### Feature branch chain (PR #11 and PR #12; not merged to main)

```official YouTube Data API
        |
        v
openfx/youtube_search.py
  - metadata search only; rights remain unknown
        |
        v
openfx/source_registry.py
  - source metadata, rights status, segment timestamps, text hashes
        |
        v
openfx/transcript_import.py
  - local VTT/SRT/plain-text parsing
        |
        v
openfx/transcript_quality.py
  - selected numeric/negation/token-similarity heuristics
        |
        v
openfx/evidence.py
  - quote-to-segment/source linkage and claim classification
        |
        v
rule/claim records (manual review still needed)

experiment/result side:
openfx/experiment.py -> mock lifecycle / artifact metadata
openfx/backtest_result.py -> result metadata validation
openfx/mt5_report_parser.py -> limited English MT5 HTML summary parsing
openfx/result_cli.py -> local artifact/result checks

Missing end-to-end link:
validated strategy rule -> compiled EA -> real MT5 Strategy Tester
-> raw report/journal/data artifacts -> independent reproduction.
```

## 5. Capability matrix

| Capability | Evidence and location | Assessment |
|---|---|---|
| Local file discovery and metadata | `data_collection.py` on main | Implemented at a basic level; not video ingestion. |
| Basic duplicate/metadata evaluation | `evaluation.py` on main | Implemented; not scientific quality assessment. |
| Experiment manifest and state transitions | `openfx/experiment.py` on PR #11 branch; earlier scaffold on main | Prototype; strict validation exists on feature branch. |
| Mock lifecycle worker | `openfx/mock_worker.py` | Implemented simulation only; no market/backtest evidence. |
| Worker job validation/audit | `worker/openfx_worker.py` on main/PR branch | Validation prototype; explicitly does not execute MT5. |
| YouTube discovery | `openfx/youtube_search.py` on PR #11 branch | Official API metadata search; requires API key and does not download/transcribe video. |
| Transcript import | `openfx/transcript_import.py` on PR #11 branch | Local subtitle/text parsing; not automatic video transcription. |
| Transcript fidelity warnings | `openfx/transcript_quality.py` on PR #12/#14 chain | Heuristics for selected differences; cannot establish semantic equivalence. |
| Source/claim provenance | `openfx/source_registry.py`, `openfx/evidence.py` on PR #11 branch | Useful structural traceability prototype; not source-truth verification. |
| MT5 report parsing | `openfx/mt5_report_parser.py` on PR #11 branch | Limited English HTML summary parser; not terminal execution or report authenticity verification. |
| Backtest-result schema validation | `openfx/backtest_result.py` on PR #11 branch | Metadata/review-readiness checks; it explicitly does not verify artifact bytes or profitability. |
| Actual MT5 Strategy Tester execution | No execution adapter found; worker docs say it does not invoke MT5 | Not established / not implemented in inspected code. |
| Autonomous full research pipeline | Components remain separate and partially manual | Not established. |
| Trading edge/profitability | No real MT5 test artifacts or independently reproduced results established | Not established. |

## 6. Initial findings and priority

### F-01 — Feature branch capabilities are not in the default branch
**Severity:** P1 — mission/release blocker  
**Status:** Observed  
**Evidence:** `main` tree at `25c1366097c2ddf3a7951111ca9e9a1e6e4928b6` lacks `openfx/evidence.py`, `openfx/source_registry.py`, `openfx/transcript_import.py`, `openfx/youtube_search.py`, and `openfx/backtest_result.py`; these files are included in PR #11's changed-file list. PR #11 and #12 remain open.  
**Impact:** Users may mistake a feature branch's capabilities for what is actually available from the default branch. PR #13 alone does not resolve this.  
**Action:** Keep branch/commit attached to every capability claim; review PR dependency order and CI before any owner-approved merge. Do not merge automatically.

### F-02 — No end-to-end MT5 execution or strategy-performance evidence
**Severity:** P1 — mission blocker  
**Status:** Observed / not established  
**Evidence:** `README.md` states the current worker is mock-only and VPS/MT5 deployment is deferred; `worker/openfx_worker.py` states it does not invoke MT5; feature-branch result validation describes itself as metadata-level.  
**Impact:** OpenFX cannot yet demonstrate real strategy execution or profitability from the inspected code.  
**Action:** Treat MT5 integration as a separate controlled pilot with immutable inputs, actual tester logs/reports, data/cost manifests, and independent reproduction. No paid host or live trading without owner approval.

### F-03 — Transcript numeric token comparison has equivalent-glyph false positives
**Severity:** P2 — quality issue with research consequences  
**Status:** Code-reviewed and CI-confirmed for the exact PR #14 head  
**Evidence:** Before PR #14, `openfx/transcript_quality.py` compared token strings without normalizing Persian/Arabic-Indic digits, Persian percent glyph, or Unicode minus/plus variants.  
**Impact:** Equivalent numeric expressions may be flagged as changed; that can inflate review burden and reduce consistency. Conversely, this heuristic still cannot detect all semantic changes.  
**Action taken:** PR #14 normalizes equivalent digit/sign/percent glyphs and adds regression tests while retaining tests for missing percent and sign changes. Exact-head CI status must be refreshed before calling this fix test-confirmed.  
**Residual limitation:** Token similarity and a list of negation words do not understand units, numeric scope, clause meaning, or all paraphrases.

### F-04 — A nested workflow file is outside GitHub Actions' active workflow directory
**Severity:** P2 — repository hygiene / misleading duplication  
**Status:** Observed  
**Evidence:** Main tree contains `.github/workflows/.github/workflows/.github/workflows/test.yml` in addition to root-level workflows. The nested file duplicates an older test workflow; GitHub Actions discovers workflow definitions from the immediate `.github/workflows` directory, not arbitrary nested subdirectories.  
**Impact:** The nested copy is not an active workflow and can mislead maintainers about which tests are actually running.  
**Action:** After confirming no intended archival purpose, remove or relocate it in a separate reviewed PR and keep a single canonical workflow.

### F-05 — CI validates JSON syntax but does not consistently validate JSON Schema conformance
**Severity:** P2 — validation coverage gap  
**Status:** Code-reviewed; a feature-branch fix is CI-confirmed, but not merged to main  
**Evidence:** Root-level workflows previously checked JSON syntax only. Main's `schemas/experiment-v1.schema.json` uses permissive root `additionalProperties: true`, while PR #11's Python manifest validator rejects unknown fields and its feature-branch schema uses stricter rules.  
**Impact:** A JSON file can parse successfully while violating the intended contract; schema and Python behavior may drift.  
**Action taken:** PR #15 adds pinned `jsonschema==4.25.1`, Draft 2020-12 schema checks, positive/negative fixtures, and selected parity tests against Python validation. Exact-head CI run `40924445011` passed (8 dedicated schema tests; 117 repository tests; 15 worker tests). This branch is still open and based on the PR #14 feature branch; main remains unchanged.

### F-06 — Human verification is represented as a status, not an auditable review event
**Severity:** P1/P2 — evidence governance gap  
**Status:** Code-reviewed on PR #11 branch  
**Evidence:** `openfx/evidence.py` accepts `review_status == "human_verified"` for `source_confirmed` claims, but the claim structure has no reviewer identity, review timestamp, review note/version, or signed/append-only audit event. Exact quote matching checks linkage to a registered segment, not whether the segment accurately represents the original source or whether the claim follows from it.  
**Impact:** The field can assert that review occurred without a durable record of who reviewed what and when; source fidelity and logical entailment remain outside the validator's proof.  
**Action:** Add an auditable review record/event and explicitly label provenance validation separately from source truth and rule interpretation.

### F-07 — Artifact integrity checks exist, but do not prove the authenticity of an MT5 run
**Severity:** P1 — financial-research integrity gap  
**Status:** Code-reviewed on PR #11 branch  
**Evidence:** `openfx/backtest_result.py` contains `verify_artifact_files` for declared file sizes and SHA-256; `openfx/result_cli.py` calls it, parses a verified tester HTML artifact, and compares selected metrics. `openfx/mt5_report_parser.py` is a limited English HTML summary parser and states that its scope is not profitability verification.  
**Impact:** These checks are stronger than metadata-only validation, but file hashes prove integrity only relative to the supplied manifest. They do not prove the files came from a genuine MT5 terminal run, that the EA/data were actually used by that run, or that journal/data coverage and cost/split assertions are true.  
**Action:** Preserve raw artifacts and hashes, but derive each verification flag from an evidence-specific checker or auditable human-review event. Bind run identity, terminal build, EA/data hashes, configuration, logs, and report to one manifest, then independently reproduce selected runs.

### F-19 — Backtest verification flags can be self-asserted in the result JSON
**Severity:** P1 — research result integrity  
**Status:** Code-reviewed on PR #11 branch  
**Evidence:** `validate_backtest_result` accepts `journal_complete`, `data_coverage_verified`, `costs_recorded`, and `split_boundaries_verified` when their input values are simply `true`. The CLI independently sets `tester_report_parsed` after parsing, but does not independently derive the other flags from journal/data artifacts or an auditable reviewer record.  
**Impact:** A result can be labelled `ready_for_independent_review` while some important verification statements are only assertions in the JSON. The status means review readiness, not proven verification, but the field names can overstate what the tool checked.  
**Action taken:** PR #22 adds a `verification_claims` section to the CLI output: the report-parsed flag is labelled `verified_by_cli` only after the artifact/report/metric checks, while journal/data/cost/split flags are labelled `declared_not_independently_verified`. Exact-head CI run `40926577896` passed: 109 repository tests and 15 worker tests. The PR is based on the open audit branch and is not in main. The remaining work is to implement evidence-specific validators or auditable human review events for those fields.

### F-08 — Gemini workflow can finish successfully when the AI review did not run
**Severity:** P2 — status interpretation risk  
**Status:** Observed in workflow code  
**Evidence:** `.github/workflows/ai-review-gemini.yml` exits with status 0 when `GEMINI_API_KEY` is absent and writes “AI review not run” to the step summary. The workflow uses `pull_request_target` with read-only repository/PR permissions, does not check out PR code, and fetches only the diff; this reduces but does not eliminate untrusted-input/prompt-injection concerns.  
**Impact:** A green workflow badge alone may be misread as an AI review having occurred.  
**Action:** Keep explicit skip reporting and ensure any dashboard/report distinguishes skipped from reviewed; do not use the workflow's green status as a review-quality metric.

### F-09 — No labelled adversarial corpus or measured false-positive/false-negative rates
**Severity:** P1/P2 — research-quality gap  
**Status:** Observed in inspected tests  
**Evidence:** `tests/test_source_research.py` includes targeted cases for dropped negation, changed signed numbers, percentages, and provenance, but no broad labelled corpus or measured error rates was found.  
**Impact:** Passing hand-selected unit tests does not show how reliably transcript checks behave on realistic Persian/English transcripts, ASR errors, units, dates, paraphrases, or clause changes.  
**Action:** Build a small, versioned, human-labelled adversarial fixture set; report confusion matrix and known blind spots before expanding automation claims.

### F-10 — Malformed subtitle blocks can be silently omitted
**Severity:** P1/P2 — silent research-data loss  
**Status:** Code-reviewed; fix CI-confirmed on PR #16  
**Evidence:** Before PR #16, `openfx/transcript_import.py` skipped any subtitle block with no timestamp line. If a valid cue existed elsewhere in the file, import could still succeed while silently dropping the malformed block.  
**Impact:** Lost text could include a negation, number, threshold, or condition, while the importer returns a seemingly valid partial transcript.  
**Action taken:** PR #16 changes this path to fail closed for non-header/non-metadata blocks without timestamps, distinguishes valid cue identifiers such as `NOTE`/`STYLE` from metadata blocks, and adds regression fixtures. An intermediate test-only commit failed when the new fixture exposed the prefix-matching bug (run `40925250131`); the parser was corrected and exact-head CI run `40925335092` passed (112 repository tests and 15 worker tests). The failed run remains in GitHub history.  
**Residual limitation:** A timestamped subtitle file can still contain incorrect captions or audio/transcript mismatches; this parser does not validate speech.

### F-11 — Unknown rights status was not a hard ingestion gate
**Severity:** P1/P2 — compliance and provenance risk  
**Status:** Code-reviewed; fix CI-confirmed on PR #17  
**Evidence:** The prior importer blocked only `restricted` and `permission_required`, so `unknown` rights could still be imported despite docs saying unknown rights must remain unapproved until reviewed.  
**Impact:** The application could process transcript material without a recorded rights decision, weakening the project's authorized-source boundary.  
**Action taken:** PR #17 now permits ingestion only for `reviewed_permitted` or `public_domain` records with a rights reference; unknown/restricted/permission-required are rejected. Its first CI run failed because an existing CLI fixture still relied on unknown rights (run `40924728291`); the fixture was corrected to record explicit synthetic permission, and exact-head CI run `40924903871` passed (111 repository tests and 15 worker tests). The failed run remains in GitHub history.  
**Residual limitation:** The software checks the recorded status/reference, not the legal validity of the permission itself.

### F-12 — Local file scanning followed symlinks outside the selected root
**Severity:** P2 — local privacy/scope boundary  
**Status:** Code-reviewed; tests and CodeQL CI-confirmed on PR #18  
**Evidence:** In main's `data_collection.py`, `Path.is_file()` follows symlinks, and the collector hashed any supported target reachable through a link inside the selected directory.  
**Impact:** A scan could read/hash a file outside the directory the user selected. The content is not uploaded, but the scan scope was wider than expected.  
**Action taken:** PR #18 skips symbolic links, adds a root-relative path to disambiguate same-named files, and tests both an external symlink and duplicate basenames. On the current head `29f7fcf061bf8c274bda79787dc3c0eb0749d2ec`, Project Tests run `40925208557`, OpenFX Unit Tests run `40925208133`, and CodeQL run `40925208196` all passed. PR #18 remains open and is not in main.  
**Residual limitation:** This check does not establish a sandbox for other file-processing components.

### F-13 — Local collection records omit a root-relative file locator
**Severity:** P2 — provenance/reproducibility gap  
**Status:** Code-reviewed on main  
**Evidence:** `data_collection.py` records `file_name`, extension, size, timestamps, and SHA-256, but not a root-relative path.  
**Impact:** Two files with the same basename in different subdirectories are hard to distinguish in the record, and a future workflow cannot reliably map a record back to its local source path without re-scanning and matching hashes.  
**Action:** Decide whether the metadata format should include a root-relative path (preferable to an absolute path) or a stable source locator that avoids leaking full local paths. Add duplicate-basename tests and document privacy implications before changing the contract.

### F-14 — High-similarity transcript changes can remove rule conditions
**Severity:** P1/P2 — research rule integrity  
**Status:** Code-reviewed; conservative fix CI-confirmed on PR #20  
**Evidence:** Before PR #20, `compare_transcript_fidelity("Buy only above 1.5 ATR.", "Buy above 1.5 ATR.")` could pass the selected checks because token similarity remained above 0.85 and the number/negation lists were unchanged.  
**Impact:** Dropping a limiting word such as `only`, changing `unless` to `if`, or changing a temporal/threshold marker can alter a trading rule without necessarily tripping the previous checks.  
**Action taken:** PR #20 adds `condition_mismatch` and `unit_mismatch` flags for selected English/Persian condition, threshold, and unit markers. A 24-case labelled synthetic corpus and confusion-matrix script were added. An intermediate CI run `40925884008` failed because the script could not import the package when invoked by file path; the import path was corrected. Exact-head CI run `40925975774` passed: 115 repository tests, 15 worker tests, and the corpus evaluator. On the 24 curated cases, the observed confusion matrix was TP=18, FN=0, FP=0, TN=6.  
**Residual limitation:** The zero FP/FN result applies only to 24 small synthetic cases selected to exercise these exact rules; it is not an estimate of real-world performance. The marker list is incomplete and can create false positives; the checker does not understand syntax, scope, synonyms, or semantic entailment. A broader independently labelled corpus is still required.

### F-15 — Imported transcript provenance does not retain the raw transcript artifact hash
**Severity:** P1 — research reproducibility gap  
**Status:** Code-reviewed on PR #11 branch  
**Evidence:** `openfx/transcript_import.py` reads local transcript bytes as UTF-8 text, normalizes line endings/markup, and records hashes for cleaned segment text. The importer does not record the original file's byte-level SHA-256, size, exact format/encoding, or parser version in a separate import-artifact record; the source record's optional `content_sha256` is not populated by the importer.  
**Impact:** Later reviewers cannot establish exactly which raw transcript file produced a set of normalized segments. Segment hashes protect the normalized text, not the original file or the transformations applied.  
**Action:** Add an immutable transcript-import artifact record with raw-byte hash, size, source ID, format, encoding, parser version, import timestamp, and segment-manifest hash. Preserve the original authorized artifact or a controlled content-addressed reference.

### F-16 — The meaning of transcript segment confidence is easy to misinterpret
**Severity:** P2 — evidence interpretation risk  
**Status:** Code-reviewed  
**Evidence:** `openfx/transcript_import.py` sets each segment's `confidence` to `1.0` and comments that this is parser confidence only, not confidence that captions match speech. The field name itself does not encode that distinction.  
**Impact:** Downstream code or a reviewer could misread 1.0 as confidence in transcript fidelity or source truth, even though no audio comparison or semantic validation occurred.  
**Action:** Version the segment schema to use an explicit name such as `parser_confidence` or require a `confidence_basis` value; keep ASR/source-fidelity confidence separate and unknown unless measured.

### F-17 — Scheduled health reports are generated but not retained as workflow artifacts
**Severity:** P2 — operational continuity gap  
**Status:** Observed in workflow code  
**Evidence:** `.github/workflows/auto-report.yml` writes `health-report/report.json` and `health-report/report.md` and prints the report, but has no artifact-upload step.  
**Impact:** The report files disappear when the runner is discarded; only console logs remain, making routine historical comparison less convenient and less durable.  
**Action:** Upload the generated directory as a workflow artifact with a defined retention period. Do not automatically commit generated reports to the public repository unless explicitly intended.

### F-18 — YouTube API key is included in the request URL query string
**Severity:** P2 — secret-handling hardening  
**Status:** Code-reviewed on PR #11 branch  
**Evidence:** `openfx/youtube_search.py` constructs the official API request URL with the API key as a query parameter. The current error handling avoids echoing the URL, but query strings may be retained by proxies, traces, or diagnostics.  
**Impact:** A key could leak through infrastructure logs even when application logs are careful.  
**Action taken:** PR #21 moves the key into the `X-Goog-Api-Key` header and tests that the URL contains no `key` query parameter. Exact-head CI run `40926204432` passed: 104 repository tests and 15 worker tests. PR #21 is based on PR #11's feature branch and is not in main. Keep the key restricted to the YouTube Data API and rotate it if exposure is suspected.

## 7. Security and operational observations

- `worker/openfx_worker.py` explicitly avoids command execution and MT5 invocation. This is an appropriate prototype boundary, not production readiness.
- The worker has URL/config/job allow-list checks and bounded time/range settings; those controls require additional testing for canonicalization, state persistence, stale locks, retry behavior, and real control-plane threat modeling before deployment.
- Gemini review uses `pull_request_target`, but currently does not check out or execute PR code and scopes its token to read-only contents/PR access. Diff content remains untrusted and can still influence model output.
- The YouTube API key is placed in the API request URL by the feature-branch code. The current exception handler avoids echoing the request URL, which is a useful safeguard, but query-string credentials are still generally less desirable than header-based authentication where the API supports it; ensure logs, proxies, and traces never retain the URL.
- The repository is public but its `LICENSE` reserves rights; public visibility is not permission to reuse the project code. External-source licenses must be assessed separately.

## 8. Testing and execution evidence

### Tests actually evidenced
- GitHub Actions reported successful syntax/unit-test/worker checks for PR #11 at run `40921215811`.
- GitHub Actions reported successful CI for PR #12 at run `40921649710`.
- GitHub Actions reported successful unit/project test workflows and CodeQL for PR #13 at runs `40923717266`, `40923717250`, and `40923717315`.
- PR #14 exact-head check completed successfully; 109 repository tests and 15 worker tests passed.
- PR #15 exact-head schema contract checks passed; 8 dedicated schema tests, 117 repository tests, and 15 worker tests passed.
- PR #16 exact-head CI passed with 110 repository tests and 15 worker tests.
- PR #17 exact-head CI passed with 111 repository tests and 15 worker tests.
- PR #18 exact-head CI passed on commit `29f7fcf061bf8c274bda79787dc3c0eb0749d2ec`; project/unit tests and CodeQL completed successfully.
- PR #19 test workflows and CodeQL all passed.
- PR #20 exact-head CI run `40925975774` passed with 115 repository tests, 15 worker tests, and the 24-case synthetic corpus. Curated matrix: TP=18, FN=0, FP=0, TN=6; no real-world accuracy claim is implied. Earlier failure `40925884008` exposed a script import-path problem, which was fixed and preserved in history.
- PR #21 exact-head CI run `40926204432` passed with 104 repository tests and 15 worker tests; API key is now sent in a header on that feature branch.
- PR #22 exact-head CI run `40926577896` passed with 109 repository tests and 15 worker tests; the CLI now distinguishes parsed-report verification from other self-declared checks.
- No MT5 execution occurred.

### Not performed / not established
- No local test execution in this environment (network DNS prevented cloning the repository).
- No real MT5 compile or Strategy Tester run.
- No VPS deployment.
- No end-to-end autonomous source-to-claim-to-rule-to-backtest pipeline.
- No independent reproduction of trading results.
- No profitability or durable-edge conclusion.

## 9. Recommended next sequence

1. Refresh PR #14 CI and inspect the exact job result/logs; keep the fix only if all regression tests pass.
2. Review the full PR #11/12 dependency chain and compare each file/schema/workflow with `main`; do not merge automatically.
3. Add a schema-validation job with negative fixtures and parity checks against Python validators.
4. Add durable reviewer identity/time/version records to source-confirmed claims and tests for contradictory or unsupported claims.
5. Add labelled transcript adversarial fixtures and measure false positives/false negatives.
6. Audit worker recovery/idempotency and artifact verification with explicit failure injection.
7. Define a non-trading MT5 pilot specification and acceptance artifacts before any VPS purchase/deployment.
8. Only after the baseline and dependency order are clear, consider removing the nested duplicate workflow in a separate PR.

## 10. Acceptance criteria for the next audit checkpoint

- Every capability statement names branch and commit.
- PR #14 has a refreshed successful test result for the exact head or a documented failure.
- Schema validation is executed, not merely JSON syntax checked.
- A human-review record is auditable.
- Transcript checks have a labelled adversarial fixture set and documented limitations.
- Worker tests cover recovery and duplicate/retry behavior.
- No report claims real MT5 execution until raw tester logs/reports and reproducible artifacts exist.
