from controllers import CategoryController
from app import app

# ToDo: test all category controller methods

def test_category_insert():
    test_category = "PyTest Category"
    
    with app.app_context():
        ins_resp = CategoryController.insert_category(test_category)
        assert ins_resp["categories"][0].category_name == test_category
    
    