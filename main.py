from flask import Flask, render_template, request, redirect, url_for, session, flash
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Date, DECIMAL, extract
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_mail import Mail, Message
import bcrypt
import pyotp
import qrcode
import base64
import secrets
import datetime
from datetime import date, datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_password'

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

class Transaction(Base):
    __tablename__ = 'transaction'

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey(Account.account_id))
    date = Column(Date)
    amount = Column(DECIMAL(10, 2))
    title = Column(String(255))
    category_id = Column(Integer, ForeignKey(Category.category_id))
    amount_remaining = Column(DECIMAL(10, 2))





try:
    connection = engine.connect()
    print("Connection successful!")
except Exception as e:
    print("Connection failed:", e)

#### Handling Login System 

@app.route('/', methods=['GET','POST'])
def home():
    if 'user_id' in session and session.get('mfa_completed', False):
        user_id = session['user_id']
        db_session = Session()
        user = db_session.query(User).filter_by(user_id=user_id).first()
        account = db_session.query(Account).filter_by(user_id=user_id)
        db_session.close()
        return render_template('index.html', user=user, account=account)
    else:
        msg = ''
        return render_template('landing.html', msg=msg)

@app.route('/test')
def test():
    if 'user_id' in session:
        return render_template('test.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db_session = Session()
        user = db_session.query(User).filter_by(email=email).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            session['user_id'] = user.user_id
            session['email'] = user.email

            if user.mfa_key is None:
                otp_secret = pyotp.random_base32() # generate secret setup key
                user.mfa_key = otp_secret
                db_session.commit()

            db_session.close()  # Close the session after all database operations
            return redirect(url_for('mfa'))
        else:
           db_session.close()
           return render_template('login.html', error='Invalid email or password')
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

def get_user_id(email):
    db_session = Session()
    user = db_session.query(User).filter_by(email=email).first()
    db_session.close()
    return user.user_id if user else None


@app.route('/signup', methods=['GET','POST'])
def signup():
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
        
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # Clear session data
    session.clear()
    return redirect(url_for('login'))

### Handling Settings

'''
@app.route('/settings', methods=['GET','POST'])
def settings():
    if 'user_id' in session  and session.get('mfa_completed', False):
        user_id = session['user_id']
        db_session = Session()
        user = db_session.query(User).filter_by(user_id=user_id).first()
        account = db_session.query(Account).filter_by(user_id=user_id).first()
        
        if request.method == 'POST':
            new_email = request.form.get('email')
            if new_email:
                user.email = new_email
            
            new_account_name = request.form.get('account_name')
            if new_account_name:
                account.account_name = new_account_name
            
            new_first_name = request.form.get('first_name')
            if new_first_name:
                user.first_name = new_first_name

            new_last_name = request.form.get('last_name')
            if new_last_name:
                user.last_name = new_last_name
            
            new_student_id = request.form.get('student_id')
            if new_student_id:
                user.student_id = new_student_id

            new_phone_number = request.form.get('phone_number')
            if new_phone_number:
                user.phone_number = new_phone_number
            
            new_image_link = request.form.get('image_link')
            if new_image_link:
                user.image_link = new_image_link
            
            new_social_name = request.form.get('social_name')
            if new_social_name:
                user.social_name = new_social_name
            
            new_password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            if new_password and confirm_password and new_password == confirm_password:
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                user.password = hashed_password
            else:
                flash('Passwords do not match.')
                db_session.close()
                return render_template('settings.html', user=user, account=account)
            
            db_session.commit()
            db_session.close()
        return render_template('settings.html', user=user, account=account)
    else:
        return redirect(url_for('login'))
'''
# Function to render settings page
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'user_id' in session and session.get('mfa_completed', False):
        user_id = session['user_id']
        db_session = Session()
        user = db_session.query(User).filter_by(user_id=user_id).first()
        account = db_session.query(Account).filter_by(user_id=user_id).all()
        db_session.close()
        
        return render_template('settings.html', user=user, account=account)
    else:
        return redirect(url_for('login'))
    

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    
##### Handling Accounts
'''
@app.route('/account')
def account():
    if 'user_id' in session and session.get('mfa_completed', False):
        user_id = session['user_id']
        db_session = Session()

        # Query the user from the database
        user = db_session.query(User).filter_by(user_id=user_id).first()

        if user:
            # If user exists, query the accounts associated with the user
            accounts = db_session.query(Account).filter_by(user_id=user_id).all()
            current_month = datetime.now().month

            # Query transactions for the current month associated with the user's accounts
            transactions = db_session.query(Transaction).filter(
                extract('month', Transaction.date) == current_month,
                Transaction.account_id.in_([account.account_id for account in accounts])
            ).all()

            db_session.close()
            return render_template('dashboard.html', user=user, accounts=accounts, transactions=transactions)
        else:
            db_session.close()
            return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

'''
@app.route('/account', methods=['GET', 'POST'])
def account():
    if 'user_id' in session and session.get('mfa_completed', False):
        user_id = session['user_id']
        db_session = Session()
        
        account = db_session.query(Account).filter_by(user_id=user_id).first()

        if not account:
            db_session.close()
            return redirect(url_for('home'))

        transactions = db_session.query(Transaction).filter_by(account_id=account.account_id).order_by(Transaction.date.desc()).limit(10).all()

        db_session.close()
        return render_template('dashboard.html', account=account, transactions=transactions)
    else:
        return redirect(url_for('login'))

        
@app.route('/add-account', methods=['GET','POST'])
def add_account():
    if 'user_id' in session and session.get('mfa_completed', False):
        user_id = session['user_id']
        db_session = Session()
        user = db_session.query(User).filter_by(user_id=user_id).first()
        db_session.close()

        if request.method == 'POST':
            account_name = request.form['accountname']
            new_account = Account(
                account_name=account_name,
                user_id=session['user_id'],
                is_active=True
            )

            db_session_add = Session()
            db_session_add.add(new_account)
            db_session_add.commit()
            db_session_add.close()
            return redirect(url_for('home'))
            
        return render_template('add_account.html', user=user)
    else:
        return redirect(url_for('login'))


@app.route('/account/transaction', methods=['GET'])
def transactions():
    if 'user_id' in session  and session.get('mfa_completed', False):
        user_id = session['user_id']
        account = Account.query.filter_by(user_id=user_id).first()

        if account:
            account_id = account.account_id
            transactions = Transaction.query.filter_by(account_id=account_id).all()
            return render_template('account/transactions.html',transactions=transactions)
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/account/transaction/add', methods=['POST', 'GET'])
def addtransaction():
    if 'user_id' in session  and session.get('mfa_completed', False):
        if request.method == 'POST':
            user_id = session['user_id']
            date = request.form['date']
            amount = request.form['amount']
            title = request.form['title']
            category_id = request.form['category_id']
            db_session = Session()  
            account = db_session.query(Account).filter_by(user_id=user_id).first()
            db_session.close()
            if account:
                new_transaction = Transaction(account_id=account.account_id, date=date, amount=amount,title=title, category_id=category_id)
                db_session = Session() 
                db_session.add(new_transaction)
                db_session.commit()
                db_session.close()
                return redirect(url_for('transactions'))
            else:
                return "Account not found"
        return render_template('forms/add_transaction.html')
    else:
        return redirect(url_for('login'))

@app.route('/account/transaction/edit/<int:transaction_id>', methods=['POST', 'GET'])
def edittransaction(transaction_id):
    if 'user_id' in session  and session.get('mfa_completed', False):
        user_id = session['user_id']
        db_session = Session()
        transaction = db_session.query(Transaction).filter_by(transaction_id=transaction_id).first()
        
        if not transaction:
            flash('Transaction not found')
            db_session.close()
            return redirect(url_for('transactions'))
            
        if transaction.account.user_id != user_id:
            flash('You do not have permission to edit this transaction')
            db_session.close()
            return redirect(url_for('transactions'))
            
        if request.method == 'POST':
            new_date = request.form.get('date')
            if new_date:
                transaction.date = new_date
            
            new_amount = request.form.get('amount')
            if new_amount:
                transaction.amount = new_amount
            
            new_title = request.form.get('title')
            if new_title:
                transaction.title = new_title
            
            new_category_id = request.form.get('category_id')
            if new_category_id:
                transaction.category_id = new_category_id

            db_session.commit()
            db_session.close()
            return redirect(url_for('transactions'))
        db_session.close()
        return render_template('edit_transaction.html', transaction=transaction)
    return render_template('forms/edit_transaction.html')

@app.route('/account/transaction/share', methods=['POST', 'GET'])
def sharetransaction():
    if request.method == 'POST':
        # post share request
        return redirect(url_for('transactions'))
    return render_template('forms/share_transaction.html')


def generate_reset_token():
    return secrets.token_urlsafe(32)

def calculate_expiry_time():
    expiry_time = datetime.datetime.now() + datetime.timedelta(hours=1)
    return expiry_time

def send_reset_password_email(user_email, reset_token):
    subject = "Reset Your Password"
    sender = "your_email@gmail.com"
    recipients = [user_email]
    text_body = f"Hello,\n\nPlease click the following link to reset your password:\n\nReset Password Link: http://your_website.com/reset-password/{reset_token}\n\nIf you did not request a password reset, please ignore this email.\n\nBest regards,\nYour Website Team"
    html_body = f"<p>Hello,</p><p>Please click the following link to reset your password:</p><p><a href='http://your_website.com/reset-password/{reset_token}'>Reset Password Link</a></p><p>If you did not request a password reset, please ignore this email.</p><p>Best regards,<br>Your Website Team</p>"

    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body

    mail.send(msg)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']

        db_session = Session()
        user = db_session.query(User).filter_by(email=email).first()
        db_session.close()

        if user:
            # Generate and store reset token
            reset_token = generate_reset_token()
            user.reset_token = reset_token
            user.reset_token_expiry = calculate_expiry_time()

            session = Session()
            session.add(user)
            session.commit()
            session.close()
            
            send_reset_password_email(user.email, reset_token)

            return render_template('password_reset_link_sent.html', email=email)
        else:
            return render_template('forgot_password.html', error='Email not found')
    return render_template('forgot_password.html')

@app.route('/reset-password/<reset_token>', methods=['GET', 'POST'])
def reset_password(reset_token):
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        Session = sessionmaker(bind=engine)
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
                    return render_template('reset_password.html', error='Passwords Do Not Match')
            else:
                return render_template('reset_password.html', error='Expired Code')
        else:
            return render_template('reset_password.html', error='Invalid Token')
    return render_template('reset_password.html')