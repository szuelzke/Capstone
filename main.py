from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 
import bcrypt
import pyotp
import qrcode
import base64
import secrets
import datetime
from datetime import date

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

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

class Account(Base):
    __tablename__ = 'account'

    account_id = Column(Integer, primary_key=True)
    account_name = Column(String(255))
    user_id = Column(Integer)
    is_active = Column(Boolean)

try:
    connection = engine.connect()
    print("Connection successful!")
except Exception as e:
    print("Connection failed:", e)

@app.route('/')
def home():
    if 'user_id' in session:
        return render_template('index.html')
    else:
        msg = ''
        return render_template('landing.html', msg=msg)

@app.route('/test')
def test():
    if 'user_id' in session:
        return render_template('test.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db_session = Session()
        user = db_session.query(User).filter_by(email=email).first()
        db_session.close()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            session['user_id'] = user.user_id
            session['email'] = user.email
            otp_secret = pyotp.random_base32()  # Generate new OTP secret for each login attempt
            otp_uri = pyotp.totp.TOTP(otp_secret).provisioning_uri(user.email, issuer_name="FlashFin")
            session['otp_secret'] = otp_secret  # Store OTP secret in session
            session['otp_uri'] = otp_uri  # Store OTP URI in session
            return redirect(url_for('verify_mfa'))
            
            #return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid email or password')
    return render_template('login.html')

@app.route('/verify_mfa', methods=['GET', 'POST'])
def verify_mfa():
    if 'user_id' in session:
#        user_id = session['user_id']
#        db_session = Session()
#        user = db_session.query(User).filter_by(user_id=user_id).first()
#        db_session.close()
#        if request.method == 'POST':
        
#            otp = request.form['otp']
#            otp_secret = session.get('otp_secret')
#            if otp_secret and pyotp.TOTP(otp_secret).verify(otp):
#               return redirect(url_for('home'))
#            else:
#                return render_template('verify_mfa.html', error='Invalid OTP', qr_code='', setup_key='')
        otp_uri = session['otp_uri']
        # Generate QR code image
        qr = qrcode.make(otp_uri)
        # Convert QR code image to Base64 string
        qr_base64 = base64.b64encode(qr.tobytes()).decode()
        # Get setup key for manual addition to Google Authenticator
        setup_key = pyotp.TOTP(session['otp_secret']).secret
        # Render the template with QR code and setup key
        return render_template('verify_mfa.html', otp_uri=otp_uri, qr_code=qr_base64, setup_key=setup_key)
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

@app.route('/settings')
def settings():
    if 'user_id' in session:
        user_id = session['user_id']
        db_session = Session()
        user = db_session.query(User).filter_by(user_id=user_id).first()
        db_session.close()

        return render_template('settings.html', user=user)

    else:
        return redirect(url_for('login'))

@app.route('/account')
def account():
    if 'user_id' in session:
        return render_template('/account/dashboard.html')
    else:
        return redirect(url_for('login'))

@app.route('/add-account', methods=['POST', 'GET'])
def add_account():
    # don't know if this works 
    if request.method == 'POST':
        account_name = request.form['accountname']
        new_account = Account(
            account_name = account_name
        )

        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(new_account)
        session.commit()
        session.close()
        return redirect(url_for('home'))
    return render_template('/forms/add_account.html')

@app.route('/account/transaction', methods=['GET'])
def transactions():
    # show all transactions
    return render_template('account/transactions.html')

@app.route('/account/transaction/add', methods=['POST', 'GET'])
def addtransaction():
    if request.method == 'POST':
        # add new transaction
        return redirect(url_for('transactions'))
    return render_template('forms/add_transaction.html')

@app.route('/account/transaction/edit', methods=['POST', 'GET'])
def edittransaction():
    if request.method == 'POST':
        # post editted transaction
        return redirect(url_for('transactions'))
    # display transaction info to form
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
            
            # send_reset_password_email(user.email, reset_token)

            return render_template('password_reset_link_sent.html', email=email)
        else:
            return render_template('forgot_password.html', error='Email not found')
    return render_template('forgot_password.html')

@app.route('/reset-password/<reset_token>', methods=['GET', 'POST'])
def reset_password(reset_token):
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        session = Session()
        user = session.query(User).filter_by(reset_token=reset_token).first()
        session.close()

        if user:
            if new_password == confirm_password:
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

                user.password = hashed_password
                user.reset_token = None
                user.reset_token_expiry = None

                session = Session()
                session.add(user)
                session.commit()
                session.close()

                return render_template('password_reset_success.html')
            else:
                return render_template('password_mismatch_error.html')
        else:
            return render_template('invalid_reset_token_error.html')
    return render_template('reset_password.html')