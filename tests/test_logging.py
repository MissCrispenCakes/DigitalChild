# Logging test
import glob
import os
import subprocess
import sys

import pytest

LOG_DIR = "logs"


@pytest.mark.parametrize(
    "args,expect_module_logs",
    [
        ([], True),  # default → unified + per-module logs
        (["--no-module-logs"], False),  # unified only
    ],
)
def test_pipeline_creates_logs(args, expect_module_logs):
    os.makedirs(LOG_DIR, exist_ok=True)

    # Record existing logs
    before = set(glob.glob(os.path.join(LOG_DIR, "*.log")))

    # Run pipeline_runner.py as subprocess
    cmd = [
        sys.executable,
        "pipeline_runner.py",
        "--source",
        "au_policy",
        "--tags-version",
        "v1",
    ] + args
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Ensure pipeline executed successfully
    assert result.returncode == 0, f"Pipeline failed: {result.stderr}"

    # Collect logs after run
    after = set(glob.glob(os.path.join(LOG_DIR, "*.log")))
    new_logs = after - before

    # Verify new logs were created
    assert new_logs, "No new log files created"

    # Unified log should always exist
    unified_logs = [f for f in new_logs if f.endswith(f"_run.log")]
    assert unified_logs, "Unified run log missing"

    if expect_module_logs:
        module_logs = [f for f in new_logs if not f.endswith(f"_run.log")]
        assert module_logs, "Module logs expected but not found"
    else:
        module_logs = [f for f in new_logs if not f.endswith(f"_run.log")]
        assert not module_logs, f"Module logs found unexpectedly: {module_logs}"
