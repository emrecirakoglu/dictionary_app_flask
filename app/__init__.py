from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager

app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(Exception)
def handle_error(error):
    return render_template('500.html', error=str(error)), 500

# Import a modules
from app.auth import auth_module
from app.dashboard import dashboard_module
from app.search import search_module
from app.practise import practice_module
from app.word import word_module

# Register blueprint(s)
app.register_blueprint(auth_module)
app.register_blueprint(dashboard_module)
app.register_blueprint(search_module)
app.register_blueprint(practice_module)
app.register_blueprint(word_module)

db.create_all()

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from app.auth.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))