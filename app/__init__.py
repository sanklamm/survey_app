from flask import Flask, redirect, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_admin import Admin, helpers, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_user import UserManager, current_user
from flask_babelex import Babel

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)

# for debugging
# app.debug = True
# toolbar = DebugToolbarExtension(app)

# for login
login = LoginManager(app)
from app import models

# initialize db
db.create_all()

print("--------- DB created ----------")
print(models.Role.query.filter_by(name="Admin").first())
if not models.Role.query.filter_by(name="Admin").first():
    print("------------ No Admin Role found ------------")
    role_admin = models.Role(name='Admin')
    db.session.add(role_admin)
    db.session.commit()
if not models.Role.query.filter_by(name="User").first():
    print("------------ No User Role found ------------")
    role_user = models.Role(name='User')
    db.session.add(role_user)
    db.session.commit()
if not models.User.query.filter_by(password="MTS61PWD").first():
    print("------------ No Admin User found ------------")
    role_ = models.Role.query.filter_by(name="Admin").first()
    admin_user = models.User(password="MTS61PWD", used=False)
    admin_user.roles = [role_,]
    db.session.add(admin_user)
    db.session.commit()

from app import routes

# Initialize Flask-BabelEx
babel = Babel(app)

class MyModelView(ModelView):
    # Allow only admins to access Admin views
    def is_accessible(self):
        if not current_user.is_authenticated: return False
        return current_user.has_roles('Admin')

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        return super(MyAdminIndexView, self).index()

admin = Admin(app, name='Backend', index_view=MyAdminIndexView(), template_mode='bootstrap3')
admin.add_view(MyModelView(models.Question, db.session))
admin.add_view(MyModelView(models.Answer, db.session))
admin.add_view(MyModelView(models.User, db.session))