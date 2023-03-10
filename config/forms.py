from tkinter.tix import Select
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, TextAreaField, SelectMultipleField, SubmitField
from wtforms.validators import (DataRequired, Length)

class TransactionForm(FlaskForm):
    merchant: StringField = StringField("Merchant", validators=[DataRequired(), Length(max=200)])
    category: StringField = StringField("Category", validators=[DataRequired(), Length(max=200)])
    amount: DecimalField = DecimalField("Transaction Amount", validators=[DataRequired()])
    note: TextAreaField = TextAreaField("Notes")
    submit: SubmitField = SubmitField("Submit")
    
class CategoryForm(FlaskForm):
    name: StringField = StringField("Category Name", validators=[DataRequired(), Length(max=200)])
    submit: SubmitField = SubmitField("Submit")
    
class BudgetForm(FlaskForm):
    category_options = ""
    name: StringField = StringField("Budget Name", validators=[DataRequired(), Length(max=200)])
    amount: DecimalField = DecimalField("Budget Amount", validators=[DataRequired()])
    categories: SelectMultipleField = SelectMultipleField("Budget Categories", choices=category_options, validators=[DataRequired()])
    submit: SubmitField = SubmitField("Submit")
    
