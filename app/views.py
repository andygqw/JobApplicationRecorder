from flask import render_template, session, redirect, url_for, request, jsonify
from app import app
from app.logger import log

import requests, re
from bs4 import BeautifulSoup as bs
from datetime import datetime

from dotenv import load_dotenv
import os

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
                #job['is_marked'] = str(int.from_bytes(job['is_marked'], 'big'))
                if job['job_description'] == None:
                    job['job_description'] = ""
                if job['notes'] == None:
                    job['notes'] = ""
                if job['resume_version'] == None:
                    job['resume_version'] = ""

            rejected_count = sum(1 for job in jobs if job['status'] == 'Rejected')
            rejected_rate = (len(jobs)/rejected_count)

            jobStatusOptions = ['Applied', 'Viewed','Rejected', 'Gave up', 'Interviewing', 'Expired', 'Saved'] 
            return render_template('dashboard.html', username=session.get('username'),
                                        jobs = jobs, jobStatusOptions = jobStatusOptions,
                                        rejected_count=rejected_count,
                                        rejected_rate=calculate_percentage(rejected_count, len(jobs)))
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

            # cur = mysql.connection.cursor()

            s = "UPDATE job_applications SET job_title = '" + userDetails['job_title'].replace("'", "\\'") + "', "
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
            s += "is_marked = " + ('1' if 'is_marked' in userDetails and userDetails['is_marked'] == 'on' else '0')
            s += " WHERE id = " + userDetails['id'] + ";"
            # cur.execute(s)

            # mysql.connection.commit()
            # cur.close()

            response = make_request_by_query(s)
            if(response.ok):
                log(op, session['username'], "Job edited successfully ", True)
                return redirect(url_for('dashboard'))
            else:
                raise Exception(response.text)
            
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
            # cur = mysql.connection.cursor()

            s = "INSERT INTO job_applications (user_id, job_title, company_name, job_description, job_location, job_url, application_deadline_date, application_date, resume_version, status, notes, is_marked)"
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
            s += ('1' if 'is_marked' in userDetails and userDetails['is_marked'] == 'on' else '0')
            s += ");"

            # cur.execute(s)

            # mysql.connection.commit()
            # cur.close()

            response = make_request_by_query(s)
            if(response.ok):
                log(op, session['username'], "Job added successfully ", True)
                return redirect(url_for('dashboard'))
            else:
                raise Exception(response.text)
            
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
            # cur = mysql.connection.cursor()
            s = "DELETE FROM job_applications WHERE id = " + str(item_id) + ";"
            # cur.execute(s)
            # mysql.connection.commit()
            # cur.close()

            response = make_request_by_query(s)
            if(response.ok):
                log(op, session['username'], "Job deleted succesfully ", True)
                return '', 204
            else:
                raise Exception(response.text)
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

            LINKEDIN = "linkedin.com"
            HANDSHAKE = "handshake.com"
            INDEED = "indeed.com"

            title = ""
            companyName = ""
            location = ""

            if LINKEDIN in url:

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
                else:
                    raise Exception("Failed to load page: " + str(response.status_code))

            # elif INDEED in url:

            #     headers = {
            #         'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
            #         'Priority':'i',
            #         'Referer':'www.indeed.com',
            #         'Accept':'text/html, application/xhtml+xml, image/jxr, */*',
            #         'Accept-Language':'en-US,en;q=0.8',
            #         'Cache-Control':'no-cache',
            #         'authority':'t.indeed.com'
            #     }
            #     response = requests.get(url, headers=headers)

            #     titleClass = "jobsearch-JobInfoHeader-title"#h2
            #     companyClass = "jobsearch-CompanyInfoContainer"#div
            #     locationClass= "inlineHeader-companyLocation"#div

            #     if response.ok:

            #         content = response.text
            #         print(content)

            #         soup = bs(content, "html.parser")

            #         # Find all h2 elements with the specified class
            #         h2_elements = soup.find_all('h2', class_= titleClass)

            #         for h2 in h2_elements:
            #             span = h2.find('span')
            #             if span:
            #                 title = span.text
                    
            #         div_elements = soup.find_all('div', class_= companyClass)
            #         for div in div_elements:
            #             a_tag = div.find('a')
            #             if a_tag:
            #                 companyName = a_tag.text
            #             loc = div.find(class_=locationClass)
            #             if loc:
            #                 location = loc.text                       
                    
            #     else:
            #         raise Exception("Failed to load page: " + str(response.status_code))

            # cur = mysql.connection.cursor()

            # cur.execute("SELECT * FROM `Config` WHERE user_id = %s;", [session['user_id']])
            # config = cur.fetchone()
            else:
                raise Exception("Unsupported site")
            
            response = make_request_by_query(f"SELECT * FROM `config` WHERE user_id = {session['user_id']};")
            if(response.ok):

                data = response.json()
    
                config = []
                rows = data['result'][0]['results']['rows']
                columns = data['result'][0]['results']['columns']
                for row in rows:
                    c = {columns[i]: row[i] for i in range(len(columns))}
                    config.append(c)
                
            else:
                raise Exception(response.text)

            resumeVer = ""

            if config == None:
                s = "INSERT INTO Config (user_id, quickAddResumeVersion, create_time) VALUES ("
                s += str(session['user_id']).replace("'", "\\'") + ","
                s += "NULL, "
                s += "NOW()"
                s += ");"
                response = make_request_by_query(s)
                if not response.ok:
                    raise Exception(response.text)
            else:
                resumeVer = config[0]['quickAddResumeVersion']

            s = "INSERT INTO job_applications (user_id, job_title, company_name, job_location, job_url, application_date, resume_version, status, is_marked)"
            s += " VALUES ("
            s += str(session['user_id']).replace("'", "\\'") + ","
            s += "'" + title.replace("'", "\\'") + "',"
            s += "'" + companyName + "',"
            s += "'" + location.replace("'", "\\'") + "',"
            s += "'" + url.replace("'", "\\'") + "',"
            s += "'" + str(datetime.now().strftime('%Y-%m-%d')) + "',"
            s += "'" + resumeVer + "',"
            s += "'Applied', "
            s += '0' + ");"
            # cur.execute(s)
            # mysql.connection.commit()
            # cur.close()
            response = make_request_by_query(s)
            if response.ok:
                log(op, session['username'], "Quick Add successfully: " + title, True)
                return redirect(url_for('dashboard'))
            else:
                raise Exception(response.text)
            
        except Exception as e:
            log(op, "FailedQuickAddHolder", str(e), False)
            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

    
# def fetch_all_jobs_for_user(user_id):
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM `JobApplications` WHERE user_id = %s ORDER BY application_date DESC, id DESC", [user_id])
#     jobs = cur.fetchall()
#     cur.close()
#     return jobs

def fetch_all_jobs_for_user(user_id):

    payload = {
        "params": [user_id],
        "sql": "SELECT * FROM job_applications WHERE user_id = ? ORDER BY application_date DESC, id DESC;"
    }
    
    response = make_request(payload)
    if response.ok:

        data = response.json()
    
        job_list = []
        rows = data['result'][0]['results']['rows']
        columns = data['result'][0]['results']['columns']
        for row in rows:
            job = {columns[i]: row[i] for i in range(len(columns))}
            job_list.append(job)
        return job_list
    else:
        raise Exception("Failed to retrieve data: " + str(response.status_code))

def make_request(payload):
    load_dotenv()
    url = f"https://api.cloudflare.com/client/v4/accounts/{os.getenv('CF_ACCOUNT_ID')}/d1/database/{os.getenv('CF_DATABASE_ID')}/raw"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('CF_DATABASE_TOKEN')}"
    }

    return requests.request("POST", url, json=payload, headers=headers)

def make_request_by_query(query):
    url = f"https://api.cloudflare.com/client/v4/accounts/{os.getenv('CF_ACCOUNT_ID')}/d1/database/{os.getenv('CF_DATABASE_ID')}/raw"

    payload = {
        "params": [],
        "sql": query
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('CF_DATABASE_TOKEN')}"
    }

    return requests.request("POST", url, json=payload, headers=headers)

def calculate_percentage(numerator, denominator):
    if denominator == 0:
        return "Denominator cannot be zero"
    result = (numerator / denominator) * 100
    return f"{result:.2f}%"