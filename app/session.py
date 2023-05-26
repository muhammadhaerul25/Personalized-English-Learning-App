from datetime import timedelta

from flask import session, jsonify
from flask_session import Session

import prompts as prompt
from prompts import custom_prompt


#PROMPT SESSION
pronunciation_dict = {}
context_dict = {}
reading_dict = {}
placement_test_dict = {}
study_plan_dict = {}

#TOKENS SESSION
tokens_used_dict = {}
tokens_had_dict = {}

#SESSION FUNCTIONS
def configure_session(app):
    app.config['SECRET_KEY'] = 'personalized_english_learning'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(weeks=1)
    Session(app)

def configure_sesion_name(app, user_id):
    app.config['SESSION_COOKIE_NAME'] = 'session_' + str(user_id)

def create_session(user):
    user_id = user["_id"]
    session['user'] = user_id
    create_prompt_session('all', user)
    create_tokens_session(user)


def check_session():
    if session.get('user'):
        return True
    else:
        return False
    

def delete_session():
    session.pop('user', None)


#PROMPT SESSION FUNCTIONS
def create_prompt_session(dictionary_name, user):
    user_id = user['_id']
    if dictionary_name == "all":
        pronunciation_dict[user_id] = custom_prompt(prompt.pronunciation_prompt.copy(), user["name"], user["english_level"], "pronunciation, speaking and conversation")
        context_dict[user_id] = custom_prompt(prompt.context_prompt.copy(), user["name"], user["english_level"], "context, vocabulary, and grammar")
        reading_dict[user_id] = custom_prompt(prompt.reading_prompt.copy(), user["name"], user["english_level"], "reading and writing")
        placement_test_dict[user_id] = custom_prompt(prompt.placement_test_prompt.copy(), user["name"], user["english_level"], "placement test")
        study_plan_dict[user_id] = custom_prompt(prompt.study_plan_prompt.copy(), user["name"], user["english_level"], "study plan")
    elif dictionary_name == "pronunciation_dict":
        pronunciation_dict[user_id] = custom_prompt(prompt.pronunciation_prompt.copy(), user["name"], user["english_level"], "pronunciation, speaking and conversation")
    elif dictionary_name == "context_dict":
        context_dict[user_id] = custom_prompt(prompt.context_prompt.copy(), user["name"], user["english_level"], "context, vocabulary, and grammar")
    elif dictionary_name == "reading_dict":
        reading_dict[user_id] = custom_prompt(prompt.reading_prompt.copy(), user["name"], user["english_level"], "reading and writing")
    elif dictionary_name == "placement_test_dict":
        placement_test_dict[user_id] = custom_prompt(prompt.placement_test_prompt.copy(), user["name"], user["english_level"], "placement test")
    elif dictionary_name == "study_plan_dict":
        study_plan_dict[user_id] = custom_prompt(prompt.study_plan_prompt.copy(), user["name"], user["english_level"], "study plan")



def check_prompt_session():
    user_id = session.get('user')
    if user_id not in pronunciation_dict:
        return False
    if user_id not in context_dict:
        return False
    if user_id not in reading_dict:
        return False
    if user_id not in placement_test_dict:
        return False
    if user_id not in study_plan_dict:
        return False
    return True


def recreate_placement_test_prompt_session(user):
    user_id = user["_id"]
    del placement_test_dict[user_id]
    create_prompt_session("placement_test_dict", user)


def recreate_study_plan_prompt_session(user):
    user_id = user["_id"]
    del study_plan_dict[user_id]
    create_prompt_session("study_plan_dict", user)


#TOKENS SESSION FUNCTIONS
def create_tokens_session(user):
    user_id = user["_id"]
    tokens_had_dict[user_id] = user['tokens_had']
    tokens_used_dict[user_id] = user['tokens_used']



def update_tokens_session(user_id, new_tokens_had, new_tokens_used):
    tokens_had_dict[user_id] = new_tokens_had
    tokens_used_dict[user_id] = new_tokens_used
