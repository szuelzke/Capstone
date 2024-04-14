from datetime import datetime, timedelta
from flask_mail import Message
import secrets
from main import session, Session, mail  # Importing Session and mail from main
from models import User,Transaction, ShareSpend, Notification

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
