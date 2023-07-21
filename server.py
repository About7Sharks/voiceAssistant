from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

def query_db():
    conn = sqlite3.connect('transcriptions.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Speech")
    rows = cur.fetchall()
    return rows

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    rows = query_db()
    # Start table
    table = '<table class="w-full">'
    # Header
    table += '<thead class="bg-blue-50"><tr><th class="px-4 py-2 text-left">ID</th><th class="px-4 py-2 text-left">Timestamp</th><th class="px-4 py-2 text-left">Transcription</th></tr></thead><tbody>'
    # Rows
    for row in rows:
        table += f'<tr><td class="border-t px-4 py-2">{row[0]}</td><td class="border-t px-4 py-2">{row[1]}</td><td class="border-t px-4 py-2">{row[2]}</td></tr>'
    # End table
    table += '</tbody></table>'
    return table

if __name__ == '__main__':
    app.run(debug=True)
