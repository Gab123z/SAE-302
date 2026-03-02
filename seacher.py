"""Search engine module for searching keywords in various file types."""

import os
from collections import defaultdict
from readers import (
    read_txt_file,
    read_html_file,
    read_excel_file,
    read_pdf_file
)

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_PATH)
PATH_DOCUMENTS = os.path.join(PROJECT_ROOT, "data")


# Map file extensions to their respective reader functions
SUPPORTED_READERS = {
    ".txt": read_txt_file,
    ".html": read_html_file,
    ".xlsx": read_excel_file,
    ".pdf": read_pdf_file,
}


def get_reader(file_path):
    """
    Return the reader function based on the file extension.
    Returns None if the file type is not supported.
    """
    _, ext = os.path.splitext(file_path)
    return SUPPORTED_READERS.get(ext.lower())


def search_in_file(file_path, keyword):
    """Search for a keyword inside a single file."""
    reader = get_reader(file_path)
    filename = os.path.basename(file_path)

    # Skip unsupported file types
    if not reader:
        return filename, []

    # Try reading the file
    try:
        data = reader(file_path)
    except Exception:
        return filename, []

    matches = []
    keyword = keyword.lower()

    # Excel files
    if file_path.endswith(".xlsx"):
        for cell in data:
            if keyword in cell["content"].lower():
                matches.append({
                    "line": cell["row"],
                    "column": cell["column"],
                    "content": cell["content"]
                })
        return filename, matches

    # TXT, HTML, PDF
    for line_number, line in enumerate(data, start=1):
        if keyword in line.lower():
            matches.append({
                "line": line_number,
                "content": line.strip(),
            })

    return filename, matches


def search_in_directory(keyword):
    """
    Search for a keyword in all supported files within the documents directory.
    
    Returns:
        grouped_results (dict): mapping filename -> list of matches
        total_matches (int): total number of keyword occurrences
        total_files (int): number of files containing the keyword
    """
    if not keyword.strip():
        return {}, 0, 0

    grouped_results = defaultdict(list)
    total_matches = 0

    # Walk through all files in the documents directory
    for root, _, files in os.walk(PATH_DOCUMENTS):
        for file in files:
            file_path = os.path.join(root, file)
            filename, matches = search_in_file(file_path, keyword)

            if matches:
                grouped_results[filename].extend(matches)
                total_matches += len(matches)

    total_files = len(grouped_results)

    return grouped_results, total_matches, total_files