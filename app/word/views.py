from typing import List
from flask import json, request, render_template, redirect, url_for, flash, jsonify
from flask_login.utils import login_required
from flask_login import current_user
from app import db
from .models import Word, Definition
from app.word import word_module
from werkzeug.exceptions import NotFound
import random

@word_module.route("/", methods=['GET'])
@login_required
def get_all() -> list:
  """
  Return all words that logged in user has
  """
  all_words = Word.query.filter_by(user_id=current_user.id).all()
  return all_words

@word_module.route("/<int:id>", methods=['GET'])
@login_required
def getByid(id):
  try:
    word = Word.query.get_or_404(id)
  except NotFound:
    return None
  return word

@login_required
def getByName(word):
  return Word.query.filter_by(name=word).first()

@word_module.route("/add", methods=['POST'])
@login_required
def add():
  """
  Add word to personal dictionary
  """
  data = eval(request.get_json())
  word_text = data.get('word')
  definitions = data.get('definitions')

  #check word exist in Database
  if bool(Word.query.filter_by(name=word_text).first()):
    error_message = f"\"{word_text}\" allready exist in favorites"
    return jsonify(success=False, status_code=409, message=error_message, ContentType="application/json"), 409
  
  word = Word(name = word_text, user=current_user)
  db.session.add(word)

  for definition in definitions:
    db.session.add(Definition(content=definition, word=word))

  db.session.commit()

  return jsonify(success=True, status_code=200, message=f"\"{word_text}\" added to favorites.", ContentType="application/json"), 200

@word_module.route("/delete/<int:id>", methods=['GET'])
@login_required
def delete(id):
  pass

@login_required
def get_all_definitions():
  """
  Return all definitions that logged in user have
  """
  all_definitions = Definition.query.all()
  users_all_definition = list(filter(lambda definition: definition.word.user_id == current_user.id, all_definitions))
  return users_all_definition

def increase_searched_count(word: Word):
  """
  Increases by one searched count words.
  """
  word.searched_count = word.searched_count + 1
  db.session.commit()

def increase_appeared_count(word: Word):
  """
  Increases by one appeared count of word.
  """
  word.appeared_count = word.appeared_count + 1
  db.session.commit()

def increase_practising_point(word:Word):
  """
  Increases by one practising point of word.
  """
  word.practising_point = word.practising_point + 1
  db.session.commit()
  
def decrease_by_two_practising_point(word:Word):
  """
  Decreases by two practising point of word.
  """
  word.practising_point = word.practising_point - 2
  db.session.commit()

def decrease_by_one_practising_point(word:Word):
  """
  Decreases by one practising point of word.
  """
  word.practising_point = word.practising_point - 1
  db.session.commit()
