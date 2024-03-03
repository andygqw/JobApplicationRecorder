from flask import render_template, session, redirect, url_for, request
from app import app, mysql
from app.logger import log

# Main route
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    try:
        if session.get('logged_in'):

            jobs = fetch_all_jobs_for_user(session['user_id'])
            return render_template('dashboard.html', username=session.get('username'),jobs = jobs)
        else:
            return redirect(url_for('login'))
    except Exception as e:
        log("Dashboard", "FailedLoadHolder", str(e))
        return redirect(url_for('login'))

@app.route('/editjob', methods=['POST'])
def edit_job():
    op = "Edit job"
    if session.get('logged_in'):
        try:
            userDetails = request.form
            cur = mysql.connection.cursor()

            s = "UPDATE JobApplications SET job_title = '" + userDetails['job_title'] + "', "
            s += "company_name = '" + userDetails['company_name'] + "', "
            s += "job_description = '" + userDetails['job_description'] + "', "
            s += "job_location = '" + userDetails['job_location'] + "', "
            s += "job_url = '" + userDetails['job_url'] + "', "
            if userDetails['application_deadline_date'] == None or userDetails['application_deadline_date'] == "":
                s += "application_deadline_date = NULL, "
            else:
                s += "application_deadline_date = '" + str(userDetails['application_deadline_date']) + "', "
            if userDetails['application_date'] == None or userDetails['application_date'] == "":
                s += "application_date = NULL, "
            else:
                s += "application_date = '" + str(userDetails['application_date']) + "', "
            s += "resume_version = '" + userDetails['resume_version'] + "', "
            s += "status = '" + userDetails['status'] + "', "
            s += "notes = '" + userDetails['notes'] + "' "
            s += "WHERE id = " + userDetails['id'] + ";"
            cur.execute(s)

            mysql.connection.commit()
            cur.close()
            log(op, session['username'], "Job edited successfully " + s)
            return redirect(url_for('dashboard'))
        except Exception as e:
            log(op, "FailedEditJobHolder", str(e) + " " + s)
            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))
    
@app.route('/addjob', methods=['POST'])
def add_job():
    op = "Add job"
    if session.get('logged_in'):
        try:
            userDetails = request.form
            cur = mysql.connection.cursor()

            s = "INSERT INTO JobApplications (user_id, job_title, company_name, job_description, job_location, job_url, application_deadline_date, application_date, resume_version, status, notes)"
            s += " VALUES ("
            s += str(session['user_id']) + ","
            s += "'" + userDetails['job_title'] + "',"
            s += "'" + userDetails['company_name'] + "',"
            s += "'" + userDetails['job_description'] + "',"
            s += "'" + userDetails['job_location'] + "',"
            s += "'" + userDetails['job_url'] + "',"
            if userDetails['application_deadline_date'] == None or userDetails['application_deadline_date'] == "":
                s += "NULL,"
            else:
                s += "'" + str(userDetails['application_deadline_date']) + "',"
            if userDetails['application_date'] == None or userDetails['application_date'] == "":
                s += "NULL,"
            else:
                s += "'" + str(userDetails['application_date']) + "',"
            s += "'" + userDetails['resume_version'] + "',"
            s += "'" + userDetails['status'] + "',"
            s += "'" + userDetails['notes'] + "'"
            s += ");"

            cur.execute(s)

            mysql.connection.commit()
            cur.close()
            log(op, session['username'], "Job added successfully " + s)
            return redirect(url_for('dashboard'))
        except Exception as e:
            log(op, "FailedAddJobHolder", str(e) + " " + s)
            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

    
def fetch_all_jobs_for_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `JobApplications` WHERE user_id = %s ORDER BY application_date DESC", [user_id])
    jobs = cur.fetchall()
    cur.close()
    return jobs