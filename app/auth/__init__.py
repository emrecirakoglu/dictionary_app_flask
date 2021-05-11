from flask import Blueprint

auth_module = Blueprint('auth', __name__, url_prefix='/auth', template_folder="templates", static_folder="static")

from . import views