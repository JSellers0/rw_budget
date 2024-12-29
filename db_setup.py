import json
from os import path
from sqlalchemy import text
from app import app, db
from controllers.objects import *


BASE_DIR = path.dirname(__file__)


def load_initial_values():
    with open(f"{BASE_DIR}/database/init/initial_values.json") as in_f:
        config = json.loads(in_f.read())
    return config


def build_categories(cat_config: list):
    with app.app_context():
        for config in cat_config:
            db.session.add(
                Category(category_name=config)
            )
        db.session.commit()

def build_accounts(acct_config: list[dict]):
    # ToDo: add care credit account
    with app.app_context():
        for acct in acct_config:
            db.session.add(Account(
                account_name=acct.get("account_name"),
                account_type=acct.get("account_type"),
                rewards_features=acct.get("rewards_features"),
                payment_day=acct.get("payment_day"),
                statement_day=acct.get("statement_day")
            ))
        db.session.commit()


def main():
    config = load_initial_values()
    print("Welcome to DB Setup.  Options: ")
    print("\t1. Build DB")
    print("\t2. Rebuild DB")

    user_select = input("Please select an option > ")

    with app.app_context():
        if user_select == "2":
            print("Dropping existing tables")
            db.drop_all()
        print("Running DB initialization.")
        db.create_all()
        db.session.commit()
        build_accounts(config.get("Accounts"))
        build_categories(config.get("Categories"))

    user_select = input("Do you need to rebuild Views? (y/n) > ")
    if 'y' in user_select.lower():
        with open(f"{BASE_DIR}/database/sql/views/vw_card_current_balances.sql", 'r') as view_f:
            with app.app_context():
                db.session.execute(text(view_f.read()))
                db.session.commit()
        with open(f"{BASE_DIR}/database/sql/views/vw_cashflow_chart.sql", 'r') as view_f:
            with app.app_context():
                db.session.execute(text(view_f.read()))
                db.session.commit()

    user_select = input("Do you need to rebuild Stored Procs? (y/n) > ")
    if 'y' in user_select.lower():
        with open(f"{BASE_DIR}/database/sql/stored_proc/sp_agg_account_balances.sql", 'r') as proc_f:
            with app.app_context():
                db.session.execute(proc_f.read())
                db.session.commit()

    user_select = input("Do you need to rebuild Events? (y/n) > ")
    if 'y' in user_select.lower():
        with open(f"{BASE_DIR}/database/sql/events/ev_agg_account_balances.sql", 'r') as ev_f:
            with app.app_context():
                db.session.execute(ev_f.read())
                db.session.commit()



if __name__ == '__main__':
    main()
