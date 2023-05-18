import time
from pymongo import MongoClient
from test_functions import english_level_mapping

#MONGODB
client = MongoClient("mongodb://localhost:27017")
db = client["personalized_english_learning"]
users = db["users"]
learning_history = db['learning']
placements_test = db['placement_tests']


class User:
    def __init__(self, name=None, email=None, password=None, english_level='Unknown'):
        self.name = name
        self.email = email
        self.password = password
        self.english_level = english_level
 

    def is_email_registered(self):
        return users.find_one({"email": self.email}) is not None
    
    def insert(self):
        users.insert_one({
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "english_level": self.english_level
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
        if existing_user["password"] != self.password:
            return existing_user, {"message": "Invalid email or password"}, 401
        return existing_user, {"message": "Login successful"}, 200
    
    @staticmethod
    def get_user(session):
        user_id = session.get('user')
        if user_id:
            return users.find_one({'_id': user_id})
        else:
            return None
    
    @staticmethod
    def get_name(id):
        user_data = users.find_one({"_id": id})
        if user_data:
            return user_data.get("name")
        return None

    @staticmethod
    def get_english_level(id):
        user_data = users.find_one({"_id": id})
        if user_data:
            return user_data.get("english_level")
        return None
    
    @staticmethod
    def update_english_level(id, english_level):
        users.update_one({'_id': id}, {'$set': {'english_level': english_level}})
        

class LearningHistory:
    @staticmethod
    def insert(user_id, email, mode, message, response):
        learning_history.insert_one({
            'user_id': user_id,
            'email': email,
            'mode': mode,
            'message': message,
            'response': response,
            'timestamp': int(time.time())
        })


class PlacementTest:
    @staticmethod
    def insert(user_id, email, placement_result, english_level):
        placements_test.insert_one({
            'user_id': user_id,
            'email': email,
            'placement_result': placement_result,
            'english_level': english_level_mapping(english_level),
            'timestamp': int(time.time())
        })

