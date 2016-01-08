
from config import configure_app
from utils import get_instance_folder_path

from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

from flask.ext.login import UserMixin, LoginManager, login_user, logout_user
from flask.ext.blogging import SQLAStorage, BloggingEngine

app = Flask(__name__)


configure_app(app)

# extensions
db = SQLAlchemy(app)
storage = SQLAStorage(db=db)

db.create_all(bind=['blog'])

blog_engine = BloggingEngine(app, storage)
login_manager = LoginManager(app)
#meta.create_all(bind=engine)


# user class for providing authentication
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

    def get_name(self):
        return "kirk"  # typically the user's name

@login_manager.user_loader
@blog_engine.user_loader
def load_user(user_id):
    return User(user_id)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login/")
def login():
    user = User("testuser")
    login_user(user)
    return redirect("/blog")

@app.route("/logout/")
def logout():
    logout_user()
    return redirect("/")
