from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/')
def home():
    msg = ' '
    return render_template('index.html', msg=msg)

if __name__ == "__main__":
    app.run(debug=True)