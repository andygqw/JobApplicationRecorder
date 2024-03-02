from flask import render_template, session, redirect, url_for, request
from app import app, mysql
from app.logger import log

# Main route
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if session.get('logged_in'):

        jobs = fetch_all_jobs_for_user(session['user_id'])
        return render_template('dashboard.html', username=session.get('username'),jobs = jobs)
    else:
        return redirect(url_for('login'))

@app.route('/editjob', methods=['POST'])
def edit_job():
    op = "Edit job"
    if session.get('logged_in'):
        try:
            userDetails = request.form
            cur = mysql.connection.cursor()
            cur.execute("UPDATE JobApplication SET job_title = %s, company_name = %s, job_description = %s, job_location = %s, job_url = %s, application_deadline_date = %s, application_date = %s, resume_version = %s, status = %s, notes = %s WHERE id = %s", 
                        (userDetails['job_title'], userDetails['company_name'], userDetails['job_description'], userDetails['job_location'], userDetails['job_url'], userDetails['application_deadline_date'], userDetails['application_date'], userDetails['resume_version'], userDetails['status'], userDetails['notes'], userDetails['id']))
            mysql.connection.commit()
            cur.close()
            log(op, session['username'], "Job edited successfully")
            return redirect(url_for('dashboard'))
        except Exception as e:
            log(op, "Failed to edit job", str(e))
            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))


    
def fetch_all_jobs_for_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `JobApplications` WHERE user_id = %s ORDER BY application_date DESC", [user_id])
    jobs = cur.fetchall()
    cur.close()
    return jobs