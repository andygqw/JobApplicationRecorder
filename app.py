from flask import Flask
from flask import request, render_template, redirect, url_for, flash
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

mysql = MySQL(app)

@app.route("/")
def users():
    cur = mysql.connection.cursor()
    cur.execute("""SELECT user, host FROM mysql.user""")
    rv = cur.fetchall()
    return str(rv)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        userDetails = request.form
        #username = userDetails['username']
        email = userDetails['email']
        password = userDetails['password']  # TODO: hash this
        lastName = userDetails['lastName']
        firstName = userDetails['firstName']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Users(email, password, lastName, firstName) VALUES(%s, %s, %s, %s)",(email, password, lastName, firstName))
        mysql.connection.commit()
        cur.close()
        flash('Registration successful!')
        return redirect(url_for('login')) # login route
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userDetails = request.form
        email = userDetails['email']
        password = userDetails['password']  # TODO: hash this
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", [email, password])
        if result > 0:
            # User exists and password is correct
            return redirect(url_for('dashboard'))  # Redirect to a protected dashboard
        else:
            flash('Invalid login credentials')
    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)