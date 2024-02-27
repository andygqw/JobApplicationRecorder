from flask import render_template, session, redirect, url_for
from app import app

# Main route
@app.route('/')
def home():
    return render_template('home.html')

# Dashboard (protected area)
@app.route('/dashboard')
def dashboard():
    if session.get('logged_in'):
        return render_template('dashboard.html', username=session.get('username'))
    else:
        return redirect(url_for('login'))