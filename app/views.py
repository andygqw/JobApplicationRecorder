from flask import render_template, session, redirect, url_for, request
from app import app, mysql
from app.logger import log

import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime

# Main route
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    try:
        if session.get('logged_in'):

            jobs = fetch_all_jobs_for_user(session['user_id'])

            for job in jobs:
                job['isMarked'] = str(int.from_bytes(job['isMarked'], 'big'))
                if job['job_description'] == None:
                    job['job_description'] = ""
                if job['notes'] == None:
                    job['notes'] = ""
                if job['resume_version'] == None:
                    job['resume_version'] = ""
            applied_count = sum(1 for job in jobs if job['status'] != 'Rejected')
            rejected_count = sum(1 for job in jobs if job['status'] == 'Rejected')

            jobStatusOptions = ['Applied', 'Viewed','Rejected', 'Gave up', 'Interviewing', 'Expired'] 
            return render_template('dashboard.html', username=session.get('username'),
                                        jobs = jobs, jobStatusOptions = jobStatusOptions,
                                        applied_count=applied_count, rejected_count=rejected_count)
        else:
            return redirect(url_for('login'))
    except Exception as e:
        log("Dashboard", "FailedLoadHolder", str(e), False)
        return redirect(url_for('login'))

@app.route('/editjob', methods=['POST'])
def edit_job():
    op = "Edit job"
    if session.get('logged_in'):
        try:
            userDetails = request.form

            cur = mysql.connection.cursor()

            s = "UPDATE JobApplications SET job_title = '" + userDetails['job_title'].replace("'", "\\'") + "', "
            s += "company_name = '" + userDetails['company_name'].replace("'", "\\'") + "', "
            s += "job_description = '" + userDetails['job_description'].replace("'", "\\'") + "', "
            s += "job_location = '" + userDetails['job_location'].replace("'", "\\'") + "', "
            s += "job_url = '" + userDetails['job_url'].replace("'", "\\'") + "', "
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
            s += "notes = '" + userDetails['notes'].replace("'", "\\'") + "', "
            s += "isMarked = " + ('1' if 'isMarked' in userDetails and userDetails['isMarked'] == 'on' else '0')
            s += " WHERE id = " + userDetails['id'] + ";"
            cur.execute(s)

            mysql.connection.commit()
            cur.close()
            log(op, session['username'], "Job edited successfully ", True)
            return redirect(url_for('dashboard'))
        except Exception as e:
            log(op, "FailedEditJobHolder", str(e) + " " + s, False)
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

            s = "INSERT INTO JobApplications (user_id, job_title, company_name, job_description, job_location, job_url, application_deadline_date, application_date, resume_version, status, notes, isMarked)"
            s += " VALUES ("
            s += str(session['user_id']).replace("'", "\\'") + ","
            s += "'" + userDetails['job_title'].replace("'", "\\'") + "',"
            s += "'" + userDetails['company_name'].replace("'", "\\'") + "',"
            s += "'" + str(userDetails['job_description']).replace("'", "\\'") + "',"
            s += "'" + userDetails['job_location'].replace("'", "\\'") + "',"
            s += "'" + userDetails['job_url'].replace("'", "\\'") + "',"
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
            s += "'" + userDetails['notes'].replace("'", "\\'") + "',"
            s += ('1' if 'isMarked' in userDetails and userDetails['isMarked'] == 'on' else '0')
            s += ");"

            cur.execute(s)

            mysql.connection.commit()
            cur.close()
            log(op, session['username'], "Job added successfully ", True)
            return redirect(url_for('dashboard'))
        except Exception as e:
            log(op, "FailedAddJobHolder", str(e) + " " + s, False)
            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))
    
@app.route('/delete_job/<int:item_id>', methods=['POST'])
def delete_job(item_id):
    op = "Delete job"
    if session.get('logged_in'):
        try:
            cur = mysql.connection.cursor()
            s = "DELETE FROM JobApplications WHERE id = " + str(item_id) + ";"
            cur.execute(s)
            mysql.connection.commit()
            cur.close()
            log(op, session['username'], "Job deleted succesfully ", True)
            return '', 204
        except Exception as e:
            log(op, "FailedDeleteJobHolder", str(e), False)
            return '', 400
    else:
        return '', 401
    
@app.route('/quick_add', methods=['POST'])
def quick_add():
    op = "quick_add"
    if session.get('logged_in'):
        try:
            userDetails = request.form
            url = userDetails['quickAddUrl']
            headers = {
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'
            }

            response = requests.get(url, headers=headers)

            titleClass = "top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title"
            companyClass = "top-card-layout__second-subline font-sans text-sm leading-open text-color-text-low-emphasis mt-0.5"
            companyNameClass = "topcard__org-name-link topcard__flavor--black-link"
            companyLocClass = "topcard__flavor topcard__flavor--bullet"

            if response.ok:

                content = response.text

                soup = bs(content, "html.parser")

                titleTag = soup.find_all("h1", class_=titleClass)
                title = ""
                for t in titleTag:
                    title = t.contents[0]

                c = soup.find_all("a", class_=companyNameClass)
                l = soup.find_all("span",class_=companyLocClass)
                for name in c:
                    companyName = (name.contents[0]).strip()
                for loc in l:
                    location = (loc.contents[0]).strip()

                cur = mysql.connection.cursor()

                cur.execute("SELECT * FROM `Config` WHERE user_id = %s;", [session['user_id']])
                config = cur.fetchone()

                resumeVer = ""

                if config == None:
                    s = "INSERT INTO Config (user_id, quickAddResumeVersion, create_time) VALUES ("
                    s += str(session['user_id']).replace("'", "\\'") + ","
                    s += "NULL, "
                    s += "NOW()"
                    s += ");"
                else:
                    resumeVer = config['quickAddResumeVersion']

                s = "INSERT INTO JobApplications (user_id, job_title, company_name, job_location, job_url, application_date, resume_version, status, isMarked)"
                s += " VALUES ("
                s += str(session['user_id']).replace("'", "\\'") + ","
                s += "'" + title.replace("'", "\\'") + "',"
                s += "'" + companyName + "',"
                s += "'" + location.replace("'", "\\'") + "',"
                s += "'" + url.replace("'", "\\'") + "',"
                s += "'" + str(datetime.now()) + "',"
                s += "'" + resumeVer + "',"
                s += "'Applied', "
                s += '0' + ");"
                cur.execute(s)
                mysql.connection.commit()
                cur.close()
                log(op, session['username'], "Quick Add successfully: ", True)
            else:
                log(op, "FailedQuickAddHolder", "Failed to load page: " + str(response.status_code), False)
            return redirect(url_for('dashboard'))
        except Exception as e:
            log(op, "FailedQuickAddHolder", str(e), False)
            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

    
def fetch_all_jobs_for_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `JobApplications` WHERE user_id = %s ORDER BY application_date DESC, id DESC", [user_id])
    jobs = cur.fetchall()
    cur.close()
    return jobs