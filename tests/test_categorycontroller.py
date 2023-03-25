from controllers import CategoryController
from app import app

# ToDo: test all category controller methods

def test_category_insert():
    test_category = "PyTest Category"
    
    with app.app_context():
        CategoryController.insert_category(test_category)
        assert CategoryController.get_category_by_name(test_category).category_name == test_category
    
    