from controllers import CategoryController as CC
from app import app

# ToDo: test all category controller methods

def test_category_insert():
    test_category = "Insert Test Category"
    
    with app.app_context():
        ins_resp = CC.insert_category(test_category)
        assert ins_resp["categories"][0].category_name == test_category

def test_insert_dupe_name():
    assert 0==0

def test_category_update():
    test_category = "Update Test Category Insert"
    
    with app.app_context():
        ins_resp = CC.insert_category(test_category)
        # combine ins response carid and new cat name.
        update_data = {
            "categoryid": catid,
            "category_name": "Update Test Category Update"
            }
        upd_resp = CC.update_category(update_data)
        assert upd_resp["categories"][0].category_name == update_data["category_name"]

def test_update_bad_id():
    assert 0==0

def test_update_dupe_name():
    assert 0==0

def test_get_all_catergories():
    test_category = "Test Get All Categories"
    
    with app.app_context():
        ins_resp = CC.insert_category(test_category)
        get_all_resp = CC.get_all_categories()
        assert len(get_all_resp["categories"]) > 0

def test_get_category_by_id():
    assert 0==0

def test_get_category_bad_id():
    with app.app_context():
        get_resp = CC.get_category_by_id(9999)
        assert get_resp["status_code"] == 404

def test_get_category_by_name():
    assert 0==0

def test_get_category_bad_name():
    assert 0==0
    
    