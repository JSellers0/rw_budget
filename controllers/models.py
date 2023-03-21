from sqlalchemy import Column, Integer, String, DECIMAL, Date, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql import func
from app import app, db
import sys
from typing import Any

# TODO: User table
class Transaction(db.Model): # type: ignore
    __tablename__ = 'transaction'
    transactionid: Column = Column(Integer, primary_key=True)
    categoryid: Column = Column(Integer, ForeignKey('category.categoryid'), default=1)
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
    
    def to_json(self, category_name: str='Uncategorized') -> dict[str, Any]:
        return {
            "transactionid": self.transactionid,
            "transaction_date": self.transaction_date,
            "categoryid": self.categoryid,
            "merchant_name": self.merchant_name,
            "transaction_type": self.transaction_type,
            "amount": self.amount,
            "note": self.note,
            "category": category_name
        }

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
            
