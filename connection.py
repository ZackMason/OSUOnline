import pymysql

def connect(usr, pswd, db):
    return pymysql.connect(host='classmysql.engr.oregonstate.edu',
        user=usr,
        password=pswd,
        database=db,
        cursorclass=pymysql.cursors.DictCursor)
