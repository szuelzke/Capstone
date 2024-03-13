from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/home/')
def home():
    msg = ''
    return render_template('index.html', msg=msg)

def login():
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

        # Connect to SQLite database
        conn = sqlite3.connect('user_database.db')
        cursor = conn.cursor()

        # Hash the password to match with the hashed one stored in the database
        hashed_password = hash_password(password)

        # Check if account exists using SQLite
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hashed_password,))
        account = cursor.fetchone()

        # If account exists in users table in our database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account[0]  # Assuming id is the first column in your users table
            session['username'] = account[1]  # Assuming username is the second column in your users table

            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesn't exist or username/password incorrect
            msg = 'Incorrect username/password!'

        # Close database connection
        cursor.close()
        conn.close()

    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)

app.run(host='localhost', port=5003)