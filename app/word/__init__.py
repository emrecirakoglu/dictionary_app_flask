from flask import Blueprint

word_module = Blueprint('word', __name__, url_prefix='/word')

from . import views