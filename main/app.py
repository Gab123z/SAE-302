"""Flask web application for document search."""

from flask import Flask, render_template, request
from seacher import search_in_directory

# Server configuration (local host and port)
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8080

# Create the Flask application
# Specify where templates and static files are located
app = Flask(
    __name__,
    template_folder="../web/templates",
    static_folder="../web/static"
)


# Main route of the application
# Handles both page display (GET) and form submission (POST)
@app.route("/", methods=["GET", "POST"])
def index():
    # Variables used to store search results and stats
    grouped_results = {}
    total_matches = 0
    total_files = 0
    keyword = ""

    # If the user submitted the search form
    if request.method == "POST":
        # Get the keyword from the form and remove extra spaces
        keyword = request.form.get("keyword", "").strip()

        # Run the search if a keyword is provided
        if keyword:
            grouped_results, total_matches, total_files = search_in_directory(keyword)

    results = []

    # Convert grouped results into a format easier for the template
    for filename, matches in grouped_results.items():
        formatted_matches = []

        # Process each match found in the file
        for match in matches:
            # Build the location string (line and optional column)
            if "column" in match:
                where = f"Line {match['line']}, column {match['column']}"
            else:
                where = f"Line {match['line']}"

            # Store formatted match data
            formatted_matches.append({
                "where": where,
                "snippet": match["content"]
            })

        # Add file results to the final list
        results.append({
            "file": filename,
            "matches": formatted_matches
        })

    # Render the HTML template and pass search data to it
    return render_template(
        "index.html",
        keyword=keyword,
        results=results,
        total_matches=total_matches,
        scanned_files=total_files
    )


# Start the Flask development server if the script is run directly
if __name__ == "__main__":
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=True)
