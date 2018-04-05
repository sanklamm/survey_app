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

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)

# for debugging
app.debug = True
# toolbar = DebugToolbarExtension(app)

# for login
login = LoginManager(app)
from app import routes, models

class MyModelView(ModelView):
    # Allow only admins to access Admin views
    def is_accessible(self):
        if not current_user.is_authenticated: return False
        return current_user.has_roles('Admin')
        # return current_user.is_authenticated

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