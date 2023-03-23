from controllers.objects.forms import TransactionForm, CategoryForm, AccountForm
from controllers import TransactionController as TC, CategoryController as CC, AccountController as AC
from datetime import date
from flask import render_template, redirect, url_for
from app import app

# ToDo: Implement flash message system
# ToDo: Recurring transaction system

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/transactions", methods=["GET","POST"])
def transactions():
    transactions = TC.get_all_transactions()
    form:TransactionForm = TransactionForm()
    form.category.choices = CC.get_categories_for_listbox()
    form.account.choices = AC.get_accounts_for_listbox()
    if form.validate_on_submit():
        tr = TC.insert_transaction_form(transaction_data=form)
        return redirect(url_for("transactions"))
        # ToDo: Flash insert failure
        
        
    return render_template(
        "transactions/transactions.html", 
        transactions=transactions,
        form=form
        )
    
@app.route("/transactions/<int:transaction_id>", methods=['GET','POST'])
def update_transaction(transaction_id:int):
    transaction = TC.get_transaction_by_id(transactionid=transaction_id)
    form:TransactionForm = TransactionForm()
    form.category.choices = CC.get_categories_for_listbox()
    form.account.choices = AC.get_accounts_for_listbox()
    
    if form.validate_on_submit():
        
        transaction_data = {
            "transaction_date": form.transaction_date.data,
            "transaction_type": form.transaction_type.data,
            "merchant_name": form.merchant_name.data,
            "amount": form.amount.data,
            "categoryid": form.category.data,
            "note": form.note.data
        }
        
        tr = TC.update_transaction(transaction_data=transaction_data)
        
        return redirect(url_for("transactions"))
                  
    return render_template(
        "transactions/transaction_update.html",
        transaction=transaction,
        categories=CC.get_categories_for_listbox(),
        accounts = AC.get_accounts_for_listbox(),
        form=form
    )
    
@app.route("/category", methods=["GET", "POST"])
def categories():
    form = CategoryForm()
    if form.validate_on_submit():
        CC.insert_category(form.category_name.data)
        return redirect(url_for("categories"))
    return render_template(
        "categories/categories.html",
        form=form,
        categories=CC.get_all_categories()
        )
    
@app.route("/category/new", methods=["GET","POST"])
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        CC.insert_category(form.category_name.data)
        return redirect(url_for("transactions"))
    return render_template(
        "categories/category_new.html",
        form=form,
        categories=CC.get_all_categories()
        )
    
@app.route("/category/<int:categoryid>", methods=["GET","POST"])
def update_category(categoryid: int):
    form = CategoryForm()
    category = CC.get_category_by_id(categoryid)
    if form.validate_on_submit():
        category_data = {
            "categoryid": categoryid,
            "category_name": form.category_name.data
        }
        CC.update_category(category_data)
        return redirect(url_for("categories"))
    return render_template(
        "categories/category_update.html",
        form=form,
        category=category,
        categories=CC.get_all_categories
        )

@app.route("/budgets", methods=["GET"])
def budgets():
    return render_template("budgets.html")

@app.route("/account", methods=["GET", "POST"])
def accounts():
    form = AccountForm()
    if form.validate_on_submit():
        AC.insert_account(form)
        return redirect(url_for("accounts"))
    return render_template(
        "accounts/accounts.html",
        form=form,
        accounts=AC.get_all_accounts()
        )
    
@app.route("/account/new", methods=["GET","POST"])
def new_account():
    form = AccountForm()
    if form.validate_on_submit():
        AC.insert_account(form)
        return redirect(url_for("transactions"))
    return render_template(
        "accounts/account_new.html",
        form=form,
        accounts=AC.get_all_accounts()
        )
    
@app.route("/account/<int:accountid>", methods=["GET","POST"])
def update_account(accountid: int):
    form = AccountForm()
    account = AC.get_account_by_id(accountid).to_json()
    if form.validate_on_submit():
        account_data = {
            "accountid": accountid,
            "account_name": form.account_name.data
        }
        AC.update_account(account_data)
        return redirect(url_for("accounts"))
    return render_template(
        "accounts/account_update.html",
        form=form,
        account=account
        )