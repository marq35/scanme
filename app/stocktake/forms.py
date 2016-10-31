from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField
from flask_wtf.file import FileField, FileRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required, regexp


class StocktakeForm(Form):
    name = StringField('Item name', validators=[Required()])
    submit = SubmitField('Submit')


class UploadCsvFileForm(Form):
    file = FileField('Choose CSV file:', validators=[FileRequired(), regexp(r'.*.csv$')])
    stock = SelectField()
    submit = SubmitField('upload')




