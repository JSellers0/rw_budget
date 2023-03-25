from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectMultipleField, SubmitField, DateField, SelectField, HiddenField
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
    
    def to_json(self):
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
    note: StringField = StringField("Notes")
    submit: SubmitField = SubmitField("Insert")
    
class CategoryForm(FlaskForm):
    category_name: StringField = StringField("Category Name", validators=[DataRequired(), Length(max=200)])
    submit: SubmitField = SubmitField("Submit")
    
    def to_json(self):
        return {
            "category_name": self.category_name.data
        }
    
class BudgetForm(FlaskForm):
    category_options = ""
    name: StringField = StringField("Budget Name", validators=[DataRequired(), Length(max=200)])
    amount: DecimalField = DecimalField("Budget Amount", validators=[DataRequired()])
    categories: SelectMultipleField = SelectMultipleField("Budget Categories", choices=category_options, validators=[DataRequired()])
    submit: SubmitField = SubmitField("Submit")
    
class AccountForm(FlaskForm):
    account_name: StringField = StringField("Account Name", validators=[DataRequired(), Length(max=200)])
    account_type: StringField = StringField("Account Type", validators=[DataRequired(), Length(max=100)])
    payment_day: StringField = StringField("Payment Due Date", validators=[DataRequired(), Length(max=50)])
    statement_day: StringField = StringField("Statement Date", validators=[DataRequired(), Length(max=50)])
    rewards_features: StringField = StringField("Rewards Features", validators=[DataRequired(), Length(max=300)])
    submit: SubmitField = SubmitField("Submit")
    
    
