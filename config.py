from flask import Flask
from flask_mail import Mail
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import openai
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'flashfin.alerts@gmail.com'
app.config['MAIL_PASSWORD'] = 'x'
app.config['MAIL_DEFAULT_SENDER'] = 'flashfin.alerts@gmail.com'

mail = Mail(app)

engine = create_engine('mysql+mysqlconnector://capstone:CapStone2024@localhost/FLASHFIN?unix_socket=/var/lib/mysql/mysql.sock')

Session = sessionmaker(bind=engine)

# Set up database
Base.metadata.create_all(engine)

with open('/var/www/html/Capstone/.env', 'r') as file:
     openai.api_key = file.read().replace('\n', '')
     
client = openai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# test database connection
try:
    connection = engine.connect()
    print("Connection successful!")
except Exception as e:
    print("Connection failed:", e)
