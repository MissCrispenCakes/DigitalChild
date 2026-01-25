# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

"""
Unified + per-module logging.
- Console output (INFO+)
- Unified run log file (all modules)
- Optional per-module log file (toggle via pipeline_runner)
"""

import logging
import os
import sys
from datetime import datetime, timezone

# Default log dir, but tests go into logs/tests/
BASE_LOG_DIR = "logs"
if "pytest" in sys.modules:
    BASE_LOG_DIR = os.path.join(BASE_LOG_DIR, "tests")

os.makedirs(BASE_LOG_DIR, exist_ok=True)

RUN_LOGFILE = None
MODULE_LOGS_ENABLED = True
RUN_TIMESTAMP = None


def set_run_logfile(name="pipeline", module_logs=True, log_dir=None):
    """
    Called by pipeline_runner once per run to define the shared log file.
    - name: name of the pipeline run
    - module_logs: enable/disable per-module log files
    - log_dir: optional override for log directory
    """
    global RUN_LOGFILE, MODULE_LOGS_ENABLED, RUN_TIMESTAMP

    log_dir = log_dir or BASE_LOG_DIR
    os.makedirs(log_dir, exist_ok=True)

    RUN_TIMESTAMP = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
    RUN_LOGFILE = os.path.join(log_dir, f"{RUN_TIMESTAMP}_{name}.log")
    MODULE_LOGS_ENABLED = module_logs

    # Clear existing root handlers so old ones don’t persist
    logging.getLogger().handlers.clear()
    return RUN_LOGFILE


def get_logger(name="pipeline"):
    """
    Returns a logger that writes to console, shared run log,
    and optionally its own per-module log.
    Prevents duplicate handlers.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Avoid duplicate handlers if logger already configured
    if logger.handlers:
        return logger

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("[%(levelname)s] [%(name)s] %(message)s"))
    logger.addHandler(ch)

    # Shared run log handler
    if RUN_LOGFILE:
        if not any(
            isinstance(h, logging.FileHandler)
            and getattr(h, "baseFilename", None) == os.path.abspath(RUN_LOGFILE)
            for h in logger.handlers
        ):
            fh_shared = logging.FileHandler(RUN_LOGFILE, encoding="utf-8")
            fh_shared.setLevel(logging.DEBUG)
            fh_shared.setFormatter(
                logging.Formatter("%(asctime)s [%(levelname)s] [%(name)s] %(message)s")
            )
            logger.addHandler(fh_shared)

    # Module-specific log handler (optional, consistent run timestamp)
    if MODULE_LOGS_ENABLED and RUN_TIMESTAMP:
        log_dir = os.path.dirname(RUN_LOGFILE) if RUN_LOGFILE else BASE_LOG_DIR
        logfile = os.path.join(log_dir, f"{RUN_TIMESTAMP}_{name}.log")
        if not any(
            isinstance(h, logging.FileHandler)
            and getattr(h, "baseFilename", None) == os.path.abspath(logfile)
            for h in logger.handlers
        ):
            fh_module = logging.FileHandler(logfile, encoding="utf-8")
            fh_module.setLevel(logging.DEBUG)
            fh_module.setFormatter(
                logging.Formatter("%(asctime)s [%(levelname)s] [%(name)s] %(message)s")
            )
            logger.addHandler(fh_module)

    return logger
