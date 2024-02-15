from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/home/')
def home():
    msg = ''
    return render_template('index.html', msg=msg)

app.run(host='localhost', port=5003)