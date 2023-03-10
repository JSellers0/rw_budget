from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app import db

class Category(db.Model): # type: ignore
    __tablename__ = 'category'
    categoryid: Column = Column(Integer, primary_key=True)
    category_name: Column = Column(String(200), nullable=False)
    insert_date: Column = Column(DateTime(timezone=False), server_default=func.sysdate())
    insert_by: Column = Column(String(100), server_default=func.current_user())
    update_date: Column = Column(DateTime(timezone=False), server_default=func.sysdate(), server_onupdate=func.sysdate())
    update_by: Column = Column(String(100), server_default=func.current_user(), server_onupdate = func.current_user())
