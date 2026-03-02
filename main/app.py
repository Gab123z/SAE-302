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

    if request.method == "POST":
        keyword = request.form.get("keyword")
        grouped_results, total_matches, total_files = search_in_directory(keyword)

    return render_template(
        "index.html",
        results=grouped_results,
        total_matches=total_matches,
        total_files=total_files
    )


if __name__ == "__main__":
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=True)
