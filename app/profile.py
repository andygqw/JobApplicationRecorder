from flask import render_template, session, redirect, url_for, request
from app import app, mysql
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
                s += "email = '" + userDetails['email'].replace("'", "\\'")
                s += "' WHERE id = " + str(session['user_id'])
                s += ";"

                cur = mysql.connection.cursor()
                cur.execute(s)
                mysql.connection.commit()
                cur.close()

                session['username'] = userDetails['username']

                log(op, session['username'], "User edited succesfully")
                return redirect(url_for('profile'))
            except Exception as e:
                log(op, "FailedEditUserHolder", str(e))
        else:

            u = get_profile_for_user(session['user_id'])
            c = get_config_for_user(session['user_id'])
            return render_template('profile.html', user = u, config = c)  
    else:
        return redirect(url_for('login'))

def get_profile_for_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `Users` WHERE id = %s;", [user_id])
    user = cur.fetchone()
    cur.close()
    return user

def get_config_for_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `Config` WHERE user_id = %s;", [user_id])
    config = cur.fetchone()
    cur.close()
    return config