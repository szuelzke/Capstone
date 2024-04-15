from flask import Flask, render_template, request, redirect, url_for, session, flash
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Date, DECIMAL, extract, func, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
import openai
import bcrypt
import pyotp
import secrets
import datetime
from datetime import date, datetime, timedelta
import logging
import time

from models import Base, User, Account, Category, Budget, Transaction, SvcPlan, FlashCash_Transaction, Notification, ShareSpend
from config import app, Session, mail, engine, client, logger
'''
from utility import (
    get_user_id,
    generate_reset_token,
    calculate_expiry_time,
    send_reset_password_email,
    allowed_file,
    update_balance,
    check_balance_and_send_alert
)
'''
#### ------------------------------- Utility Functions --------------------------------------------------------

# Login Utility Functions

def get_user_id(email):
    db_session = Session()
    user = db_session.query(User).filter_by(email=email).first()
    db_session.close()
    return user.user_id if user else None

def generate_reset_token():
    return secrets.token_urlsafe(32)

def calculate_expiry_time():
    expiry_time = datetime.now() + timedelta(hours=1)
    return expiry_time

# reset password email sent to user email
def send_reset_password_email(user_email, reset_token):
    subject = "Reset Your Password"
    sender = "flashfin.alerts@gmail.com"
    recipients = [user_email]
    text_body = f"Hello,\n\nPlease click the following link to reset your password:\n\nReset Password Link: http://capstone1.cs.kent.edu/reset-password/{reset_token}\n\nIf you did not request a password reset, please ignore this email.\n\nBest regards,\nYour FlashFin Team"
    html_body = f"<p>Hello,</p><p>Please click the following link to reset your password:</p><p><a href='http://capstone1.cs.kent.edu/reset-password/{reset_token}'>Reset Password Link</a></p><p>If you did not request a password reset, please ignore this email.</p><p>Best regards,<br>Your FlashFin Team</p>"

    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body

    mail.send(msg)


# Settings Utility Functions

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Accounts Utility Functiosns

# returns dictionary of accounts connected to user
# used in sidebar nav 
@app.template_global()
def get_account_list():
    user_id = session['user_id']
    db_session = Session()
    accounts = db_session.query(Account).filter_by(user_id=user_id).all()
    account_list = {}
    for account in accounts:
        account_list[account.account_id] = {}
        account_list[account.account_id]["name"] = account.account_name
    db_session.close()
    return account_list

# returns dict of stats for all budgets in an account
@app.template_global()
def get_budget_stats(account_id):
    stats = {}
    db_session = Session()
    categories = db_session.query(Budget).filter_by(account_id=account_id).all()
    if categories:
        for category in categories:
            # calculate transactions in budget
            transactions = db_session.query(Transaction).filter_by(category_id=category.category_id).all()
            total = 0
            for transaction in transactions:
                total = total + transaction.amount

            # assignment of dict values
            stats[category.category.category_name] = {}
            stats[category.category.category_name]["count"] = db_session.query(Transaction).filter_by(category_id=category.category_id).count()
            stats[category.category.category_name]["amount"] = category.amount
            stats[category.category.category_name]["activity"] = total
            stats[category.category.category_name]["available"] = category.amount + total
    db_session.close()
    return stats

@app.template_global()
def category_symbols():
    symbol = ["landmark", "cash-register", "utensils", "gas-pump", "star", "house", "paperclip", "car", "heart"]
    return symbol

# returns dict of stats for all accounts made by user
@app.template_global()
def get_account_stats(account_id):
    stats = {} 
    db_session = Session()
    account = db_session.query(Account).filter_by(account_id=account_id).first()
    
    # balance of account
    get_balance = db_session.query(Transaction).filter_by(account_id=account_id).order_by(Transaction.date.desc(), Transaction.transaction_id.desc()).first()
    if get_balance:
        balance = get_balance.amount_remaining
    else: # there are no transactions for account
        balance = "0.00"

    # calculate debit and credit
    debit = 0
    credit = 0
    for transaction in db_session.query(Transaction).filter_by(account_id=account_id).all():
        if transaction.amount > 0:
            debit += transaction.amount
        else:
            credit += transaction.amount
    
    # assignment of dict values
    stats["name"] = account.account_name
    stats["id"] = account_id
    stats["balance"] = balance
    stats["debit"] = debit
    stats["credit"] = credit
    stats["transaction_count"] = db_session.query(Transaction).filter_by(account_id=account_id).count()
    db_session.close()
    return stats

@app.template_global()
def get_transaction_data(account_id):
    transaction_data = []
    db_session = Session()

    # Query transactions for the specified account
    transactions = db_session.query(Transaction).filter_by(account_id=account_id).all()

    # Calculate total balance change over time
    total_balance_change = db_session.query(func.sum(Transaction.amount)).filter_by(account_id=account_id).scalar()

    if transactions:
        for transaction in transactions:
            transaction_data.append({
                'date': transaction.date.strftime('%Y-%m-%d'),  # Assuming date is stored as a datetime object
                'amount': transaction.amount,
                'title': transaction.title,
                'category_id': transaction.category_id,
                'amount_remaining': transaction.amount_remaining
            })

    db_session.close()
    return {
        'transactions': transaction_data,
        'total_balance_change': total_balance_change
    }



# More Transactions Utility Functions

# math for getting current balance after an add/edit
# updates transaction.amount_remaining
def update_balance(account_id):
    db_session = Session()
    transactions = db_session.query(Transaction).filter_by(account_id=account_id).order_by(Transaction.date.asc(), Transaction.transaction_id.asc()).all()
    for i, transaction in enumerate(transactions):
        if i == 0: # starting balance
            transaction.amount_remaining = transaction.amount
        else:
            is_shared = db_session.query(ShareSpend).filter_by(transaction_id=transaction.transaction_id, is_paid=True)
            transaction.amount_remaining = current_amount + transaction.amount
        current_amount = transaction.amount_remaining
    db_session.commit()
    db_session.close()

# math for all transactions amount remaining 
@app.template_global()
def get_category_balance(category_id, budget_id):
    # get month
    current_month = date.today().month
    db_session = Session()
    budget = db_session.query(Budget).filter_by(budget_id=budget_id).first()
    transactions = db_session.query(Transaction).filter(Transaction.category_id == category_id).filter(Transaction.date <= current_month).filter(Transaction.date >= current_month)
    balance = budget.amount
    for transaction in transactions:
        balance = balance + transaction.amount
    db_session.close()
    return balance

# Alerts 

# Function to check balance and send alert/email to user
def check_balance_and_send_alert(account_id):
    user_id = session['user_id']
    db_session = Session()
    user = db_session.query(User).filter_by(user_id=user_id).first()
    try:
        # Query the latest transaction for the account
        latest_transaction = db_session.query(Transaction).filter_by(account_id=account_id).order_by(Transaction.date.desc(), Transaction.transaction_id.desc()).first()
        
        if latest_transaction:
            balance = latest_transaction.amount_remaining
            if balance < 50.00:
                # Create a new notification for low balance
                new_notification = Notification(
                    account_id=account_id, 
                    notification_type="balance",
                    notification_type_id=1,
                    is_opt_in=True,
                    timestamp= datetime.now(),  # Using current timestamp
                    is_read=False
                ) 
                db_session.add(new_notification)
                db_session.commit()

                subject = "Alert: Low Account Balance"
                sender = "flashfin.alerts@gmail.com"
                recipients = [user.email]
                text_body = f"Hello,\n\nAn account in your FlashFin account has a low balance. Balanace is below $50.00.\n\nBest regards,\nYour FlashFin Team"
                html_body = f"<p>Hello,</p><p>An account in your FlashFin account has a low balance. Balanace is below $50.00.</p><p>Best regards,<br>Your FlashFin Team</p>"

                msg = Message(subject, sender=sender, recipients=recipients)
                msg.body = text_body
                msg.html = html_body

                mail.send(msg)

    except Exception as e:
        print("Error while checking balance and sending alert:", e)
        db_session.rollback()  # Rollback the changes if an error occurs
    finally:
        db_session.close()

# Function to get notifications for a specific account
@app.template_global()
def get_notifications(account_id):
    db_session = Session()
    notifications = db_session.query(Notification).filter_by(account_id=account_id).order_by(Notification.timestamp.asc()).all()
    db_session.close()
    
    opted_in_notifications = {}
    for notification in notifications:
        if notification.is_opt_in:
            opted_in_notifications[notification.notification_id] = notification
    
    return opted_in_notifications

@app.template_global()
def get_sharespend_requests():
    user_id = session['user_id']
    db_session = Session()
    ss_requests = db_session.query(ShareSpend).filter_by(receiver_id=user_id).filter_by(is_paid=False).all()
    ss_list = {}
    if ss_requests:
        for request in ss_requests:
            ss_list[request.share_id] = {}
            ss_list[request.share_id]['sender_name'] = request.sender.social_name
            ss_list[request.share_id]['amount_split'] = request.amount_split
        return ss_list
    else:
        return "No requests"


#### ------------------------------- Handling Login System --------------------------------------------------------

# route to home screen, routes to landing page if user not logged in
@app.route('/', methods=['GET','POST'])
def home():
    if 'user_id' in session and session.get('mfa_completed', False):
        user_id = session['user_id']
        db_session = Session()
        user = db_session.query(User).filter_by(user_id=user_id).first()
        if db_session.query(Account).filter_by(user_id=user_id).all(): 
            db_session.close()
            return render_template('index.html', user=user)
        else:
            return redirect(url_for('add_account'))
    else:
        msg = ''
        return render_template('landing.html', msg=msg)

# testing route
@app.route('/test')
def test():
    if 'user_id' in session:
        db_session = Session()
        accounts = db_session.query(Account).count()
        budgets = db_session.query(Budget).count()
        categories = db_session.query(Category).count()
        transactions = db_session.query(Transaction).count()
        sharespend = db_session.query(ShareSpend).count()
        db_session.close()
        return render_template('test.html', accounts=accounts, budgets=budgets, categories=categories, transactions=transactions, sharespend=sharespend)
    else:
        return redirect(url_for('login'))

# Route to login screen
@app.route('/login', methods=['GET', 'POST'])
def login():
    start_time = time.time()  # Performance monitoring - start time
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        logger.info(f"Attempting login for email: {email}")

        db_session = Session()
        user = db_session.query(User).filter_by(email=email).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            session['user_id'] = user.user_id
            session['email'] = user.email
            logger.info(f"User {user.user_id} logged in successfully")

            if user.mfa_key is None:
                otp_secret = pyotp.random_base32() # generate secret setup key
                user.mfa_key = otp_secret # stores user setup key in user model
                db_session.commit()

            db_session.close()  # Close the session after all database operations
            
            end_time = time.time()  # Performance monitoring - end time
            logger.info(f"Login request processed in {end_time - start_time} seconds")
            
            return redirect(url_for('mfa'))
        else:
           db_session.close()
           logger.error("Invalid email or password") # handling for invalid credentials
           return render_template('login.html', error='Invalid email or password')
    
    end_time = time.time()  # Performance monitoring - end time
    logger.info(f"Login request processed in {end_time - start_time} seconds")
    
    return render_template('login.html')

# multi-factor authentication route
@app.route('/mfa', methods=['GET', 'POST'])
def mfa():
    if 'user_id' in session:
        user_id = session['user_id']
        db_session = Session()
        user = db_session.query(User).filter_by(user_id=user_id).first()
        if user:
            mfa_key = user.mfa_key
            if request.method == 'POST':
                otp = request.form['otp']
                if mfa_key and pyotp.TOTP(mfa_key).verify(otp): # verifies OTP 
                    session['mfa_completed'] = True
                    db_session.close()
                    return redirect(url_for('home'))
                else:
                    db_session.close()
                    return render_template('mfa.html', error='Invalid OTP', user=user) # handling for invalid code
            db_session.close()
            return render_template('mfa.html', user=user)
        else:
            db_session.close()
            return redirect(url_for('login'))  # Redirect to login if user not found
    return render_template('login.html')

# signup page route
@app.route('/signup', methods=['GET','POST'])
def signup():
    start_time = time.time()  # Performance monitoring - start ti
    if request.method == 'POST':
       
        # gets data from signup form
        username = request.form['username']
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['password2']

        db_session = Session()
        check_username = db_session.query(User).filter_by(social_name=username).first()
        db_session.close()
        if check_username: # check username is unique
            return render_template('signup.html', error='Username already taken, try something else')
       
        if password != confirm_password: # check passwords match
            return render_template('signup.html', error='Passwords do not match')

       
       # encrypt password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # adds new user to database
        new_user = User(
            social_name=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone,
            email=email,
            password=password_hash,
            created_date = date.today(),
            is_active=True  # Assuming user is active upon signup
        )

        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(new_user)
        session.commit()
        session.close()
        
        end_time = time.time()  # Performance monitoring - end time
        logger.info(f"Signup request processed in {end_time - start_time} seconds")
        return redirect(url_for('login'))
    
    end_time = time.time()  # Performance monitoring - end time
    logger.info(f"Signup request processed in {end_time - start_time} seconds")
    return render_template('signup.html')


# forgot password route
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']

        db_session = Session()
        user = db_session.query(User).filter_by(email=email).first()

        if user:
            # Generate and store reset token
            reset_token = generate_reset_token()
            user.reset_token = reset_token
            user.reset_token_expiry = calculate_expiry_time()


            db_session.commit()
            db_session.close()
            
            # calls utility function to send email
            send_reset_password_email(email, reset_token)

            return redirect(url_for('password_reset_link_sent', email=email))
        else:
            db_session.close()
            return render_template('forgot_password.html', error='Email not found') # error message if email not in system
    return render_template('forgot_password.html')

# Define the route for showing password reset link sent page
@app.route('/password_reset_link_sent')
def password_reset_link_sent():
    email = request.args.get('email')
    return render_template('password_reset_link_sent.html', email=email)

# Define the route for reset password page
@app.route('/reset-password/<reset_token>', methods=['GET', 'POST'])
def reset_password(reset_token):
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        session = Session()
        user = session.query(User).filter_by(reset_token=reset_token).first()

        if user:
            if user.reset_token_expiry and user.reset_token_expiry > datetime.now(): # checks token expired
                if new_password == confirm_password:
                    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

                    user.password = hashed_password
                    user.reset_token = None
                    user.reset_token_expiry = None
                    
                    session.commit()
                    session.close()
                   
                    return render_template('password_reset_success.html')
                else:
                    session.close()
                    return render_template('reset_password.html', error='Passwords Do Not Match')
            else:
                session.close()
                return render_template('reset_password.html', error='Expired Code')
        else:
            session.close()
            return render_template('reset_password.html', error='Invalid Token. Please go back to Reset Password.')
    return render_template('reset_password.html')

# logout route
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # Clear session data
    session.clear()
    return redirect(url_for('login'))




###------------------------------- Handling Settings --------------------------------------------------------


# Function to render settings page
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    start_time = time.time()  # Performance monitoring - start time
    if 'user_id' in session and session.get('mfa_completed', False):
        user_id = session['user_id']
        db_session = Session()
        user = db_session.query(User).filter_by(user_id=user_id).first()
        accounts = db_session.query(Account).filter_by(user_id=user_id).all()
        db_session.close()
        
        end_time = time.time()  # Performance monitoring - end time
        logger.info(f"Settings request processed in {end_time - start_time} seconds")
        return render_template('settings.html', user=user, accounts=accounts)
    else:
        return redirect(url_for('login'))
    
# function for uploading picture - not tested
@app.route('/upload_picture', methods=['POST'])
def upload_picture():
    if 'user_id' in session and session.get('mfa_completed', False):
        
        if 'profile_picture' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['profile_picture']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        user_id = session['user_id']
        db_session = Session()
        user = db_session.query(User).filter_by(user_id=user_id).first()

        # Read the file as bytes and store it in the database
        user.image_link = file.read()
        db_session.commit()
        db_session.close()

        flash('Profile picture uploaded successfully.')
        return redirect(url_for('settings'))
    else:
        return redirect(url_for('login'))  # Redirect to login page if not logged in

# Function to update password
@app.route('/update_password', methods=['POST'])
def update_password():
    if 'user_id' in session and session.get('mfa_completed', False):
        user_id = session['user_id']
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        db_session = Session()
        user = db_session.query(User).filter_by(user_id=user_id).first()

        # Verify current password
        if bcrypt.checkpw(current_password.encode('utf-8'), user.password.encode('utf-8')):
            if new_password == confirm_password:
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                user.password = hashed_password.decode('utf-8')
                db_session.commit()
                db_session.close()
                flash('Password updated successfully.')
            else:
                flash('New passwords do not match.')
        else:
            flash('Incorrect current password.')

        return redirect(url_for('settings'))
    else:
        return redirect(url_for('login'))

# Function to update social name
@app.route('/update_social_name', methods=['POST'])
def update_social_name():
    if 'user_id' in session and session.get('mfa_completed', False):
        user_id = session['user_id']
        social_name = request.form.get('social_name')
        current_password = request.form.get('current_password')

        db_session = Session()
        check_username = db_session.query(User).filter_by(social_name=social_name).first()
        user = db_session.query(User).filter_by(user_id=user_id).first()
        if check_username:
            db_session.close()
            return render_template('settings.html', error='Username already taken, try something else', user=user)

        # Verify current password
        if bcrypt.checkpw(current_password.encode('utf-8'), user.password.encode('utf-8')):
            user.social_name = social_name
            db_session.commit()
            db_session.close()
            flash('Social name updated successfully.')
        else:
            flash('Incorrect current password.')
            
        db_session.close()
        return redirect(url_for('settings'))
    else:
        return redirect(url_for('login'))

# Function to delete account
@app.route('/delete_account/<int:account_id>', methods=['POST'])
def delete_account(account_id):
    if 'user_id' in session and session.get('mfa_completed', False):
        user_id = session['user_id']
        current_password = request.form.get('current_password')

        db_session = Session()
        user = db_session.query(User).filter_by(user_id=user_id).first()
        account = db_session.query(Account).filter_by(account_id=account_id).first()

        if account:
            db_session.query(Notification).filter_by(account_id=account_id).delete()
            # delete budgets and transactions in budget for account
            budgets = db_session.query(Budget).filter_by(account_id=account_id).all()
            for budget in budgets:
                delete_budget(account_id, budget.budget_id)
            # delete uncategorized transactions
            db_session.query(Transaction).filter_by(account_id=account_id).delete()
            db_session.query(Budget).filter_by(account_id=account_id).delete()
            db_session.delete(account)
            db_session.commit()
            db_session.close()
            flash('Account deleted successfully.')
        else:
            db_session.close()
            flash('Account not found.')

        return redirect(url_for('settings'))
    else:
        return redirect(url_for('login'))

# route to edit account popupup
@app.route('/edit_popup/<int:account_id>', methods=['GET'])
def edit_popup(account_id):
    if 'user_id' in session and session.get('mfa_completed', False):
        user_id = session['user_id']
        db_session = Session()
        user = db_session.query(User).filter_by(user_id=user_id).first()
        return render_template('edit_account.html', account_id=account_id, user=user)
    else:
        return redirect(url_for('login'))

# function to update account info
@app.route('/edit_account/<int:account_id>', methods=['POST'])
def edit_account(account_id):
    if 'user_id' in session and session.get('mfa_completed', False):
        user_id = session['user_id']
        new_account_name = request.form.get('new_account_name')
        current_password = request.form.get('current_password')
        db_session = Session()
        user = db_session.query(User).filter_by(user_id=user_id).first()
        # Verify current password
        if bcrypt.checkpw(current_password.encode('utf-8'), user.password.encode('utf-8')):
            account = db_session.query(Account).filter_by(account_id=account_id).first()
            if account:
                account.account_name = new_account_name
                db_session.commit()
                db_session.close()
                flash('Account updated successfully.')
            else:
                db_session.close()
                flash('Account not found.') # error handling
        else:
            db_session.close()
            flash('Incorrect current password.') # error handling
        return redirect(url_for('settings'))
    else:
        return redirect(url_for('login'))

# function to add student id to user account
@app.route('/add-studentid', methods=['GET','POST'])
def add_studentid():
    if 'user_id' in session and session.get('mfa_completed', False):
        user_id = session['user_id']
        db_session = Session()
        user = db_session.query(User).filter_by(user_id=user_id).first()

        if request.method == 'POST':
            student_id = request.form['studentid']

            user.student_id = student_id
            db_session.commit()
            db_session.close()
            return redirect(url_for('settings'))

        db_session.close()
        return render_template('settings.html', user=user)
    else:
        return redirect(url_for('login'))



#### ---------------------------- Handling Accounts ---------------------------------

# function for adding account
@app.route('/add-account', methods=['GET','POST'])
def add_account():
    if 'user_id' in session and session.get('mfa_completed', False):
        user_id = session['user_id']
        db_session = Session()
        user = db_session.query(User).filter_by(user_id=user_id).first()

        if request.method == 'POST':
            ## prevents user from adding more than 5 accounts
            if (db_session.query(Account).filter_by(user_id=user_id).count() >= 5):
                db_session.close()
                return render_template('add_account.html', user=user,
                error="User cannot have more than 5 accounts.")

            account_name = request.form['accountname']

            # adds account to database, tied to current user
            new_account = Account(
                account_name=account_name,
                user_id=session['user_id'],
                is_active=True
            )
            amount = request.form['startbalance']

            # adds starting transaction to database, tied to account  
            start_transaction = Transaction(
                date=datetime.now(),
                amount=amount,
                title="Start Balance",
                amount_remaining=amount
            )
            db_session.add(new_account)
            db_session.add(start_transaction)
            db_session.commit()
            start_transaction.account_id=new_account.account_id
            new_id = new_account.account_id
            db_session.commit()
            db_session.close()
            return redirect(url_for('transactions', account_id=new_id))   
        db_session.close() 
        return render_template('add_account.html', user=user)
    else:
        return redirect(url_for('login'))

# dashboard for account
@app.route('/<account_id>', methods=['GET'])
def account(account_id):
    if 'user_id' in session and session.get('mfa_completed', False):
        user_id = session['user_id']
        db_session = Session()
        user = db_session.query(User).filter_by(user_id=user_id).first()
        account = db_session.query(Account).filter_by(user_id=user_id, account_id=account_id).first()
        # account not found
        if not account:
            db_session.close()
            return redirect(url_for('home'))
        
        # get most recent transactions
        transactions = db_session.query(Transaction).filter_by(account_id=account.account_id).order_by(Transaction.date.desc(), Transaction.transaction_id.desc()).limit(5).all()
        db_session.close()

        return render_template('dashboard.html', user=user, account=account,transactions=transactions)
    else:
        return redirect(url_for('login'))


#### ---------------------------- Handling Transactions ---------------------------------

# view all transactions in account
@app.route('/<account_id>/transactions', methods=['GET'])
def transactions(account_id):
    if 'user_id' in session  and session.get('mfa_completed', False):
        user_id = session['user_id']
        # getting info
        db_session = Session()
        user = db_session.query(User).filter_by(user_id=user_id).first()
        account = db_session.query(Account).filter_by(user_id=user_id, account_id=account_id).first()
        categories = db_session.query(Budget).filter_by(account_id=account_id).all()
        date_cutoff = db_session.query(Transaction).filter_by(account_id=account_id).order_by(Transaction.date.asc()).first().date
        if account:
            # get transactions 
            transactions_list = db_session.query(Transaction).filter_by(account_id=account_id).order_by(Transaction.date.desc(), Transaction.transaction_id.desc()).all()
            db_session.close()
            return render_template('transactions.html',transactions=transactions_list, user=user, account=account, categories=categories, min_date=date_cutoff)
        else:
            return redirect(url_for('add_account'))
    else:
        return redirect(url_for('login'))

# function to filter transactions based on dates
@app.route('/<account_id>/transactions/filter', methods=['GET'])
def filter_transactions(account_id):
    if 'user_id' in session  and session.get('mfa_completed', False):
        user_id = session['user_id']
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        # getting info
        db_session = Session()
        user = db_session.query(User).filter_by(user_id=user_id).first()
        account = db_session.query(Account).filter_by(user_id=user_id, account_id=account_id).first()
        categories = db_session.query(Budget).filter_by(account_id=account_id).all()
        if account:
            # get transactions 
            transactions_list = db_session.query(Transaction).filter(Transaction.account_id==account_id, Transaction.date.between(start_date, end_date)).order_by(Transaction.date.desc()).all()
            return render_template('transactions.html',transactions=transactions_list, user=user, account=account, categories=categories)
        else:
            return redirect(url_for('add_account'))
    else:
        return redirect(url_for('login'))


# add new transaction to account
@app.route('/<account_id>/transactions/add', methods=['POST'])
def addtransaction(account_id):
    if 'user_id' in session and session.get('mfa_completed', False):
        if request.method == 'POST':
            user_id = session['user_id']
            db_session = Session()  
            user = db_session.query(User).filter_by(user_id=user_id).first()
            account = db_session.query(Account).filter_by(user_id=user_id, account_id=account_id).first()
            if account: # add transaction to account
                amount = 0
                if request.form.get('c_or_d') == "credit":
                    amount = float(request.form.get('amount')) * -1.0
                else:
                    amount = float(request.form.get('amount'))

                new_transaction = Transaction(
                    account_id=account.account_id, 
                    date=request.form.get('date'), 
                    amount=amount,
                    title=request.form.get('title'),
                    category_id=request.form.get('category_id')
                ) 
                db_session.add(new_transaction)
                db_session.commit()
                db_session.close()

                # update transaction.amount_remaining
                update_balance(account_id) 

                check_balance_and_send_alert(account_id)

                return redirect(url_for('transactions', account_id=account_id))
            else:
                db_session.close()
                return "Account not found"
    else:
        return redirect(url_for('login'))

# edit existing transaction
@app.route('/<account_id>/<transaction_id>/edit', methods=['POST', 'GET'])
def edittransaction(account_id, transaction_id):
    if 'user_id' in session and session.get('mfa_completed', False):
        user_id = session['user_id']
        db_session = Session()
        user = db_session.query(User).filter_by(user_id=user_id).first()
        account = db_session.query(Account).filter_by(user_id=user_id, account_id=account_id).first()
        transaction = db_session.query(Transaction).filter_by(transaction_id=transaction_id).first()
        categories = db_session.query(Budget).filter_by(account_id=account_id).all()

        if request.method == 'POST':
            new_date = request.form.get('date')
            new_title = request.form.get('title')
            new_amount = request.form.get('amount')
            new_category = request.form.get('category_id')

            transaction.date = new_date
            transaction.title = new_title
            transaction.amount = new_amount
            transaction.category_id = new_category

            db_session.commit()
            db_session.close()
            # update transaction.amount_remaining
            update_balance(account_id) 
            return redirect(url_for('transactions', account_id=account_id))
        else:
            db_session.close()
            return render_template("edit_transaction.html", user=user, account=account, transaction=transaction, categories=categories)
    else:
        return redirect(url_for('login'))

# delete transaction
@app.route('/<account_id>/<transaction_id>/delete', methods=['POST']) 
def deletetransaction(account_id, transaction_id):
    if 'user_id' in session and session.get('mfa_completed', False):
        user_id = session['user_id']
        db_session = Session()
        transaction = db_session.query(Transaction).filter_by(account_id=account_id, transaction_id=transaction_id).first()
        if transaction:
            # checks if transaction is connected to sharespend
            is_shared = db_session.query(ShareSpend).filter_by(transaction_id=transaction.transaction_id).first()
            if is_shared:
                # is the parent transaction
                receiver_transaction = db_session.query(Transaction).filter_by(transaction_id=is_shared.receiver_transaction_id).first()
                if receiver_transaction:
                    db_session.delete(receiver_transaction)
                # is the child transaction
                else:
                    return redirect(url_for('transactions', account_id=account_id))
                db_session.delete(is_shared)
                db_session.commit()
            db_session.delete(transaction)
            db_session.commit()
            db_session.close()
            flash('Transaction deleted successfully.')
        else:
            db_session.close()
            flash('Transaction not found.')
        update_balance(account_id)
        return redirect(url_for('transactions', account_id=account_id))
    else:
        return redirect(url_for('login'))
    
# share transaction 
@app.route('/<account_id>/<transaction_id>/share', methods=['POST', 'GET'])
def sharetransaction(account_id, transaction_id):
    if 'user_id' in session and session.get('mfa_completed', False):
        user_id = session['user_id']
        db_session = Session()
        user = db_session.query(User).filter_by(user_id=user_id).first()
        account = db_session.query(Account).filter_by(user_id=user_id, account_id=account_id).first()
        transaction = db_session.query(Transaction).filter_by(transaction_id=transaction_id).first()

        if request.method == 'GET':
            active_share = db_session.query(ShareSpend).filter(ShareSpend.transaction_id==transaction_id).first()
            if active_share:
                other_social = ""
                if active_share.sender_id == user_id:
                    other_social = active_share.receiver.social_name
                else:
                    other_social = active_share.sender.social_name
                db_session.close()
                return render_template('share_transaction.html', user=user, account=account, transaction=transaction, active_share=active_share, other_social=other_social, msg='This transaction is already shared with another user')
            else:
                return render_template('share_transaction.html', user=user, account=account, transaction=transaction)
        else:
            split_amount = request.form.get("split_amount")
            receiver_name = request.form.get("receiver")

            # find user in database
            receiver_user = db_session.query(User).filter_by(social_name=receiver_name).first()
            # user is found, send request
            if receiver_user:
                if receiver_user.user_id == user_id: # receiver user is sender user
                    return render_template('share_transaction.html', user=user, account=account, transaction=transaction, msg='Cant share transaction with self')
                else:
                    new_sharespend = ShareSpend(
                        transaction_id=transaction_id,
                        sender_id = user.user_id,
                        receiver_id = receiver_user.user_id,
                        amount_split = split_amount,
                        is_paid = False
                    )
                    db_session.add(new_sharespend)
                    db_session.commit()
                    db_session.close()
                    return redirect(url_for('transactions', account_id=account_id))
            
            else: # receiver couldn't be found
                return render_template('share_transaction.html', user=user, account=account, transaction=transaction, msg='User not found')
    else:
        return redirect(url_for('login'))

# routing for accepting share request
@app.route('/<sharespend_id>/accept', methods=['POST'])
def accept_ss_request(sharespend_id):
    if 'user_id' in session and session.get('mfa_completed', False):
        user_id = session['user_id']
        db_session = Session()
        user = db_session.query(User).filter_by(user_id=user_id).first()
        ss_request = db_session.query(ShareSpend).filter_by(share_id=sharespend_id).first()

        account_id = request.form.get("account_id")
        amount_split = float(ss_request.amount_split) * -1.0

        # credit transaction to user that accepts request
        receiver_transaction = Transaction(
            account_id = account_id,
            date = ss_request.init_transaction.date,
            amount = amount_split,
            title = ss_request.init_transaction.title
        )
        # debit transaction to user that sent request
        sender_transaction = Transaction(
            account_id = ss_request.init_transaction.account_id,
            date = ss_request.init_transaction.date,
            amount = ss_request.amount_split,
            title = "Income from " + user.social_name + " for " + ss_request.init_transaction.title
        )

        db_session.add(receiver_transaction)
        db_session.add(sender_transaction)
        db_session.commit()
        ss_request.is_paid = True
        ss_request.receiver_transaction_id = receiver_transaction.transaction_id
        db_session.commit()
        update_balance(ss_request.init_transaction.account_id)
        db_session.close()
        update_balance(account_id)
        return redirect(url_for('account', account_id=account_id))
    else:
        return redirect(url_for('login'))

# route for denying share spend request
@app.route('/<sharespend_id>/deny', methods=['POST'])
def deny_ss_request(sharespend_id):
    if 'user_id' in session and session.get('mfa_completed', False):
        db_session = Session()
        ss_request = db_session.query(ShareSpend).filter_by(share_id=sharespend_id).first()
        db_session.delete(ss_request)
        db_session.commit()
        db_session.close()
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))



#### ---------------------------- Handling Budget ---------------------------------

# route to budget page within an account
@app.route('/<account_id>/budget', methods=['GET'])
def get_budgets(account_id):
    if 'user_id' in session and session.get('mfa_completed', False):
        user_id = session["user_id"]
        db_session = Session()
        ## template variables
        user = db_session.query(User).filter_by(user_id=user_id).first()
        account = db_session.query(Account).filter_by(user_id=user_id, account_id=account_id).first()
        budgets = db_session.query(Budget).filter_by(account_id=account_id).all()

        allocated = 0
        for budget in budgets:
            allocated = allocated + budget.amount

        
        if request.method == "GET":
            db_session.close()
            return render_template('budget.html', user=user, account=account, budgets=budgets, allocated = allocated)
    else:
        return redirect(url_for('login'))

# add budget
@app.route('/<account_id>/budget/add', methods=['POST'])
def add_budget(account_id):
    if 'user_id' in session and session.get('mfa_completed', False):
        db_session = Session()
        new_budget = Budget(
            account_id=account_id,
            amount=request.form.get('amount')
        )
        new_category = Category(
            category_name=request.form.get('title'),
            color=request.form.get('color'),
            symbol=request.form.get('symbol')
        )
        db_session.add(new_budget)
        db_session.add(new_category)
        db_session.commit()
        new_budget.category_id = new_category.category_id
        db_session.commit()
        db_session.close()
        return redirect(url_for('get_budgets', account_id=account_id))
        
# delete budget
@app.route('/<account_id>/budget/<budget_id>/delete', methods=['POST'])
def delete_budget(account_id, budget_id):
    if 'user_id' in session and session.get('mfa_completed', False):
        user_id = session["user_id"]
        db_session = Session()
        ## template variables
        user = db_session.query(User).filter_by(user_id=user_id).first()
        # get query to delete
        budget = db_session.query(Budget).filter_by(budget_id=budget_id).first()
        category = db_session.query(Category).filter_by(category_id=budget.category_id).first()
        if category:
            db_session.query(Transaction).filter_by(category_id=category.category_id).delete()
            db_session.delete(category)
            db_session.delete(budget)
        db_session.commit()
        db_session.close()
        update_balance(account_id)
        return redirect(url_for('get_budgets', account_id=account_id))
    else:
        return redirect(url_for('login'))

# edit budget
@app.route('/<account_id>/budget/<budget_id>/edit', methods=['GET', 'POST'])
def edit_budget(account_id, budget_id):
    if 'user_id' in session and session.get('mfa_completed', False):
        user_id = session["user_id"]
        db_session = Session()
        ## template variables
        user = db_session.query(User).filter_by(user_id=user_id).first()
        account = db_session.query(Account).filter_by(user_id=user_id, account_id=account_id).first()
        # get query to edit
        budget = db_session.query(Budget).filter_by(budget_id=budget_id).first()
        
        if request.method == 'GET':
            db_session.close()
            return render_template('edit_budget.html', user=user, account=account, budget=budget)
        else:
            budget.category.category_name = request.form.get('title')
            budget.category.symbol=request.form.get('symbol')
            budget.amount=request.form.get('amount')
            budget.category.color=request.form.get('color')
            db_session.commit()
            db_session.close()
            return redirect(url_for('get_budgets', account_id=account_id))
    else:
        return redirect(url_for('login'))
    


# ------------------------ Notification System ---------------------------------------

# Get Notifications
@app.route('/notifications', methods=['GET', 'POST'])
def display_notifications():
    if 'user_id' in session and session.get('mfa_completed', False):
        user_id = session["user_id"]
        db_session = Session()
        user = db_session.query(User).filter_by(user_id=user_id).first()
        accounts = db_session.query(Account).filter_by(user_id=user_id).all()
        # Fetch notifications for each account and compile them into a single dictionary
        all_notifications = {}
        for account in accounts:
            notifications = db_session.query(Notification).filter_by(account_id=account.account_id).all()
            if notifications:
                for notification in notifications:
                    all_notifications[notification.notification_id] = {
                        "account": account.account_name,
                        "timestamp": notification.timestamp
                    }
        db_session.close()
        return render_template('notifications.html', user=user, accounts=accounts, all_notifications=all_notifications)
    else:
        return redirect(url_for('login'))



#### ---------------------- Manage FlashCard - FlashCash Balance and Transactions -----------------------------

# route to flashcard screen
@app.route('/<student_id>/flashcash-transactions', methods=['GET','POST'])
def flashcash_transaction(student_id):
    if 'user_id' in session and session.get('mfa_completed', False):
        user_id = session['user_id']
        # Getting user info
        db_session = Session()
        user = db_session.query(User).filter_by(user_id=user_id).first()
        db_session.close()
        if user:
            # Fetching FlashCash transactions
            db_session = Session()
            flashcash_transactions = db_session.query(FlashCash_Transaction, SvcPlan).join(SvcPlan).filter(FlashCash_Transaction.student_id==student_id).order_by(FlashCash_Transaction.transaction_date.desc()).all()
            db_session.close()
            return render_template('flashcash_transactions.html', flashcash_transactions=flashcash_transactions, user=user)
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
    

#### ------------------------------------------- Chatbot -----------------------------------------------------

# route to chatbot
@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if 'user_id' in session and session.get('mfa_completed', False):
        user_id = session['user_id']
        # Retrieve user info
        db_session = Session()
        user = db_session.query(User).filter_by(user_id=user_id).first()
        db_session.close()

        if 'messages' not in session:
            session['messages'] = []

        if request.method == 'POST':
            user_message = request.form['message']
            session['messages'].append({'role': 'user', 'content': user_message})

            # manage history context
            max_conversation_length = 10  # Maintain last 10 interactions
            trimmed_messages = session['messages'][-max_conversation_length:]

            # Construct messages for API, including context for behavior instructions and conversation history
            messages_for_api = [
                {"role": "system", "content": "You are Flashy, adept at breaking down intricate financial concepts into easy-to-understand tips and tricks, sprinkled with engaging anecdotes to keep users hooked. You only answer questions related to financial tips or advice, any questions outside of this scope and you will say that it beyond your scope. You keep your responses within the token limit which is 75 tokens."}
            ] + trimmed_messages

            # OpenAI API call to generate a response
            try:
                completion = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    max_tokens=75,
                    temperature=0.3,
                    messages=messages_for_api
                )
                chatbot_response = completion.choices[0].message.content
                session['messages'].append({'role': 'assistant', 'content': chatbot_response})
            except Exception as e:
                session['messages'].append({'role': 'error', 'content': str(e)})

            session.modified = True

        return render_template('chatbot.html', user=user, messages=session['messages'])
    else:
        return redirect(url_for('login'))

# function to clear chatbot conversations
@app.route('/clear_chat')
def clear_chat():
    session.pop('messages', None)  # Clear the chat history from the session
    return '', 204  # No content to return


    