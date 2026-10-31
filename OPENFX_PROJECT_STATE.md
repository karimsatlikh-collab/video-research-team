# OpenFX Project State and Continuation Ledger

**Last reconciled:** 2026-10-29  
**Repository:** `karimsatlikh-collab/openfx-research-lab`  
**Default branch observed:** `main`  
**Purpose:** Preserve evidence-backed project state and a precise continuation point across chats.

> This ledger is a checkpoint, not proof that a feature works. Re-check the live repository and workflow runs before relying on any status below.

## 1. Mission and governing constraints

The standing mission is defined in `OPENFX_MISSION.md`: build a source-traceable, reproducible AI-assisted Forex research and validation platform. Do not confuse source extraction, hypotheses, mock workflows, metadata checks, historical backtests, and independent validation.

Owner approval is required before paid services/API/cloud compute, VPS purchase/deployment, production worker activation, broker access, live trading, material public commitments, or merging any PR into `main`.

## 2. Repository state observed on 2026-10-29

- The GitHub repository is `karimsatlikh-collab/openfx-research-lab`.
- The `main` branch was listed at commit `25c1366097c2ddf3a7951111ca9e9a1e6e4928b6` during this reconciliation.
- Branches observed included `openfx-audit-fixes` at `28161cb4622e4bd92ba356508b97409f6149a1af` and `openfx-transcript-adversarial-checks` at `649631de5f3a08be1ca0941ede4ff3646b346063`.
- PR #11, “Harden OpenFX experiment and worker validation,” was reported open and not merged by the connector at the time checked. Its declared scope includes stricter experiment/worker validation and explicitly excludes a production control plane, video discovery/transcription, semantic evidence tracing, and an MT5 execution adapter.
- PR #12, “Flag percentage changes in transcript fidelity checks,” was reported open and not merged by the connector at the time checked. Its head is `openfx-transcript-adversarial-checks`, based on `openfx-audit-fixes`.
- A historical project checkpoint reported OpenFX CI run `40921649710` as successful for the transcript-percentage changes. This is a historical report, not confirmation of the current workflow state; refresh the Actions run before relying on it.
- Do not merge either PR without explicit owner approval.

## 3. Verified limits and current capability boundaries

The following boundaries are explicitly documented in the repository and/or were visible in inspected code during this reconciliation:

- The worker at `worker/openfx_worker.py` is a validation/audit prototype. Its module documentation and implementation state that it does not invoke MT5 or execute jobs.
- The mock worker simulates experiment lifecycle behavior; it is not a market backtest and does not establish strategy performance.
- A source registry or transcript-quality heuristic is not the same as fully autonomous source discovery, complete transcript extraction, or semantic verification.
- Numeric, date, percentage, and negation checks are heuristics. They can flag suspicious changes but cannot prove that meaning was preserved.
- MT5 report metadata validation is not equivalent to independently validating the original report bytes, reproducing the Strategy Tester run, or verifying profitability.
- The repository's Windows VPS/MT5 planning documents state that no VPS purchase/deployment or MT5 VPS installation/backtest has been confirmed.
- No live trading is authorized by this ledger.

## 4. Reconciliation cautions

Repository documents and implementation may have advanced on non-main branches and may not describe the same revision. Before making claims about a feature:

1. Identify the exact branch and commit containing it.
2. Read the relevant implementation and tests at that same revision.
3. Check whether the branch is merged into `main`.
4. Inspect the latest relevant Actions run and its individual jobs.
5. State exactly what the evidence proves and what it does not prove.

If README, roadmap, checkpoint, code, or CI status disagree, record the disagreement as a finding and resolve it based on current evidence. Do not silently treat a PR's contents as part of `main`.

## 5. Work completed in this documentation reconciliation

- Created this continuity ledger and the standing mission charter on the task branch `openfx-mission-state-docs`, based on the observed `main` branch.
- No existing source code, strategy code, workflow, or open PR was merged or modified by this documentation task.
- The documentation branch itself is not the main branch; its files must be reviewed before merging.

The commit SHA for the first file creation is recorded in the GitHub action result; record the second file's commit SHA in the final task report.

## 6. Priority backlog for the next audit cycle

These are proposed priorities, not claims that the work has been completed.

### P1 — Establish an evidence-backed baseline
- Refresh PR #11 and #12 status and all relevant Actions runs, including individual job results.
- Inventory the actual tree on `main` and relevant feature branches.
- Compare README, ROADMAP, CHANGELOG, schemas, tests, worker behavior, and docs at matching commits.
- Produce a capability matrix with branch/commit and evidence for each claim.

### P1 — Source/evidence integrity
- Inspect `openfx/evidence.py`, source registry schemas, claim-register schema, transcript importer, and transcript-quality checks on the correct branch.
- Verify that source-confirmed claims require the expected human verification and exact segment/quote linkage.
- Test Persian/Latin digits, signed numbers, dates, units, percentages, dropped negation, changed values, and benign formatting differences.
- Measure both false positives and false negatives on a small labelled adversarial fixture set.

### P1 — Reproducible experiment integrity
- Audit manifest/result schemas and CLI validation against malformed, incomplete, inconsistent, or forged records.
- Verify artifact hashes against actual files in a trusted root.
- Separate metadata consistency checks from independent report parsing and actual tester reproduction.
- Add synthetic cases for costs, order timing, missing bars, gaps, and look-ahead leakage.

### P1 — Worker and security boundary
- Review URL validation, redirect behavior, host allowlists, idempotency, retries, persistence, and failure recovery.
- Check GitHub Actions permissions, external pull-request handling, prompt-injection exposure, and secret boundaries.
- Do not deploy or enable real execution until a separate control plane, threat model, and owner approval are in place.

### P1 — MT5 validation plan
- Keep the Windows host compatibility and procurement work as planning only until the owner approves a specific purchase.
- Define a controlled non-trading smoke test and required raw artifacts.
- Do not report a real MT5 test until a compatible host actually runs it and the report/logs are retained.

### P2 — Maintainability and cost
- Identify duplicated workflows, stale docs, nested/misplaced workflow files, unpinned dependencies/actions, and unnecessary complexity.
- Prefer the smallest architecture that meets measured needs.
- Preserve negative results and avoid expanding infrastructure before the pilot demonstrates a need.

## 7. Continuation protocol

At the start of each continuation:
1. Read `OPENFX_MISSION.md` and this file.
2. Refresh live GitHub branch, PR, commit, and Actions status.
3. Confirm the last documented action against actual repository evidence.
4. Pick the highest-priority unblocked task and proceed without asking the owner to restate the mission.
5. Update this file only with evidence-backed state, and keep plans clearly labelled as plans.

At the end of each meaningful work cycle, add:
- date and branch/commit;
- files changed;
- tests actually executed and exact outcomes;
- links/IDs for relevant runs or artifacts;
- unresolved risks and decisions needed;
- the next precise action.

## 8. Audit checkpoint — 2026-10-29

The evolving evidence-backed baseline report is saved at:
`docs/OPENFX_AUDIT_BASELINE_2026-10-29.md`
on branch `openfx-mission-state-docs`, latest report commit `166a80cce48793acdc852d1701170c56508667bd`.

### Findings established so far
- Main is at `25c1366097c2ddf3a7951111ca9e9a1e6e4928b6`; research/evidence modules introduced by PR #11/#12 are not in main.
- PR #11 and PR #12 are an open dependency chain; PR #13 contains only the mission/state documentation based on main.
- No real MT5 execution adapter, VPS deployment, or independently reproduced trading result is established.
- The nested path `.github/workflows/.github/workflows/.github/workflows/test.yml` is an inactive duplicate candidate because it is not directly under `.github/workflows`.
- Feature-branch source-confirmed claims record a `human_verified` status but do not preserve an auditable reviewer identity/time event.
- JSON syntax checks are not JSON Schema validation; main's experiment schema is looser than the strict feature-branch Python validator.
- Transcript numeric glyph normalization has been implemented on `openfx-audit-round1`, PR #14, with regression tests for Persian/Arabic-Indic digits, percent glyphs, and Unicode signs. Exact-head OpenFX CI run `40924158772` completed successfully: 109 repository tests and 15 worker regression tests passed; JSON syntax validation and worker offline self-test also passed. This does not establish semantic equivalence.

### Actions evidence refreshed
- PR #11: run `40921215811` (OpenFX CI) success; run `40921215571` (CodeQL) success for head `28161cb4622e4bd92ba356508b97409f6149a1af`.
- PR #12: run `40921649710` (OpenFX CI) success for head `649631de5f3a08be1ca0941ede4ff3646b346063`.
- PR #13: runs `40923717266` (OpenFX Unit Tests), `40923717250` (Project Tests), and `40923717315` (CodeQL) success for docs head `9c360866b744ac83b4f8d720019d964f1b0d85b1`.
- PR #14 exact-head check ID `123625086035` completed successfully in run `40924158772`; logs show 109 repository tests and 15 worker tests passed, JSON syntax validation passed, and worker offline self-test passed.

### Additional audit branches and verified fixes
- PR #14 `openfx-audit-round1` (base `openfx-transcript-adversarial-checks`): normalizes equivalent Persian/Arabic-Indic digits and common percent/sign glyphs. CI run `40924158772` passed: 109 repository tests and 15 worker tests.
- PR #15 `openfx-schema-validation` (base `openfx-audit-round1`): adds pinned JSON Schema validation and fixtures. CI run `40924445011` passed: 8 dedicated schema tests, 117 repository tests, 15 worker tests.
- PR #16 `openfx-transcript-import-strictness` (base `openfx-audit-round1`): rejects malformed subtitle blocks without timestamps and distinguishes valid cue IDs such as `NOTE`/`STYLE` from metadata. Exact-head CI run `40925335092` passed: 112 repository tests and 15 worker tests. An intermediate failed run `40925250131` exposed the cue-ID bug; it was corrected and the failure remains in GitHub history.
- PR #17 `openfx-rights-gate` (base `openfx-audit-round1`): blocks transcript import unless rights are `reviewed_permitted` or `public_domain` with a reference. After correcting a CLI fixture that still relied on unknown rights, exact-head CI run `40924903871` passed: 111 repository tests and 15 worker tests.
- PR #18 `openfx-local-scan-boundary` (base `main`): skips symlinks and records root-relative paths to disambiguate same-named files. Current-head Project Tests `40925208557`, OpenFX Unit Tests `40925208133`, and CodeQL `40925208196` all passed.
- PR #19 `openfx-ci-least-privilege` (base `main`): adds `contents: read` permissions and five-minute timeouts to the two baseline test workflows. Test runs `40925003750` and `40925003699`, CodeQL `40925003707`, and Gemini review `40925001639` all passed.
- PR #20 `openfx-transcript-critical-conditions` (base `openfx-audit-round1`): adds condition/unit markers and a 24-case synthetic labelled transcript corpus with a confusion-matrix script. Exact-head CI run `40925975774` passed: 115 repository tests, 15 worker tests, and corpus evaluation. Curated matrix TP=18, FN=0, FP=0, TN=6; these 24 hand-selected synthetic cases do not estimate real-world transcript accuracy. Intermediate run `40925884008` failed because the evaluator script lacked the repository root on `sys.path`; fixed in the current head and preserved in history.
- PR #21 `openfx-youtube-key-header` (base `openfx-audit-fixes`): moves the YouTube Data API key from the query string to the `X-Goog-Api-Key` header. Exact-head CI run `40926204432` passed: 104 repository tests and 15 worker tests.
- PR #22 `openfx-result-assertion-labels` (base `openfx-audit-round1`): labels report parsing as CLI-verified only after artifact/report/metric checks, while journal/data/cost/split flags are explicitly marked as declarations not independently verified. Exact-head CI run `40926577896` passed: 109 repository tests and 15 worker tests.
- PR dependency caution: #14 follows #12; #15, #16, #17, and #20 are based on #14's branch; #21 is based on #11. PRs #16 and #17 touch the same transcript-import files and may conflict when sequenced even though each is currently mergeable against its own base.
- None of PRs #14–#22 has been merged by this work.

### Audit limitations
The repository could not be cloned in the local execution container because DNS/network access to GitHub was unavailable. This audit checkpoint uses GitHub connector file/branch/PR/Actions evidence and code review. No local test command, real MT5 run, VPS deployment, or trading backtest is claimed.

## 9. Latest continuation point

**Next action:** refresh current head CI and mergeability of PRs #14–#22, including the latest docs PR checks for head `a9d4a8093fcda7e4803319678d6f88333bbafe7a`. The 24-case synthetic transcript corpus is in PR #20; expand it with independently labelled real-world examples and measure error rates. Then address auditable human-review events, raw transcript artifact provenance, confidence-field semantics, further evidence-specific verification for journal/data/cost/splits, worker failure/recovery and idempotency, artifact verification/MT5 pilot acceptance criteria, and auto-report artifact retention. Review whether to consolidate duplicate workflows. Do not merge any PR without explicit owner approval. Review the PR #11/#12 dependency chain and the inactive nested workflow, but do not merge any PR without explicit owner approval.


## 10. Continuation reconciliation — 2026-10-30

This section supersedes older status snapshots above where they conflict with live GitHub state. It is a status refresh, not an endorsement to merge any PR.

### Standing two-mission instruction

The continuation keyword **“ادامه OpenFX”** invokes both workstreams together:

1. **Independent, evidence-based project audit:** determine whether the current repository is ready to serve as an automated, reliable, reproducible research system. Inspect code, tests, workflows, provenance, security boundaries, branches, dependencies, and actual evidence; distinguish implemented features from plans and mocks.
2. **Research-team process engineering:** build a disciplined strategy-discovery and validation process that cheaply rejects weak ideas and fairly validates promising ones, with separated roles, Hypothesis Cards, gates G0–G5, source-to-claim traceability, frozen experiments, independent checks, and preservation of negative results.

Neither mission replaces the other. Infrastructure is only useful insofar as it enables trustworthy strategy research; strategy claims must not outrun the evidence infrastructure can support.

### Live repository and PR reconciliation

- Current `main` branch observed at `25c1366097c2ddf3a7951111ca9e9a1e6e4928b6`.
- PRs #11–#23 were refreshed through the GitHub connector on 2026-10-30: all were open and unmerged at the time checked; GitHub reported each as mergeable. This is not approval to merge.
- The dependency chain remains important: #12 is based on #11's branch; #14 is based on #12; #15, #16, #17, #20, and #22 are based on #14's branch; #21 is based on #11. PRs #13, #18, #19, and #23 are based on `main`. Review sequencing and cross-branch integration before considering any merge.
- PR #23 head is `9323341e1a4dfa4e76d87d6315f4875c8d997494`. It adds a fail-closed `validate_attested_run` helper and negative tests. On that exact head, OpenFX Unit Tests completed successfully, Project Tests completed successfully, and AI review completed successfully; CodeQL was still in progress at the last refresh.
- An earlier OpenFX Unit Tests run for PR #23 head `40f355c0630d7125bf141f031d7b3b2e7d799326` failed on a mismatched expected error message; the test assertion was corrected in the later head. Preserve this failed run as evidence, not as current-head status.
- The attestation helper is only a fail-closed interface to an externally supplied verifier. No trusted-key provisioning, production signature verification policy, or mandatory executor/registrar integration has been established. It does not prove MT5 execution.
- The current PR #23 branch has not been merged; its contents must not be described as part of `main`.

### Next continuation actions

1. Complete the cross-PR audit from the two missions above, beginning with dependency/merge order and exact-head CI status rather than merging anything.
2. For mission 1, prioritize the trust boundary and artifact/manifest integrity audit: atomic writes, symlink/TOCTOU behavior, provenance and hashes, forged result assertions, and mandatory verifier integration.
3. For mission 2, review the current research-team operating contract and gate design against the actual code; identify which G0–G5 controls are enforced versus merely documented, and define a small end-to-end acceptance path from authorized source to reviewed hypothesis and reproducible result.
4. Refresh this ledger after meaningful work with exact branch/head, test outcomes, remaining risks, and the next action. No PR merge, paid service, VPS deployment, broker access, or live trading without explicit owner approval.


## 11. Continuation work — 2026-10-30 (artifact integrity + gate reality check)

### Verified repository observations
- Refreshed the PR list: 18 open PRs were returned, including #23; the list is not a merge queue and no PR was merged.
- On PR #23's previously recorded head `9323341e1a4dfa4e76d87d6315f4875c8d997494`, the three exact-head runs were confirmed complete and successful: OpenFX Unit Tests `40958813257`, Project Tests `40958813294`, and CodeQL `40958813182`.
- Reviewed `openfx/experiment.py`, `tests/test_experiment.py`, `openfx/statistical_gate.py`, and `docs/RESEARCH_TEAM_OPERATING_CONTRACT.md` from PR #23's branch.

### Bounded code changes on the PR #23 branch
- Commit `8077f6c007d249aa09b53d48e49f1dc224003f39`: replaced the predictable shared manifest temp filename with a unique same-directory temporary file; flushes and fsyncs file content before atomic `os.replace`; attempts best-effort directory fsync; cleans up temporary files.
- The same commit changes artifact hashing to open the artifact once, reject a final-component symlink where `O_NOFOLLOW` is supported, require a regular file, hash through that descriptor, and reject changes detected by before/after device/inode/size/mtime checks.
- Commit `51d3e5a1c247f622d1980eb971ac9d0c3137ca63`: adds a regression test proving the old predictable `.tmp` path is not overwritten by manifest saving.
- These changes are committed to the existing PR #23 head branch, not main. The new head's Actions runs were not yet returned by the immediate workflow lookup; therefore the new changes are **not yet CI-verified**. Do not transfer the earlier head's green checks to this new head.

### Important remaining technical limitations
- Unique temp names eliminate the shared predictable-temp collision/symlink issue and support atomic replacement, but simultaneous writers to the same destination remain last-writer-wins; no compare-and-swap/version precondition is implemented.
- Artifact path containment still uses resolved paths before opening. The final-component no-follow check does not eliminate all ancestor-directory replacement/TOCTOU races on hostile writable filesystems. On platforms without `O_NOFOLLOW`, that protection is unavailable. The before/after metadata check is a race detector, not a cryptographic snapshot guarantee.
- Directory fsync is best-effort and intentionally swallowed when unsupported; power-loss durability is not guaranteed on every platform/filesystem.

### Research-team G0–G5 control reality check
- The operating contract explicitly defines roles, evidence chain, trial accounting/OOS protection, staged M1–M5 releases, and independence requirements. It labels itself a proposed control-plane policy.
- Runtime evidence reviewed confirms only partial controls: local JSONL registry lifecycle/budget/idempotency checks, synthetic harness, descriptive gate, schema/contract checks, and a fail-closed attestation callback boundary.
- Not runtime-enforced or not established: role permissions/separation, independent proposer/implementer/replicator identities, source authorization and complete source-to-claim traceability, controlled access to final-OOS metrics, trusted central trial-family assignment, production cryptographic executor identity, mandatory attestation wiring, and independent reproduction.
- The current gate accepts a caller-supplied summary and a registry-derived trial count helper, but it does not calculate DSR/PBO/familywise correction or establish market validity. Therefore a gate verdict is only a descriptive prototype verdict, not a research acceptance decision.
- G0–G5 should be treated as policy/design gates until each has a specific runtime-enforced control and adversarial acceptance test. The next design task is a control matrix mapping each gate to: required input, enforcing component, negative test, immutable evidence output, and human authorization boundary.

### Next action
Refresh PR #23's current head and Actions after the two commits; add adversarial artifact tests (symlink rejection where supported, file mutation during hashing, and concurrent manifest writers), then define the G0–G5 enforcement matrix and identify the smallest end-to-end path that can honestly reach a reproducible synthetic result. No merge, paid service, VPS, broker, MT5 demo, or live trading without explicit approval.


## 12. G0–G5 enforcement matrix — 2026-10-30

- Added `docs/G0_G5_ENFORCEMENT_MATRIX.md` on the PR #23 work branch; commit `8fcbb7901d98890e6b416539b75cafa03188b2b1`.
- The matrix defines G0 source admissibility, G1 claim/hypothesis, G2 implementation and synthetic qualification, G3 market-data evaluation, G4 independent reproduction/demo acceptance, and G5 release/deployment decision.
- Each gate has required inputs, target enforcing component, adversarial tests, immutable evidence output, human authorization boundary, and current implementation status.
- Added explicit gate semantics (`BLOCKED/PASS/WAIVED`), non-waivable integrity/OOS/authorization controls, gate invariants, a minimum end-to-end synthetic-only acceptance path, ordered implementation backlog, and criteria for using “research-ready” or “production-ready”.
- This is an engineering contract/design artifact, not a claim that G0–G5 are now implemented. The current honest first vertical slice stops at a reproducible synthetic result; it must not be called a market backtest or profitability validation.
- No code tests were added or run for this documentation-only change. The matrix commit is on the PR #23 head branch, not main. No merge was performed.

### Next action
Implement the smallest G0→G1 data contract slice: define and validate a source record with rights basis, immutable content hash, exact locator, extraction method, and explicit provenance state; add fail-closed tests for missing rights/locator/hash and source-content mismatch. Keep the test fixture explicitly synthetic/local and do not ingest third-party media without an established rights basis. Then wire one HypothesisCard to a source-backed atomic claim without promoting hypotheses to verified rules.


## 13. G0→G1 provenance vertical slice — 2026-10-30

### Implementation committed on the PR #23 work branch

- Branch: `openfx-foundation-m1-contracts` (PR #23); no changes to `main`.
- `openfx/source_provenance.py`, commit `23e040fa5517438a0e87bbc17a90509ff120a39d`:
  - Adds a source record with stable source ID, identity, rights basis, permission evidence, timezone-aware retrieval timestamp, exact locator, capture method, SHA-256 of the raw bytes, and explicit provenance state.
  - G0 validation fails closed on missing/invalid identity fields, ambiguous or unreviewed rights, unsupported rights basis, malformed timestamps, missing locator/method, malformed hash, and source-byte/hash mismatch.
  - Explicit-permission records require approval actor, timestamp, and reason fields.
  - Adds an atomic source-backed claim bound to source ID + exact locator + content hash.
  - Adds a HypothesisCard bound to source-backed claims and explicitly labelled `hypothesis` with `is_verified_rule=false`.
- `tests/test_source_provenance.py`, commit `07665dfa145d1634a33014ec93edd99f4ce44c46`:
  - Adds adversarial tests for missing/ambiguous rights, absent explicit-permission approval, missing locator, malformed/missing hash, content tampering, invalid timestamp/provenance, locator mismatch, unlinked hypotheses, and prevention of hypothesis-to-verified-rule promotion.
  - The only positive fixture is inline synthetic/local bytes created for the test; no third-party media was ingested.

### Exact-head CI status at checkpoint

For commit `07665dfa145d1634a33014ec93edd99f4ce44c46`, GitHub Actions returned:
- OpenFX Unit Tests: run `40969729907`, in progress at the time checked.
- Project Tests: run `40969730036`, in progress at the time checked.
- CodeQL: run `40969729944`, in progress at the time checked.

These are pending statuses, not passes. Refresh exact-head Actions before describing the implementation as CI-verified.

### Boundaries and unresolved issues

- The code records a rights basis and approval fields; it does not provide legal advice, independently authenticate permission, or decide whether a source's license actually covers the intended use.
- The current `explicit_permission` approval fields are caller-supplied metadata, not signed/audited reviewer events. Role separation and reviewer identity are not runtime-enforced.
- Source identity and exact locator are asserted fields; no external source fetcher, immutable capture store, transcript segmenter, or semantic-fidelity verifier is wired into this slice.
- The provenance state is a controlled vocabulary, not proof that the corresponding activity occurred. In particular, `test_confirmed` is only appropriate where a test actually confirms the relevant assertion.
- G1 currently binds a claim and hypothesis to a source reference but does not yet implement a claim graph, contradiction tracking, StrategySpec generation, reviewer workflow, or independent review.
- This is a local contract prototype only. It does not enable external ingestion, market-data evaluation, MT5, broker access, or trading.

### Next action

Refresh exact-head CI for `07665dfa145d1634a33014ec93edd99f4ce44c46`. If green, add schema-level contracts and tamper tests for persisted SourceRecord/Claim/HypothesisCard serialization, then build the synthetic-only end-to-end path (source → claim → hypothesis → frozen trial → two identical synthetic executions → independent hash comparison). Preserve the result as synthetic evidence only.


### CI correction — 2026-10-30

- The first exact-head attempt exposed a syntax error in the new test module's optional `__main__` guard (`if __ __name__`); both OpenFX Unit Tests run `40969729907` and Project Tests run `40969730036` failed during `compileall` for that same reason. This is a real failed check and is retained in the history.
- Corrected the guard in `tests/test_source_provenance.py`, commit `d707b2a46b947431379b47f788c247c4005f3964`.
- The workflow lookup immediately after that commit returned no runs yet. The corrected head is therefore pending CI evidence; do not describe the G0/G1 slice as passing CI until new exact-head runs are available.


## 14. Synthetic-only G0→G2 end-to-end replay prototype — 2026-10-30

### G0/G1 corrected-head CI refresh

For source head `d707b2a46b947431379b47f788c247c4005f3964`:
- Project Tests run `40969808391`: success.
- OpenFX Unit Tests run `40969808424`: success.
- CodeQL run `40969808460`: success.

The earlier failed compile runs `40969729907` and `40969730036` remain preserved; the correction was committed as `d707b2a46b947431379b47f788c247c4005f3964`.

### New G0→G2 implementation on PR #23 branch

- `openfx/synthetic_e2e.py`, commit `101f77665a5d007de87df18c4301529ec03c535d`:
  - Freezes the source reference, claim ID, hypothesis ID/status, synthetic engine parameters, trial/family IDs, and gate configuration into a canonical SHA-256-bound trial specification.
  - Validates source bytes and claim/source binding before freezing.
  - Registers the trial as pending before execution in the local hash-chained trial registry.
  - Executes the same frozen synthetic input twice in separate workspace directories and stores canonical raw run-record JSON bytes.
  - Compares both run-record and artifact hashes; records a terminal registry event; evaluates the descriptive gate using the registry-derived trial count.
  - Rejects altered frozen inputs before trial registration and accepts synthetic evidence only.
- `tests/test_synthetic_e2e.py`, commit `69107bc606ae18bce8fe91f073696dd5ac05a644`:
  - Tests identical replay hashes, registration lifecycle and trial count, frozen-input tampering rejection, and refusal to relabel a hypothesis as a verified rule.
  - Fixtures are locally authored synthetic bytes and deterministic synthetic returns only.

### Exact-head CI status

For PR #23 head `69107bc606ae18bce8fe91f073696dd5ac05a644`, Actions runs were created:
- OpenFX Unit Tests: `40973530989` — queued at last check.
- CodeQL: `40973531033` — queued at last check.
- Project Tests: `40973531157` — queued at last check.

No pass is claimed yet. Refresh these exact-head runs before treating this slice as CI-verified.

### What this demonstrates — and what it does not

- It is a runnable code path intended to connect local synthetic G0 provenance, G1 claim/hypothesis binding, frozen synthetic inputs, pre-registration, two deterministic replays, artifact hash comparison, and a registry-derived descriptive gate.
- The two replays are performed by the same code in one process; they are not independent human/code reproductions or a clean-room G4 replication.
- The registry is a local prototype and can be rewritten by a privileged actor; it is not a trusted central registrar.
- The descriptive gate does not calculate DSR/PBO/familywise correction; `multiple_testing_correction_applied=false` remains explicit.
- The runner is synthetic-only and does not invoke market data, MT5, broker, VPS, paid APIs, or trading.
- A passing synthetic replay is not evidence of market validity, strategy edge, or profitability.

### Next action

Refresh all three exact-head Actions runs for `69107bc606ae18bce8fe91f073696dd5ac05a644`; inspect any failures and correct them on the same PR branch. If green, add persisted JSON Schema contracts and artifact re-read/hash verification, then review the complete two-mission audit and cross-PR integration risks. Do not merge PRs.


## 15. Persisted synthetic artifact integrity — 2026-10-30

### Changes on PR #23 branch `openfx-foundation-m1-contracts`

- `openfx/synthetic_e2e.py`, commit `20de21a70ddbd153b1c5879ecad7ad0ef922f058`: after writing each synthetic run record, re-opens the exact path, compares persisted bytes to the expected bytes, parses JSON, enforces the strict v1 field set and synthetic evidence label, compares decoded content with the execution record, and hashes the bytes read back from disk.
- `schemas/synthetic-run-record-v1.schema.json`, created in commit `1b5935b17be6af5ae7585ec7485c37cc59a53656`, corrected to match the actual synthetic engine output in commit `f3bcc524d2b00b7112ff13dc8278b11c4ce2c4ca`. The schema is Draft 2020-12, versioned, rejects unknown fields, pins `evidence_level=synthetic` and `is_market_backtest=false`, and defines the actual run metrics/parameters.
- `tests/test_synthetic_e2e.py`, commit `ecb523bafa36d0cfbfb9768043963cca4ab52e10`: injects post-write disk tampering; expects read-back verification to reject the artifact and the registry to record `pending → failed`.
- `tests/test_json_schema_validation.py`, commits `1bbc5988fcf8c63fb4e776d061cbde5cd2afd232` and `cda92cbc2320e1bf96ea473eded5ef9fe167721e`: adds a valid schema fixture plus negative cases for market-level evidence relabeling, missing result, malformed frozen hash, and unsupported schema version.

### CI evidence

- The preceding head `69107bc606ae18bce8fe91f073696dd5ac05a644` has now completed all three exact-head checks successfully:
  - OpenFX Unit Tests run `40973530989`: success.
  - Project Tests run `40973531157`: success.
  - CodeQL run `40973531033`: success (Analyze Python job completed).
- The new hardening head `cda92cbc2320e1bf96ea473eded5ef9fe167721e` had no workflow runs returned at the time of this ledger update. Its CI status is pending/not yet observed; do not infer it from the previous head.

### Remaining limitations

- The persisted artifact is now read back and structurally checked by a small runtime contract plus a JSON Schema. The production execution path does not yet load/validate this schema through a general schema-validation service; the runtime check is deliberately local and narrow.
- This slice still runs the same synthetic engine twice in one process. It is not independent implementation reproduction, market-data testing, MT5 validation, or profitability evidence.
- SourceRecord, AtomicClaim, HypothesisCard, FrozenTrial, and registry event structures do not yet all have dedicated persisted JSON Schema files. This commit adds only the actual synthetic RunRecord contract.
- No local execution is claimed. Only GitHub Actions can establish repository CI results.

### Next action

Refresh exact-head Actions for `cda92cbc2320e1bf96ea473eded5ef9fe167721e`; inspect failures and correct them. Then extend schema contracts to the remaining persisted provenance/frozen-trial/registry objects and expand adversarial checks (invalid JSON, malformed event chains, duplicate event IDs, replay divergence, and source-content mismatch). Resume the broader two-mission audit after that, including cross-PR integration and actual worker/source-extraction boundaries. No merge.


### CI refresh correction — exact hardening head

For `cda92cbc2320e1bf96ea473eded5ef9fe167721e`, refreshed Actions now show:
- OpenFX Unit Tests run `40975873137`: completed success (syntax check and unit-test step both successful).
- Project Tests run `40975873003`: completed success (syntax check and project data-evaluation step successful).
- CodeQL run `40975872872`: still in progress at the latest refresh; the Analyze Python job was in progress at Initialize CodeQL. This is not yet a pass.


## 16. Provenance and registry contract hardening — 2026-10-30

### Exact-head CI correction for the prior hardening head

The earlier note that CodeQL was still running for `cda92cbc2320e1bf96ea473eded5ef9fe167721e` is superseded by the completed refresh:
- OpenFX Unit Tests `40975873137`: success.
- Project Tests `40975873003`: success.
- CodeQL `40975872872`: success.

### New changes on `openfx-foundation-m1-contracts`

- Added strict Draft 2020-12 schemas:
  - `schemas/source-record-v1.schema.json`, commit `822b353c9fc6e0e857706b4c997b87f27db2b873`.
  - `schemas/atomic-claim-v1.schema.json`, commit `ab5a23743c006d9a26a01efa4f62ca4470dce8c2`.
  - `schemas/hypothesis-card-v1.schema.json`, commit `cc910c85e76ca997dc664fdbaa52c105f7c3fd22`.
  - `schemas/registry-event-v1.schema.json`, commit `ffceae7aafa83ae34291813bcbd3727b297291d9`.
- Added valid fixtures for these contracts to `tests/test_json_schema_validation.py`, commit `57b8eedabfbb50a3be77d828fab6b7a565d715da`. Existing suite checks Draft 2020-12 schema validity, fixture validity, version rejection, and unknown top-level-field rejection across all listed schemas.
- Hardened `openfx/trial_registry.py`, commit `c0f0b9ce183aa40894c0a7ea40048a548856fab2`: event reads now require the exact v1 field set and reject unsupported `schema_version` before trusting the event hash. This closes the prior gap where extra event fields and unvalidated schema_version could be accepted if the event hash was recomputed.

### CI for current head

Current code head: `c0f0b9ce183aa40894c0a7ea40048a548856fab2`.
- OpenFX Unit Tests run `40979851698`: completed success.
- Project Tests run `40979851708`: completed success.
- CodeQL run `40979851703`: in progress at latest refresh; not yet a pass.

### Work not completed / explicit gaps

- A dedicated FrozenTrial JSON Schema was attempted but not committed; the schema-creation action was blocked. FrozenTrial remains protected by canonical freeze hash and runtime validation, not a persisted JSON Schema contract.
- An additional standalone adversarial Registry test file was not created. The runtime change is committed, but its dedicated tests for invalid JSON, duplicate event IDs, and schema-version tampering remain to be added. Do not describe those cases as newly tested.
- The JSON Schema suite structurally validates persisted examples, but it does not automatically validate every runtime object before persistence. SourceRecord legal rights, identity, locator truth, and human reviewer authenticity remain asserted metadata.
- Registry remains a local hash-chain ledger; a privileged actor can rewrite the full ledger. Strict shape and hash checks do not make it tamper-proof.
- HypothesisCard remains explicitly a hypothesis; it is not a verified rule.
- No independent human/clean-room reproduction, real market-data evaluation, MT5 test, or profitability evidence has been produced.

### Next action

Add a dedicated FrozenTrial schema and adversarial registry tests, then refresh all three exact-head Actions. Afterward resume the broader audit: review open PR dependency/cross-file conflict risks, compare worker implementation to its claimed role, and map actual source discovery/extraction/transcript accuracy and rights enforcement against G0-G5. No merge.


## 17. Frozen provenance binding and cross-PR integration audit — 2026-10-30

### FrozenTrial provenance binding

A review of `freeze_trial` found that the frozen digest previously carried the source locator/hash and claim/hypothesis IDs, but not digests of the complete SourceRecord, AtomicClaim, and HypothesisCard documents. That left descriptive/evidential fields outside the frozen binding.

Corrected on `openfx-foundation-m1-contracts`:
- `openfx/synthetic_e2e.py`, commit `684c1415b393b5278e2521d0b7af3149b7e54853`: the frozen spec now includes SHA-256 digests of the complete source record, claim, and hypothesis card, in addition to the existing source-content binding.
- `tests/test_synthetic_e2e.py`, commit `e89130c906030becf14879869590e604787a8582`: verifies these three digests exist and tampering with one invalidates the frozen hash.
- `schemas/frozen-trial-v1.schema.json`, commit `d3a6ce87e6f48c646f2f5a3a6767be1d5de1a160`: strict v1 FrozenTrial contract includes those three document digests.
- `tests/test_json_schema_validation.py`, commit `8ca1217de674c6c959db4476a211d05977f41767`: adds a structural FrozenTrial fixture.

### Registry event adversarial coverage

- `openfx/trial_registry.py`, commit `c0f0b9ce183aa40894c0a7ea40048a548856fab2`: strict event field set and schema-version enforcement.
- `tests/test_m2_research_controls.py`, commits `01499a4b3fc4a5ecde5cdb8ea98225d90b52d6c7` and `e1e1f082d51ca2f5bddfb391e5d54d5c81d04c22`: added tests for malformed JSON, extra event fields even when the event hash is recomputed, and unsupported event schema version. Duplicate event-ID checking already existed in the registry verification implementation and prior tests in this project; the new test additions above do not add a separate duplicate-ID fixture.

### CI evidence

- Previous strict-registry head `c0f0b9ce183aa40894c0a7ea40048a548856fab2`:
  - OpenFX Unit Tests `40979851698`: success.
  - Project Tests `40979851708`: success.
  - CodeQL `40979851703`: success.
- Current code head `e1e1f082d51ca2f5bddfb391e5d54d5c81d04c22`:
  - OpenFX Unit Tests `40980126134`: queued at latest refresh.
  - Project Tests `40980126108`: queued at latest refresh.
  - No CodeQL run was returned for this head at latest refresh. Do not infer any pass until refreshed.

### Broader integration audit — observed branch relationships

Live GitHub PR metadata confirms the following currently open, unmerged PRs and base/head relationships:

- PR #11: `openfx-audit-fixes → main`.
- PR #12: `openfx-transcript-adversarial-checks → openfx-audit-fixes` (depends on #11's branch).
- PR #14: `openfx-audit-round1 → openfx-transcript-adversarial-checks` (extends #12).
- PRs #15, #16, #17, #20, and #22 target `openfx-audit-round1`.
- PR #21 targets `openfx-audit-fixes`.
- PRs #18 and #19 independently target `main`.
- PR #23 targets `main` independently; it is not integrated with the #11–#22 branch chain.

All these PRs were observed open and unmerged in the latest metadata read. GitHub reports each individually mergeable against its declared base; this does not prove the entire chain is safe to merge in arbitrary order.

### Confirmed cross-PR collision

PR #16 and PR #17 are both based on `openfx-audit-round1`, and both change:
- `openfx/transcript_import.py`
- `tests/test_transcript_import.py`

PR #17 additionally changes `docs/SOURCE_INGESTION.md` and `tests/test_source_cli.py`. Their branch comparison is `diverged` (PR #16 head branch `openfx-transcript-import-strictness` vs PR #17 head branch `openfx-rights-gate`; 4 commits ahead / 7 behind from the selected comparison direction). They need a deliberate combined rebase/integration and a single test run; do not merge both independently based only on their individual mergeable flags.

PR #12 and PR #14 form a sequential branch chain; both touch `openfx/transcript_quality.py` and `tests/test_source_research.py`, but PR #14 is directly based on PR #12's head branch. PR #20 further changes those same transcript-quality/test paths plus its synthetic corpus and workflow. Treat this as an ordered chain, not independent cherry-picks.

### Worker capability audit

Reviewed `worker/openfx_worker.py` on `main` and the later `openfx-audit-fixes` branch:
- It validates declarative job fields, polls an HTTPS control-plane placeholder/configuration, and records local state/events.
- `process_job` returns `VALIDATED_NOT_EXECUTED`; there is no subprocess invocation, MT5 terminal API, strategy tester invocation, or broker execution path.
- The later audit branch adds cross-job idempotency-key rejection, host allow-list configuration, and a local state-file lock, but still explicitly does not execute jobs.
- It is therefore a validation/queue-worker prototype, not an MT5 execution worker or deployed VPS service. A control-plane server, trusted approval/attestation, MT5 adapter, durable registrar, and independent run-artifact capture are absent.

### Current limitations and next action

- Current branch head CI is still queued/not observed; refresh before further code edits or claims.
- Registry duplicate-event rejection is implemented, but a new dedicated duplicate-ID adversarial test was not added in this increment.
- The new FrozenTrial schema fixture is structural; the runtime path still does not invoke a generic schema-validation service on every frozen object.
- PR #23 remains independent of the transcript/source feature chain. A planned integration order and branch conflict resolution are required before a combined product can be evaluated.
- Continue with exact-head CI, then a conflict-aware PR integration plan and a G0–G5 capability/evidence audit. Do not merge or change `main`.


CI update for head `e1e1f082d51ca2f5bddfb391e5d54d5c81d04c22`: OpenFX Unit Tests run `40980126134` succeeded; Project Tests run `40980126108` succeeded; CodeQL run `40980126174` remains in progress at latest refresh.


## 18. Engineering decision and end-to-end readiness audit — 2026-10-30

### Exact-head CI refresh

For PR #23 branch `openfx-foundation-m1-contracts`, exact head `e1e1f082d51ca2f5bddfb391e5d54d5c81d04c22`:
- OpenFX Unit Tests run `40980126134`: completed success.
- Project Tests run `40980126108`: completed success.
- CodeQL run `40980126174`: completed success; its Analyze Python job completed successfully.

This establishes the listed GitHub Actions checks on this exact commit only. It does not establish market testing, production security, or profitability.

### Threat-model review against implementation

Reviewed `docs/THREAT_MODEL_M3.md`, `docs/G0_G5_ENFORCEMENT_MATRIX.md`, `docs/ARCHITECTURE_FOUNDATION_M1.md`, and `worker/openfx_worker.py` on the PR #23 head.

Confirmed:
- The threat model accurately labels itself an initial code-reviewed threat register, not a security certification.
- The attestation helper is a fail-closed control-flow boundary that delegates to an external verifier; no trusted key store, signature policy, revocation/expiry/nonce enforcement, or mandatory executor/registrar integration is established.
- Source rights, identity, locator, approval actor/time/reason, and source truth remain caller-asserted metadata. Hashing binds the supplied bytes/documents; it does not independently authenticate source ownership, legal permission, or reviewer identity.
- The worker is explicitly validation/audit-only. Its module states it does not invoke MT5 or execute jobs. The reviewed implementation is not a production control plane, MT5 adapter, broker connector, or VPS deployment.
- The local JSONL registry is not a trusted central registrar and can be rewritten by a privileged actor. Local locking/concurrency tests do not establish multi-host atomicity, power-loss durability, or crash recovery.
- Synthetic replay uses the same implementation twice in separate workspaces. This is useful deterministic regression evidence, but not independent implementation reproduction or G4 clean-room replication.
- The statistical gate is descriptive and does not calculate DSR, PBO, familywise error correction, or statistical power. It must not be used to certify an optimized strategy.
- The G0–G5 matrix and architecture docs are acceptance/design contracts. Their presence is not evidence that access controls, role separation, OOS secrecy, or every gate are enforced at runtime.

### G0–G5 capability verdict (current evidence)

| Gate | Current status | What is actually demonstrated | Blocking gap |
|---|---|---|---|
| G0 source admissibility | PARTIAL / BLOCKED for external autonomous ingestion | Local source-record/claim contracts, hashes, rights vocabulary, schema fixtures | No independently verified source capture, permission, reviewer identity, or full ingestion-to-transcript provenance |
| G1 claim and hypothesis | PARTIAL | Atomic claim and hypothesis structures bound to source references and full-document digests | No enforced human review workflow, contradiction graph, or independent semantic verification |
| G2 implementation and synthetic qualification | PARTIAL; synthetic slice CI-green | Frozen trial, local registration, deterministic synthetic replay, persisted artifact read-back, schemas and adversarial tests | Same-code replay, local rewriteable registry, incomplete runtime schema enforcement, no production authorization |
| G3 market-data evaluation | NOT IMPLEMENTED / BLOCKED | Data/cost/gate contracts exist | No trusted market-data pipeline, executable market runner, full cost model validation, untouched OOS access controls, or multiple-testing correction |
| G4 independent reproduction / MT5 demo | NOT IMPLEMENTED / BLOCKED | Attestation boundary helper and mock worker contract only | No trusted executor, independent clean-room reproducer, MT5 adapter, or evidenced MT5 demo run |
| G5 release/deployment | NOT IMPLEMENTED / BLOCKED | Human approval boundary documented | No release controls, deployed service, operational monitoring/rollback evidence, VPS or live-trading authorization |

### Engineering decision

**Do not add an MT5 executor, VPS worker, or further statistical-gate complexity yet. Do not merge PR #23 or any other PR.** The next highest-value increment is a bounded source-to-claim evidence vertical slice and an integration baseline, because without trustworthy G0/G1 evidence the later experiment machinery can only reproducibly test untrusted or invented hypotheses.

Before coding that slice, resolve the feature-branch integration graph and select one canonical integration branch. PR #16 and #17 require deliberate combination because they modify the same transcript-import implementation and tests. The #11 → #12 → #14 chain must remain ordered; #15/#20/#22 depend on the #14 branch; #21 depends on #11; #18/#19 and #23 are independent main-based branches. Individual mergeable flags are not a safe integration plan.

The next implementation increment should be limited to:
1. Define one canonical source-ingestion acceptance fixture with original bytes, stable locator, rights basis, capture timestamp, content hash, transcript artifact, and exact segment locator.
2. Add an auditable human-review event (reviewer identity, timestamp, decision, reason, reviewed content digest) rather than trusting a `human_verified` boolean or caller-supplied approval fields.
3. Bind each atomic claim to the exact transcript artifact digest and segment offsets/timecodes, then test tampering, missing/ambiguous rights, dropped negation, altered numbers/units/dates, and Persian/Arabic-Indic digit normalization.
4. Separate mechanical fidelity checks from semantic review; do not label heuristic checks as proof of semantic equivalence.
5. Produce one reproducible evidence package and negative-case report before connecting this path to strategy generation.

No external source should be scraped or ingested without an admissible rights basis. No paid service, API, VPS, MT5 demo, broker access, or live trading is authorized by this decision.

### Next precise action

Refresh and inventory all PR heads/files once more, then produce a single conflict-aware integration plan and a minimal acceptance-test specification for the source→transcript→review-event→claim→hypothesis chain. Keep all work on non-main branches and preserve every failed CI run and negative result.
