from controllers.objects.forms import TransactionForm, CategoryForm, AccountForm, RecurringTransactionForm
from controllers import TransactionController as TC, CategoryController as CC, AccountController as AC
from datetime import date
from flask import render_template, redirect, url_for
from app import app

# ToDo: Implement flash message system
# ToDo: Recurring transaction system
# ToDo: Error Handling

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/transactions", methods=["GET","POST"])
def transactions():
    response: TC.TransactionResponse = TC.get_all_transactions()
    form:TransactionForm = TransactionForm()
    form.category.choices = CC.get_categories_for_listbox()
    form.account.choices = AC.get_accounts_for_listbox()
    if form.validate_on_submit():
        insert_response: TC.TransactionResponse = TC.insert_transaction(transaction_data=form.to_json())
        return redirect(url_for("transactions"))
        
    return render_template(
        "transactions/transactions.html", 
        transactions=response["transactions"],
        form=form
        )
    
@app.route("/transactions/<int:transaction_id>", methods=['GET','POST'])
def update_transaction(transaction_id:int):
    response: TC.TransactionResponse = TC.get_transaction_by_id(transactionid=transaction_id)
    form:TransactionForm = TransactionForm()
    form.category.choices = CC.get_categories_for_listbox()
    form.account.choices = AC.get_accounts_for_listbox()
    
    if form.validate_on_submit():        
        update_response: TC.TransactionResponse = TC.update_transaction(transaction_data=form.to_json())
        return redirect(url_for("transactions"))
                  
    return render_template(
        "transactions/transaction_update.html",
        transaction=response["transactions"][0],
        form=form
    )
    
@app.route("/transactions/recurring", methods=["GET","POST"])
def recurring_transactions():
    form = RecurringTransactionForm()
    if form.validate_on_submit():
        return redirect(url_for("recurring_transactions"))
    return render_template(
        "transactions/recurring_transactions.html"
    )
    
@app.route("/transactions/recurring/new", methods=["GET","POST"])
def new_recurring_transactions():
    form = RecurringTransactionForm()
    if form.validate_on_submit():
        return redirect(url_for("transactions"))
    return render_template(
        "transactions/recurring_transactions_new.html"
    )
    

@app.route("/transactions/recurring/<int:rtranid>", methods=["GET","POST"])
def update_recurring_transactions(rtranid):
    form = RecurringTransactionForm()
    if form.validate_on_submit():
        return redirect(url_for("recurring_transactions"))
    return render_template(
        "transactions/recurring_transactions_update.html"
    )
    
@app.route("/category", methods=["GET", "POST"])
def categories():
    response: CC.CategoryResponse = CC.get_all_categories()
    form = CategoryForm()
    if form.validate_on_submit():
        insert_response: CC.CategoryResponse = CC.insert_category(form.category_name.data)
        return redirect(url_for("categories"))
    return render_template(
        "categories/categories.html",
        form=form,
        categories=response["categories"]
        )
    
@app.route("/category/new", methods=["GET","POST"])
def new_category():
    # Need all categories for the datalist
    response: CC.CategoryResponse = CC.get_all_categories()
    form = CategoryForm()
    if form.validate_on_submit():
        insert_response: CC.CategoryResponse = CC.insert_category(form.category_name.data)
        return redirect(url_for("transactions"))
    return render_template(
        "categories/category_new.html",
        form=form,
        categories=response["categories"]
        )
    
@app.route("/category/<int:categoryid>", methods=["GET","POST"])
def update_category(categoryid: int):
    # Need all categories for the datalist
    all_cats_response: CC.CategoryResponse = CC.get_all_categories()
    form = CategoryForm()
    category_response: CC.CategoryResponse = CC.get_category_by_id(categoryid)
    if form.validate_on_submit():
        category_data = {
            "categoryid": categoryid,
            "category_name": form.category_name.data
        }
        update_response: CC.CategoryResponse = CC.update_category(category_data)
        return redirect(url_for("categories"))
    return render_template(
        "categories/category_update.html",
        form=form,
        category=category_response["categories"][0],
        categories=all_cats_response["categories"]
        )

@app.route("/budgets", methods=["GET"])
def budgets():
    return render_template("budgets/budgets.html")

@app.route("/account", methods=["GET", "POST"])
def accounts():
    # Need all accounts for datalist
    response: AC.AccountResponse = AC.get_all_accounts()
    form = AccountForm()
    if form.validate_on_submit():
        response: AC.AccountResponse = AC.insert_account(form.to_json())
        return redirect(url_for("accounts"))
    return render_template(
        "accounts/accounts.html",
        form=form,
        accounts=response["accounts"]
        )
    
@app.route("/account/new", methods=["GET","POST"])
def new_account():
    # Need all accounts for datalist
    response: AC.AccountResponse = AC.get_all_accounts()
    form = AccountForm()
    if form.validate_on_submit():
        response: AC.AccountResponse = AC.insert_account(form.to_json())
        return redirect(url_for("transactions"))
    return render_template(
        "accounts/account_new.html",
        form=form,
        accounts=response["accounts"]
        )
    
@app.route("/account/<int:accountid>", methods=["GET","POST"])
def update_account(accountid: int):
    form = AccountForm()
    response: AC.AccountResponse = AC.get_account_by_id(accountid)
    if form.validate_on_submit():
        account_data = {
            "accountid": accountid,
            "account_name": form.account_name.data
        }
        response: AC.AccountResponse = AC.update_account(account_data)
        return redirect(url_for("accounts"))
    return render_template(
        "accounts/account_update.html",
        form=form,
        account=response["accounts"][0]
        )