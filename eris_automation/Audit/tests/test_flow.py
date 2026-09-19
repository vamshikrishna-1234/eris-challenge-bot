from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[2] / "Tools" / "flow.py"


class FlowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.automation = root / "eris_automation"
        self.project = root / "project"
        (self.project / "challenge_registry").mkdir(parents=True)
        self.env = os.environ.copy()
        self.env["ERIS_AUTOMATION_HOME"] = str(self.automation)
        self.env["ERIS_PROJECT_ROOT"] = str(self.project)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_flow(self, *args: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            env=self.env,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(expected, result.returncode, msg=result.stderr or result.stdout)
        return result

    def create(self, count: int = 1) -> dict:
        result = self.run_flow(
            "create",
            str(count),
            "--batch-id",
            "batch-test",
            "--authorization",
            f"Create {count} Task",
        )
        return json.loads(result.stdout)

    def test_create_exact_slots_and_local_status_is_not_live(self) -> None:
        created = self.create(3)
        self.assertEqual(3, created["requested_tasks"])
        self.assertEqual(3, len(set(created["task_ids"])))
        status = json.loads(self.run_flow("status", "--json").stdout)
        self.assertFalse(status["live_check_performed"])
        self.assertEqual({"queued": 3}, status["state_counts"])
        self.assertEqual("challenge_checks_passed", status["completion_stage"])
        self.assertEqual("successful_goal_target", status["completion_contract"])

    def test_default_batch_completes_before_run_agents(self) -> None:
        task_id = self.create()["task_ids"][0]
        for state in (
            "scouting",
            "build_ready",
            "building",
            "dataset_draft",
            "dataset_ready",
            "challenge_draft",
            "challenge_checks_passed",
        ):
            self.run_flow("set-state", task_id, "--state", state)
        status = json.loads(self.run_flow("status", "--json").stdout)
        self.assertEqual(1, status["successful_tasks"])
        self.assertEqual(0, status["remaining_to_goal"])
        self.assertTrue(json.loads(self.run_flow("ready").stdout)["cleared"])

    def test_revision_after_green_is_not_counted_as_current_success(self) -> None:
        task_id = self.create()["task_ids"][0]
        for state in (
            "scouting",
            "build_ready",
            "building",
            "dataset_draft",
            "dataset_ready",
            "challenge_draft",
            "challenge_checks_passed",
            "revision_requested",
        ):
            self.run_flow("set-state", task_id, "--state", state)
        status = json.loads(self.run_flow("status", "--json").stdout)
        self.assertEqual(0, status["successful_tasks"])
        self.assertEqual(1, status["remaining_to_goal"])

    def test_retry_after_green_preserves_verified_checkpoint(self) -> None:
        task_id = self.create()["task_ids"][0]
        for state in (
            "scouting",
            "build_ready",
            "building",
            "dataset_draft",
            "dataset_ready",
            "challenge_draft",
            "challenge_checks_passed",
            "retry_wait",
        ):
            self.run_flow("set-state", task_id, "--state", state)
        status = json.loads(self.run_flow("status", "--json").stdout)
        self.assertEqual(1, status["successful_tasks"])
        self.assertEqual(0, status["remaining_to_goal"])

    def test_second_active_batch_is_rejected(self) -> None:
        self.create()
        result = self.run_flow(
            "create",
            "1",
            "--batch-id",
            "batch-two",
            "--authorization",
            "Create 1 Task",
            expected=2,
        )
        self.assertIn("still active", result.stderr)

    def test_ready_requires_run_agents_success_not_rejection(self) -> None:
        task_id = self.create()["task_ids"][0]
        pending = self.run_flow("ready", expected=2)
        self.assertFalse(json.loads(pending.stdout)["ready"])
        self.run_flow("set-state", task_id, "--state", "rejected", "--note", "Bad candidate")
        still_pending = self.run_flow("ready", expected=2)
        self.assertFalse(json.loads(still_pending.stdout)["ready"])
        resumed = json.loads(self.run_flow("resume-incomplete").stdout)
        self.assertEqual("scouting", resumed["resumed"][0]["to"])
        for state in (
            "build_ready",
            "building",
            "dataset_draft",
            "dataset_ready",
            "challenge_draft",
            "challenge_checks_passed",
            "agent_runs_started",
        ):
            self.run_flow("set-state", task_id, "--state", state)
        cleared = json.loads(self.run_flow("ready").stdout)
        self.assertTrue(cleared["cleared"])
        self.assertTrue((self.automation / "State" / "tasks" / f"{task_id}.json").is_file())

    def test_candidate_rejection_preserves_slot_and_requests_replacement(self) -> None:
        task_id = self.create()["task_ids"][0]
        self.run_flow("set-state", task_id, "--state", "scouting")
        self.run_flow("set-state", task_id, "--state", "pilot")
        replacement = json.loads(
            self.run_flow(
                "replace-candidate",
                task_id,
                "--candidate",
                "public-noaa-labels",
                "--verdict",
                "rejected",
                "--reason",
                "Exact hidden-answer lookup",
            ).stdout
        )
        self.assertTrue(replacement["replacement_required"])
        self.assertEqual("scouting", replacement["state"])
        status = json.loads(self.run_flow("status", "--json").stdout)
        self.assertEqual(0, status["successful_tasks"])
        self.assertEqual(1, status["remaining_to_goal"])
        self.assertEqual(1, len(status["tasks"][0]["candidate_attempts"]))

    def test_rate_limit_is_retryable_and_does_not_block_or_finish_slot(self) -> None:
        task_id = self.create()["task_ids"][0]
        self.run_flow("set-state", task_id, "--state", "scouting")
        transient = json.loads(
            self.run_flow(
                "record-transient",
                task_id,
                "--kind",
                "rate_limit",
                "--message",
                "TPM limit",
                "--retry-after",
                "20.97",
            ).stdout
        )
        self.assertTrue(transient["retry_required"])
        self.assertEqual("retry_wait", transient["state"])
        self.assertFalse(transient["goal_achieved"])
        resumed = json.loads(self.run_flow("resume-incomplete").stdout)
        self.assertEqual("scouting", resumed["resumed"][0]["to"])

    def test_revision_does_not_change_task_count(self) -> None:
        task_id = self.create()["task_ids"][0]
        for state in ("scouting", "build_ready", "building"):
            self.run_flow("set-state", task_id, "--state", state)
        self.run_flow(
            "record-live",
            task_id,
            "--platform-state",
            "challenge_needs_revision",
            "--url",
            "https://shipd.ai/example",
            "--note",
            "One yellow warning",
        )
        status = json.loads(self.run_flow("status", "--json").stdout)
        self.assertEqual(1, status["requested_tasks"])
        self.assertEqual(1, status["revision_total"])
        self.assertEqual("revision_requested", status["tasks"][0]["state"])

    def test_bind_requires_existing_registry_record(self) -> None:
        task_id = self.create()["task_ids"][0]
        missing = self.run_flow(
            "bind", task_id, "--registry-key", "missing-record", expected=2
        )
        self.assertIn("does not exist", missing.stderr)
        (self.project / "challenge_registry" / "real-record.json").write_text(
            '{"status":"claimed"}\n', encoding="utf-8"
        )
        bound = json.loads(
            self.run_flow("bind", task_id, "--registry-key", "real-record").stdout
        )
        self.assertTrue(bound["bound"])

    def test_bind_records_exact_link_pair_and_derives_ids(self) -> None:
        task_id = self.create()["task_ids"][0]
        (self.project / "challenge_registry" / "real-record.json").write_text(
            '{"status":"claimed"}\n', encoding="utf-8"
        )
        dataset_url = "https://shipd.ai/quests/eris/datasets/jd7dataset123"
        problem_url = "https://shipd.ai/quests/eris/problems/jx7problem456"
        bound = json.loads(
            self.run_flow(
                "bind",
                task_id,
                "--registry-key",
                "real-record",
                "--dataset-url",
                dataset_url,
                "--problem-url",
                problem_url,
            ).stdout
        )
        self.assertEqual("jd7dataset123", bound["dataset_id"])
        self.assertEqual("jx7problem456", bound["problem_id"])
        self.assertEqual(dataset_url, bound["dataset_url"])
        self.assertEqual(problem_url, bound["problem_url"])

    def test_visible_worker_binding_is_preserved(self) -> None:
        task_id = self.create()["task_ids"][0]
        first = json.loads(
            self.run_flow(
                "bind-worker",
                task_id,
                "--thread-id",
                "worker-one",
                "--host-id",
                "local",
                "--title",
                "Eris Slot 1 Worker",
            ).stdout
        )
        self.assertEqual("worker-one", first["worker_thread_id"])
        self.run_flow(
            "bind-worker",
            task_id,
            "--thread-id",
            "worker-two",
            "--host-id",
            "local",
            "--title",
            "Eris Slot 1 Replacement Worker",
        )
        status = json.loads(self.run_flow("status", "--json").stdout)
        task = status["tasks"][0]
        self.assertEqual("worker-two", task["worker_thread_id"])
        self.assertEqual("worker-one", task["worker_history"][0]["thread_id"])

    def test_bind_rejects_mismatched_link_and_explicit_id(self) -> None:
        task_id = self.create()["task_ids"][0]
        (self.project / "challenge_registry" / "real-record.json").write_text(
            '{"status":"claimed"}\n', encoding="utf-8"
        )
        result = self.run_flow(
            "bind",
            task_id,
            "--registry-key",
            "real-record",
            "--dataset-id",
            "different",
            "--dataset-url",
            "https://shipd.ai/quests/eris/datasets/jd7dataset123",
            expected=2,
        )
        self.assertIn("does not match", result.stderr)

    def test_path_traversal_batch_id_is_rejected(self) -> None:
        result = self.run_flow(
            "create",
            "1",
            "--batch-id",
            "../escape",
            "--authorization",
            "Create 1 Task",
            expected=2,
        )
        self.assertIn("Invalid batch ID", result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
