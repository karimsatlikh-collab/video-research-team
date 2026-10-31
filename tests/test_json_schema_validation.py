"""Full JSON Schema validation for all versioned OpenFX contracts.

These tests validate structural contracts only. Cross-document consistency,
authorization, state transitions, engine attestation, and statistical validity
require separate runtime controls.
"""
import copy
import json
import unittest
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = ROOT / "schemas"
FORMAT_CHECKER = FormatChecker()
HASH = "a" * 64
NOW = "2026-01-01T00:00:00Z"

EXAMPLES = {
    "strategy-spec-v1.schema.json": {
        "schema_version": 1, "strategy_id": "demo", "version": "1.0",
        "description": "Structural fixture only.",
        "rules": {
            "entry": [{"rule_id": "e1", "statement": "Example entry", "status": "hypothesis"}],
            "exit": [{"rule_id": "x1", "statement": "Example exit", "status": "hypothesis"}],
            "filters": [],
            "risk": [{"rule_id": "r1", "statement": "Example risk", "status": "hypothesis"}],
        },
        "claims": [{"claim_id": "c1", "text": "Unverified example", "label": "hypothesis"}],
        "created_at_utc": NOW,
    },
    "job-spec-v1.schema.json": {
        "schema_version": 1, "job_id": "job-1",
        "strategy_spec_ref": {"id": "demo", "version": "1.0", "sha256": HASH},
        "implementation": {"source_revision": "abc123", "build_sha256": HASH},
        "data_profile_ref": {"id": "data", "version": "1.0", "sha256": HASH},
        "cost_profile_ref": {"id": "cost", "version": "1.0", "sha256": HASH},
        "gate_config_ref": {"id": "gate", "version": "1.0", "sha256": HASH},
        "frozen_parameters": {"example": 1},
        "budget": {"max_trials": 1, "timeout_seconds": 60},
        "requested_engine": "synthetic", "created_at_utc": NOW,
    },
    "run-record-v1.schema.json": {
        "schema_version": 1, "run_id": "run-1", "job_id": "job-1",
        "status": "COMPLETED", "evidence_level": "synthetic",
        "timestamps": {"created_at_utc": NOW, "started_at_utc": NOW, "finished_at_utc": NOW},
        "inputs": {
            "job_spec_sha256": HASH, "strategy_spec_sha256": HASH,
            "implementation_sha256": HASH, "data_profile_sha256": HASH,
            "cost_profile_sha256": HASH, "gate_config_sha256": HASH,
        },
        "outputs": [{"name": "summary.json", "sha256": HASH, "media_type": "application/json"}],
        "error": None,
    },
    "frozen-trial-v1.schema.json": {
        "schema_version": 1, "evidence_level": "synthetic",
        "source_ref": {"source_id": "source-1", "exact_locator": "fixture://source/1", "content_sha256": HASH},
        "source_record_sha256": HASH, "claim_sha256": HASH, "hypothesis_sha256": HASH,
        "claim_id": "claim-1", "hypothesis_id": "hyp-1", "hypothesis_status": "hypothesis",
        "family_id": "family-1", "trial_id": "trial-1",
        "engine": "openfx.synthetic_engine.run_synthetic",
        "engine_parameters": {"seed": 1, "n": 20, "edge": 0.0, "noise": 1.0},
        "gate_config": {"frozen_before_trials": True}, "frozen_sha256": HASH,
    },
    "source-record-v1.schema.json": {
        "source_id": "fixture-source-1", "identity": "local fixture",
        "rights_basis": "owner_created", "permission_evidence": "created for tests",
        "retrieved_at_utc": NOW, "exact_locator": "fixture://source/1",
        "capture_method": "inline bytes", "content_sha256": HASH,
        "provenance_state": "test_confirmed", "human_approval": None,
    },
    "atomic-claim-v1.schema.json": {
        "claim_id": "claim-1", "statement": "Fixture observation.",
        "source_ref": {"source_id": "fixture-source-1", "exact_locator": "fixture://source/1", "content_sha256": HASH},
        "provenance_state": "test_confirmed", "claim_kind": "source_backed",
    },
    "hypothesis-card-v1.schema.json": {
        "hypothesis_id": "hyp-1", "title": "Fixture hypothesis",
        "falsifiable_statement": "If X then Y.", "predicted_mechanism": "Mechanism",
        "invalidation_criteria": "Reject if Y does not occur.",
        "linked_claims": [{"claim_id": "claim-1", "source_ref": {"source_id": "fixture-source-1", "exact_locator": "fixture://source/1", "content_sha256": HASH}, "claim_provenance_state": "test_confirmed"}],
        "epistemic_status": "hypothesis", "is_verified_rule": False,
        "limitations": ["Fixture only."],
    },
    "registry-event-v1.schema.json": {
        "schema_version": 1, "sequence": 1, "family_sequence": 1, "trial_index": 1,
        "event_id": "event-1", "family_id": "family-1", "trial_id": "trial-1",
        "outcome": "pending", "payload": {}, "previous_event_sha256": "0" * 64,
        "event_sha256": HASH,
    },
    "attempt-event-v1.schema.json": {
        "schema_version": 1, "sequence": 1, "event_id": "attempt-event-1",
        "attempt_id": "attempt-1", "event_type": "started",
        "occurred_at_utc": NOW, "payload": {"request_sha256": HASH},
        "previous_event_sha256": "0" * 64, "event_sha256": HASH,
    },
    "synthetic-run-record-v1.schema.json": {
        "schema_version": 1, "frozen_sha256": HASH, "trial_id": "trial-1",
        "evidence_level": "synthetic", "engine": "openfx.synthetic_engine.run_synthetic",
        "engine_parameters": {"seed": 17, "n": 50, "edge": 0.0, "noise": 1.0},
        "result": {
            "seed": 17, "sample_size": 50, "mean_return": 0.0,
            "positive_fraction": 0.5, "max_drawdown_units": 4.0,
            "returns_sha256": HASH, "evidence_level": "synthetic",
            "is_market_backtest": False,
        },
    },
    "trial-registry-entry-v1.schema.json": {
        "schema_version": 1, "trial_id": "trial-1", "family_id": "family-1",
        "job_id": "job-1", "run_id": "run-1", "trial_index": 1,
        "registered_at_utc": NOW, "outcome": "completed", "parameter_count": 1,
        "gate_verdict": "not_run",
    },
    "gate-verdict-v1.schema.json": {
        "schema_version": 1, "verdict_id": "verdict-1", "run_id": "run-1",
        "decision": "inconclusive", "gate_version": "1.0",
        "gate_config_sha256": HASH, "trial_family_id": "family-1",
        "trial_count_at_decision": 1, "checks": [],
        "created_at_utc": NOW, "limitations": ["Fixture only; no market inference."],
    },
    "data-profile-v1.schema.json": {
        "schema_version": 1, "profile_id": "data", "version": "1.0",
        "source": {"provider": "synthetic-fixture", "dataset_id": "seeded-1"},
        "symbol": "TEST", "timeframe": "M1",
        "date_range": {"start_utc": NOW, "end_utc": "2026-01-02T00:00:00Z"},
        "price_data_mode": "synthetic", "data_sha256": HASH, "created_at_utc": NOW,
    },
    "cost-profile-v1.schema.json": {
        "schema_version": 1, "profile_id": "cost", "version": "1.0", "symbol": "TEST",
        "spread_model": {"mode": "fixed", "value_points": 1},
        "commission": {"amount": 0, "currency": "USD", "basis": "per_lot_round_turn"},
        "slippage": {"model": "none", "value_points": 0},
        "swap": {"model": "none"},
        "symbol_spec": {"digits": 5, "point_size": 0.00001, "contract_size": 100000,
                        "tick_size": 0.00001, "tick_value": 1},
        "created_at_utc": NOW,
    },
    "gate-config-v1.schema.json": {
        "schema_version": 1, "gate_id": "gate", "version": "1.0",
        "frozen_before_trials": True,
        "trial_family_policy": {"family_id": "family-1", "max_trials": 10,
                                "count_failures_and_abandoned": True},
        "data_split": {"development": "dev", "validation": "val", "final_oos": "untouched",
                       "final_oos_access_policy": "single_use"},
        "multiple_testing_method": "other_pre_registered",
        "acceptance_thresholds": {"min_samples": 100},
        "cost_sensitivity_scenarios": [
            {"scenario_id": "base", "description": "Base costs", "cost_multiplier": 1.0}
        ],
        "created_at_utc": NOW,
    },
}


class JsonSchemaValidationTests(unittest.TestCase):
    def load_schema(self, filename):
        with (SCHEMAS_DIR / filename).open(encoding="utf-8") as handle:
            return json.load(handle)

    def test_every_schema_is_valid_draft_2020_12(self):
        for filename in EXAMPLES:
            with self.subTest(schema=filename):
                schema = self.load_schema(filename)
                Draft202012Validator.check_schema(schema)

    def test_minimal_contract_examples_validate(self):
        for filename, instance in EXAMPLES.items():
            with self.subTest(schema=filename):
                schema = self.load_schema(filename)
                validator = Draft202012Validator(schema, format_checker=FORMAT_CHECKER)
                errors = sorted(validator.iter_errors(instance), key=lambda e: list(map(str, e.path)))
                self.assertEqual([], [f"{list(e.path)}: {e.message}" for e in errors])

    def test_invalid_schema_version_is_rejected_for_every_contract(self):
        for filename, instance in EXAMPLES.items():
            with self.subTest(schema=filename):
                invalid = copy.deepcopy(instance)
                invalid["schema_version"] = 2
                validator = Draft202012Validator(
                    self.load_schema(filename), format_checker=FORMAT_CHECKER
                )
                self.assertTrue(list(validator.iter_errors(invalid)))

    def test_synthetic_run_record_rejects_market_level_missing_fields_and_bad_hash(self):
        filename = "synthetic-run-record-v1.schema.json"
        schema = self.load_schema(filename)
        validator = Draft202012Validator(schema, format_checker=FORMAT_CHECKER)
        valid = copy.deepcopy(EXAMPLES[filename])
        for mutate in (
            lambda value: value.update(evidence_level="market"),
            lambda value: value.pop("result"),
            lambda value: value.update(frozen_sha256="not-a-sha256"),
            lambda value: value.update(schema_version=2),
        ):
            invalid = copy.deepcopy(valid)
            mutate(invalid)
            self.assertTrue(list(validator.iter_errors(invalid)))

    def test_unknown_top_level_fields_are_rejected(self):
        for filename, instance in EXAMPLES.items():
            with self.subTest(schema=filename):
                invalid = copy.deepcopy(instance)
                invalid["unexpected_unreviewed_field"] = True
                validator = Draft202012Validator(
                    self.load_schema(filename), format_checker=FORMAT_CHECKER
                )
                self.assertTrue(list(validator.iter_errors(invalid)))


if __name__ == "__main__":
    unittest.main()
