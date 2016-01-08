
from config import configure_app
from utils import get_instance_folder_path

from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

from flask.ext.blogging import SQLAStorage, BloggingEngine

# create the application
app = Flask(__name__)

# configure the application
configure_app(app)

# start the database 
db = SQLAlchemy(app)

# configure the security
from security import security, configure_security

configure_security()

# blogging extention
storage = SQLAStorage(db=db)
blog_engine = BloggingEngine(app, storage)
db.create_all(bind=['blog'])


# execute before first request is processed
@app.before_first_request
def before_first_request():
    pass

# Views
@app.route('/')
@login_required
def home():
    return render_template('index.html')


