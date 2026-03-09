import pandas as pd
import pdfplumber
from bs4 import BeautifulSoup, Comment


def read_txt_file(file_path):
    """Return a list of lines from a TXT file."""
    # Open the text file with UTF-8 encoding and ignore decoding errors
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        # Read all lines and return them as a list
        return file.readlines()


def read_html_file(file_path):
    """
    Extract visible text from an HTML file and return it as a list of clean lines.
    """
    # Parse the HTML file using BeautifulSoup
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Remove tags that do not contain useful visible text
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # Remove HTML comments
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    # Extract all visible text and separate it by lines
    text = soup.get_text(separator="\n")

    # Clean lines by stripping spaces and removing empty lines
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    return lines


def read_excel_file(file_path):
    """Return structured data from an Excel file as a list of dictionaries."""
    # Read all sheets from the Excel file
    sheets = pd.read_excel(file_path, sheet_name=None, engine="openpyxl")
    data = []

    # Iterate through each sheet and its dataframe
    for sheet_name, dataframe in sheets.items():
        for row_index, row in dataframe.iterrows():
            # Iterate through each cell in the row
            for col_index, cell in enumerate(row):
                # Ignore empty cells
                if pd.notna(cell):
                    # Store row, column and content information
                    data.append({
                        "row": row_index + 2,
                        "column": col_index + 1,
                        "content": str(cell)
                    })

    return data


def read_pdf_file(file_path):
    """Return a list of text lines extracted from a PDF file."""
    lines = []

    # Open the PDF file using pdfplumber
    with pdfplumber.open(file_path) as pdf:
        # Iterate through each page of the PDF
        for page in pdf.pages:
            text = page.extract_text()

            # If text exists on the page, split it into lines
            if text:
                lines.extend(text.splitlines())

    return lines
