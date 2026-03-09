"""Flask web application for document search."""

from flask import Flask, render_template, request
from seacher import search_in_directory

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8080

app = Flask(
    __name__,
    template_folder="../web/templates",
    static_folder="../web/static"
)


@app.route("/", methods=["GET", "POST"])
def index():
    grouped_results = {}
    total_matches = 0
    total_files = 0
    keyword = ""

    if request.method == "POST":
        keyword = request.form.get("keyword", "").strip()

        if keyword:
            grouped_results, total_matches, total_files = search_in_directory(keyword)

    results = []

    for filename, matches in grouped_results.items():
        formatted_matches = []

        for match in matches:
            if "column" in match:
                where = f"Line {match['line']}, column {match['column']}"
            else:
                where = f"Line {match['line']}"

            formatted_matches.append({
                "where": where,
                "snippet": match["content"]
            })

        results.append({
            "file": filename,
            "matches": formatted_matches
        })

    return render_template(
        "index.html",
        keyword=keyword,
        results=results,
        total_matches=total_matches,
        scanned_files=total_files
    )


if __name__ == "__main__":
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=True)
