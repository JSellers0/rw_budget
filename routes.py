from config.forms import TransactionForm
from controllers import TransactionController as tc
from datetime import date
from flask import render_template, redirect, url_for
from app import app

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/transactions", methods=["GET","POST"])
def transactions():
    transactions = tc.get_all_transactions()
    form = TransactionForm()
    if form.validate_on_submit():
        transaction_data = {
            "transaction_date": date.today(),
            "categoryid": form.category.data,
            "merchant_name": form.merchant_name.data,
            "transaction_type": form.transaction_type.data,
            "amount": form.amount.data,
            "note": form.note.data
        }
        tr = tc.insert_transaction(transaction_data=transaction_data)
        if tr["state"] == "SUCCESS":
            return redirect(url_for("transactions"))
        # ToDo: Flash insert failure
        # ToDo: Implement flash message system
        
    return render_template(
        "transactions/transactions.html", 
        transactions=transactions,
        form=form
        )

@app.route("/budgets", methods=["GET"])
def budgets():
    return render_template("budgets.html")

@app.route("/accounts", methods=["GET"])
def accounts():
    return render_template("accounts.html")