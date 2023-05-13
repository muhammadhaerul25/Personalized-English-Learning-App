from flask import Flask, session

#SESSION
def create_user(user):
    session["user"] = user["_id"]

def check_session():
    if session.get('user'):
        return True
    else:
        return False