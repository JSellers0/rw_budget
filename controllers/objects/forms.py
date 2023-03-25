from flask_wtf import FlaskForm
from typing import Any
from wtforms import StringField, IntegerField, DecimalField, SubmitField, DateField, SelectField, HiddenField
from wtforms.validators import (DataRequired, Length)

# ToDo: category as single select field
# ToDo: transactiontype as single select field
# ToDo: transaction date as date selection field

class TransactionForm(FlaskForm):
    tran_types = [
        ('credit','Credit'),
        ('debit','Debit'),
        ('pending','Pending'),
        ('ccp','Card Pmnt'),
    ]
    transactionid: HiddenField = HiddenField("Transactionid")
    transaction_date:DateField = DateField("Date", validators=[DataRequired()])
    transaction_type: SelectField = SelectField("Type", choices=tran_types, validators=[DataRequired()])
    merchant_name: StringField = StringField("Merchant", validators=[DataRequired(), Length(max=200)])
    category: SelectField = SelectField("Category", validators=[DataRequired()])
    account: SelectField = SelectField("Account", validators=[DataRequired()])
    amount: DecimalField = DecimalField("Amount", validators=[DataRequired()])
    note: StringField = StringField("Notes")
    submit: SubmitField = SubmitField("Insert")
    
    def to_json(self) -> dict[str, Any]:
        return {
            "transactionid": self.transactionid.data,
            "transaction_date": self.transaction_date.data,
            "transaction_type": self.transaction_type.data,
            "merchant_name": self.merchant_name.data,
            "category": self.category.data,
            "account": self.account.data,
            "amount": self.amount.data,
            "note": self.note.data,
        }
    
class RecurringTransactionForm(FlaskForm):
    rtranid: HiddenField = HiddenField("RecuringTransactionID")
    merchant_name: StringField = StringField("Merchant", validators=[DataRequired(), Length(max=200)])
    category: SelectField = SelectField("Category", validators=[DataRequired()])
    account: SelectField = SelectField("Account", validators=[DataRequired()])
    amount: DecimalField = DecimalField("Amount", validators=[DataRequired()])
    expected_day: StringField = StringField("Expected Day of Transaction", validators=[DataRequired(), Length(max=200)])
    recur_interval_type: SelectField = SelectField("Recurrance Interval", validators=[DataRequired()])
    recur_interval: IntegerField = IntegerField("Recurrance Interval", validators=[DataRequired()])
    note: StringField = StringField("Notes")
    submit: SubmitField = SubmitField("Insert")
    
    def to_json(self) -> dict[str, Any]:
        return {
            "rtranid": self.rtranid.data,
            "merchant_name": self.merchant_name.data,
            "category": self.category.data,
            "account": self.account.data,
            "amount": self.amount.data,
            "expected_day": self.expected_day.data,
            "recur_interval_type": self.recur_interval_type.data,
            "recur_interval": self.recur_interval.data,
            "note": self.note.data,
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
    category: SelectField = SelectField("Budget Categories", validators=[DataRequired()])
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
    payment_day: StringField = StringField("Payment Due Date", validators=[DataRequired(), Length(max=50)])
    statement_day: StringField = StringField("Statement Date", validators=[DataRequired(), Length(max=50)])
    rewards_features: StringField = StringField("Rewards Features", validators=[DataRequired(), Length(max=300)])
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
    
    
