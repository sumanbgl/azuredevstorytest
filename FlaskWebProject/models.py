from datetime import datetime
from FlaskWebProject import app, db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import string, random
from werkzeug import secure_filename
from flask import flash


def id_generator(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Income_Expense(db.Model):
    __tablename__ = 'income_expense'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(150))
    date = db.Column(db.Date)
    amount = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Amount {}>'.format(self.amount)

    def save_changes(self, form, userId, new=False):
        self.category = form.category.data
        self.amount = form.amount.data
        self.date = form.date.data
        self.user_id = userId
        
        if new:
            db.session.add(self)
        db.session.commit()        
