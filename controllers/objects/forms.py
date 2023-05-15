from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from typing import Any
from wtforms import StringField, BooleanField, DecimalField, SubmitField, DateField, SelectField, HiddenField, IntegerField
from wtforms.validators import (DataRequired, Length)

TRAN_TYPES = [
        ('credit','Credit'),
        ('debit','Debit'),
        ('ccp','Card Pmnt'),
        ('trfr', 'Transfer'),
        ('fin', 'Finance Purchase'),
        ('finpay', 'Finance Payment')
    ]

class TransactionForm(FlaskForm):
    transactionid: HiddenField = HiddenField("Transactionid")
    transaction_date:DateField = DateField("Transaction Date", validators=[DataRequired()])
    cashflow_date:DateField = DateField("Cashflow Date", validators=[DataRequired()])
    transaction_type: SelectField = SelectField("Transaction Type", choices=TRAN_TYPES, validators=[DataRequired()])
    merchant_name: StringField = StringField("Merchant", validators=[DataRequired(), Length(max=200)])
    transfer_account: SelectField = SelectField("Transfer To", choices=['placeholder'])
    category: SelectField = SelectField("Category", validators=[DataRequired()])
    amount: DecimalField = DecimalField("Amount", validators=[DataRequired()])
    account: SelectField = SelectField("Account", validators=[DataRequired()])
    note: StringField = StringField("Notes")
    submit: SubmitField = SubmitField("Insert")
    
    def to_json(self) -> dict[str, Any]:
        return {
            "transactionid": self.transactionid.data,
            "transaction_date": self.transaction_date.data,
            "cashflow_date": self.cashflow_date.data,
            "merchant_name": self.merchant_name.data,
            "transfer_account": self.transfer_account.data,
            "category": self.category.data,
            "amount": self.amount.data,
            "account": self.account.data,
            "transaction_type": self.transaction_type.data,
            "note": self.note.data,
        }
    
class RecurringTransactionForm(FlaskForm):
    rtranid: HiddenField = HiddenField("RecuringTransactionID")
    expected_day: StringField = StringField("Expected Day of Transaction", validators=[DataRequired(), Length(max=200)])
    merchant_name: StringField = StringField("Merchant", validators=[DataRequired(), Length(max=200)])
    category: SelectField = SelectField("Category", validators=[DataRequired()])
    amount: DecimalField = DecimalField("Amount", validators=[DataRequired()])
    account: SelectField = SelectField("Account", validators=[DataRequired()])
    transaction_type: SelectField = SelectField("Transaction Type", choices=TRAN_TYPES, validators=[DataRequired()])
    note: StringField = StringField("Notes")
    is_monthly: BooleanField = BooleanField("Monthly Transaction")
    submit: SubmitField = SubmitField("Insert")
    
    def to_json(self) -> dict[str, Any]:
        return {
            "rtranid": self.rtranid.data,
            "expected_day": self.expected_day.data,
            "merchant_name": self.merchant_name.data,
            "category": self.category.data,
            "amount": self.amount.data,
            "account": self.account.data,
            "transaction_type": self.transaction_type.data,
            "is_monthly": self.is_monthly.data,
            "note": self.note.data,
        }
        
class ApplyRecurringTransactions(FlaskForm):
    RTranIDs: StringField = StringField("List recurring transaction ids:")
    month: IntegerField = IntegerField("Month to apply rtrans to this year:")
    submit: SubmitField = SubmitField("Apply")
    
    def to_json(self) -> dict[str, Any]:
        return {
            "RTranIDs": self.RTranIDs.data,
            "month": self.month.data
        }
    
class CategoryForm(FlaskForm):
    category_name: StringField = StringField("Category Name", validators=[DataRequired(), Length(max=200)])
    submit: SubmitField = SubmitField("Submit")
    
    def to_json(self) -> dict[str, Any]:
        return {
            "category_name": self.category_name.data
        }
    
class BudgetForm(FlaskForm):
    budgetid: HiddenField = HiddenField("BudgetID")
    budget_name: StringField = StringField("Budget Name", validators=[DataRequired(), Length(max=200)])
    budget_amount: DecimalField = DecimalField("Budget Amount", validators=[DataRequired()])
    category: SelectField = SelectField("Budget Category", validators=[DataRequired()])
    submit: SubmitField = SubmitField("Submit")
    
    def to_json(self) -> dict[str, Any]:
        return {
            "budgetid": self.budgetid.data,
            "budget_name": self.budget_name.data,
            "budget_amount": self.budget_amount.data,
            "category": self.category.data,
        }
    
class AccountForm(FlaskForm):
    accountid: HiddenField = HiddenField("AccountID")
    account_name: StringField = StringField("Account Name", validators=[DataRequired(), Length(max=200)])
    account_type: StringField = StringField("Account Type", validators=[DataRequired(), Length(max=100)])
    payment_day: StringField = StringField("Payment Due Date", validators=[Length(max=50)])
    statement_day: StringField = StringField("Statement Date", validators=[Length(max=50)])
    rewards_features: StringField = StringField("Rewards Features", validators=[Length(max=300)])
    submit: SubmitField = SubmitField("Submit")
    
    def to_json(self) -> dict[str, Any]:
        return {
            "accountid": self.accountid.data,
            "account_name": self.account_name.data,
            "account_type": self.account_type.data,
            "payment_day": self.payment_day.data,
            "statement_day": self.statement_day.data,
            "rewards_features": self.rewards_features.data
        }
    
class UploadTransactionsForm(FlaskForm):
    file = FileField()
    submit: SubmitField = SubmitField("Upload")
