from flask import Flask
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from datetime import timedelta

# Initialize the Flask application
app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Required
app.config['MYSQL_HOST'] = 'localhost'
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "--s"
app.config["MYSQL_DB"] = "JobApplications"

# Set session to expire after 30 minutes of inactivity
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)

# Extra configs, optional:
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # This enables dictionary cursor

app.secret_key = 'd#*$&^' 

mysql = MySQL(app)
bcrypt = Bcrypt(app)

from app import views, auth