from login.connections import getconnection

def common_query(privilege,finalroleid):
    db_conn=getconnection()
    c=db_conn.cursor()
    pidrow = c.execute("""SELECT id from privileges where privilege_name=%s""", (privilege,))
    pidrows = c.fetchall()
    finalpid = pidrows[0][0]
    c.execute("""INSERT INTO role_privilege (role_id,privilege_id)
        VALUES (%s, %s)""",
          (finalroleid, finalpid))