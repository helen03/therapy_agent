# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# # File Name: models.py
# #
# # Creates sql tables for use by flask
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from sqlalchemy import DateTime
import bcrypt
import jwt
from datetime import datetime, timedelta
import os


class User(db.Model):  # noqa
    __tablename__ = 'user'  # noqa
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))  # Changed from password to password_hash
    email = db.Column(db.String(120), unique=True)
    is_active = db.Column(db.Boolean, default=True)
    protocols = db.relationship('Protocol', backref='user')
    choices = db.relationship('Choice', backref='user')
    sessions = db.relationship('UserModelSession', backref='user')
    date_created = db.Column(DateTime, default=datetime.utcnow)
    last_accessed = db.Column(DateTime)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        """Hash and set password"""
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password):
        """Check if password matches hash"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def generate_auth_token(self, expires_in=3600):
        """Generate JWT token"""
        secret_key = os.getenv('JWT_SECRET_KEY', 'fallback-secret-key-change-in-production')
        return jwt.encode(
            {'user_id': self.id, 'exp': datetime.utcnow() + timedelta(seconds=expires_in)},
            secret_key,
            algorithm='HS256'
        )

    @staticmethod
    def verify_auth_token(token):
        """Verify JWT token"""
        secret_key = os.getenv('JWT_SECRET_KEY', 'fallback-secret-key-change-in-production')
        try:
            data = jwt.decode(token, secret_key, algorithms=['HS256'])
            return User.query.get(data['user_id'])
        except:
            return None


class Protocol(db.Model):  # noqa
    __tablename__ = 'protocol'  # noqa
    id = db.Column(db.Integer(), primary_key=True)
    protocol_chosen = db.Column(db.Integer())
    protocol_was_useful = db.Column(db.String(64))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    session_id = db.Column(db.Integer(), db.ForeignKey('model_session.id'))
    run_id = db.Column(db.Integer(), db.ForeignKey('model_run.id'))
    date_created = db.Column(DateTime, default=datetime.utcnow)


class Choice(db.Model):  # noqa
    __tablename__ = 'choice'  # noqa
    id = db.Column(db.Integer(), primary_key=True)
    choice_desc = db.Column(db.String(120))
    option_chosen = db.Column(db.String(60))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    session_id = db.Column(db.Integer(), db.ForeignKey('model_session.id'))
    run_id = db.Column(db.Integer(), db.ForeignKey('model_run.id'))
    date_created = db.Column(DateTime, default=datetime.utcnow)


class UserModelRun(db.Model):  # noqa
    __tablename__ = 'model_run'  # noqa
    id = db.Column(db.Integer(), primary_key=True)

    emotion_happy_score = db.Column(db.Integer())
    emotion_sad_score = db.Column(db.Integer())
    emotion_angry_score = db.Column(db.Integer())
    emotion_neutral_score = db.Column(db.Integer())
    emotion_anxious_score = db.Column(db.Integer())
    emotion_scared_score = db.Column(db.Integer())

    antisocial_score = db.Column(db.Integer())
    internal_persecutor_score = db.Column(db.Integer())
    personal_crisis_score = db.Column(db.Integer())
    rigid_thought_score = db.Column(db.Integer())
    session_id = db.Column(db.Integer(), db.ForeignKey('model_session.id'))
    date_created = db.Column(DateTime, default=datetime.utcnow)
    protocols = db.relationship('Protocol', backref='model_run')


class UserModelSession(db.Model):  # noqa
    __tablename__ = 'model_session'  # noqa
    id = db.Column(db.Integer(), primary_key=True)
    conversation = db.Column(db.Text(), default="")

    protocols = db.relationship('Protocol', backref='model_session')
    choices = db.relationship('Choice', backref='model_session')
    runs = db.relationship("UserModelRun", backref='model_session')
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    date_created = db.Column(DateTime, default=datetime.utcnow)
    last_updated = db.Column(DateTime)
