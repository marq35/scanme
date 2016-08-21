from flask import render_template, session, flash, redirect, url_for
from flask.ext.login import login_required, current_user
from .forms import ItemForm
from .. import db
from ..models import Permission, Role, User, Item
from ..decorators import admin_required
from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    form = ItemForm()
    if current_user.can(Permission.ADD) and form.validate_on_submit():
        item = Item(number=form.number.data,
                    name=form.name.data,
                    count=form.count.data,
                    price=form.price.data,
                    sn=form.sn.data,
                    barcode=form.barcode.data,
                    description=form.description.data,
                    author=current_user._get_current_object())
        db.session.add(item)
        return redirect(url_for('.index'))
    items = Item.query.order_by(Item.timestamp.desc()).all()
    return render_template('index.html', form=form, items=items)

@main.route('/item/<number>')
def item(number):
    item = Item.query.filter_by(number=number).first_or_404()
    return render_template('item.html', item=item)