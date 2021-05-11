from flask import request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.auth.models import User
from app import db

from app.auth import auth_module

@auth_module.route("/login", methods=['GET', 'POST'])
def login():
  if request.method == "GET":
    return render_template(
      "login.html",
      title="Login"
    )
  else:
    username = request.form.get("username")
    password = request.form.get("password")
    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
      flash("Incorrect username or password.")
      return redirect(url_for("auth.login"))
    login_user(user)
    return redirect(url_for('dashboard.index'))

@auth_module.route("/register", methods=['GET', 'POST'])
def register():
  if request.method == "GET":
    return render_template(
      "register.html",
      title = "Register"
    )
  else:
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()

    if user:
      flash('User address already exists')
      return redirect(url_for('auth.register'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(username=username, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))  


@auth_module.route("/logout")
def logout():
  logout_user()
  return redirect(url_for('auth.login'))