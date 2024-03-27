from datetime import datetime
from flask import flash
from app import mysql

def log(operation, user, notes, category):
    if(operation != "" and operation != None):
        if category:
            flash(operation + ": " + notes, 'success')
        else:
            flash(operation + ": " + notes, 'danger')
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT id FROM `Users` WHERE username = %s", [user])
        if result > 0:
            user = cur.fetchone()
            user_id = user['id']
            cur.execute("INSERT INTO `Log` (operation, date, user_id, notes) VALUES (%s, %s, %s, %s)", (operation, datetime.now(), user_id, notes))
            mysql.connection.commit()
            cur.close()
        else:
            cur.execute("INSERT INTO `Log` (operation, date, notes) VALUES (%s, %s, %s)", (operation, datetime.now(), notes))
            mysql.connection.commit()
            cur.close()