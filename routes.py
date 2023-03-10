from controllers import TransactionController
from flask import render_template
from app import app

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/transactions", methods=["GET"])
def transactions():
    return render_template("transactions.html")

@app.route("/budgets", methods=["GET"])
def budgets():
    return render_template("budgets.html")

@app.route("/accounts", methods=["GET"])
def accounts():
    return render_template("accounts.html")