import hashlib
import os

from flask import request
from flask_login import UserMixin, AnonymousUserMixin
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    avatar_hash = db.Column(db.String(256))
    interviewed = db.Column(db.Boolean, default=False)

    interest = relationship('Interest', uselist=False, back_populates='user')

    @staticmethod
    def _bootstrap(count=10):
        from sqlalchemy.exc import IntegrityError
        from faker import Faker

        fake = Faker()

        for i in range(count):
            u = User(
                email=fake.email(),
                username=fake.name(),
                password=fake.password()
            )
            u.gravatar()
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_administrator(self):
        return self.email == os.environ.get('ADMIN_EMAIL')

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    def update_interest_from_form(self, form):
        self.interest.action = float(form.action.data)
        self.interest.adventure = float(form.adventure.data)
        self.interest.animation = float(form.animation.data)
        self.interest.childrens = float(form.childrens.data)
        self.interest.comedy = float(form.comedy.data)
        self.interest.crime = float(form.crime.data)
        self.interest.documentary = float(form.documentary.data)
        self.interest.drama = float(form.drama.data)
        self.interest.fantasy = float(form.fantasy.data)
        self.interest.horror = float(form.horror.data)
        self.interest.musical = float(form.musical.data)
        self.interest.mystery = float(form.mystery.data)
        self.interest.romance = float(form.romance.data)
        self.interest.science = float(form.science.data)
        self.interest.thriller = float(form.thriller.data)
        self.interest.war = float(form.war.data)
        self.interest.western = float(form.western.data)

    def calculate(self):
        from math import pow, sqrt
        from operator import itemgetter

        result = []
        users = User.query.all()
        users_interest = [user.interest for user in users if user.id != self.id]
        for interest in users_interest:
            distance = 0
            for col in Interest.__table__.columns:
                if col.key != 'id':
                    distance += pow(self.interest.__dict__[col.key] - interest.__dict__[col.key], 2)
            distance = sqrt(distance)
            result.append((interest.user.username, distance))
        result.sort(key=itemgetter(1))
        return result

    def __repr__(self):
        return '<User %r>' % self.username


class AnonymousUser(AnonymousUserMixin):
    def is_admin(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Interest(db.Model):
    __tablename__ = 'interests'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    action = db.Column(db.Integer, default=0)
    adventure = db.Column(db.Integer, default=0)
    animation = db.Column(db.Integer, default=0)
    childrens = db.Column(db.Integer, default=0)
    comedy = db.Column(db.Integer, default=0)
    crime = db.Column(db.Integer, default=0)
    documentary = db.Column(db.Integer, default=0)
    drama = db.Column(db.Integer, default=0)
    fantasy = db.Column(db.Integer, default=0)
    horror = db.Column(db.Integer, default=0)
    musical = db.Column(db.Integer, default=0)
    mystery = db.Column(db.Integer, default=0)
    romance = db.Column(db.Integer, default=0)
    science = db.Column(db.Integer, default=0)
    thriller = db.Column(db.Integer, default=0)
    war = db.Column(db.Integer, default=0)
    western = db.Column(db.Integer, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship('User', back_populates='interest')

    @staticmethod
    def _bootstrap():
        from sqlalchemy.exc import IntegrityError
        from random import choice
        choices = [0.5, 1, 1.5, 2, 2.5, 3.0, 3.5, 4.0, 4.5, 5]
        for i in range(1, User.query.count() + 1):
            i = Interest(
                user_id=i,
                action=choice(choices),
                adventure=choice(choices),
                animation=choice(choices),
                childrens=choice(choices),
                comedy=choice(choices),
                crime=choice(choices),
                documentary=choice(choices),
                drama=choice(choices),
                fantasy=choice(choices),
                horror=choice(choices),
                musical=choice(choices),
                mystery=choice(choices),
                romance=choice(choices),
                science=choice(choices),
                thriller=choice(choices),
                war=choice(choices),
                western=choice(choices),
            )
            db.session.add(i)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __repr__(self):
        return '<Interest of %r user>' % self.user.username
