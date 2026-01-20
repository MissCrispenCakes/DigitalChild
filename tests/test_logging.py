import glob
import os
import subprocess
import sys

import pytest

# ✅ Pipeline runs as subprocess, so logs go to main logs/ directory
LOG_DIR = "logs"


@pytest.mark.parametrize(
    "args,expect_module_logs",
    [
        ([], True),
        (["--no-module-logs"], False),
    ],
)
def test_pipeline_creates_logs(args, expect_module_logs):
    os.makedirs(LOG_DIR, exist_ok=True)

    # Clean slate
    before = set(glob.glob(os.path.join(LOG_DIR, "*.log")))

    # Run pipeline_runner.py as subprocess
    cmd = [
        sys.executable,
        "pipeline_runner.py",
        "--source",
        "au_policy",
        "--tags-version",
        "queerai",  # ✅ must match configs/tags_main.json
    ] + args
    result = subprocess.run(cmd, capture_output=True, text=True)

    assert result.returncode == 0, f"Pipeline failed: {result.stderr}"

    after = set(glob.glob(os.path.join(LOG_DIR, "*.log")))
    new_logs = after - before
    assert new_logs, f"No new log files created in {LOG_DIR}"

    # Unified log always ends with "_run.log"
    unified_logs = [f for f in new_logs if f.endswith("_run.log")]
    assert unified_logs, "Unified run log missing"

    # Module logs may or may not exist depending on flag
    module_logs = [f for f in new_logs if not f.endswith("_run.log")]
    if expect_module_logs:
        assert module_logs, "Module logs expected but not found"
    else:
        assert not module_logs, f"Module logs found unexpectedly: {module_logs}"
