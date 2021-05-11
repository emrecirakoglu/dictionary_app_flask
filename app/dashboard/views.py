from flask import request, render_template, redirect, url_for, flash
from flask_login.utils import login_required
from app.word import views as word_api
from app.dashboard import dashboard_module
from flask_login import current_user

@dashboard_module.route("/", methods=['GET', 'POST'])
def index():
  if not current_user.is_authenticated:
    return redirect(url_for("auth.login"))

  words = word_api.get_all()
  return render_template(
    "dashboard.html",
    title = "Dashboard",
    words = words,
  )