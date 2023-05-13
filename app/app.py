#MODULES
import time

#PACKAGES
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_session import Session
from pymongo import MongoClient


#FILES
import prompts as prompt
from prompts import pronunciation_dict, context_dict, reading_dict, placement_test_dict, study_plan_dict
from models import chatgpt
from helpers import check_session


#FLASK
app = Flask(__name__)
app.secret_key = 'personalized_english_learning'

#FLASK-SESSION
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
Session(app)


#MONGODB
client = MongoClient("mongodb://localhost:27017")
db = client["personalized_english_learning"]
users = db["users"]
learning_history = db['learning']



#ROUTES
@app.before_request
def require_login():
    allowed_routes = ['registration', 'login', 'register','logout', 'static']
    if not session.get('user') and request.endpoint not in allowed_routes:
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
    name = request.json.get("name")
    email = request.json.get("email")
    password = request.json.get("password")

     # Cek apakah email sudah terdaftar
    if users.find_one({"email": email}):
        return jsonify({"message": "Email already registered"}), 400

    # Save data ke database
    user = {"name": name, "email": email, "password": password}
    users.insert_one(user)

    return jsonify({"message": "Registration successful"}), 200


@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    user = users.find_one({"email": email})
    if not user:
        return jsonify({"message": "Email not found"}), 404

    if user.get("password") != password:
        return jsonify({"message": "Invalid email or password"}), 401

    # Login berhasil, buat session
    session["user"] = user["_id"]
    pronunciation_dict[session["user"]] = prompt.pronunciation_prompt.copy()
    context_dict[session["user"]] = prompt.context_prompt.copy()  
    reading_dict[session["user"]] = prompt.reading_prompt.copy()
    placement_test_dict[session["user"]] = prompt.placement_test_prompt.copy()
    study_plan_dict[session["user"]] = prompt.study_plan_prompt.copy()

    return jsonify({"message": "Login successful"}), 200


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/registration')



#LEARNING
@app.route('/learning')
def learning():
    return render_template('learning.html')


@app.route('/chat', methods=['POST'])
def chat():
    try:
        message = request.json.get('user_input')
        mode = request.json.get('mode')
        if not (message and mode):
            return jsonify({'message': 'Please try again.'}), 400
        response = get_response(mode, message)
        user = users.find_one({'_id': session.get('user')})
        if user:
            learning_history.insert_one({
                'user_id': user['_id'],
                'email': user['email'],
                'mode': mode,
                'message': message,
                'response': response,
                'timestamp': int(time.time())
            })
        return jsonify({'message': response}), 200
    except:
        return jsonify({'message': 'Sorry, something went wrong. Please, try again later.'}), 500


def get_response(mode, message):
    # if check_session():
    #     return 'Please log in to access personalized learning features'
    
    if mode == 'pronunciation':
        pronunciation_dict[session["user"]].append({"role": "user", "content": message})
        response = chatgpt(pronunciation_dict[session["user"]])
        pronunciation_dict[session["user"]].append({"role": "assistant", "content": response})

    elif mode == 'context':
        context_dict[session["user"]].append({"role": "user", "content": message})
        response = chatgpt(context_dict[session["user"]])
        context_dict[session["user"]].append({"role": "assistant", "content": response}
                                    )
    elif mode == 'reading':
        reading_dict[session["user"]].append({"role": "user", "content": message})
        response = chatgpt(reading_dict[session["user"]])
        reading_dict[session["user"]].append({"role": "assistant", "content": response})

    else:
        response = 'Sorry, something went wrong. Please, try again later'
    
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
    try:
        placement_test_dict[session['user']].append(prompt.section1_prompt)
        response = chatgpt(placement_test_dict[session['user']])
        placement_test_dict[session['user']].append({"role": "assistant", "content": response})

        questions = response.split("\n\n")
        
    except Exception as e:
        questions = ['Sorry, something went wrong. Please, refresh the page.']

    return jsonify({"questions": questions})



@app.route('/section2')
def section2():
    try:
        placement_test_dict[session['user']].append(prompt.section2_prompt)
        response = chatgpt(placement_test_dict[session['user']])
        placement_test_dict[session['user']].append({"role": "assistant", "content": response})

        questions = response.split("\n\n")
        
    except Exception as e:
        questions = ['Sorry, something went wrong. Please, refresh the page.']

    return jsonify({"questions": questions})


@app.route('/section3')
def section3():
    try:
        placement_test_dict[session['user']].append(prompt.section3_prompt)
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
    plan = f"My English level is {english_level}, so I will focus on {', '.join(goals)} + {other_goals}. I plan to start studying on ${start_date} and finish on ${end_date}, for a total of ${days} days per week and ${hours} hours per day. Based on these information, give me a study plan."

    try:
        study_plan_dict[session['user']].append({"role": "user", "content": plan})
        response = chatgpt(study_plan_dict[session['user']])
        study_plan_dict[session['user']].append({"role": "assistant", "content": response})
        study_plan = response
    except Exception as e:
        study_plan = 'Sorry, something went wrong. Please, refresh the page.'

    return jsonify({"study_plan": study_plan})

   

if __name__ == '__main__':
    app.run(debug=True)
