import MySQLdb

def getconnection():
    db_conn = MySQLdb.connect(host='172.16.1.99', port=3306, user='appuser', passwd='appuser', db='djangotest')
    db_conn.autocommit = True
    return db_conn
