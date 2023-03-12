from sqlalchemy import Column, Integer, String, DECIMAL, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from app import app, db
import sys

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
    
    def to_json(self) -> dict[str, Column]:
        return {
            "transactionid": self.transactionid,
            "transaction_date": self.transaction_date,
            "categoryid": self.categoryid,
            "merchant_name": self.merchant_name,
            "transaction_type": self.transaction_type,
            "amount": self.amount,
            "note": self.note
        }
    
class Category(db.Model): # type: ignore
    __tablename__ = 'category'
    categoryid: Column = Column(Integer, primary_key=True)
    category_name: Column = Column(String(200), nullable=False)
    insert_date: Column = Column(DateTime(timezone=False), server_default=func.sysdate())
    insert_by: Column = Column(String(100), server_default=func.current_user())
    update_date: Column = Column(DateTime(timezone=False), server_default=func.sysdate(), server_onupdate=func.sysdate())
    update_by: Column = Column(String(100), server_default=func.current_user(), server_onupdate = func.current_user())
    
class Budget(db.Model): # type: ignore
    __tablename__ = 'budget'
    budgetid: Column = Column(Integer, primary_key=True)
    budget_name: Column = Column(String(200), nullable=False)
    budget_amount: Column = Column(DECIMAL(7,2))
    insert_date: Column = Column(DateTime(timezone=False), server_default=func.sysdate())
    insert_by: Column = Column(String(100), server_default=func.current_user())
    update_date: Column = Column(DateTime(timezone=False), server_default=func.sysdate(), server_onupdate=func.sysdate())
    update_by: Column = Column(String(100), server_default=func.current_user(), server_onupdate = func.current_user())
    
class BudgetCategory(db.Model): # type: ignore
    __tablename__ = 'budgetcategory'
    budgetcategoryid: Column = Column(Integer, primary_key=True)
    budgetid: Column = Column(Integer, ForeignKey('budget.budgetid'), nullable=False)
    categoryid: Column = Column(Integer, ForeignKey('category.categoryid'), nullable=False)
    insert_date: Column = Column(DateTime(timezone=False), server_default=func.sysdate())
    insert_by: Column = Column(String(100), server_default=func.current_user())
    update_date: Column = Column(DateTime(timezone=False), server_default=func.sysdate(), server_onupdate=func.sysdate())
    update_by: Column = Column(String(100), server_default=func.current_user(), server_onupdate = func.current_user())
    
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
            
