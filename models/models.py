from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, validate

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255),nullable=False)
    email = db.Column(db.String(255),nullable=False,unique=True)
    password = db.Column(db.String(255),nullable=False)

class UserSchema(Schema):
    full_name = fields.Str(required=True, validate=validate.Length(min=3,max=255))
    password = fields.Str(required=True, validate=validate.Length(min=8))
    email = fields.Email(required=True)