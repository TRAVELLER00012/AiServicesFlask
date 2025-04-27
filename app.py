from flask import Flask
from routes import user

app = Flask(__name__)

app.register_blueprint(user.user_routes,url_prefix="/user")

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == '__main__':
    app.run(debug=True)