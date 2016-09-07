from flask import render_template, abort, flash, redirect, url_for, request,\
    current_app
from flask.ext.login import login_required
from . import stocktake
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


@login_required
@stocktake.route('/delete')
def delete():
    pass