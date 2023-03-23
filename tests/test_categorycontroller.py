from controllers import CategoryController
from app import app

# ToDo: test all category controller methods

def test_category_insert():
    test_category = "PyTest Category"
    
    with app.app_context():
        CategoryController.insert_category(test_category).to_json()
        new_category = CategoryController.get_category_by_name(test_category).to_json()
    
    assert new_category.get('category_name') == test_category.lower()
    
    