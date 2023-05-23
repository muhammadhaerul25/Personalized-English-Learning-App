from flask import session
from flask_session import Session
import prompts as prompt
from prompts import custom_prompt
from database import User, Learning, PlacementTest, StudyPlan


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
    app.config['SESSION_PERMANENT'] = False
    Session(app)

def create_session(user):
    user_session = session["user"] = user["_id"]
    create_prompt_session(user_session, user)

def check_session():
    if session.get('user'):
        return True
    else:
        return False
    
def delete_session():
    session.clear()

def create_prompt_session(user_session, user):
    pronunciation_dict[user_session] = custom_prompt(prompt.pronunciation_prompt.copy(), user["name"], user["english_level"], "pronunciation, speaking and conversation")
    context_dict[user_session] = custom_prompt(prompt.context_prompt.copy(), user["name"], user["english_level"], "context, vocabulary, and grammar")
    reading_dict[user_session] = custom_prompt(prompt.reading_prompt.copy(), user["name"], user["english_level"], "reading and writing")
    placement_test_dict[user_session] = custom_prompt(prompt.placement_test_prompt.copy(), user["name"], user["english_level"], "placement test")
    study_plan_dict[user_session] = custom_prompt(prompt.study_plan_prompt.copy(), user["name"], user["english_level"], "study plan")
    add_data_to_prompt_session(user_session, user)
    

def add_data_to_prompt_session(user_session, user):
    learning_history = Learning.get_chat_history(user["_id"])
    if len(learning_history) > 30:
        learning_history = learning_history[:30]
    for data in learning_history:
        if data["mode"] == "pronunciation":
            pronunciation_dict[user_session].append({"role": "user", "content": data["message"]})
            pronunciation_dict[user_session].append({"role": "assistant", "content": data["response"]})
        elif data["mode"] == "context":
            context_dict[user_session].append({"role": "user", "content": data["message"]})
            context_dict[user_session].append({"role": "assistant", "content": data["response"]})
        elif data["mode"] == "reading":
            reading_dict[user_session].append({"role": "user", "content": data["message"]})
            reading_dict[user_session].append({"role": "assistant", "content": data["response"]})
        