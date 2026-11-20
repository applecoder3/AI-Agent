from pypdf import PdfReader, PdfWriter


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts text from a PDF file to analyze its content."""

    #Creating a PdfReader object to read file
    reader = PdfReader(file_path)

    # List to hold the content of each page
    page_text = []

    # Iterating through each page in the PDF and extracting text
    for page in reader.pages:
        
        content = page.extract_text()

        if content:
            page_text.append(content.strip())

    full_text = "\n\n".join(page_text)

    if not full_text:
        raise ValueError("No text found in the PDF file.")

    return full_text






