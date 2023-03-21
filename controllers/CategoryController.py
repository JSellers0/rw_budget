from app import db
from controllers.models import Category
from typing import Any

def get_category_by_id(categoryid: int) -> Category:
    category: Category = Category.query.filter(Category.categoryid == categoryid).one_or_none()
    
    if category == None:
        raise ValueError(f"{categoryid} is not a valid category id.")
    
    return category

def get_category_by_name(category_name: str) -> Category:
    category: Category = Category.query.filter(Category.category_name == category_name).one_or_none()
    
    if category == None:
        raise ValueError(f"{category_name} does not exist.")
    
    return category
    
def get_all_categories() -> list[dict[str, Any]]:
    categories = Category.query.all()
    category_dump = [category.to_tuple() for category in categories]
    
    return category_dump

def insert_category(category_name: str)-> Category:
    category: Category = Category(category_name = category_name.lower())
    
    db.session.add(category)
    db.session.commit()
    
    return category

def update_category(category_data: dict) -> Category:
    category: Category = Category.query.filter(Category.categoryid == category_data.get('categoryid')).one_or_none()
    
    if category == None:
        raise ValueError(f"{category_data.get('categoryid')} is not a valid category id.")
    
    if category_data.get('category_name') != category.category_name:
        category.category_name = category_data.get('category_name', '')
    
    db.session.commit()
    
    return category

def delete_category(categoryid: int) -> None:
    category: Category = Category.query.filter(Category.categoryid == categoryid).one_or_none()
    
    if category == None:
        raise ValueError(f"{categoryid} is not a valid category id.")
    
    db.session.delete(category)
    db.session.commit()
     
     