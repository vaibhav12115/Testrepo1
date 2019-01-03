import MySQLdb

def get_connection_ref():
        db_conn = MySQLdb.connect(host='172.16.1.99', port=3306, user='appuser', passwd='appuser',
                          db='referrals')
        db_conn.autocommit = True
        return db_conn