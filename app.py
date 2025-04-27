import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from routes import user, auth
from models.models import db,User

load_dotenv()

app = Flask(__name__)

mysql_username = os.getenv("MYSQL_USERNAME")
mysql_password = os.getenv("MYSQL_PASSWORD")
mysql_db_name = os.getenv("MYSQL_DB_NAME")

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{mysql_username}:{mysql_password}@localhost/{mysql_db_name}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

migrate = Migrate(app,db)

app.register_blueprint(user.user_routes,url_prefix="/user")
app.register_blueprint(auth.auth_routes)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
