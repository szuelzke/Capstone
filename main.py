from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import create_engine

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

engine = create_engine('mysql+mysqldb://capstone:CapStone2024@localhost/FLASHFIN?unix_socket=/var/lib/mysql/mysql.sock')

# Test the connection
try:
    connection = engine.connect()
    print("Connection successful!")
except Exception as e:
    print("Connection failed:", e)

@app.route('/')
def home():
    msg = ''
    return render_template('index.html', msg=msg)

