import sqlite3

dbpath = 'database/myDatabase'
    
def show_users():
    conn = sqlite3.connect(dbpath)
    curs = conn.cursor()
    curs.execute('select * from User')
    rows = curs.fetchall()
    # close the connection
    conn.close()
    # show
    for row in rows:
        print(row)

def show_marks():
    conn = sqlite3.connect(dbpath)
    curs = conn.cursor()
    curs.execute('select * from Bookmark')
    rows = curs.fetchall()
    # close the connection
    conn.close()
    # show
    for row in rows:
        print(row)

def delete_user(uname):
    conn = sqlite3.connect(dbpath)
    curs = conn.cursor()
    curs.execute('delete from User where username = ?', (uname,))
    conn.commit()
    conn.close()

