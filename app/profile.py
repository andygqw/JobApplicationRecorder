from flask import Flask, render_template, request, redirect, url_for, flash, session
from app import app, mysql


app = Flask(__name__)

@app.route('/profile', methods=['GET', 'POST'])
def edit_profile():
    if session.get('logged_in'):
        if request.method == 'POST':
            # Process form data and update user profile
            # Assume 'get_profile_for_user' and 'update_profile_for_user' are defined
            # Retrieve profile based on current user's identification
            profile = get_profile_for_user(user_id)
            profile.username = request.form['username']
            profile.email = request.form['email']
            profile.bio = request.form['bio']
            profile.location = request.form['location']
            flash('Your profile has been updated.')
            return redirect(url_for('dashboard'))
        else:
            # Display the form with existing profile data
            user_id =  session["user_id"]
            user = get_profile_for_user(user_id)
            return render_template('profile.html', user=user)  
    else:
        return redirect(url_for('login'))

def get_profile_for_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `Users` WHERE id = %s;", [user_id])
    user = cur.fetchall()
    cur.close()
    return user