import PyPDF2
from io import BytesIO
def extract_rules(file_bytes: bytes) -> str:
    """Reads raw pdf file and extracts all text page by page."""
    pdf = PyPDF2.PdfReader(BytesIO(file_bytes))
    extracted_text = ""
    total_pages = len(pdf.pages)

    print(f"extracting page of  {total_pages} pages")

    for i, page in enumerate(pdf.pages):
        print(f"Reading page {i + 1}/{total_pages}...")
        text = text = page.extract_text() or ""
        extracted_text += page.extract_text() + "\n"
    print("extraction complete")
    return extracted_text