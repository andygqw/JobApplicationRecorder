from datetime import datetime
from flask import flash
from app import views

def log(operation, user, notes, category):
    if(operation != "" and operation != None):
        if category:
            flash(operation + ": " + notes, 'success')
        else:
            flash(operation + ": " + notes, 'danger')
        # cur = mysql.connection.cursor()
        # result = cur.execute("SELECT id FROM `Users` WHERE username = %s", [user])
        response = views.make_request_by_query(f"SELECT id FROM `users` WHERE username = \'{user}\'")
        if response.ok:
            data = response.json()
            id = data['result'][0]['results']['rows']
        else:
            raise Exception(response.text)

        if id != None:
            # user = cur.fetchone()
            # user_id = user['id']
            # cur.execute("INSERT INTO `Log` (operation, date, user_id, notes) VALUES (%s, %s, %s, %s)", (operation, datetime.now(), user_id, notes))
            # mysql.connection.commit()
            # cur.close()
            response = views.make_request_by_query(f"INSERT INTO `log` (operation, date, user_id, notes) VALUES (\'{operation}\', \'{datetime.now().strftime('%Y-%m-%d')}\', \'{id[0][0]}\', \'{notes}\')")
            if not response.ok:
                raise Exception(response.text)
        else:
            # cur.execute("INSERT INTO `Log` (operation, date, notes) VALUES (%s, %s, %s)", (operation, datetime.now(), notes))
            # mysql.connection.commit()
            # cur.close()
            response = views.make_request_by_query(f"INSERT INTO `log` (operation, date, notes) VALUES (\'{operation}\', \'{datetime.now()}\', \'{notes}\')")
            if not response.ok:
                raise Exception(response.text)