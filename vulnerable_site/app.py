from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)

# Simple in-memory database setup for demo purposes
DATABASE = 'example.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vulnerabilities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT
            )
        ''')
        conn.commit()

@app.route('/')
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Vulnerable Website</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }
                .container {
                    width: 80%;
                    margin: auto;
                    overflow: hidden;
                }
                header {
                    background: #333;
                    color: #fff;
                    padding-top: 30px;
                    min-height: 70px;
                    border-bottom: #fff 3px solid;
                    text-align: center;
                }
                header h1 {
                    margin: 0;
                }
                .form-group {
                    margin: 20px 0;
                }
                .form-group input[type="file"],
                .form-group input[type="text"] {
                    width: calc(100% - 22px);
                    padding: 10px;
                    margin: 5px 0;
                }
                .form-group input[type="submit"] {
                    width: 100%;
                    padding: 10px;
                    background: #333;
                    color: #fff;
                    border: none;
                    cursor: pointer;
                }
                .form-group input[type="submit"]:hover {
                    background: #555;
                }
                .results {
                    margin-top: 20px;
                    padding: 20px;
                    background: #fff;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                }
            </style>
        </head>
        <body>
            <header>
                <h1>Vulnerable Website</h1>
            </header>
            <div class="container">
                <div class="form-group">
                    <h2>Upload File</h2>
                    <form action="/upload" method="post" enctype="multipart/form-data">
                        <input type="file" name="file">
                        <input type="submit" value="Upload">
                    </form>
                </div>
                <div class="form-group">
                    <h2>Search Vulnerabilities</h2>
                    <form action="/search" method="get">
                        <input type="text" name="query" placeholder="Enter search query">
                        <input type="submit" value="Search">
                    </form>
                </div>
                <div class="form-group">
                    <h2>Submit Input</h2>
                    <form action="/xss" method="post">
                        <input type="text" name="input" placeholder="Enter your input">
                        <input type="submit" value="Submit">
                    </form>
                </div>
                {% if results %}
                <div class="results">
                    <h2>Results:</h2>
                    <pre>{{ results }}</pre>
                </div>
                {% endif %}
            </div>
        </body>
        </html>
    ''')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    file.save(os.path.join('/tmp', file.filename))
    return 'File uploaded successfully'

@app.route('/search')
def search():
    query = request.args.get('query')
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM vulnerabilities WHERE description LIKE '%{query}%'")
        results = cursor.fetchall()
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Search Results</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }
                .container {
                    width: 80%;
                    margin: auto;
                    overflow: hidden;
                }
                header {
                    background: #333;
                    color: #fff;
                    padding-top: 30px;
                    min-height: 70px;
                    border-bottom: #fff 3px solid;
                    text-align: center;
                }
                header h1 {
                    margin: 0;
                }
                .results {
                    margin-top: 20px;
                    padding: 20px;
                    background: #fff;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                }
                .results pre {
                    margin: 0;
                    white-space: pre-wrap;
                }
            </style>
        </head>
        <body>
            <header>
                <h1>Search Results</h1>
            </header>
            <div class="container">
                <div class="results">
                    <h2>Results:</h2>
                    <pre>{{ results }}</pre>
                </div>
                <a href="/">Back to home</a>
            </div>
        </body>
        </html>
    ''', results=results)

@app.route('/xss', methods=['POST'])
def xss():
    user_input = request.form['input']
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>XSS Result</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }
                .container {
                    width: 80%;
                    margin: auto;
                    overflow: hidden;
                }
                header {
                    background: #333;
                    color: #fff;
                    padding-top: 30px;
                    min-height: 70px;
                    border-bottom: #fff 3px solid;
                    text-align: center;
                }
                header h1 {
                    margin: 0;
                }
                .results {
                    margin-top: 20px;
                    padding: 20px;
                    background: #fff;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                }
            </style>
        </head>
        <body>
            <header>
                <h1>XSS Result</h1>
            </header>
            <div class="container">
                <div class="results">
                    <h2>Submitted Input:</h2>
                    <p>{{ user_input }}</p>
                </div>
                <a href="/">Back to home</a>
            </div>
        </body>
        </html>
    ''', user_input=user_input)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
