from config import configure_app
from flask import Flask, render_template, redirect, logging
from flask_sqlalchemy import SQLAlchemy
from flask.ext.security import login_required, logout_user

# create the application
app = Flask(__name__)

# configure the application
configure_app(app)

# logging setup
#logger = logging.getLogger('flask-blogging')
#logger.setLevel(logging.DEBUG)
#logger.addHandler(logging.StreamHandler())
#logger.debug('debug message')

# start the database 
db = SQLAlchemy(app)

# configure the security
from security import security, configure_security, User

# blogging extention
from blogging import blogging_engine, configure_blogging

# execute before first request is processed
@app.before_first_request
def before_first_request():
    configure_security()
    configure_blogging()
    pass

# Views
@app.route('/')
@login_required
def home():
    return render_template('index.html')
