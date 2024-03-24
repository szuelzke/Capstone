from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

cnx = mysql.connector.connect(user='capstone', password='CapStone2024',
                              host='localhost',
                              database='FLASHFIN')
cnx.close()

@app.route('/')
def home():
    msg = ''
    return render_template('index.html', msg=msg)

