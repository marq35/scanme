from flask import render_template
from flask.ext.login import login_required
from . import stocktake


@login_required
@stocktake.route('/menu')
def menu():
    return render_template('stocktake/menu.html')
