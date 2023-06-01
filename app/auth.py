from flask import render_template, jsonify, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
from oauthlib.oauth2 import WebApplicationClient

from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

client = None

def configure_google_oauth(app):
    client_id = GOOGLE_CLIENT_ID
    client_secret = GOOGLE_CLIENT_SECRET
    scope = ["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"]

    google_blueprint = make_google_blueprint(
        client_id=client_id,
        client_secret=client_secret,
        scope=scope,
    )

    app.register_blueprint(google_blueprint, url_prefix="/login")
    client = WebApplicationClient(GOOGLE_CLIENT_ID)


def google_register():
    if not google.authorized:
        print('not authorized')
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    if resp.ok:
        user_info = resp.json()
        email = user_info["email"]
        name = user_info["name"]
        phone = user_info.get("phone")
        print(name, email, phone)
        return { "name": name, "email": email, "phone": phone}
    else:
        print("Failed to fetch user info from Google.")
        return None