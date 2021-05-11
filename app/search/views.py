from flask import json, request, render_template, redirect, url_for, flash,jsonify
from flask_login.utils import login_required
import requests
from config import WORDS_API_URL, WORDS_API_HEADERS

from app.word import views as word_api
from app.search import search_module

@search_module.route("/", methods=['GET', 'POST'])
@login_required
def index():
  return render_template(
    "search.html",
    title = "Search"
  )

#Search a word from WordApi
@search_module.route("/api", methods=['GET', 'POST'])
@login_required
def search_from_api():
  word = request.form.get("word")

  #Check word added personal dictionary, if exist increase searced count
  word_in_dictionary = word_api.getByName(word)
  if word_in_dictionary:
    word_api.increase_searched_count(word_in_dictionary)

  url = WORDS_API_URL + word
  response = requests.request("GET", url, headers=WORDS_API_HEADERS).json()
  try:
    data = {
      'word': response['word'],
      'definitions': list(map(lambda result: result['definition'], response['results']))
    }
  except KeyError:
    flash("Word not found.", 'error')
    return redirect(url_for('search.index'))

  flash(data, 'info')
  return redirect(url_for('search.index'))
