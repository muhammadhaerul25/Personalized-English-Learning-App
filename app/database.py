import time
import bcrypt
from pymongo import MongoClient, ASCENDING
 
from session import update_tokens_session
from helpers import english_level_mapping, check_content_on_list_of_dict, check_content_on_string
from config import INITIAL_TOKENS, UPDATE_TOKENS, MAX_UPDATE_TOKENS

#MONGODB
client = MongoClient("mongodb://localhost:27017")
db = client["personalized_english_learning"]
users = db["users"]
learning = db['learning']
placements_tests = db['placement_tests']
study_plans = db['study_plans']


class User:
    def __init__(self, name=None, email=None, phone=None, password=None, english_level='Unknown', tokens_had=INITIAL_TOKENS, tokens_used=0):
        self.name = name
        self.email = email
        self.phone = phone
        self.password = password
        self.english_level = english_level
        self.tokens_had = tokens_had
        self.tokens_used = tokens_used
    
    def is_email_registered(self):
        return users.find_one({"email": self.email}) is not None
    
    def hash_password(self, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')
    
    def verify_password(self, password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    def insert(self):
        if self.password is not None:
            hashed_password = self.hash_password(self.password)
        users.insert_one({
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "password": hashed_password,
            "english_level": self.english_level,
            "tokens_had": self.tokens_had,
            "tokens_used": self.tokens_used,
            "timestamp": int(time.time()),
            "joined_date": time.strftime("%d/%m/%Y")
        })

    def register(self):
        if self.is_email_registered():
            return {"message": "Email already registered"}, 400
        self.insert()
        return {"message": "Registration successful"}, 200
    
    def login(self):
        existing_user = users.find_one({"email": self.email})
        if not existing_user:
            return existing_user, {"message": "Email not found"}, 404
        if not self.verify_password(self.password, existing_user["password"]):
            return existing_user, {"message": "Invalid email or password"}, 401
        return existing_user, {"message": "Login successful"}, 200
    
    def login_with_google(self):
        existing_user = users.find_one({"email": self.email})
        if not existing_user:
            return existing_user, {"message": "Email not found"}, 404
        return existing_user, {"message": "Login successful"}, 200
    
    #GETTERS
    @staticmethod
    def get_user(session):
        user_id = session.get('user')
        if user_id:
            return users.find_one({'_id': user_id})
        else:
            return None
    
    @staticmethod
    def get_name(user_id):
        user_data = users.find_one({"_id": user_id})
        if user_data:
            return user_data.get("name")
        return None

    @staticmethod
    def get_english_level(user_id):
        user_data = users.find_one({"_id": user_id})
        if user_data:
            return user_data.get("english_level")
        return None
    
    @staticmethod
    def get_tokens_used(user_id):
        user_data = users.find_one({"_id": user_id})
        if user_data:
            return user_data.get("tokens_used")
        return 0
    
    def get_tokens_had(user_id):
        user_data = users.find_one({"_id": user_id})
        if user_data:
            return user_data.get("tokens_had")
        return 0
    
    def get_user_by_email(email):
        return users.find_one({"email": email})
    

    #UPDATERS
    @staticmethod
    def update_english_level(user_id, english_level):
        users.update_one({'_id': user_id}, {'$set': {'english_level': english_level_mapping(english_level)}})

    @staticmethod
    def update_tokens_used(user_id, tokens_used):
        users.update_one({'_id': user_id}, {'$set': {'tokens_used': tokens_used}})
    
    @staticmethod
    def update_tokens_had(user_id, tokens_had):
        users.update_one({'_id': user_id}, {'$set': {'tokens_had': tokens_had}})

    @staticmethod
    def update_tokens_periodically():
        all_users = users.find()
        for user in all_users:
            tokens_had = user["tokens_had"]
            if tokens_had < MAX_UPDATE_TOKENS:
                tokens_to_add = UPDATE_TOKENS
                new_tokens_had = tokens_had + tokens_to_add
                if new_tokens_had > MAX_UPDATE_TOKENS:
                    new_tokens_had = MAX_UPDATE_TOKENS
                users.update_one(
                    {"_id": user["_id"]},
                    {"$set": {"tokens_had": new_tokens_had}}
                )
                update_tokens_session(user["_id"], new_tokens_had, user["tokens_used"])



class Learning:
    @staticmethod
    def insert(user_id, email, mode, message, response):
        learning.insert_one({
            'user_id': user_id,
            'email': email,
            'mode': mode,
            'message': message,
            'response': check_content_on_string(response),
            'timestamp': int(time.time()),
            'date': time.strftime("%d/%m/%Y")
        })

    @staticmethod
    def get_chat_history(user_id):
        chat_history = learning.find({'user_id': user_id}).sort('timestamp', ASCENDING)
        result = []
        for doc in chat_history:
            result.append({
                'mode': doc['mode'],
                'message': doc['message'],
                'response': doc['response']
            })
        return result



class PlacementTest:
    @staticmethod
    def insert(user_id, email, placement_test_dict, placement_result, english_level):
        placements_tests.insert_one({
            'user_id': user_id,
            'email': email,
            'placement_test_dict': check_content_on_list_of_dict(placement_test_dict),
            'placement_result': placement_result,
            'english_level': english_level_mapping(english_level),
            'timestamp': int(time.time()),
            'date': time.strftime("%d/%m/%Y"),
        })
    
    @staticmethod
    def get_placement_test(user_id):
        placement_test = placements_tests.find_one({'user_id': user_id}, sort=[('_id', -1)])
        if placement_test:
            return placement_test
        return None



class StudyPlan:
    @staticmethod
    def insert(user_id, email, study_plan_dict, study_plan):
        study_plans.insert_one({
            'user_id': user_id,
            'email': email,
            'study_plan_dict': check_content_on_list_of_dict(study_plan_dict),
            'study_plan': study_plan,
            'timestamp': int(time.time()),
            'date': time.strftime("%d/%m/%Y"),
        })
        
    @staticmethod
    def get_study_plan(user_id):
        study_plan = study_plans.find_one({'user_id': user_id}, sort=[('_id', -1)])
        if study_plan:
            return study_plan
        return None

