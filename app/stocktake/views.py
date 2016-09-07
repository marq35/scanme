from flask import render_template, abort, flash, redirect, url_for, request,\
    current_app
from flask.ext.login import login_required
from . import stocktake
from .forms import StocktakeForm
from .. import db
from ..models import User, Stocktake


@login_required
@stocktake.route('/menu', methods=['GET', 'POST'])
def menu():
    page = request.args.get('page', 1, type=int)
    st_count = Stocktake.query.count()
    pagination = Stocktake.query.order_by(Stocktake.start_date).paginate(
        page, per_page=current_app.config['SCANME_STOCKS_PER_PAGE'],
        error_out=False)
    stocks = pagination.items
    return render_template('stocktake/menu.html', stocks=stocks,
                           pagination=pagination, st_count=st_count)


@stocktake.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = StocktakeForm()
    if form.validate_on_submit():
        st = Stocktake(name=form.name.data)
        db.session.add(st)
        db.session.commit()
        flash('Stocktake added.')
        return redirect(url_for('.menu'))
    return render_template('add.html', form=form)


@stocktake.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    item = Stocktake.query.get_or_404(id)
    Stocktake.query.filter(Stocktake.id == item.id).delete()
    flash('Stocktake deleted!!!')
    return redirect(url_for('.menu'))