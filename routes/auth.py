from flask import Blueprint

auth_routes = Blueprint("auth",__name__)

@auth_routes.route("/login")
def home():
    return "<h1>Auth</h1>"

