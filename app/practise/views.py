import random
from flask.json import jsonify
from app.word.models import Definition, Word
from app.word import views as word_api 
from flask import request, render_template
from flask_login.utils import login_required

from app.practise import practice_module

@practice_module.route("/", methods=['GET', 'POST'])
@login_required
def index():

  # check user have minimum 10 word if less than 10 return 
  count_of_word = get_count_of_word()
  if count_of_word < 10 :
    return render_template(
      "practise.html",
      title = "Practise",
      count_of_word = count_of_word,
    )

  # get a random definition
  random_correct_definition = get_random_definition()

  # answer of practise  
  correct_word_option = random_correct_definition.word

  # generate wrong answers
  first_wrong_answer = get_random_word_expect_given(correct_word_option)
  second_wrong_answer = get_random_word_expect_given(first_wrong_answer, correct_word_option)

  all_options = [correct_word_option, first_wrong_answer, second_wrong_answer]

  #increase by one appeared count of word
  for word in all_options:
    word_api.increase_appeared_count(word)

  return render_template(
    "practise.html",
    title = "Practise",
    count_of_word = count_of_word,
    definition=random_correct_definition,
    options = all_options
  )

@practice_module.route("/check", methods=['GET', 'POST'])
@login_required
def check_answer():
  data = request.form.to_dict()
  other_answers = request.form.getlist('other_answers[]') 

  definition_id, selected_word, x = data.values() 

  if selected_word == Definition.query.get(definition_id).word.name:
    word_api.increase_practising_point(word_api.getByName(selected_word))
    return jsonify(success=True, status_code=200, message="Correct Answer!",ContentType="application/json"), 200
  else:
    word_api.decrease_by_two_practising_point(word_api.getByName(selected_word))
    for word in other_answers:
      word_api.decrease_by_one_practising_point(word_api.getByName(word))
    return jsonify(success=False, status_code=400, message= "Wrong Answer!",  ContentType="application/json"), 400

def get_count_of_word() -> int:
  """
    Get count of word that user have
  """
  return len(word_api.get_all())

def get_random_definition() -> Definition:
  """
    Get random word definition for practice
  """
  count_of_all_definitions = len(word_api.get_all_definitions())
  random_definition_id = random.randint(1, count_of_all_definitions)
  return Definition.query.get(random_definition_id)

def get_random_word_expect_given(*args) -> Word:
  """
    Get random words for practice options
    @param: word or words to be excluded
  """
  all_words = word_api.get_all()
  all_other_words = [word for word in all_words if word not in list(args)]
  return random.choice(all_other_words)