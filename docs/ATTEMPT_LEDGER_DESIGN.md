# Pre-registration Attempt Ledger — design and prototype

**Status:** Isolated prototype on `feat/pre-registration-attempt-ledger`; not yet connected to the canonical adapter.  
**Parent:** PR #67 head `67c2405129d8cb07ed07d53aa154ee42ad818dd9`.  
**Purpose:** Preserve an audit record for a request that fails before a durable trial-registration event exists, without corrupting trial counts or mixing request attempts into the trial lifecycle.

## 1. The accounting distinction

OpenFX needs two different identities:

- **Attempt:** one invocation/request to validate and possibly register work. Invalid schemas, digest mismatches, duplicate trial IDs, budget denials, and registry lock failures are attempts even when no trial was admitted.
- **Trial:** a research experiment admitted durably to `LocalTrialRegistry`. The trial registry remains the sole authority for trial-family counting and accepted-trial outcomes.

A rejected attempt MUST NOT create a trial event and MUST NOT consume trial-family budget. A trial consumes budget only when its first durable trial-registry event is accepted.

## 2. Proposed lifecycle

The separate append-only attempt ledger supports these event types:

1. `started` — written before validation begins; binds a request fingerprint and optional job/family/trial IDs.
2. `pre_registration_rejected` — validation or policy rejected the request before trial admission.
3. `registration_failed` — admission was attempted but the trial registry rejected it or could not durably accept it.
4. `trial_registered` — links the attempt to the accepted pending event in the trial registry by event ID, sequence, and SHA-256.
5. `reconciliation_required` — an explicit marker for a crash/partial-write case that cannot yet be resolved automatically.

Every attempt begins with exactly one `started` event and may receive exactly one terminal attempt event. The prototype deliberately does not duplicate the trial's later completed/failed/interrupted lifecycle; that remains in the trial registry.

## 3. Ordering and crash handling

The intended adapter integration order is:

1. Canonicalize the request and compute a request fingerprint (hash only; do not persist raw request documents).
2. Append and fsync `started`. If this cannot be persisted, fail closed and do not proceed to validation or execution.
3. Validate schemas, cross-document references, frozen-trial binding, implementation digest, and policy.
4. On a pre-registration rejection, append `pre_registration_rejected` with a categorical `error_code` and optional exception type only.
5. Before/with trial admission, include `attempt_id` in the trial registry's pending-event payload.
6. Once the trial registry confirms durable admission, append `trial_registered` linked to that exact registry event.
7. Only then allow execution side effects.

There is an unavoidable two-file commit gap between the trial registry and attempt ledger. If the process stops after trial admission but before `trial_registered` is appended, recovery MUST correlate the attempt ID in the trial registry and append an explicit reconciliation result. An unfinished `started` event is reported as open/unknown; it MUST NOT be silently converted to failed or rejected. If no matching durable trial event exists, an operator/recovery procedure may close it as interrupted only with recorded evidence.

## 4. Data minimization and integrity

- No raw exception messages, file paths, secrets, prompts, source text, or complete job documents in the ledger.
- Store only a request SHA-256, identifiers, categorical error codes/types, and cross-ledger event references.
- Events use a strict field set, UTC timestamp, global sequence, previous-event hash, and event hash.
- A local exclusive lock prevents concurrent local appends; hash chaining detects accidental edits.
- This is not a signed attestation, trusted central registrar, multi-host lock, or protection against a privileged actor rewriting the whole file.

## 5. Prototype contents and current limits

- `openfx/attempt_ledger.py`: standard-library-only local append-only ledger.
- `schemas/attempt-event-v1.schema.json`: structural event schema.
- `tests/test_attempt_ledger.py`: unit/adversarial tests for transitions, interleaved attempts, idempotent retries, unsafe payload rejection, hash tampering, open attempts, and lock timeout.

**Important:** This PR adds the isolated ledger primitive and its tests only. It does not yet modify `run_canonical_synthetic_job`, does not write attempt events during real adapter calls, and does not claim to have solved the pre-registration audit gap. The next integration step must add `attempt_id` correlation to the trial pending event and test failures at every boundary, including crashes between the two ledgers.

## 6. Acceptance gates before integration

- Run exact-head CI and inspect each job.
- Add schema-validation tests for the new event schema.
- Integrate the ledger into the adapter with fail-closed start recording and safe error categorization.
- Prove pre-registration rejects create attempt events but zero trial events / zero trial budget consumption.
- Prove accepted registration links both ledgers to the same exact event hash/sequence.
- Inject failures before start, during validation, during registry admission, after registry admission, and before/after execution; verify no false status inference.
- Test recovery of an open attempt and duplicate/replay behavior.
- Keep PR #67's scope and existing trial-registry semantics intact.

No merge, production deployment, paid service, VPS, MT5, broker, or live trading is authorized by this work.
