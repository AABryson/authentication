from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db=SQLAlchemy()

bcrypt=Bcrypt()

def connect_db(app):
    db.app=app
    db.init_app(app)


class User(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer, autoincrement=True)
    username=db.Column(db.Text, primary_key=True, unique=True)
    password=db.Column(db.Text, nullable=False)
    email=db.Column(db.Text, nullable=False)
    first_name=db.Column(db.Text, nullable=False)
    last_name=db.Column(db.Text, nullable=False)
    feedback=db.relationship("Feedback", backref="user")

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        pwd=bcrypt.generate_password_hash(password)
        pwd_decoded=pwd.decode('utf-8')
        user = cls(username=username, password=pwd_decoded, email=email, first_name=first_name, last_name=last_name)
        db.session.add(user)
        ##################################
        # db.session.commit()
        ####################################
        return user


    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False
    # def authenticate(cls, username, password, email, first_name, last_name):
    #     pwd=bcrypt.generate_password_hash(password)
    #     pwd_decoded=pwd.decode('utf-8')
    #     return cls(username=username, password=pwd_decoded, email=email, first_name=first_name, last_name=last_name)
    
    #     user = User.query.filter_by(username=username).first()

    #     if user and bcrypt.check_password_hash(user.password, password):
    #         return user
    #     else:
    #         return False
    

    @classmethod
    def login(cls, username, pwd):
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, pwd):
            # return user instance/object if password is correct
            return user
        else:
            return False
        

class Feedback(db.Model):
    __tablename__='feedback'
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    title=db.Column(db.Text, nullable=False)
    content=db.Column(db.Text, nullable=False)
    #####################################################################
    username=db.Column(db.Text, db.ForeignKey('users.username'))
    
