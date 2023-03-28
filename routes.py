from controllers import (
    TransactionController as TC, CategoryController as CC,
    AccountController as AC, BudgetController as BC
)
from controllers.objects.forms import (
    AccountForm, ApplyRecurringTransactions, BudgetForm, 
    CategoryForm, RecurringTransactionForm, TransactionForm
)
from controllers.objects.models import TransactionInterface
from datetime import date
from flask import render_template, redirect, request, url_for
from app import app

# ToDo: Implement flash message system
# ToDo: Recurring transaction system
# ToDo: Error Handling
# ToDo: Dynamic back buttons based on where user just was
# ToDo: Month end dict?

@app.route("/", methods=["GET"])
def home():
    cashflow_data = TC.get_cashflow()
    
    return render_template(
        "home.html",
        cashflow=cashflow_data,
        month=date.today().strftime("%B")
        )

@app.route("/transaction", methods=["GET","POST"])
def transactions():
    curr_response: TC.TransactionResponse = TC.get_all_transactions(is_pending=0)
    pend_response: TC.TransactionResponse = TC.get_all_transactions(is_pending=1)
    form:TransactionForm = TransactionForm()
    form.category.choices = CC.get_categories_for_listbox()
    form.account.choices = AC.get_accounts_for_listbox()
    if form.validate_on_submit():
        insert_response: TC.TransactionResponse = TC.insert_transaction(transaction_data=form.to_json())
        return redirect(url_for("transactions"))
        
    return render_template(
        "transactions/transactions.html", 
        current_transactions=curr_response["transactions"],
        pending_transactions=pend_response["transactions"],
        form=form
        )
    
@app.route("/transaction/<int:transaction_id>", methods=['GET','POST'])
def update_transaction(transaction_id:int):
    response: TC.TransactionResponse = TC.get_transaction_by_id(transactionid=transaction_id)
    
    target_transaction: TransactionInterface = response["transactions"][0]#type: ignore # ToDo: Figure out how to handle multiple return types
    form:TransactionForm = TransactionForm(
        transactionid=target_transaction.transaction.transactionid,
        transaction_date = target_transaction.transaction.transaction_date,
        merchant_name=target_transaction.transaction.merchant_name,
        category=target_transaction.category.categoryid,
        amount=target_transaction.transaction.amount,
        account=target_transaction.account.accountid,
        transaction_type=target_transaction.transaction.transaction_type,
        note=target_transaction.transaction.note
    )
    form.category.choices = CC.get_categories_for_listbox()
    form.account.choices = AC.get_accounts_for_listbox()
    
    if form.validate_on_submit():        
        update_response: TC.TransactionResponse = TC.update_transaction(transaction_data=form.to_json())
        print(update_response)
        return redirect(url_for("transactions"))
                  
    return render_template(
        "transactions/transaction_update.html",
        form=form
    )
    
@app.route("/transaction/recurring", methods=["GET","POST"])
def recurring_transactions():
    get_response = TC.get_all_recurring_transactions()
    form = RecurringTransactionForm()
    form.category.choices = CC.get_categories_for_listbox()
    form.account.choices = AC.get_accounts_for_listbox()
    
    if form.validate_on_submit():
        insert_response = TC.insert_recurring_transaction(form.to_json())
        return redirect(url_for("recurring_transactions"))
    return render_template(
        "transactions/recurring_transactions.html",
        form=form,
        transactions=get_response["transactions"]
    )
    
@app.route("/transaction/recurring/new", methods=["GET","POST"])
def new_recurring_transaction():
    form = RecurringTransactionForm()
    if form.validate_on_submit():
        return redirect(url_for("transactions"))
    return render_template(
        "transactions/recurring_transactions_new.html",
        form=form
    )
    
@app.route("/transaction/recurring/<int:rtranid>", methods=["GET","POST"])
def update_recurring_transaction(rtranid):
    get_response = TC.get_rtran_by_id(rtranid)
    form = RecurringTransactionForm()
    if form.validate_on_submit():
        return redirect(url_for("recurring_transactions"))
    return render_template(
        "transactions/recurring_transactions_update.html",
        form=form
    )
    
@app.route("/transaction/recurring/apply", methods=["GET","POST"])
def apply_recurring_transactions():
    get_response = TC.get_all_recurring_transactions()
    # ToDo: loop through trans to get all monthly trans and add them as default to form.RTranIDs
    form = ApplyRecurringTransactions()
    if form.validate_on_submit():
        apply_rtran_response = TC.apply_recurring_transactions(form.to_json())
        return redirect(url_for("transactions"))
    return render_template(
        "transactions/apply_recurring_transactions.html",
        form=form,
        transactions=get_response["transactions"]
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

@app.route("/budget", methods=["GET","POST"])
def budgets():
    budgets = BC.get_all_budgets()
    form = BudgetForm()
    return render_template(
        "budgets/budgets.html",
        form=form,
        budgets=budgets["budgets"]
        )

@app.route("/budget/new", methods=["GET","POST"])
def new_budget():
    form = BudgetForm()
    return render_template(
        "budgets/budget_new.html",
        form=form
        )

@app.route("/budget/<int:budgetid>", methods=["GET","POST"])
def update_budget(budgetid):
    budget = BC.get_budget_by_id(budgetid=budgetid)
    form = BudgetForm()
    return render_template(
        "budgets/budget_update.html",
        form=form,
        budget=budget
        )

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