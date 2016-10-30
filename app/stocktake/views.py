from flask import render_template, abort, flash, redirect, url_for, request,\
    current_app
from flask.ext.login import login_required, current_user
from . import stocktake
from .forms import StocktakeForm, UploadCsvFileForm
from .. import db
from ..models import User, Stocktake, Item, StItem
from werkzeug import secure_filename
import os


@login_required
@stocktake.route('/menu', methods=['GET', 'POST'])
def menu():
    page = request.args.get('page', 1, type=int)
    pagination = Stocktake.query.order_by(Stocktake.start_date).paginate(
        page, per_page=current_app.config['SCANME_STOCKS_PER_PAGE'],
        error_out=False)
    stocks = pagination.items
    return render_template('stocktake/menu.html', stocks=stocks,
                           pagination=pagination)


@stocktake.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = StocktakeForm()
    if form.validate_on_submit():
        st = Stocktake(name=form.name.data)
        db.session.add(st)
        db.session.commit()
        items = Item.get_items()
        for item in items:
            st_item = StItem(number=item.number,
                             name=item.name,
                             count=item.count,
                             price=item.price,
                             sn=item.sn,
                             barcode=item.barcode,
                             description=item.description,
                             stocktake=st.id)
            db.session.add(st_item)
            db.session.commit()
        flash('Stocktake created.')
        return redirect(url_for('.menu'))
    return render_template('add.html', form=form)


@stocktake.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    item = Stocktake.query.get_or_404(id)
    Stocktake.query.filter(Stocktake.id == item.id).delete()
    flash('Stocktake deleted!!!')
    return redirect(url_for('.menu'))


@login_required
@stocktake.route('/stitem/<int:id>', methods=['GET', 'POST'])
def stitem(id):
    stitems = StItem.query.filter_by(stocktake=id)
    return render_template('stocktake/stitem.html', stitems=stitems)


@login_required
@stocktake.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadCsvFileForm()
    if request.method == 'POST':
        f = request.files['file']
        f.save('app/uploads/' + secure_filename(f.filename))
        flash('Uploaded')
        return redirect(url_for('.menu'))
    return render_template('stocktake/upload.html', form=form)

