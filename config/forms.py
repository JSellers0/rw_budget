from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, TextAreaField, SelectMultipleField, SubmitField, DateField, SelectField
from wtforms.validators import (DataRequired, Length)

# ToDo: category as single select field
# ToDo: transactiontype as single select field
# ToDo: transaction date as date selection field

class TransactionForm(FlaskForm):
    tran_types = [
        ('Credit','credit'),
        ('Debit','debit')
    ]
    transaction_date:DateField = DateField("Date", validators=[DataRequired()])
    transaction_type: SelectField = SelectField("Type", choices=tran_types, validators=[DataRequired()])
    merchant_name: StringField = StringField("Merchant", validators=[DataRequired(), Length(max=200)], description="Merchant Name")
    category: SelectField = SelectField("Category", validators=[DataRequired()])
    amount: DecimalField = DecimalField("Transaction Amount", validators=[DataRequired()])
    note: TextAreaField = TextAreaField("Notes")
    submit: SubmitField = SubmitField("Insert")
    
class CategoryForm(FlaskForm):
    category_name: StringField = StringField("Category Name", validators=[DataRequired(), Length(max=200)])
    submit: SubmitField = SubmitField("Submit")
    
class BudgetForm(FlaskForm):
    category_options = ""
    name: StringField = StringField("Budget Name", validators=[DataRequired(), Length(max=200)])
    amount: DecimalField = DecimalField("Budget Amount", validators=[DataRequired()])
    categories: SelectMultipleField = SelectMultipleField("Budget Categories", choices=category_options, validators=[DataRequired()])
    submit: SubmitField = SubmitField("Submit")
    
