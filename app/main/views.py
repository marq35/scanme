from flask import render_template, abort, flash, redirect, url_for, request,\
    current_app
from flask.ext.login import login_required, current_user
from .forms import ItemForm
from .. import db
from ..barcode_gen import generate_barcode, delete_barcode, barcode_file_exists
from ..models import Permission, Role, User, Item
from ..decorators import admin_required
from . import main
import random


@main.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Item.query.order_by(Item.number).paginate(
        page, per_page=current_app.config['SCANME_ITEMS_PER_PAGE'],
        error_out=False)
    items = pagination.items
    return render_template('index.html', items=items,
                           pagination=pagination)


@main.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = ItemForm()
    if form.validate_on_submit():
        item = Item(number=form.number.data,
                    name=form.name.data,
                    count=form.count.data,
                    price=form.price.data,
                    sn=form.sn.data,
                    barcode=form.barcode.data,
                    description=form.description.data,
                    author=current_user._get_current_object())
        db.session.add(item)
        db.session.commit()
        generate_barcode(form.barcode.data)
        flash('Item added.')
        return redirect(url_for('.index'))
    form.barcode.data = random.randrange(11111111, 99999999)
    return render_template('add.html', form=form)


@main.route('/item/<id>')
def item(id):
    item = Item.query.get_or_404(id)
    return render_template('item.html', item=item)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    item = Item.query.get_or_404(id)
    form = ItemForm()
    if form.validate_on_submit():
        item.number = form.number.data
        item.name = form.name.data
        item.count = form.count.data
        item.price = form.price.data
        item.sn = form.sn.data
        item.barcode = form.barcode.data
        item.description = form.description.data
        db.session.add(item)
        flash('The item has been updated.')
        return redirect(url_for('.item', id=item.id))
    form.number.data = item.number
    form.name.data = item.name
    form.count.data = item.count
    form.price.data = item.price
    form.sn.data = item.sn
    form.barcode.data = item.barcode
    form.description.data = item.description
    return render_template('edit_item.html', form=form)


@main.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    item = Item.query.get_or_404(id)
    Item.query.filter(Item.id == item.id).delete()
    barcode_value = '{0}.png'.format(item.barcode)
    if barcode_file_exists(barcode_value):
        delete_barcode(barcode_value)
    flash('Item deleted!!!')
    return redirect(url_for('.index'))
