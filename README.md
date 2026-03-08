# Communicating Document Search Application

## Project Context

This project was developed as part of the **SAE3.02 – Developing Communicating Applications** course during the **3rd semester of the BUT Networks & Telecommunications program at IUT Béthune**.

The goal of this project is to develop a **Python application capable of searching for specific keywords inside multiple types of documents**.

The application acts as a **local server** that allows a user to enter a keyword through a web interface.
The server then scans several documents stored in a directory and returns information about where the word appears.

---

## Project Objective

The objective of the application is to:

* Search for a keyword inside multiple document formats
* Analyze several files automatically
* Return useful information about the matches

Supported file formats:

* **TXT**
* **HTML**
* **PDF**
* **XLSX (Excel)**

For each match, the program can return:

* the file name
* the line or cell where the word was found
* the text containing the keyword

---

## How the Application Works

1. The user starts the application by running the server.
2. A **Flask web server** starts locally.
3. The user opens the web interface in a browser.
4. The user enters a keyword to search.
5. The server scans all files located in the `data` directory.
6. Depending on the file type, a specific reader is used to extract the text.
7. The program searches for the keyword in the extracted content.
8. The results are sent back to the web page and displayed to the user.

---

## Technologies Used

This project was developed using **Python 3** and several libraries.

Main technologies:

* **Flask** – Web server and user interface
* **Pandas** – Reading Excel files
* **Openpyxl** – Excel engine
* **BeautifulSoup (bs4)** – Parsing HTML files
* **PdfPlumber** – Extracting text from PDF files

Python standard libraries used:

* `os`
* `collections`

---

## Project Structure

```
SAE-302-main
│
├── main
│   ├── app.py
│   ├── readers.py
│   └── seacher.py
│
├── data
│   ├── fichierHTML.html
│   ├── fichierPDF.pdf
│   ├── fichierXLSX.xlsx
│   └── fichiertTXT.txt
│
├── web
│   ├── static
│   │   └── style.css
│   │
│   └── templates
│       └── main.html
│
├── requirement.txt
└── README.md
```

### Description of the files

**main/app.py**

Main entry point of the application.
Starts the Flask server and handles the user requests.

**main/readers.py**

Contains the functions used to read different types of files:

* TXT reader
* HTML reader
* Excel reader
* PDF reader

Each function extracts the text content from a specific format.

**main/seacher.py**

Contains the search logic of the application.

Responsibilities:

* Detect the type of file
* Select the appropriate reader
* Search the keyword in the file content
* Return the matches

**data/**

Directory containing the documents that will be analyzed by the application.

**web/templates/main.html**

HTML interface used by the user to enter a keyword and view results.

**web/static/style.css**

CSS file used to style the web interface.

---

## Installation

First, clone the repository:

```
git clone <repository_url>
cd SAE-302-main
```

Install the required dependencies:

```
pip install -r requirement.txt
```

---

## Running the Application

To start the server, run:

```
python main/app.py
```

The Flask server will start locally.

Then open your browser and go to:

```
http://127.0.0.1:8080
```

Enter a keyword in the search field and start the search.

---

## Example

Example search:

```
keyword: python
```

The program will scan all documents inside the **data** directory and display the files and lines where the word appears.

---

## Possible Improvements

Possible improvements for the project:

* Add support for additional file formats
* Improve the result display
* Allow searching multiple keywords
* Add advanced filtering options
* Improve the user interface

---

## Author

Student project – BUT Networks & Telecommunications
IUT of Béthune
