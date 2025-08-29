# Logger
"""
Unified + per-module logging.
- Console output (INFO+)
- Unified run log file (all modules)
- Optional per-module log file (toggle via pipeline_runner)
"""

import os
import logging
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

RUN_LOGFILE = None
MODULE_LOGS_ENABLED = True
RUN_TIMESTAMP = None


def set_run_logfile(name="pipeline", module_logs=True):
    """
    Called by pipeline_runner once per run to define the shared log file.
    - name: name of the pipeline run
    - module_logs: enable/disable per-module log files
    """
    global RUN_LOGFILE, MODULE_LOGS_ENABLED, RUN_TIMESTAMP
    RUN_TIMESTAMP = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    RUN_LOGFILE = os.path.join(LOG_DIR, f"{RUN_TIMESTAMP}_{name}.log")
    MODULE_LOGS_ENABLED = module_logs

    # Clear existing root handlers so old ones don’t persist
    logging.getLogger().handlers.clear()
    return RUN_LOGFILE


def get_logger(name="pipeline"):
    """
    Returns a logger that writes to console, shared run log,
    and optionally its own per-module log.
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
        fh_shared = logging.FileHandler(RUN_LOGFILE, encoding="utf-8")
        fh_shared.setLevel(logging.DEBUG)
        fh_shared.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] [%(name)s] %(message)s"))
        logger.addHandler(fh_shared)

    # Module-specific log handler (optional, consistent run timestamp)
    if MODULE_LOGS_ENABLED and RUN_TIMESTAMP:
        logfile = os.path.join(LOG_DIR, f"{RUN_TIMESTAMP}_{name}.log")
        fh_module = logging.FileHandler(logfile, encoding="utf-8")
        fh_module.setLevel(logging.DEBUG)
        fh_module.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] [%(name)s] %(message)s"))
        logger.addHandler(fh_module)

    return logger
