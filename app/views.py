from flask import render_template, session, redirect, url_for
from app import app, mysql

# Main route
@app.route('/')
def home():
    return render_template('home.html')

# Dashboard (protected area)
@app.route('/dashboard')
def dashboard():
    if session.get('logged_in'):

        jobs = fetch_all_jobs_for_user(session['user_id'])
        return render_template('dashboard.html', username=session.get('username'),jobs = jobs)
    else:
        return redirect(url_for('login'))
    
def fetch_all_jobs_for_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `JobApplications` WHERE user_id = %s ORDER BY application_date DESC", [user_id])
    jobs = cur.fetchall()
    cur.close()
    return jobs