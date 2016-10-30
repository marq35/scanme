from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
import re
from flask_wtf.file import FileField, FileRequired
from wtforms import ValidationError
from wtforms.validators import Required


class StocktakeForm(Form):
    name = StringField('Item name', validators=[Required()])
    submit = SubmitField('Submit')


class UploadCsvFileForm(Form):
    file = FileField('CSV file', validators=[FileRequired()])
    # submit = SubmitField('Choose file')
    #image = FileField('File', validators=[regexp(r'.*.csv$')])
    submit = SubmitField('upload')




