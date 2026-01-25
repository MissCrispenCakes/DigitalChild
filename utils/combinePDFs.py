"""
Combine PDFs Utility
--------------------
Merges multiple PDF files into a single PDF.

Example usage:
```bash
python utils/combinePDFs.py combined.pdf data/raw/au_policy/AU_AI_Strategy_2024.pdf data/raw/au_policy/AU_Digital_Compact.pdf
```
"""

import sys

from pypdf import PdfMerger


def combine_pdfs(pdf_list, output_path="combined.pdf"):
    merger = PdfMerger()
    for pdf in pdf_list:
        try:
            merger.append(pdf)
            print(f"Added {pdf}")
        except Exception as e:
            print(f"Error adding {pdf}: {e}")
    merger.write(output_path)
    merger.close()
    print(f"✅ Combined PDF written to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python utils/combinePDFs.py output.pdf input1.pdf input2.pdf ...")
    else:
        output = sys.argv[1]
        inputs = sys.argv[2:]
        combine_pdfs(inputs, output)
