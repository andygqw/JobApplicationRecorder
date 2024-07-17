from flask import request, redirect, render_template, session, url_for
from app import app, mysql, bcrypt, views
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
            # cur = mysql.connection.cursor()
            # result = cur.execute("SELECT * FROM Users WHERE username = %s", [username])

            response = views.make_request_by_query(f"SELECT * FROM users WHERE username = \'{username}\'")
            if response.ok:
                data = response.json()
                rows = data['result'][0]['results']['rows']
                if(len(rows) != 0):
                    raise Exception("Username already exists")
            else:
                raise Exception(response.text)
            
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            # cur.execute("INSERT INTO Users(username, email, password, registration_date) VALUES(%s, %s, %s, %s)",(username, email, hashed_password, datetime.now()))
            # mysql.connection.commit()
            # cur.close()
            s = f"INSERT INTO users(username, email, password, registration_date) VALUES(\'{username}\', \'{email}\', \'{hashed_password}\', \'{datetime.now().strftime('%Y-%m-%d')}\')"
            response = views.make_request_by_query(s)

            if response.ok:
                log(op, username,"Registered successfully",True)
                return redirect(url_for('login')) # login route
            else:
                raise Exception(response.text)
            
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
            # cur = mysql.connection.cursor()
            # result = cur.execute("SELECT * FROM Users WHERE username = %s", [username])
            response = views.make_request_by_query(f"SELECT * FROM users WHERE username = \'{username}\'")

            if(response.ok):
                data = response.json()
    
                users = []
                rows = data['result'][0]['results']['rows']
                columns = data['result'][0]['results']['columns']
                for row in rows:
                    user = {columns[i]: row[i] for i in range(len(columns))}
                    users.append(user)
            else:
                raise Exception(response.text)

            if len(users) > 0:
                for user in users:
                    # user_details = cur.fetchone()
                    if bcrypt.check_password_hash(user['password'], password):
                        # Password is correct
                        session['logged_in'] = True
                        session['username'] = user['username']
                        session['user_id'] = user['id']
                        log(op, session['username'],"Logged in successfully", True)
                        return redirect(url_for('dashboard'))
                    
                raise Exception("Incorrect password")
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