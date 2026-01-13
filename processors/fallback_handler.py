"""
Fallback Handler
----------------
Tries different processors if a file is mislabeled or format detection fails.
"""

import os

from processors import docx_to_text, html_to_text, pdf_to_text
from processors.logger import get_logger

logger = get_logger("fallback_handler")


def process_with_fallback(filepath, output_dir):
    """
    Try to process file with available processors.
    Order: pdf_to_text → docx_to_text → html_to_text.
    Returns path to text file or None if all fail.
    """

    # 1. Try PDF
    if pdf_to_text.convert(filepath, output_dir):
        base_name = os.path.splitext(os.path.basename(filepath))[0]
        return os.path.join(output_dir, f"{base_name}.txt")

    # 2. Try DOCX
    if docx_to_text.validate_format(filepath) or filepath.lower().endswith(".pdf"):
        if docx_to_text.convert(filepath, output_dir):
            base_name = os.path.splitext(os.path.basename(filepath))[0]
            return os.path.join(output_dir, f"{base_name}.txt")

    # 3. Try HTML
    if html_to_text.validate_format(filepath) or filepath.lower().endswith(".pdf"):
        if html_to_text.convert(filepath, output_dir):
            base_name = os.path.splitext(os.path.basename(filepath))[0]
            return os.path.join(output_dir, f"{base_name}.txt")

    logger.error(f"All fallback processors failed for {filepath}")
    return None
