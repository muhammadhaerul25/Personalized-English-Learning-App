#PACKAGES
from flask import Flask, request
from flask import render_template, jsonify, redirect, url_for

#FILES
import prompts as prompt
from session import session, pronunciation_dict, context_dict, reading_dict, placement_test_dict, study_plan_dict 
from session import configure_session, create_session, check_session, delete_session
from models import chatgpt
from database import User, Learning, PlacementTest, StudyPlan
from helpers import extract_english_level, is_any_english_level 


#FLASK-APP
app = Flask(__name__)

#FLASK-SESSION
configure_session(app)


#ROUTES
@app.before_request
def require_login():
    allowed_routes = ['registration', 'login', 'register','logout', 'static']
    if not check_session() and request.endpoint not in allowed_routes:
        return redirect('/registration')

@app.route('/')
def home():
    return render_template('index.html')


#REGISTRATION    
@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    user = User(name=data.get("name"), email=data.get("email"), password=data.get("password"))
    response, status = user.register()
    return jsonify(response), status

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User(email=data.get("email"), password=data.get("password"))
    existing_user, response, status = user.login()
    if status == 200:
        create_session(existing_user)
    return jsonify(response), status

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
    try:
        message = request.json.get('user_input')
        mode = request.json.get('mode')
        if not (message and mode):
            return jsonify({'message': 'Please try again.'}), 400
        response = get_response(mode, message)
        user = User.get_user(session)
        if user:
            Learning.insert(user['_id'], user['email'], mode, message, response)
        return jsonify({'message': response}), 200
    except:
        return jsonify({'message': 'Sorry, something went wrong. Please, try again later.'}), 500

def get_response(mode, message):
    if not check_session():
        return 'Please login first'
    chat_dict = None
    if mode == 'pronunciation':
        chat_dict = pronunciation_dict[session["user"]]
    elif mode == 'context':
        chat_dict = context_dict[session["user"]]
    elif mode == 'reading':
        chat_dict = reading_dict[session["user"]]

    if chat_dict:
        chat_dict.append({"role": "user", "content": message})
        response = chatgpt(chat_dict)
        chat_dict.append({"role": "assistant", "content": response})
    else:
        response = 'Sorry, something went wrong. Please try again later.'
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
    return get_questions(prompt.section1_prompt)

@app.route('/section2')
def section2():
    return get_questions(prompt.section2_prompt)

@app.route('/section3')
def section3():
    return get_questions(prompt.section3_prompt)

def get_questions(prompt):
    try:
        placement_test_dict[session['user']].append(prompt)
        response = chatgpt(placement_test_dict[session['user']])
        placement_test_dict[session['user']].append({"role": "assistant", "content": response})
        questions = response.split("\n\n")
    except Exception as e:
        questions = ['Sorry, something went wrong. Please, refresh the page.']
    return jsonify({"questions": questions})

@app.route('/submit-answer', methods=['POST'])
def submit_answer():
    data = request.get_json()
    answers = data.get('answers')
    try:
        placement_test_dict[session['user']].append({"role": "user", "content": 'Berikut jawaban saya untuk section tersebut: ' + answers})
        response = chatgpt(placement_test_dict[session['user']])
        placement_test_dict[session['user']].append({"role": "assistant", "content": response})
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/result')
def result():
    try:
        placement_test_dict[session['user']].append(prompt.result_prompt)
        response = chatgpt(placement_test_dict[session['user']])
        placement_test_dict[session['user']].append({"role": "assistant", "content": response})
        result = response
    except Exception as e:
        result = 'Sorry, something went wrong. Please, refresh the page.'
    return jsonify({"result": result})

@app.route('/save-result-test', methods=['POST'])
def save_result_test():
    placement_result = request.get_json().get('result_test')
    english_level = extract_english_level(placement_result)
    user = User.get_user(session)
    if user:
        PlacementTest.insert(user['_id'], user['email'], placement_test_dict[session['user']], placement_result, english_level)
        User.update_english_level(user['_id'], english_level)
    return 'Result test saved successfully!'



#STUDY PLAN
@app.route('/study-plan')
def study_plan():
    return render_template('study_plan.html')


@app.route('/create-study-plan', methods=['POST'])
def create_study_plan():
    english_level = request.json['englishLevel']
    goals = request.json['goals']
    other_goals = request.json['otherInput']
    start_date = request.json['startDate']
    end_date = request.json['endDate']
    days = request.json['days']
    hours = request.json['hours']

    plan = prompt.create_study_plan_prompt(english_level, goals, other_goals, start_date, end_date, days, hours)

    try:
        study_plan_dict[session['user']].append({"role": "user", "content": plan})
        response = chatgpt(study_plan_dict[session['user']])
        study_plan_dict[session['user']].append({"role": "assistant", "content": response})
        study_plan = response
    except Exception as e:
        study_plan = 'Sorry, something went wrong. Please, refresh the page.'

    return jsonify({"study_plan": study_plan})


@app.route('/save-study-plan', methods=['POST'])
def save_study_plan():
    study_plan_data = request.get_json().get('study_plan')
    user = User.get_user(session)
    if user:
        StudyPlan.insert(user['_id'], user['email'], study_plan_dict[session['user']], study_plan_data)
    return 'Study plan saved successfully!'


@app.route('/get-english-level')
def get_english_level():
    user = User.get_user(session)
    if user:
        english_level = User.get_english_level(user['_id'])
    return jsonify({'englishLevel': english_level})

   


if __name__ == '__main__':
    app.run(debug=True)
