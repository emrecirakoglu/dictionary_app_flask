from flask import Blueprint

search_module = Blueprint('search', __name__, url_prefix='/search', template_folder="templates", static_folder="static")

from . import views