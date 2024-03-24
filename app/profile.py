from flask import render_template, session, redirect, url_for, request
from app import app, mysql
from app.logger import log


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if session.get('logged_in'):
        if request.method == 'POST':
            # Process form data and update user profile
            # Assume 'get_profile_for_user' and 'update_profile_for_user' are defined
            # Retrieve profile based on current user's identification
            # profile = get_profile_for_user(user_id)
            # profile.username = request.form['username']
            # profile.email = request.form['email']
            # profile.bio = request.form['bio']
            # profile.location = request.form['location']
            # flash('Your profile has been updated.')
            return redirect(url_for('dashboard'))
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