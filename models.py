from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Date, DECIMAL, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

#### ------------------------------- Models --------------------------------------------------------

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

class ShareSpend(Base):
    __tablename__ = 'share_spend'
    share_id= Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(Integer, ForeignKey(Transaction.transaction_id))
    receiver_transaction_id = Column(Integer, ForeignKey(Transaction.transaction_id))
    sender_id = Column(Integer, ForeignKey(User.user_id))
    receiver_id = Column(Integer, ForeignKey(User.user_id))
    amount_split = Column(DECIMAL(10, 2))
    is_paid = Column(Boolean)
    
    init_transaction = relationship('Transaction', foreign_keys='ShareSpend.transaction_id')
    receiver_transaction = relationship('Transaction', foreign_keys='ShareSpend.receiver_transaction_id')
    sender = relationship('User', foreign_keys='ShareSpend.sender_id')
    receiver = relationship('User', foreign_keys='ShareSpend.receiver_id')