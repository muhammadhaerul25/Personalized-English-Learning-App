from flask import session
from flask_session import Session
import prompts as prompt


#PROMPT SESSION
pronunciation_dict = {}
context_dict = {}
reading_dict = {}
placement_test_dict = {}
study_plan_dict = {}

#SESSION
def configure_session(app):
    app.config['SECRET_KEY'] = 'personalized_english_learning'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = True
    Session(app)

def create_session(user):
    session["user"] = user["_id"]
    pronunciation_dict[session["user"]] = prompt.pronunciation_prompt.copy()
    context_dict[session["user"]] = prompt.context_prompt.copy()  
    reading_dict[session["user"]] = prompt.reading_prompt.copy()
    placement_test_dict[session["user"]] = prompt.placement_test_prompt.copy()
    study_plan_dict[session["user"]] = prompt.study_plan_prompt.copy()
    

def check_session():
    if session.get('user'):
        return True
    else:
        return False
    

def delete_session():
    session.clear()
