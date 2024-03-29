from flask import request, redirect, render_template, session, url_for
from app import app, mysql, bcrypt
from app.logger import log
from datetime import datetime

@app.route('/register', methods=['GET', 'POST'])
def register():
    op = "Register"
    if request.method == 'POST':
        try:
            userDetails = request.form
            username = userDetails['username']
            email = userDetails['email']
            password = userDetails['password']
            cur = mysql.connection.cursor()
            result = cur.execute("SELECT * FROM Users WHERE username = %s", [username])
            if(result > 0):
                raise Exception("Username already exists")
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            cur.execute("INSERT INTO Users(username, email, password, registration_date) VALUES(%s, %s, %s, %s)",(username, email, hashed_password, datetime.now()))
            mysql.connection.commit()
            cur.close()            
            log(op, username,"Registered successfully",True)
            return redirect(url_for('login')) # login route
        except Exception as e:
            log(op, "FailedRegisterHolder" , str(e), False)
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    op = "Login"
    if request.method == 'POST':
        try:
            userDetails = request.form
            username = userDetails['username']
            password = userDetails['password']
            cur = mysql.connection.cursor()
            result = cur.execute("SELECT * FROM Users WHERE username = %s", [username])
            if result > 0:
                user_details = cur.fetchone()
                if bcrypt.check_password_hash(user_details['password'], password):
                    # Password is correct
                    session['logged_in'] = True
                    session['username'] = user_details['username']
                    session['user_id'] = user_details['id']
                    log(op, session['username'],"Logged in successfully", True)
                    return redirect(url_for('dashboard'))
                else:
                    # Password is wrong
                    raise Exception("Wrong password: " + user_details['username'])
            else:
                raise Exception("User not found")
        except Exception as e:
            log(op, "FailedLoginHolder", str(e), False)
    return render_template('login.html')

@app.route('/logout')
def logout():
    try:
        name = session['username']
        session.clear()
        log("Logout", name, "Logged out successfully", True)
        return redirect(url_for('home'))
    except Exception as e:
        log("Logout", "FailedLogoutHolder", str(e), False)
        return redirect(url_for('home'))