from app import db
from app import login
from app import app
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin
import string
import random

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('token.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

class User(UserMixin, db.Model):
    __tablename__ = 'token'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(64), index=True, unique=True)
    used = db.Column(db.Boolean)

    roles = db.relationship('Role', secondary='user_roles')

    def check_token(token):
        db_token = db.session.query(User).filter_by(password=token, used=False)
        if db_token:
            return True
        else: return False

    def is_Admin(self):
        if 'Admin' in self.roles:
            return True
        else: return False

    def generate_token(quantity, role):
        role_ = Role.query.filter_by(name=role).first()
        for _ in range(quantity):
            token = User(password=token_generator(), used=False)
            token.roles = [role_,]
            db.session.add(token)
        db.session.commit()

    def invalidate_token(self):
        self.used = True
        db.session.commit()

    def get_num_unused_token():
        num = db.session.query(User).filter_by(used=False).count()
        return num

    def __repr__(self):
        return '<Token {}>'.format(self.password)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255))
    category = db.Column(db.String(40))
    frontend = db.Column(db.String(40))
    ans01 = db.Column(db.String(255))
    ans02 = db.Column(db.String(255))
    ans03 = db.Column(db.String(255))
    ans04 = db.Column(db.String(255))
    ans05 = db.Column(db.String(255))
    ans06 = db.Column(db.String(255))
    ans07 = db.Column(db.String(255))
    ans08 = db.Column(db.String(255))
    ans09 = db.Column(db.String(255))
    ans10 = db.Column(db.String(255))
    ans11 = db.Column(db.String(255))
    ans12 = db.Column(db.String(255))
    ans13 = db.Column(db.String(255))
    ans14 = db.Column(db.String(255))
    ans15 = db.Column(db.String(255))
    ans16 = db.Column(db.String(255))
    ans17 = db.Column(db.String(255))
    ans18 = db.Column(db.String(255))
    ans19 = db.Column(db.String(255))
    ans20 = db.Column(db.String(255))
    sort = db.Column(db.Integer)

    def __repr__(self):
        return '<Question: {}>'.format(self.question)
# TODO: Bei Neustart: hier führende Nullen entfernen --> ids in DB haben auch keine!
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usedToken = db.Column(db.Integer, db.ForeignKey(User.id))
    q01 = db.Column(db.String(40))
    q02 = db.Column(db.String(40))
    q03 = db.Column(db.String(40))
    q04 = db.Column(db.String(40))
    q05 = db.Column(db.String(40))
    q06 = db.Column(db.String(40))
    q07 = db.Column(db.String(40))
    q08 = db.Column(db.String(40))
    q09 = db.Column(db.String(40))
    q10 = db.Column(db.String(40))
    q11 = db.Column(db.String(40))
    q12 = db.Column(db.String(40))
    q13 = db.Column(db.String(40))
    q14 = db.Column(db.String(40))
    q15 = db.Column(db.String(40))
    q16 = db.Column(db.String(40))
    q17 = db.Column(db.String(40))
    q18 = db.Column(db.String(40))
    q19 = db.Column(db.String(40))
    q20 = db.Column(db.String(40))
    q21 = db.Column(db.String(40))
    q22 = db.Column(db.String(40))
    q23 = db.Column(db.String(40))
    q24 = db.Column(db.String(40))
    q25 = db.Column(db.String(40))
    q26 = db.Column(db.String(40))
    q27 = db.Column(db.String(40))
    q28 = db.Column(db.String(40))
    q29 = db.Column(db.String(40))
    q30 = db.Column(db.String(40))
    q31 = db.Column(db.String(40))
    q32 = db.Column(db.String(40))
    q33 = db.Column(db.String(40))
    q34 = db.Column(db.String(40))
    q35 = db.Column(db.String(40))
    q36 = db.Column(db.String(40))
    q37 = db.Column(db.String(40))
    q38 = db.Column(db.String(40))
    q39 = db.Column(db.String(40))
    q40 = db.Column(db.String(40))

    def __repr__(self):
        return '<Answers given by token: {}>'.format(self.usedToken)

def token_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
