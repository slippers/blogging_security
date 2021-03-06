from main import app
from flask import render_template, redirect
from security import login_required, roles_accepted

# Views
@app.route('/')
def home():
    return render_template('index.html', content='home')

@app.route('/index')
@login_required
def index():
    return render_template('index.html',content='index')

@app.route('/profile')
@login_required
def profile():
    return render_template('index.html', content='profile')

@app.route('/admin')
@login_required
@roles_accepted('admin')
def admin():
    return render_template('index.html', content='admin')

@app.route('/admin_or_editor')
@roles_accepted('admin','editor')
@login_required
def admin_or_editor():
    return render_template('index.html', content='admin_or_editor')


