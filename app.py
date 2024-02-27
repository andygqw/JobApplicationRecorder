from flask import Flask
from flask import request, render_template, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# Required
app.config['MYSQL_HOST'] = 'localhost'
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "--"
app.config["MYSQL_DB"] = "JobApplications"
# Extra configs, optional:
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # This enables dictionary cursor

app.secret_key = 'd#*$&^' 


mysql = MySQL(app)
bcrypt = Bcrypt(app)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        userDetails = request.form
        username = userDetails['username']
        email = userDetails['email']
        password = userDetails['password']
        cur = mysql.connection.cursor()
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        cur.execute("INSERT INTO Users(username, email, password) VALUES(%s, %s, %s)",(username, email, hashed_password))
        mysql.connection.commit()
        cur.close()
        flash('Registration successful!')
        return redirect(url_for('login')) # login route
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
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
                return redirect(url_for('dashboard'))
            else:
                # Password is wrong
                flash('Invalid login credentials')
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if session.get('logged_in'):
        return render_template('dashboard.html', email=session.get('email'))
    else:
        flash('Please log in to access the dashboard')
        return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)