from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, DECIMAL, Date, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql import func
from app import app, db
import sys
from typing import Any

# ToDo: User table
# ToDo: Split db init from models
# ToDo: Recurring Transactions table

# ToDo: parentcategoryid
class Category(db.Model): # type: ignore
    __tablename__ = 'category'
    categoryid: Column = Column(Integer, primary_key=True)
    category_name: Column = Column(String(200), nullable=False)
    insert_date: Column = Column(DateTime(timezone=False), server_default=func.sysdate())
    insert_by: Column = Column(String(100), server_default=func.current_user())
    update_date: Column = Column(DateTime(timezone=False), server_default=func.sysdate(), server_onupdate=func.sysdate())
    update_by: Column = Column(String(100), server_default=func.current_user(), server_onupdate = func.current_user())
    transactions = db.relationship('Transaction', backref='category')
    budgets = db.relationship('Budget', backref='category')
    
    def __repr__(self) -> str:
        return "Category({},{})".format(self.categoryid, self.category_name)
    
    def to_json(self) -> dict[str, Column]:
        return {
            "categoryid": self.categoryid,
            "category_name": self.category_name,
            "transations": self.transactions,
            "budgets": self.budgets
        }
        
    def to_tuple(self) -> tuple[Column, Column]:
        return (self.categoryid, self.category_name)
    
class Budget(db.Model): # type: ignore
    __tablename__ = 'budget'
    budgetid: Column = Column(Integer, primary_key=True)
    categoryid: Column = Column(Integer, ForeignKey('category.categoryid'), default=1)
    budget_name: Column = Column(String(200), nullable=False)
    budget_amount: Column = Column(DECIMAL(7,2))
    insert_date: Column = Column(DateTime(timezone=False), server_default=func.sysdate())
    insert_by: Column = Column(String(100), server_default=func.current_user())
    update_date: Column = Column(DateTime(timezone=False), server_default=func.sysdate(), server_onupdate=func.sysdate())
    update_by: Column = Column(String(100), server_default=func.current_user(), server_onupdate = func.current_user())
    
    def __repr__(self) -> str:
        return "Budget({},{},{})".format(self.budgetid, self.budget_name, self.budget_amount)
    
    def to_json(self) -> dict[str, Column]:
        return {
            "budgetid": self.budgetid,
            "budget_name": self.budget_name,
            "budget_amount": self.budget_amount
        }

class Account(db.Model): # type: ignore
    __tablename__ = 'account'
    accountid: Column = Column(Integer, primary_key=True)
    account_name: Column = Column(String(200), nullable=False)
    account_type: Column = Column(String(100), nullable=False)
    rewards_features: Column = Column(String(300))
    payment_day: Column = Column(String(50))
    statement_day: Column = Column(String(50))
    transactions = db.relationship('Transaction', backref='account')
    
    def __repr__(self) -> str:
        return "account({},{})".format(self.accountid, self.account_name)
    
    def to_json(self) -> dict[str, Column]:
        return {
            "accountid": self.accountid,
            "account_name": self.account_name,
            "account_type": self.account_type,
            "rewards_features": self.rewards_features,
            "payment_day": self.payment_day,
            "statement_day": self.statement_day
        }
        
    def to_tuple(self) -> tuple[Column, Column]:
        return (self.accountid, self.account_name)

class Transaction(db.Model): # type: ignore
    __tablename__ = 'transaction'
    transactionid: Column = Column(Integer, primary_key=True)
    categoryid: Column = Column(Integer, ForeignKey('category.categoryid'), default=1)
    accountid: Column = Column(Integer, ForeignKey('account.accountid'), default=1)
    merchant_name: Column = Column(String(200), nullable=False)
    transaction_type: Column = Column(String(200), nullable=False)
    amount: Column = Column(DECIMAL(7,2), nullable=False)
    note: Column = Column(String(1000))
    transaction_date: Column = Column(Date(), nullable=False)
    insert_date: Column = Column(DateTime(timezone=False), server_default=func.sysdate())
    insert_by: Column = Column(String(100), server_default=func.current_user())
    update_date: Column = Column(DateTime(timezone=False), server_default=func.sysdate(), server_onupdate=func.sysdate())
    update_by: Column = Column(String(100), server_default=func.current_user(), server_onupdate = func.current_user())
    
    def __repr__(self) -> str:
        return "Transaction({},{},{})".format(self.transactionid, self.merchant_name, self.amount)
    
@dataclass
class Transaction_Interface:
    transaction: Transaction
    category: Category
    account: Account
    operation_status: str = 'SUCCESS'
    
def build_accounts():
    barlcays = Account(
        account_name='Barclays',
        account_type='Credit Card',
        rewards_features='Restaurants 3x - Streaming/Phone/Internet 2x - Grocery Stores (except Target and Walmart) 2x',
        payment_day='3rd',
        statement_day='6th'
        )
    pnc_cash = Account(
        account_name='PNC Rewards',
        account_type='Credit Card',
        rewards_features='Gas 4x - Restaurants 3x - Groceries 2x - 8,000 multiplier cap',
        payment_day='2nd',
        statement_day='7th'
        )
    pnc_spend = Account(
        account_name='PNC Spend',
        account_type='Checking Account',
        rewards_features='',
        payment_day='',
        statement_day=''
        )
    quicksilver = Account(
        account_name='Quicksilver',
        account_type='Credit Card',
        rewards_features='1.5x all purchases',
        payment_day='5th',
        statement_day='11th'
        )
    venture = Account(
        account_name='Venture',
        account_type='Credit Card',
        rewards_features='5x hotels and car rentsl booked through CapOne - 1.25x all purchases',
        payment_day='10th',
        statement_day='16th'
        )
    
    
    with app.app_context():
        db.session.add_all([venture,pnc_cash,pnc_spend,quicksilver,barlcays])
        db.session.commit()
    
# Merchant

# MerchantAlias - enable aliased merchant display

# MerchantCategory - enable default merchant categorization

if __name__ == '__main__':
    if '-rebuild' in sys.argv:
        with app.app_context():
            db.drop_all()
            db.create_all()
            db.session.execute("INSERT INTO category(category_name) VALUES ('Uncategorized');")
            db.session.commit()
            
        build_accounts()
            