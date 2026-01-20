______________________________________________________________________

🌍 Project Domains:

- https://GRIMdata.org
- https://LittleRainbowRights.com

______________________________________________________________________

# Processor Test Run Recipe

This guide shows how to test each processor (PDF, DOCX, HTML, fallback, tagger)
independently before running the full pipeline.

______________________________________________________________________

## 1. Test PDF Processor

```bash
echo "This is a test PDF with child and AI mentioned." > sample.txt
pandoc sample.txt -o sample.pdf

python -c "from processors import pdf_to_text; pdf_to_text.convert('sample.pdf', 'out')"
```

**Expected:**

- File `out/sample.txt` created.
- Contains text from the PDF.
- Log entry in `logs/*pdf_to_text.log`.

______________________________________________________________________

## 2. Test DOCX Processor

```bash
echo "This is a test DOCX mentioning youth and privacy." > sample_docx.txt
pandoc sample_docx.txt -o sample.docx

python -c "from processors import docx_to_text; docx_to_text.convert('sample.docx', 'out')"
```

**Expected:**

- File `out/sample.txt` created.
- Contains text from DOCX.
- Log entry in `logs/*docx_to_text.log`.

______________________________________________________________________

## 3. Test HTML Processor

```bash
echo '<html><body><p>This HTML mentions LGBT and data protection.</p></body></html>' > sample.html

python -c "from processors import html_to_text; html_to_text.convert('sample.html', 'out')"
```

**Expected:**

- File `out/sample.txt` created.
- Contains text: “This HTML mentions LGBT and data protection.”
- Log entry in `logs/*html_to_text.log`.

______________________________________________________________________

## 4. Test Fallback Handler

```bash
python -c "from processors import fallback_handler; print(fallback_handler.process_with_fallback('sample.html', 'out'))"
```

**Expected:**

- Prints path to extracted text file.
- Log entries show fallback attempts.

______________________________________________________________________

## 5. Run Tagger on Extracted Text

```bash
python -c "from processors import tagger; text=open('out/sample.txt').read(); print(tagger.apply_tags(text, 'configs/tags_v1.json'))"
```

**Expected:**

- Prints tags like `['ChildRights', 'AI']` or `['LGBTQ', 'Privacy']` depending on sample text.

______________________________________________________________________

## 6. Run Tests

```bash
pytest tests/ -v
```

**Expected:**

- `test_tagger.py`, `test_logging.py`, `test_fallback_handler.py`, and `test_metadata.py` all pass.
