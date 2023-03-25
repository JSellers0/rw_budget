from app import db
from controllers.objects.models import Category
from typing import TypedDict

# ToDo: Standardize response messages
# ToDo: Response status checks where appropriate
# ToDo: try/except around db operations?
# ToDo: use get functions instead of repeating Category.query in insert,update,delete

class CategoryResponse(TypedDict):
    response_code: int
    message: str
    categories: list[Category | None]

def get_category_by_id(categoryid: int) -> CategoryResponse:
    category: Category = Category.query.filter(Category.categoryid == categoryid).one_or_none()
    
    if category == None:
        return CategoryResponse(
            response_code=404,
            message=f"Category not found with Category ID {categoryid}.",
            categories=[None]
        )
    
    return CategoryResponse(
            response_code=200,
            message=f"CategoryID {categoryid} retrieved successfully",
            categories=[category]
        )

def get_category_by_name(category_name: str) -> CategoryResponse:
    category: Category = Category.query.filter(Category.category_name == category_name).one_or_none()
    
    if category == None:
        return CategoryResponse(
            response_code=404,
            message=f"Category not found with Category Name {category_name}.",
            categories=[None]
        )

    return CategoryResponse(
            response_code=200,
            message=f"Category {category_name} retrieved successfully",
            categories=[category]
        )

# ToDo: Accept return type parameter
def get_all_categories() -> CategoryResponse:
    categories = Category.query.all()
    
    if len(categories) == 0:
        return CategoryResponse(
            response_code=404,
            message=f"No Categories found.",
            categories=[None]
        )
    
    return CategoryResponse(
            response_code=200,
            message=f"Retrieved {len(categories)} Categories",
            categories=[category for category in categories]
        )

def get_categories_for_listbox() -> list[tuple[int, str]]:
    categories = Category.query.all()
    category_dump = [category.to_tuple() for category in categories]
    
    return category_dump

def insert_category(category_name: str)-> CategoryResponse:
    cat_check: CategoryResponse = get_category_by_name(category_name=category_name)
    
    if cat_check["categories"][0] is None:
        category: Category = Category(category_name=category_name)
        # ToDo: try/except?
        db.session.add(category)
        db.session.commit()
    
        return CategoryResponse(
            response_code=200,
            message=f"Category {category_name} insert successful.",
            categories=[category]
        )
    
    return CategoryResponse(
            response_code=409,
            message=f"Category {category_name} already exists.",
            categories=[cat_check["categories"][0]]
        )    

def update_category(category_data: dict) -> CategoryResponse:
    # ToDo: Check for category name existing already.
    category: Category = Category.query.filter(Category.categoryid == category_data.get('categoryid')).one_or_none()
    
    if category == None:
        return CategoryResponse(
            response_code=404,
            message=f"Category not found with Category Name {category_data.get('category_name')}.",
            categories=[None]
        )
    
    if category_data.get('category_name','').lower() != category.category_name.lower():
        category.category_name = category_data.get('category_name', '')
    
    # ToDo: try/except?
    db.session.commit()
    
    return CategoryResponse(
            response_code=200,
            message=f"Category {category_data.get('category_name')} update successful.",
            categories=[category]
        )

def delete_category(categoryid: int) -> CategoryResponse:
    category: Category = Category.query.filter(Category.categoryid == categoryid).one_or_none()
    
    if category == None:
        return CategoryResponse(
            response_code=404,
            message=f"{categoryid} is not a valid category id.",
            categories=[None]
        )
    
    # ToDo: try/except?
    db.session.delete(category)
    db.session.commit()
    
    return CategoryResponse(
            response_code=200,
            message=f"Category {categoryid} delete successful.",
            categories=[category]
        )
     
     