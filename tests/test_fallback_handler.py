import os
import tempfile
from processors import fallback_handler, pdf_to_text, docx_to_text, html_to_text

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
