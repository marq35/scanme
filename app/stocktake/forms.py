from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required


class StocktakeForm(Form):
    name = StringField('Item name', validators=[Required()])
    submit = SubmitField('Submit')
