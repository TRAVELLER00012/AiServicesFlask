import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes import user

load_dotenv()

app = Flask(__name__)

mysql_username = os.getenv("MYSQL_USERNAME")
mysql_password = os.getenv("MYSQL_PASSWORD")
mysql_db_name = os.getenv("MYSQL_DB_NAME")

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{mysql_username}:{mysql_password}@localhost/{mysql_db_name}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

app.register_blueprint(user.user_routes,url_prefix="/user")

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
