from controllers import (
    TransactionController as TC, CategoryController as CC,
    AccountController as AC, BudgetController as BC
)
from controllers.objects.forms import (
    AccountForm, ApplyRecurringTransactions, BudgetForm, 
    CategoryForm, RecurringTransactionForm, TransactionForm,
    UploadTransactionsForm
)
from controllers.objects.models import TransactionInterface
from datetime import date, timedelta
from flask import render_template, redirect, request, url_for
from app import app
from werkzeug.utils import secure_filename

# ToDo: Implement flash message system
# ToDo: Error Handling
# ToDo: Dynamic back buttons based on where user just was
# ToDo: Async db calls

@app.route("/", methods=["GET"])
def home():
    year = date.today().year
    month = date.today().month
    
    return redirect(url_for("summary", year=year, month=month))
    
@app.route("/<int:year>/<int:month>", methods=["GET"])
def summary(year:int, month:int):
    prior_year = year
    prior_month = month - 1
    if prior_month == 0:
        prior_month = 12
        prior_year -= 1
        
    next_year = year
    next_month = month + 1
    if next_month == 13:
        next_month = 1
        next_year += 1
        
    last_month = {
        "year": prior_year,
        "month": prior_month,
        "disp": date(prior_year, prior_month, 1).strftime("%B")
    }
    
    next_month = {
        "year": next_year,
        "month": next_month,
        "disp": date(next_year, next_month, 1).strftime("%B")
    }
    cashflow_data = TC.get_cashflow(year, month)
    
    return render_template(
        "home.html",
        cashflow=cashflow_data,
        month=date(year=year, month=month, day=1).strftime("%B"),
        last_month = last_month,
        next_month = next_month
        )
    

@app.route("/transaction", methods=["GET","POST"])
def transactions():
    # ToDo: Default form transaction_date to today
    month_start = date(date.today().year, date.today().month, 1).strftime("%Y-%m-%d")
    today = date.today().strftime("%Y-%m-%d")
    tomorrow = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    last_month_start = date(date.today().year, date.today().month - 1, 1).strftime("%Y-%m-%d")
    last_month_end = (date(date.today().year, date.today().month, 1) - timedelta(days=1)).strftime("%Y-%m-%d")
    
    
    curr_response: TC.TransactionResponse = TC.get_transactions_by_date_range(start=month_start, end=today)
    pend_response: TC.TransactionResponse = TC.get_transactions_by_date_range(start=tomorrow)
    past_response: TC.TransactionResponse = TC.get_transactions_by_date_range(start=last_month_start, end=last_month_end)
    
    form:TransactionForm = TransactionForm()
    account_choices = AC.get_accounts_for_listbox()
    form.category.choices = CC.get_categories_for_listbox()
    form.account.choices = account_choices
    form.transfer_account.choices = account_choices
    
    if form.validate_on_submit():
        if form.transaction_type.data in ('trfr', 'ccp', 'finpay'):
            # Doing the transfer here instead of in Transaction Controller because of access to Account and Category Data.
            # DECISION: Should I just pass that into insert transaction?
            # Get Account and Category information
            transfer_account = [account for account in form.account.choices if account[0] == int(form.transfer_account.data)][0] # type: ignore
            source_account = [account for account in form.account.choices if account[0] == int(form.account.data)][0] # type: ignore
            
            if form.transaction_type.data == 'trfr':
                new_category = [category for category in form.category.choices if category[1] == 'Transfer'][0]
            elif form.transaction_type.data == 'ccp':
                new_category = [category for category in form.category.choices if category[1] == 'Card Payment'][0]
            elif form.transaction_type.data == 'finpay':
                new_category = [category for category in form.category.choices if category[1] == 'Finance Payment'][0]
            else:
                new_category = [1]
                        
            # Set up transfer data
            credit_data:dict = form.to_json()
            credit_data['transaction_type'] = 'credit'
            credit_data['merchant_name'] = transfer_account[1]
            credit_data['category'] = new_category[0]
            
            
            debit_data:dict = form.to_json()
            debit_data['transaction_type'] = 'debit'
            debit_data['merchant_name'] = source_account[1]
            debit_data['account'] = transfer_account[0]
            debit_data['category'] = new_category[0]
            
            # Insert transfer transactions
            # ToDo: Check Responses.  Should probably have a way to roll back credit if debit fails.
            credit_insert_response = TC.insert_transaction(transaction_data=credit_data)
            debit_insert_response = TC.insert_transaction(transaction_data=debit_data)            
            
        else:
            # ToDo: Check Response
            insert_response: TC.TransactionResponse = TC.insert_transaction(transaction_data=form.to_json())
        return redirect(url_for("transactions"))
        
    return render_template(
        "transactions/transactions.html", 
        current_transactions=curr_response["transactions"],
        pending_transactions=pend_response["transactions"],
        past_transactions=past_response["transactions"],
        form=form
        )
    
@app.route("/transaction/<int:transactionid>", methods=['GET','POST'])
def update_transaction(transactionid:int):
    response: TC.TransactionResponse = TC.get_transaction_by_id(transactionid=transactionid)
    
    target_transaction: TransactionInterface = response["transactions"][0]#type: ignore # ToDo: Figure out how to handle multiple return types
    form:TransactionForm = TransactionForm(
        transactionid=target_transaction.transaction.transactionid,
        transaction_date = target_transaction.transaction.transaction_date,
        merchant_name=target_transaction.transaction.merchant_name,
        category=target_transaction.category.categoryid,
        amount=target_transaction.transaction.amount,
        account=target_transaction.account.accountid,
        transaction_type=target_transaction.transaction.transaction_type,
        note=target_transaction.transaction.note,
        transfer_account=1
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
    
@app.route("/transaction/delete/<int:transactionid>", methods=["GET"])
def delete_transaction(transactionid):
    delete_response = TC.delete_transaction(transactionid=transactionid)
    # ToDo: Check Response and flash appropriate message
    return redirect(url_for("transactions"))

@app.route("/transaction/upload", methods=['GET','POST'])
def upload_transaction():
    form = UploadTransactionsForm()
    
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename) # type: ignore
        form.file.data.save(f'uploads/{filename}')
        # Process the upload with TC
        return redirect(url_for("transactions"))
    return render_template("transactions/upload_transactions.html")
    
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
    form.account.choices = AC.get_accounts_for_listbox()
    form.category.choices = CC.get_categories_for_listbox()
    if form.validate_on_submit():
        insert_response = TC.insert_recurring_transaction(form.to_json())
        return redirect(url_for("transactions"))
    return render_template(
        "transactions/recurring_transactions_new.html",
        form=form
    )
    
@app.route("/transaction/recurring/<int:rtranid>", methods=["GET","POST"])
def update_recurring_transaction(rtranid):
    get_response = TC.get_rtran_by_id(rtranid)
    # ToDo: Check Response
    rtran = get_response["transactions"][0]
    form = RecurringTransactionForm(
        rtranid=rtran.transaction.rtranid,
        expected_day=rtran.transaction.expected_day,
        merchant_name=rtran.transaction.merchant_name,
        category=rtran.transaction.categoryid,
        amount=rtran.transaction.amount,
        account=rtran.transaction.accountid,
        transaction_type=rtran.transaction.transaction_type,
        is_monthly=rtran.transaction.is_monthly,
        note=rtran.transaction.note
    )
    
    form.account.choices = AC.get_accounts_for_listbox()
    form.category.choices = CC.get_categories_for_listbox()
    
    if form.validate_on_submit():
        upd_resp = TC.update_recurring_transaction(form.to_json())
        return redirect(url_for("recurring_transactions"))
    return render_template(
        "transactions/recurring_transactions_update.html",
        form=form
    )
    
@app.route("/transaction/recurring/delete/<int:rtranid>", methods=["GET"])
def delete_recurring_transaction(rtranid):
    delete_response = TC.delete_recurring_transaction(rtranid=rtranid)
    # ToDo: Check Response and flash appropriate message
    return redirect(url_for("recurring_transactions"))
    
@app.route("/transaction/recurring/apply", methods=["GET","POST"])
def apply_recurring_transactions():
    get_response = TC.get_all_recurring_transactions()
    monthly_trans = [str(tran.transaction.rtranid) for tran in get_response["transactions"] if tran.transaction.is_monthly == 1]
    form = ApplyRecurringTransactions(
        RTranIDs=",".join(monthly_trans)
    )
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
            "account_name": form.account_name.data,
            "account_type": form.account_type.data,
            "payment_day": form.payment_day.data,
            "statement_day": form.statement_day.data,
            "rewards_features": form.rewards_features.data
        }
        response: AC.AccountResponse = AC.update_account(account_data)
        return redirect(url_for("accounts"))
    return render_template(
        "accounts/account_update.html",
        form=form,
        account=response["accounts"][0]
        )