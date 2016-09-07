from flask import Blueprint


stocktake = Blueprint('stocktake', __name__)

from . import views
