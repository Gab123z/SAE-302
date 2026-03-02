import os
import pandas as pd
import pdfplumber
from bs4 import BeautifulSoup

def read_txt_file(file_path):
    """Return a list of lines from a TXT file."""
    # Open the text file and read all lines
    with open(file_path, "r", encoding="utf-8") as file:
        return file.readlines()


def read_html_file(file_path):
    """
    Extract visible text from an HTML file and return it as a list of clean lines.
    """
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Remove non-visible text (css and js)
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # Remove comments
    for comment in soup.find_all(string=lambda text: isinstance(text, type(soup.Comment))):
        comment.extract()

    # Get all visible text separated by newlines
    text = soup.get_text(separator="\n")

    # Clean lines and remove empty ones
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    return lines


def read_excel_file(file_path):
    """Return structured data from an Excel file as a list of dictionaries."""
    # Read all sheets
    sheets = pd.read_excel(file_path, sheet_name=None, engine="openpyxl")
    data = []

    for sheet_name, dataframe in sheets.items():
        for row_index, row in dataframe.iterrows():
            for col_index, cell in enumerate(row):
                if pd.notna(cell):
                    # Put row + column + content in a data variable
                    data.append({
                        "row": row_index + 2,
                        "column": col_index + 1,
                        "content": str(cell)
                    })

    return data


def read_pdf_file(file_path):
    """Return a list of text lines extracted from a PDF file."""
    lines = []

    # Open PDF and extract text page by page
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                # Keep real lines using splitlines for better lines readings
                lines.extend(text.splitlines())

    return lines