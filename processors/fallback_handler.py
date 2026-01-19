"""
Fallback Handler
----------------
Tries different processors if a file is mislabeled or format detection fails.
"""

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
    result = pdf_to_text.convert(filepath, output_dir)
    if result:
        return result

    # 2. Try DOCX (if format validates or has .docx/.doc extension)
    if docx_to_text.validate_format(filepath) or filepath.lower().endswith(
        (".docx", ".doc")
    ):
        result = docx_to_text.convert(filepath, output_dir)
        if result:
            return result

    # 3. Try HTML (if format validates or has .html/.htm extension)
    if html_to_text.validate_format(filepath) or filepath.lower().endswith(
        (".html", ".htm")
    ):
        result = html_to_text.convert(filepath, output_dir)
        if result:
            return result

    logger.error(f"All fallback processors failed for {filepath}")
    return None
