# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

import os
import tempfile  # noqa: F401

from processors import fallback_handler  # noqa: F401
from processors import docx_to_text, html_to_text, pdf_to_text  # noqa: F401


def test_fallback_pdf(tmp_path):
    # Create fake PDF file
    pdf_file = tmp_path / "file.pdf"
    pdf_file.write_text("fake pdf content", encoding="utf-8")

    result = fallback_handler.process_with_fallback(str(pdf_file), str(tmp_path))
    assert result is None or os.path.exists(result)


def test_fallback_docx(tmp_path):
    # Create fake DOCX (actually plain text to simulate wrong extension)
    docx_file = tmp_path / "file.docx"
    docx_file.write_text("fake docx content", encoding="utf-8")

    result = fallback_handler.process_with_fallback(str(docx_file), str(tmp_path))
    assert result is None or os.path.exists(result)


def test_fallback_html(tmp_path):
    html_file = tmp_path / "file.html"
    html_file.write_text("<html><body><p>Hello</p></body></html>", encoding="utf-8")

    result = fallback_handler.process_with_fallback(str(html_file), str(tmp_path))
    assert result and os.path.exists(result)


def test_pdf_validate_format():
    """Test that pdf_to_text.validate_format() works correctly."""
    assert pdf_to_text.validate_format("document.pdf") is True
    assert pdf_to_text.validate_format("document.PDF") is True
    assert pdf_to_text.validate_format("document.Pdf") is True
    assert pdf_to_text.validate_format("/path/to/document.pdf") is True
    assert pdf_to_text.validate_format("document.docx") is False
    assert pdf_to_text.validate_format("document.html") is False
    assert pdf_to_text.validate_format("document.txt") is False
    assert pdf_to_text.validate_format("document") is False


def test_docx_validate_format():
    """Test that docx_to_text.validate_format() works correctly."""
    assert docx_to_text.validate_format("document.docx") is True
    assert docx_to_text.validate_format("document.DOCX") is True
    assert docx_to_text.validate_format("/path/to/document.docx") is True
    assert docx_to_text.validate_format("document.pdf") is False
    assert docx_to_text.validate_format("document.html") is False


def test_html_validate_format():
    """Test that html_to_text.validate_format() works correctly."""
    assert html_to_text.validate_format("document.html") is True
    assert html_to_text.validate_format("document.HTML") is True
    assert html_to_text.validate_format("/path/to/document.html") is True
    assert html_to_text.validate_format("document.pdf") is False
    assert html_to_text.validate_format("document.docx") is False
