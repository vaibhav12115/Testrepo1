import MySQLdb

def get_connection_fm():
    db_conn = MySQLdb.connect(host='172.16.1.99', port=3306, user='appuser', passwd='appuser', db='feeds_master')
    db_conn.autocommit = True
    return db_conn