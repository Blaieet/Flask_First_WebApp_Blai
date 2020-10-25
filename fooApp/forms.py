from wtforms import Form
from wtforms import TextAreaField, TextField, FloatField
from wtforms.validators import Length, NumberRange,required

class ProductForm(Form):
    name = TextField('Name', [Length(max=255)])
    description = TextAreaField('Description')
    price = FloatField('price',[NumberRange(0.00),required()])