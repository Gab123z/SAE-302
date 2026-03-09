"""Search engine module for searching keywords in various file types."""

import os
from collections import defaultdict
from readers import (
    read_txt_file,
    read_html_file,
    read_excel_file,
    read_pdf_file
)

# Determine project paths
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_PATH)

# Directory containing the documents to search in
PATH_DOCUMENTS = os.path.join(PROJECT_ROOT, "data")


# Map file extensions to their corresponding reader functions
SUPPORTED_READERS = {
    ".txt": read_txt_file,
    ".html": read_html_file,
    ".htm": read_html_file,
    ".xlsx": read_excel_file,
    ".pdf": read_pdf_file,
}


def get_reader(file_path):
    """
    Return the reader function based on the file extension.
    Returns None if the file type is not supported.
    """
    # Extract file extension
    _, ext = os.path.splitext(file_path)

    # Return the appropriate reader from the dictionary
    return SUPPORTED_READERS.get(ext.lower())


def search_in_file(file_path, keyword):
    """Search for a keyword inside a single file."""
    # Get the appropriate reader for the file type
    reader = get_reader(file_path)

    # Extract filename from the full path
    filename = os.path.basename(file_path)

    # If the file type is not supported, return no results
    if not reader:
        return filename, []

    # Try reading the file content
    try:
        data = reader(file_path)
    except Exception:
        return filename, []

    matches = []
    keyword = keyword.lower()

    # Special case for Excel files (structured data)
    if file_path.lower().endswith(".xlsx"):
        for cell in data:
            if keyword in cell["content"].lower():
                matches.append({
                    "line": cell["row"],
                    "column": cell["column"],
                    "content": cell["content"]
                })
        return filename, matches

    # Standard text-based search for other file types
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

    # Ignore empty keywords
    if not keyword or not keyword.strip():
        return {}, 0, 0

    grouped_results = defaultdict(list)
    total_matches = 0

    # Walk through all files in the documents directory
    for root, _, files in os.walk(PATH_DOCUMENTS):
        for file in files:
            file_path = os.path.join(root, file)

            # Search keyword inside the file
            filename, matches = search_in_file(file_path, keyword)

            # Store results if matches were found
            if matches:
                grouped_results[filename].extend(matches)
                total_matches += len(matches)

    # Count how many files contain at least one match
    total_files = len(grouped_results)

    return dict(grouped_results), total_matches, total_files
