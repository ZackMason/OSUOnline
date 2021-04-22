import pymysql

def connect():
    return pymysql.connect(host='classmysql.engr.oregonstate.edu',
        user='cs340_masonblz',
        password='4022',
        database='cs340_masonblz',
        cursorclass=pymysql.cursors.DictCursor)

