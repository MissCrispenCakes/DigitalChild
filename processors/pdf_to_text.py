# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

# PDF processor placeholder
"""
PDF to Text Processor
---------------------
Converts PDFs to plain text for further processing.
"""

import os

from pypdf import PdfReader

from processors.logger import get_logger

logger = get_logger("pdf_to_text")


def convert(pdf_path, output_dir):
    """
    Convert a PDF file to plain text.
    Saves the text file in the given output directory.
    Returns the path to the text file or None if failed.
    """
    try:
        reader = PdfReader(pdf_path)
        text = "\n".join([page.extract_text() or "" for page in reader.pages])
    except Exception as e:
        logger.error(f"Error reading {pdf_path}: {e}")
        return None

    os.makedirs(output_dir, exist_ok=True)
    txt_path = os.path.join(
        output_dir, os.path.basename(pdf_path).replace(".pdf", ".txt")
    )
    try:
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)
        logger.info(f"Extracted text → {txt_path}")
        return txt_path
    except Exception as e:
        logger.error(f"Error writing text file {txt_path}: {e}")
        return None
