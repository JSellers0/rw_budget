from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from config import app, db

#Model = declarative_base(name='Model')

class Transaction(db.Model): # type: ignore
    __tablename__ = 'transaction'
    transactionid: Column = Column(Integer, primary_key=True)
    categoryid: Column = Column(Integer, ForeignKey('category.categoryid'), nullable=False)
    merchant_name: Column = Column(String(200), nullable=False)
    amount: Column = Column(DECIMAL(7,2), nullable=False)
    note: Column = Column(String(1000))
    insert_date: Column = Column(DateTime(timezone=False), server_default=func.sysdate())
    insert_by: Column = Column(String(100), server_default=func.current_user())
    update_date: Column = Column(DateTime(timezone=False), server_onupdate=func.sysdate())
    update_by: Column = Column(String(100), server_onupdate = func.current_user())
    
class Category(db.Model): # type: ignore
    __tablename__ = 'category'
    categoryid: Column = Column(Integer, primary_key=True)
    category_name: Column = Column(String(200), nullable=False)
    insert_date: Column = Column(DateTime(timezone=False), server_default=func.sysdate())
    insert_by: Column = Column(String(100), server_default=func.current_user())
    update_date: Column = Column(DateTime(timezone=False), server_onupdate=func.sysdate())
    update_by: Column = Column(String(100), server_onupdate = func.current_user())
    
class Budget(db.Model): # type: ignore
    __tablename__ = 'budget'
    budgetid: Column = Column(Integer, primary_key=True)
    budget_name: Column = Column(String(200), nullable=False)
    budget_amount: Column = Column(DECIMAL(7,2))
    insert_date: Column = Column(DateTime(timezone=False), server_default=func.sysdate())
    insert_by: Column = Column(String(100), server_default=func.current_user())
    update_date: Column = Column(DateTime(timezone=False), server_onupdate=func.sysdate())
    update_by: Column = Column(String(100), server_onupdate = func.current_user())
    
class BudgetCategory(db.Model): # type: ignore
    __tablename__ = 'budgetcategory'
    budgetcategoryid: Column = Column(Integer, primary_key=True)
    budgetid: Column = Column(Integer, ForeignKey('budget.budgetid'), nullable=False)
    categoryid: Column = Column(Integer, ForeignKey('category.categoryid'), nullable=False)
    insert_date: Column = Column(DateTime(timezone=False), server_default=func.sysdate())
    insert_by: Column = Column(String(100), server_default=func.current_user())
    update_date: Column = Column(DateTime(timezone=False), server_onupdate=func.sysdate())
    update_by: Column = Column(String(100), server_onupdate = func.current_user())
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
