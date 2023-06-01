#MODULES
import os
import time
import threading

#PACKAGES
import schedule
from flask import Flask, request
from flask import render_template, jsonify, redirect, url_for
from flask_dance.contrib.google import google


#FILES
import prompts as prompt
from auth import configure_google_oauth, client
from session import session, pronunciation_dict, context_dict, reading_dict, placement_test_dict, study_plan_dict
from session import configure_session, configure_sesion_name,create_session, check_session, delete_session, check_prompt_session, recreate_placement_test_prompt_session, recreate_study_plan_prompt_session 
from models import chatgpt
from database import User, Learning, PlacementTest, StudyPlan

from config import MESSAGES, TIME_OF_TOKENS_UPDATE
from helpers import extract_english_level, is_any_english_level, cut_messages 


#FLASK-APP
app = Flask(__name__, static_folder='static', template_folder='templates')

#FLASK-SESSION
configure_session(app)

#CONFIGURE GOOGLE OAUTH
configure_google_oauth(app)

#CONFIGURE HTTPS
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' #allow http

#ROUTES
@app.before_request
def require_login():
    allowed_routes = ['registration', 'login', 'register', 'logout', 'static', 'google.login', 'register_google', 'login_google']
    if not check_session() and request.endpoint not in allowed_routes:
        return redirect(url_for('registration'))
    if not check_prompt_session():
        logout()

#PAGES
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/profile')
def profile():
    if not check_session():
        return redirect('/registration')
    user = User.get_user(session)
    name = user['name']
    english_level = user['english_level'].replace(' ', '<br>', 1) if user['english_level'] else 'Not Available'
    email = user['email']
    phone = user['phone']
    joined_date = user['joined_date']
    tokens_had = user['tokens_had']
    tokens_used = user['tokens_used']

    placement_test_history = PlacementTest.get_placement_test(user['_id'])
    placement_test_date = placement_test_history['date'] if placement_test_history else 'Not Available'
    placement_test_english_level = placement_test_history['english_level'] if placement_test_history else 'Not Available'
    placement_test_result = placement_test_history['placement_result'] if placement_test_history else 'Not Available'

    study_plan_history = StudyPlan.get_study_plan(user['_id'])
    study_plan_date = study_plan_history['date'] if study_plan_history else 'Not Available'
    study_plan = study_plan_history['study_plan'] if study_plan_history else 'Not Available'

    return render_template('profile.html', name=name, english_level=english_level, email=email, phone=phone, 
                           joined_date=joined_date, tokens_had=tokens_had, tokens_used=tokens_used,
                           placement_test_date=placement_test_date, placement_test_english_level=placement_test_english_level, placement_test_result=placement_test_result,
                           study_plan_date=study_plan_date, study_plan=study_plan)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


#REGISTRATION    
@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    user = User(name=data.get("name"), email=data.get("email"), password=data.get("password"))
    response, status = user.register()
    if status == 200:
        return redirect(url_for("login"))
    return jsonify(response), status

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User(email=data.get("email"), password=data.get("password"))
    existing_user, response, status = user.login()
    if status == 200:
        create_session(existing_user)
        configure_sesion_name(app, existing_user['_id'])
    return jsonify(response), status


@app.route("/register-google")
def register_google():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    if resp.ok:
        user_info = resp.json()
        email = user_info["email"]
        name = user_info["name"]
        phone = user_info.get("phone")
        user = User(name=name, email=email, phone=phone)
        response, status = user.register()
        return redirect(url_for("login_google"))
    else:
        return "Registration failed"
    
@app.route("/login-google")
def login_google():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    if resp.ok:
        user_info = resp.json()
        email = user_info["email"]
        user = User(email=email)
        existing_user, response, status = user.login_with_google()
        if status == 200:
            create_session(existing_user)
            configure_sesion_name(app, existing_user['_id'])
            return render_template('home.html')
        else:
            return "Login failed. Email not found or register first"


@app.route('/logout')
def logout():
    delete_session()
    return redirect('/registration')



#LEARNING
@app.route('/learning')
def learning():
    user = User.get_user(session)
    name = user.get('name') if user else None
    english_level = is_any_english_level(user.get('english_level') if user else None)
    return render_template('learning.html', name=name, english_level=english_level)


@app.route('/chat-history', methods=['GET'])
def get_chat_history():
    user = User.get_user(session)
    chat_history = Learning.get_chat_history(user['_id'])
    return jsonify({'chat_history': chat_history}), 200


@app.route('/chat', methods=['POST'])
def chat():
    message = request.json.get('user_input')
    mode = request.json.get('mode')
    if not (message and mode):
        return jsonify({'message': 'Please try again.'}), 400
    response = get_response(mode, message)
    user = User.get_user(session)
    if user:
        Learning.insert(user['_id'], user['email'], mode, message, response)
    return jsonify({'message': response}), 200

def get_response(mode, message):
    if not check_session():
        return MESSAGES["session_expired"]
    chat_dict = None
    if mode == 'pronunciation':
        chat_dict = pronunciation_dict[session["user"]]
    elif mode == 'context':
        chat_dict = context_dict[session["user"]]
    elif mode == 'reading':
        chat_dict = reading_dict[session["user"]]
    if chat_dict:
        chat_dict.append({"role": "user", "content": message})
        chat_dict = cut_messages(chat_dict) #cut messages for request to chatgpt
        response = chatgpt(chat_dict)
        chat_dict.append({"role": "assistant", "content": response})
    else:
        response = MESSAGES['error_request']
    return response


#PLACEMENT TEST
@app.route('/placement-test')
def placement_test():
    return render_template('placement_test.html')

@app.route('/placement-test1')
def placement_test1():
    return render_template('placement_test1.html')

@app.route('/placement-test2')
def placement_test2():
    return render_template('placement_test2.html')

@app.route('/placement-test3')
def placement_test3():
    return render_template('placement_test3.html')

@app.route('/placement-result')
def placement_result():
    return render_template('placement_result.html')

@app.route('/section1')
def section1():
    recreate_placement_test_prompt_session(User.get_user(session))
    return get_questions(prompt.section1_prompt)

@app.route('/section2')
def section2():
    return get_questions(prompt.section2_prompt)

@app.route('/section3')
def section3():
    return get_questions(prompt.section3_prompt)


def get_questions(prompt):
    placement_test_dict[session['user']].append(prompt)
    response = chatgpt(placement_test_dict[session['user']])
    placement_test_dict[session['user']].append({"role": "assistant", "content": response})
    questions = response.split("\n\n")
    return jsonify({"questions": questions})


@app.route('/submit-answer', methods=['POST'])
def submit_answer():
    data = request.get_json()
    answers = data.get('answers')
    placement_test_dict[session['user']].append({"role": "user", "content": prompt.answer_prompt + answers})
    response = chatgpt(placement_test_dict[session['user']])
    placement_test_dict[session['user']].append({"role": "assistant", "content": response})
    return jsonify({"response": response})


@app.route('/get-result-test')
def get_result_test():
    placement_test_dict[session['user']].append(prompt.result_prompt)
    response = chatgpt(placement_test_dict[session['user']])
    placement_test_dict[session['user']].append({"role": "assistant", "content": response})
    result = response
    return jsonify({"result": result})



@app.route('/save-result-test', methods=['POST'])
def save_result_test():
    placement_result = request.get_json().get('result_test')
    english_level = extract_english_level(placement_result)
    user = User.get_user(session)
    if user:
        PlacementTest.insert(user['_id'], user['email'], placement_test_dict[session['user']], placement_result, english_level)
        if english_level != None:
            User.update_english_level(user['_id'], english_level)
        return 'Success to test save result test!'
    else:
        return 'Failed to save result test!'



#STUDY PLAN
@app.route('/study-plan')
def study_plan():
    return render_template('study_plan.html')


@app.route('/create-study-plan', methods=['POST'])
def create_study_plan():
    recreate_study_plan_prompt_session(User.get_user(session))
    english_level = request.json['englishLevel']
    goals = request.json['goals']
    other_goals = request.json['otherInput']
    start_date = request.json['startDate']
    end_date = request.json['endDate']
    days = request.json['days']
    hours = request.json['hours']
    plan = prompt.create_study_plan_prompt(english_level, goals, other_goals, start_date, end_date, days, hours)
    study_plan_dict[session['user']].append({"role": "user", "content": plan})
    response = chatgpt(study_plan_dict[session['user']])
    study_plan_dict[session['user']].append({"role": "assistant", "content": response})
    study_plan = response
    return jsonify({"study_plan": study_plan})



@app.route('/save-study-plan', methods=['POST'])
def save_study_plan():
    study_plan_data = request.get_json().get('study_plan')
    user = User.get_user(session)
    if user:
        StudyPlan.insert(user['_id'], user['email'], study_plan_dict[session['user']], study_plan_data)
        return 'Suceess to save study plan!'
    return 'Failed to save study plan!'


@app.route('/get-english-level')
def get_english_level():
    user = User.get_user(session)
    if user:
        english_level = User.get_english_level(user['_id'])
    return jsonify({'englishLevel': english_level})

   
def schedule_loop():
    while True:
        schedule.run_pending()
        time.sleep(1)



if __name__ == '__main__':
    #UPDATE DATABASE
    schedule.every(TIME_OF_TOKENS_UPDATE).hour.do(User.update_tokens_periodically)

    #RUN SCHEDULER
    scheduler_thread = threading.Thread(target=lambda: schedule_loop())
    scheduler_thread.start()

    #RUN FLASK APP
    app.run(debug=True)

