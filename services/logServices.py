from .. import mysql
from datetime import datetime
from flask import session


def log(operation, notes):
    if(operation != "" and operation != None):
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT user_id FROM `User` WHERE username = %s", [session['username']])
        if result > 0:
            user = cur.fetchone()
            user_id = user['user_id']
            cur.execute("INSERT INTO `Log` (operation, date, user_id, notes) VALUES (%s, %s, %s, %s)", (operation, datetime.now, user_id, notes))
            mysql.connection.commit()
            cur.close()
            return 0
        else:
            cur.execute("INSERT INTO `Log` (operation, date, notes) VALUES (%s, %s, %s)", (operation, datetime.now, notes))
            mysql.connection.commit()
            cur.close()
            return 1