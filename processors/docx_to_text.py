"""
DOCX to Text Processor
----------------------
Converts Word documents (.docx) to plain text.
"""

import os
from docx import Document
from processors.logger import get_logger

logger = get_logger("docx_to_text")


def convert(docx_path, output_dir):
    """
    Convert a DOCX file to plain text.
    Saves the text file in the given output directory.
    Returns the path to the text file or None if failed.
    """
    try:
        doc = Document(docx_path)
        text = "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        logger.error(f"Error reading {docx_path}: {e}")
        return None

    os.makedirs(output_dir, exist_ok=True)
    txt_path = os.path.join(output_dir, os.path.basename(docx_path).replace(".docx", ".txt"))
    try:
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)
        logger.info(f"Extracted text → {txt_path}")
        return txt_path
    except Exception as e:
        logger.error(f"Error writing text file {txt_path}: {e}")
        return None


def validate_format(filepath):
    return filepath.lower().endswith(".docx")
