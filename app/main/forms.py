from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField, IntegerField, FloatField
from wtforms.validators import Required, Length, Regexp
from wtforms import ValidationError
from ..models import Item, User, Role


class ItemForm(Form):
    number = StringField('Item inventory number', validators=[Required()])
    name = StringField('Item name', validators=[Required()])
    count = IntegerField('Item count', validators=[Required()])
    price = FloatField('Item prize per piece', validators=[Required()])
    sn = StringField('Item serial number')
    barcode = StringField('Item barcode')
    description = TextAreaField('Item description')
    submit = SubmitField('Submit')

    def validate_item_number(self, field):
        if field.data != self.item.number and \
                Item.query.filter_by(number=field.data).first():
            raise ValidationError('Item with this inventory number exists.')

    def validate_item_serial_number(self, field):
        if field.data != self.item.sn and \
                Item.query.filter_by(sn=field.data).first():
            raise ValidationError('Item with this serial number exists.')

    def validate_item_barcode(self, field):
        if field.data != self.item.barcode and \
                Item.query.filter_by(barcode=field.data).first():
            raise ValidationError('Item with this barcode exists.')