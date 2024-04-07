import main


def get_user_id(email):
    db_session = main.Session()
    user = db_session.query(main.User).filter_by(email=email).first()
    db_session.close()
    return user.user_id if user else None

def generate_reset_token():
    return main.secrets.token_urlsafe(32)

def calculate_expiry_time():
    expiry_time = main.datetime.now() + main.time.timedelta(hours=1)
    return expiry_time

def send_reset_password_email(user_email, reset_token):
    subject = "Reset Your Password"
    sender = "flashfin.alerts@gmail.com"
    recipients = [user_email]
    text_body = f"Hello,\n\nPlease click the following link to reset your password:\n\nReset Password Link: http://capstone1.cs.kent.edu/reset-password/{reset_token}\n\nIf you did not request a password reset, please ignore this email.\n\nBest regards,\nYour FlashFin Team"
    html_body = f"<p>Hello,</p><p>Please click the following link to reset your password:</p><p><a href='http://capstone1.cs.kent.edu/reset-password/{reset_token}'>Reset Password Link</a></p><p>If you did not request a password reset, please ignore this email.</p><p>Best regards,<br>Your FlashFin Team</p>"

    msg = main.Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body

    main.mail.send(msg)

#### ------------------ Handling Settings --------------------------------------

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#### ------------------- Handling Accounts --------------------

# returns dictionary of accounts connected to user
def get_account_list():
    user_id = main.session['user_id']
    db_session = main.Session()
    accounts = db_session.query(main.Account).filter_by(user_id=user_id).all()
    account_list = {}
    for account in accounts:
        recent_transaction = db_session.query(main.Transaction).filter_by(account_id=account.account_id).order_by(main.Transaction.date.desc()).first()
        account_list[account.account_id] = {}
        account_list[account.account_id]["name"] = account.account_name
        if recent_transaction:
            account_list[account.account_id]["balance"] = recent_transaction.amount_remaining
        else:
            account_list[account.account_id]["balance"] = "0.00"
    db_session.close()
    return account_list

#### ------------------ Alerts -----------------------------
'''
# Function to send SMS
def send_sms(to, body):
    message = client.messages.create(
        body=body,
        from_=twilio_phone_number,
        to=to
    )
    print("SMS sent to", to)

# Function to check balance and send alert
def check_balance_and_send_alert(user_phone, balance):
    if balance < 50.00:
        message = f"FlashFin: Your balance is ${balance:.2f}. "
        send_sms(user_phone, message)
'''