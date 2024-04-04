from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 
import bcrypt
import pyotp
import qrcode
import base64
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
            session['email'] = user.email
            return redirect(url_for('verify_2fa'))

            #return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid email or password')

    return render_template('login.html')

@app.route('/verify_2fa', methods=['GET', 'POST'])
def verify_2fa():
    if request.method == 'POST':
        otp = request.form['otp']
        
        otp_secret = session.get('otp_secret')
        if otp_secret:
            if pyotp.TOTP(otp_secret).verify(otp):
                session['user_id'] = get_user_id(session['email'])
                return redirect(url_for('home'))
            else:
                return render_template('2fa.html', error='Invalid OTP', qr_code='', setup_key='')
        else:
            return redirect(url_for('login'))  # If no OTP secret found, redirect to login

    otp_uri = session.get('otp_uri')
    if not otp_uri:
        return redirect(url_for('login'))  # If no OTP URI found, redirect to login

    # Generate QR code image
    qr = qrcode.make(otp_uri)

    # Convert QR code image to Base64 string
    qr_base64 = base64.b64encode(qr.tobytes()).decode()

    # Get setup key for manual addition to Google Authenticator
    setup_key = pyotp.TOTP(session['otp_secret']).secret

    # Render the template with QR code and setup key
    return render_template('2fa.html', otp_uri=otp_uri, qr_code=qr_base64, setup_key=setup_key)

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
    return render_template('/account/add_account.html')
    