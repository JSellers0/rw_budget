from config.forms import TransactionForm, CategoryForm
from controllers import TransactionController as tc, CategoryController as cc
from datetime import date
from flask import render_template, redirect, url_for
from app import app

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/transactions", methods=["GET","POST"])
def transactions():
    transactions = tc.get_all_transactions()
    form:TransactionForm = TransactionForm()
    form.category.choices = cc.get_all_categories()
    if form.validate_on_submit():
        transaction_data = {
            "transaction_date": date.today(),
            "transaction_type": form.transaction_type.data,
            "merchant_name": form.merchant_name.data,
            "amount": form.amount.data,
            "categoryid": form.category.data,
            "note": form.note.data
        }
        
        tr = tc.insert_transaction(transaction_data=transaction_data)
        return redirect(url_for("transactions"))
        # ToDo: Flash insert failure
        # ToDo: Implement flash message system
        
    return render_template(
        "transactions/transactions.html", 
        transactions=transactions,
        form=form
        )
    
@app.route("/transactions/<int:transaction_id>", methods=['GET','POST'])
def update_transaction(transaction_id:int):
    form:TransactionForm = TransactionForm()
    transaction = tc.get_transaction_by_id(transactionid=transaction_id).to_json()
    categories = cc.get_all_categories()
    
    if form.validate_on_submit():
        
        transaction_data = {
            "transaction_date": form.transaction_date.data,
            "transaction_type": form.transaction_type.data,
            "merchant_name": form.merchant_name.data,
            "amount": form.amount.data,
            "categoryid": form.category.data,
            "note": form.note.data
        }
        
        tr = tc.update_transaction(transaction_data=transaction_data)
        
        return redirect(url_for("transactions"))
                  
    return render_template(
        "transactions/transaction_update.html",
        transaction=transaction,
        categories=categories,
        form=form
    )
    
@app.route("/category/new", methods=["GET","POST"])
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        cc.insert_category(form.category_name.data)
        return redirect(url_for("transactions"))
    return render_template("categories/category_new.html")

@app.route("/budgets", methods=["GET"])
def budgets():
    return render_template("budgets.html")

@app.route("/accounts", methods=["GET"])
def accounts():
    return render_template("accounts.html")