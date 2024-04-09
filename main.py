from flask import Flask, render_template, request, redirect, url_for, session, flash
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Date, DECIMAL, extract
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from flask_mail import Mail, Message
import bcrypt
import pyotp
import qrcode
import base64
import secrets
import datetime
from datetime import date, datetime
import logging
import time

#### ------------------------------- Setup/Classes --------------------------------------------------------

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'flashfin.alerts@gmail.com'
app.config['MAIL_PASSWORD'] = 'x'
app.config['MAIL_DEFAULT_SENDER'] = 'flashfin.alerts@gmail.com'

mail = Mail(app)

engine = create_engine('mysql+mysqlconnector://capstone:CapStone2024@localhost/FLASHFIN?unix_socket=/var/lib/mysql/mysql.sock')

Base = declarative_base()
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    student_id = Column(Integer)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255), unique=True)
    phone_number = Column(String(20))
    password = Column(String(255))  # Store hashed password instead of plain text
    image_link = Column(String(255))
    social_name = Column(String(255))
    created_date = Column(String(255))
    is_active = Column(Boolean)
    reset_token = Column(String(255))
    reset_token_expiry = Column(DateTime)
    mfa_key = Column(String(255))

class Account(Base):
    __tablename__ = 'account'

    account_id = Column(Integer, primary_key=True)
    account_name = Column(String(255))
    user_id = Column(Integer, ForeignKey(User.user_id))
    is_active = Column(Boolean)

class Category(Base):
    __tablename__ = 'category'

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(255))
    symbol = Column(String(50))
    color = Column(String(50))

class Budget(Base):
    __tablename__ = 'budget'

    budget_id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey(Account.account_id))
    category_id = Column(Integer, ForeignKey(Category.category_id))
    amount = Column(DECIMAL(10, 2))
    start_date = Column(Date)
    end_date = Column(Date)

    category = relationship('Category', foreign_keys='Budget.category_id', lazy='joined')

class Transaction(Base):
    __tablename__ = 'transaction'

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey(Account.account_id))
    date = Column(Date)
    amount = Column(DECIMAL(10, 2))
    title = Column(String(255))
    category_id = Column(Integer, ForeignKey(Category.category_id))
    amount_remaining = Column(DECIMAL(10, 2))

    category = relationship('Category', foreign_keys='Transaction.category_id', lazy='joined')

class SvcPlan(Base):
    __tablename__ = 'svc_plan'

    plan_id = Column(Integer, primary_key=True)
    plan_name = Column(String(100))

class FlashCash_Transaction(Base):
    __tablename__ = 'flashcash_transaction'

    fc_transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey(User.student_id))
    plan_id = Column(Integer, ForeignKey(SvcPlan.plan_id))
    transaction_date = Column(Date)
    transaction_amount = Column(DECIMAL(10,2))
    amount_remaining = Column(DECIMAL(10,2))

class Notification(Base):
    __tablename__ = 'notification_system' 
    notification_id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey(Account.account_id))
    notification_type = Column(String(100))
    notification_type_id = Column(Integer)
    is_opt_in = Column(Boolean)
    timestamp = Column(Date)
    is_read = Column(Boolean)







try:
    connection = engine.connect()
    print("Connection successful!")
except Exception as e:
    print("Connection failed:", e)


#### ------------------------------- Utility Functions --------------------------------------------------------

def get_user_id(email):
    db_session = Session()
    user = db_session.query(User).filter_by(email=email).first()
    db_session.close()
    return user.user_id if user else None

def generate_reset_token():
    return secrets.token_urlsafe(32)

def calculate_expiry_time():
    expiry_time = datetime.now() + time.timedelta(hours=1)
    return expiry_time

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

# Handling Settings

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Handling Accounts

# returns dictionary of accounts connected to user
def get_account_list():
    user_id = session['user_id']
    db_session = Session()
    accounts = db_session.query(Account).filter_by(user_id=user_id).all()
    account_list = {}
    for account in accounts:
        recent_transaction = db_session.query(Transaction).filter_by(account_id=account.account_id).order_by(Transaction.date.desc(), Transaction.transaction_id.desc()).first()
        account_list[account.account_id] = {}
        account_list[account.account_id]["name"] = account.account_name
        if recent_transaction:
            account_list[account.account_id]["balance"] = recent_transaction.amount_remaining
        else:
            account_list[account.account_id]["balance"] = "0.00"
    db_session.close()
    return account_list

# get stats for an budget
def get_budget_stats(account_id):
    stats = {}
    db_session = Session()
    categories = db_session.query(Budget).filter_by(account_id=account_id)
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

# get stats for account
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

# Handling Transactions
# math for getting current balance after an add/edit
# updates transaction.amount_remaining
def update_balance(account_id):
    db_session = Session()
    transactions = db_session.query(Transaction).filter_by(account_id=account_id).order_by(Transaction.date.asc(), Transaction.transaction_id.asc()).all()
    for i, transaction in enumerate(transactions):
        if i == 0: # starting balance
            transaction.amount_remaining = transaction.amount
        else:
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
# Function to send email
def send_email(recipient, subject, body):
    msg = Message(subject, recipients=[recipient])
    msg.body = body
    mail.send(msg)

# Function to check balance and send alert
def check_balance_and_send_alert(user_email, balance):
    if balance < 50.00:
        subject = "Alert: Low Balance"
        body = f"Dear User,\n\nYour account balance is below $50.00. Please consider reviewing your finances.\n\nRegards,\nYour Bank"
        send_email(user_email, subject, body)

def get_notifications(account_id):
    db_session = Session()
    notifications = db_session.query(Notification).filter_by(account_id=account_id).order_by(Notification.timestamp.asc()).all()
    db_session.close()
    
    opted_in_notifications = []
    for notification in notifications:
        if notification.is_opt_in:
            opted_in_notifications.append(notification)
    
    if opted_in_notifications:
        return opted_in_notifications
    else:
        return None
#### ------------------------------- Handling Login System --------------------------------------------------------


@app.route('/', methods=['GET','POST'])
def home():
    if 'user_id' in session and session.get('mfa_completed', False):
        user_id = session['user_id']
        db_session = Session()
        user = db_session.query(User).filter_by(user_id=user_id).first()
        accounts = db_session.query(Account).filter_by(user_id=user_id).first()
        account_list = get_account_list()
        notification_list = get_notifications(accounts.account_id)
        db_session.close()
        return render_template('index.html', user=user, account_list=account_list,notification_list=notification_list)
    else:
        msg = ''
        return render_template('landing.html', msg=msg)

@app.route('/test')
def test():
    if 'user_id' in session:
        db_session = Session()
        accounts = db_session.query(Account).count()
        budgets = db_session.query(Budget).count()
        categories = db_session.query(Category).count()
        transactions = db_session.query(Transaction).count()
        db_session.close()
        return render_template('test.html', accounts=accounts, budgets=budgets, categories=categories, transactions=transactions)
    else:
        return redirect(url_for('login'))

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
                user.mfa_key = otp_secret
                db_session.commit()

            db_session.close()  # Close the session after all database operations
            
            end_time = time.time()  # Performance monitoring - end time
            logger.info(f"Login request processed in {end_time - start_time} seconds")
            
            return redirect(url_for('mfa'))
        else:
           db_session.close()
           logger.error("Invalid email or password")
           return render_template('login.html', error='Invalid email or password')
    
    end_time = time.time()  # Performance monitoring - end time
    logger.info(f"Login request processed in {end_time - start_time} seconds")
    
    return render_template('login.html')

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
                if mfa_key and pyotp.TOTP(mfa_key).verify(otp):
                    session['mfa_completed'] = True
                    db_session.close()
                    return redirect(url_for('home'))
                else:
                    db_session.close()
                    return render_template('mfa.html', error='Invalid OTP', user=user)
            db_session.close()
            return render_template('mfa.html', user=user)
        else:
            db_session.close()
            return redirect(url_for('login'))  # Redirect to login if user not found
    return render_template('login.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    start_time = time.time()  # Performance monitoring - start ti
    if request.method == 'POST':
       
        username = request.form['username']
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['password2']

       
        if password != confirm_password:
            return render_template('signup.html', error='Passwords do not match')

       
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        
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
            
            send_reset_password_email(email, reset_token)

            #return render_template('password_reset_link_sent.html', email=email)
            return redirect(url_for('password_reset_link_sent', email=email))
        else:
            db_session.close()
            return render_template('forgot_password.html', error='Email not found')
    return render_template('forgot_password.html')

# Define the route for showing password reset link sent page
@app.route('/password_reset_link_sent')
def password_reset_link_sent():
    email = request.args.get('email')
    return render_template('password_reset_link_sent.html', email=email)

@app.route('/reset-password/<reset_token>', methods=['GET', 'POST'])
def reset_password(reset_token):
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        session = Session()
        user = session.query(User).filter_by(reset_token=reset_token).first()

        if user:
            if user.reset_token_expiry and user.reset_token_expiry > datetime.now():
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
            return render_template('reset_password.html', error='Invalid Token')
    return render_template('reset_password.html')

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
        account_list = get_account_list()
        
        end_time = time.time()  # Performance monitoring - end time
        logger.info(f"Settings request processed in {end_time - start_time} seconds")
        return render_template('settings.html', user=user, accounts=accounts, account_list=account_list)
    else:
        return redirect(url_for('login'))
    

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
        user = db_session.query(User).filter_by(user_id=user_id).first()

        # Verify current password
        if bcrypt.checkpw(current_password.encode('utf-8'), user.password.encode('utf-8')):
            user.social_name = social_name
            db_session.commit()
            db_session.close()
            flash('Social name updated successfully.')
        else:
            flash('Incorrect current password.')

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
            # delete budgets and transactions in budget for account
            budgets = db_session.query(Budget).filter_by(account_id=account_id).all()
            for budget in budgets:
                delete_budget(account_id, budget.budget_id)
            # delete uncategorized transactions
            db_session.query(Transaction).filter_by(account_id=account_id).delete()
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

@app.route('/edit_popup/<int:account_id>', methods=['GET'])
def edit_popup(account_id):
    if 'user_id' in session and session.get('mfa_completed', False):
        return render_template('edit_account.html', account_id=account_id)
    else:
        return redirect(url_for('login'))
    
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
                flash('Account not found.')
        else:
            db_session.close()
            flash('Incorrect current password.')
        return redirect(url_for('settings'))
    else:
        return redirect(url_for('login'))


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

@app.route('/add-account', methods=['GET','POST'])
def add_account():
    if 'user_id' in session and session.get('mfa_completed', False):
        user_id = session['user_id']
        db_session = Session()
        user = db_session.query(User).filter_by(user_id=user_id).first()

        if request.method == 'POST':
            account_name = request.form['accountname']
            new_account = Account(
                account_name=account_name,
                user_id=session['user_id'],
                is_active=True
            )

            amount = request.form['startbalance']
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
            db_session.commit()
            db_session.close()
            return redirect(url_for('home'))   
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
        transactions = db_session.query(Transaction).filter_by(account_id=account.account_id).order_by(Transaction.date.desc(), Transaction.transaction_id.desc()).limit(10).all()
        db_session.close()

        return render_template('dashboard.html', transactions=transactions, user=user, account_list=get_account_list(), budget=get_budget_stats(account_id), account=get_account_stats(account_id))
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
        db_session.close()
        categories = db_session.query(Budget).filter_by(account_id=account_id).all()
        if account:
            # get transactions 
            transactions_list = db_session.query(Transaction).filter_by(account_id=account_id).order_by(Transaction.date.desc(), Transaction.transaction_id.desc()).all()
            db_session.close()
            return render_template('transactions.html',transactions=transactions_list, user=user, account=account, account_list=get_account_list(), categories=categories)
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

# add new transaction to account
@app.route('/<account_id>/transactions/add', methods=['POST'])
def addtransaction(account_id):
    if 'user_id' in session and session.get('mfa_completed', False):
        if request.method == 'POST':
            user_id = session['user_id']
            db_session = Session()  
            account = db_session.query(Account).filter_by(user_id=user_id, account_id=account_id).first()
            if account: # add transaction to account
                new_transaction = Transaction(
                    account_id=account.account_id, 
                    date=request.form.get('date'), 
                    amount=request.form.get('amount'),
                    title=request.form.get('title'),
                    category_id=request.form.get('category_id')
                ) 
                db_session.add(new_transaction)
                db_session.commit()

                # Sending alert if balance is low
                #transactions = db_session.query(Transaction).filter_by(account_id=account_id).order_by(Transaction.date.desc(), Transaction.transaction_id.desc()).first()
                #balance = transactions.amount_remaining
                #user_email = user.email 
                #check_balance_and_send_alert(user_email, balance)
        
                db_session.close()
                # update transaction.amount_remaining
                update_balance(account_id) 
                return redirect(url_for('transactions', account_id=account_id))
            else:
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

#### ---------------------------- Handling Budget ---------------------------------
@app.route('/<account_id>/budget', methods=['GET'])
def get_budgets(account_id):
    if 'user_id' in session and session.get('mfa_completed', False):
        user_id = session["user_id"]
        db_session = Session()
        ## template variables
        user = db_session.query(User).filter_by(user_id=user_id).first()
        account = db_session.query(Account).filter_by(user_id=user_id, account_id=account_id).first()
        budgets = db_session.query(Budget).filter_by(account_id=account_id).all()
        
        if request.method == "GET":
            db_session.close()
            return render_template('budget.html', user=user, account=account, account_list=get_account_list(), budgets=budgets)
    else:
        return redirect(url_for('login'))

# add budget
@app.route('/<account_id>/budget/add', methods=['POST'])
def add_budget(account_id):
    if 'user_id' in session and session.get('mfa_completed', False):
        db_session = Session()
        new_budget = Budget(
            account_id=account_id,
            amount=request.form.get('amount'),
            start_date=request.form.get('start_date'),
            end_date=request.form.get('end_date')
        )
        new_category = Category(
            category_name=request.form.get('title'),
            color=request.form.get('color')
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
            budget.category_id=request.form.get('category_id')
            budget.amount=request.form.get('amount')
            budget.start_date=request.form.get('start_date')
            budget.end_date=request.form.get('end_date')
            db_session.commit()
            db_session.close()
            return redirect(url_for('budget', account_id=account_id))
    else:
        return redirect(url_for('login'))

@app.route('/account/transaction/share', methods=['POST', 'GET'])
def sharetransaction():
    if request.method == 'POST':
        # post share request
        return redirect(url_for('transactions'))
    return render_template('forms/share_transaction.html')

# ------------------------ Notification System ---------------------------------------

#Get Notifications
@app.route('/<account_id>/notifications', methods = ['GET','POST'])
def display_notifications(account_id):
    if 'user_id' in session and session.get('mfa_completed', False):
        user_id = session["user_id"]
        db_session = Session()
        user = db_session.query(User).filter_by(user_id=user_id).first()
        account = db_session.query(Account).filter_by(user_id=user_id, account_id=account_id).first()
        return render_template('notifications.html', user=user, account=account, account_list = get_account_list(), notifications=get_notifications(account.account_id))



#### ---------------------- Manage FlashCard - FlashCash Balance and Transactions -----------------------------

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
            return render_template('flashcash_transactions.html', flashcash_transactions=flashcash_transactions, user=user, account_list=get_account_list())
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))