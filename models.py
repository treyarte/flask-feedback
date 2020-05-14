from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__='users'

    username = db.Column(db.String(20), primary_key=True, unique=True)

    password = db.Column(db.Text, nullable=False)

    email = db.Column(db.String(50), unique=True, nullable=False)

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)

    feedback = db.relationship('Feedback', cascade="all, delete", backref="user")

    @classmethod
    def register(cls,username, pwd, email, first_name, last_name):
        hashed = bcrypt.generate_password_hash(pwd)

        hash_string = hashed.decode('utf8')

        return cls(username=username, password=hash_string, email=email, first_name=first_name, last_name=last_name)
    
    @classmethod
    def authenticate(cls, username, pwd):
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password,pwd):
            return user
        else:
            return False

class Feedback(db.Model):
    __tablename__='feedback'

    id = db.Column(db.Integer,
                   primary_key=True, 
                   autoincrement=True)

    title = db.Column(db.String(100),
                     nullable=False)
    
    content = db.Column(db.Text,   
                       nullable=False)
    
    username = db.Column(db.String(20), db.ForeignKey('users.username'))

    