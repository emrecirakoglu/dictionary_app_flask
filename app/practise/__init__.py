from flask import Blueprint

practice_module = Blueprint('practise', __name__, url_prefix='/practise', template_folder="templates")

from . import views