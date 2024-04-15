from sqlalchemy.orm import Session
from flask_mail import Mail, Message
from flask import session
from models import User, Notification, ShareSpend
from config import app, Session as DBSession, mail
import secrets
import datetime
from datetime import date, datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Date, DECIMAL, extract, func, or_


from models import Base, User, Account, Category, Budget, Transaction, SvcPlan, FlashCash_Transaction, Notification, ShareSpend


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