from flask import Flask
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from datetime import timedelta

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Required
app.config['MYSQL_HOST'] = '54.177.5.41'
app.config["MYSQL_USER"] = "Dev"
app.config["MYSQL_PASSWORD"] = "Andywang0704!"
app.config["MYSQL_DB"] = "JobApplications"

# Set session to expire after xx minutes of inactivity
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)

# Extra configs, optional:
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # This enables dictionary cursor

app.secret_key = 'd#*$&^' 

mysql = MySQL(app)
bcrypt = Bcrypt(app)

from app import views, auth