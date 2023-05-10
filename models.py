from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
import secrets

# set variables for class instantiation
login_manager = LoginManager()
db = SQLAlchemy()
ma = Marshmallow()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    user_id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable = True, default='')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False, default = '')
    password = db.Column(db.String, nullable = True, default = '')
    location = db.Column(db.String(150), nullable = True, default = '')
    age = db.Column(db.String(10), nullable = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, email, first_name='', last_name='', password ='', age ='', location =''):
        self.user_id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.age = age
        self.location = location

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash


class Prompt(db.Model):
    id = db.Column(db.String, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    idea = db.Column(db.String(250), nullable = False)
    user_id = db.Column(db.String, db.ForeignKey('user.user_id'), nullable = False)


    def __init__(self, title, date, idea, user_id, id = ''):
        self.id = self.set_id()
        self.title = title
        self.date = date
        self.idea = idea
        self.user_id = user_id

    def set_id(self):
        return (secrets.token_urlsafe())

class PromptSchema(ma.Schema):
    class Meta:
        fields = ['id', 'title', 'date', 'idea']

Prompt_schema = PromptSchema()
Prompts_schema = PromptSchema(many=True)