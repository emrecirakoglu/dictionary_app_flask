from flask import Blueprint

dashboard_module = Blueprint('dashboard', __name__, url_prefix='', template_folder="templates", static_folder="static")

from . import views