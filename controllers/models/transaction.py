from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey
from sqlalchemy.sql import func
from app import db
from controllers.models import category

class Transaction(db.Model): # type: ignore
    __tablename__ = 'transaction'
    transactionid: Column = Column(Integer, primary_key=True)
    categoryid: Column = Column(Integer, ForeignKey(category.Category.categoryid), default=1)
    merchant_name: Column = Column(String(200), nullable=False)
    transaction_type: Column = Column(String(200), nullable=False)
    amount: Column = Column(DECIMAL(7,2), nullable=False)
    note: Column = Column(String(1000))
    transaction_date: Column = Column(DateTime(timezone=False), nullable=False)
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
 