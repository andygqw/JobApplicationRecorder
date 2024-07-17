from flask import render_template, session, redirect, url_for, request
from app import app, mysql, views
from app.logger import log


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    op = "Edit User"
    if session.get('logged_in'):
        if request.method == 'POST':

            try:
                userDetails = request.form

                s = "UPDATE Users SET "
                s += "username = '" + userDetails['username'].replace("'", "\\'") + "', "
                s += "email = '" + userDetails['email'].replace("'", "\\'") + "' "
                s += "WHERE id = " + str(session['user_id'])
                s += ";"

                # cur = mysql.connection.cursor()
                # cur.execute(s)
                # mysql.connection.commit()
                # cur.close()

                response = views.make_request_by_query(s)
                if response.ok:
                    session['username'] = userDetails['username']

                    log(op, session['username'], "User edited succesfully", True)
                    return redirect(url_for('profile'))
                else:
                    raise Exception(response.text)
                
            except Exception as e:
                log(op, "FailedEditUserHolder", str(e), False)
        else:

            u = get_profile_for_user(session['user_id'])
            c = get_config_for_user(session['user_id'])
            return render_template('profile.html', user = u, config = c)  
    else:
        return redirect(url_for('login'))
    
@app.route('/config', methods=['POST'])
def config():
    op = "Edit Config"
    if session.get('logged_in'):
        try:
            userDetails = request.form

            # cur = mysql.connection.cursor()

            # cur.execute("SELECT * FROM `Config` WHERE user_id = %s;", [session['user_id']])
            # config = cur.fetchone()
            response = views.make_request_by_query(f"SELECT * FROM `config` WHERE user_id = {session['user_id']};")
            if(response.ok):
                data = response.json()
                configs = []
                rows = data['result'][0]['results']['rows']
                columns = data['result'][0]['results']['columns']
                for row in rows:
                    config = {columns[i]: row[i] for i in range(len(columns))}
                    configs.append(config)
            else:
                raise Exception(response.text)

            if len(configs) == 0:
                s = "INSERT INTO config (user_id, quickAddResumeVersion, create_time) VALUES ("
                s += str(session['user_id']).replace("'", "\\'") + ","
                s += "'" + userDetails['quickAddResumeVersion'].replace("'", "\\'") + "', "
                s += "NOW()"
                s += ");"
            else:
                s = "UPDATE config SET "
                s += "quickAddResumeVersion = '" + userDetails['quickAddResumeVersion'].replace("'", "\\'") + "' "
                s += "WHERE id = " + str(configs[0]['id'])
                s += ";"

            # cur.execute(s)
            # mysql.connection.commit()
            # cur.close()

            response = views.make_request_by_query(s)

            if response.ok:
                log(op, session['username'], "Config edited succesfully", True)
                return redirect(url_for('profile'))
            else:
                raise Exception(response.text)

        except Exception as e:
            log(op, "FailedEditConfigHolder", str(e), False)
            return redirect(url_for('profile'))
    else:
        return redirect(url_for('login'))

def get_profile_for_user(user_id):
    # cur = mysql.connection.cursor()
    # cur.execute("SELECT * FROM `Users` WHERE id = %s;", [user_id])
    # user = cur.fetchone()
    # cur.close()
    response = views.make_request_by_query(f"SELECT * FROM `users` WHERE id = {user_id};")
    if response.ok:
        data = response.json()
        users = []
        rows = data['result'][0]['results']['rows']
        columns = data['result'][0]['results']['columns']
        for row in rows:
            user = {columns[i]: row[i] for i in range(len(columns))}
    else:
        raise Exception(response.text)

    return user

def get_config_for_user(user_id):
    # cur = mysql.connection.cursor()
    # cur.execute("SELECT * FROM `Config` WHERE user_id = %s;", [user_id])
    # config = cur.fetchone()
    # cur.close()

    response = views.make_request_by_query(f"SELECT * FROM `config` WHERE user_id = {user_id};")
    if response.ok:
        data = response.json()
        configs = []
        rows = data['result'][0]['results']['rows']
        columns = data['result'][0]['results']['columns']
        for row in rows:
            config = {columns[i]: row[i] for i in range(len(columns))}
    else:
        raise Exception(response.text)

    return config