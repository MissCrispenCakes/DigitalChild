"""
HTML to Text Processor
----------------------
Converts HTML documents to plain text by stripping tags.
"""

import os

from bs4 import BeautifulSoup

from processors.logger import get_logger

logger = get_logger("html_to_text")


def convert(html_path, output_dir):
    """
    Convert an HTML file to plain text.
    Saves the text file in the given output directory.
    Returns the path to the text file or None if failed.
    """
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            text = soup.get_text(separator="\n")
    except Exception as e:
        logger.error(f"Error reading {html_path}: {e}")
        return None

    os.makedirs(output_dir, exist_ok=True)
    txt_path = os.path.join(
        output_dir, os.path.basename(html_path).replace(".html", ".txt")
    )
    try:
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)
        logger.info(f"Extracted text → {txt_path}")
        return txt_path
    except Exception as e:
        logger.error(f"Error writing text file {txt_path}: {e}")
        return None


def validate_format(filepath):
    return filepath.lower().endswith(".html") or filepath.lower().endswith(".htm")
