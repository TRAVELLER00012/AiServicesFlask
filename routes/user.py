from flask import Blueprint

user_routes = Blueprint("users",__name__)

@user_routes.route("/")
def home():
    return "<h1>Users</h1>"

