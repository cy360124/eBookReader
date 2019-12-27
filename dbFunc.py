import sqlite3

# 数据库的数据结构如下：
# -- User table: username char(16), password char(32)
# -- Bookmark table: username char(16), bookname char(128), markname char(128), 
#                    pageNo int(4), description char(1024)  

# 数据库的搜索结果被组织成以元组为形式的列表

# the path of database
dbpath = r'E:\myLearning\eBookReader\database\myDataBase'

# given the user name and password, search the database to judge whether it exists
# if it exists, return True; else, return False
def check_user(uname, pwd):
    # connect to the database
    conn = sqlite3.connect(dbpath)
    curs = conn.cursor()
    # search
    curs.execute('select * from User where username = ? and password = ?', (uname, pwd))
    row = curs.fetchone()
    # close the connection
    conn.close()
    # judge 
    return not (row == None)

# given the uname and pwd, insert it into User table
# if uname is repeated, return 0; if successful, return 1
def add_user(uname, pwd):
    # connect to the database
    conn = sqlite3.connect(dbpath)
    curs = conn.cursor()
    # search
    curs.execute('select * from User where username = ?', [uname])
    row = curs.fetchone()
    # is a repeated uname
    if row != None:
        conn.close()
        return 0
    # is a new uname
    else:
        # insert into User table
        curs.execute('insert into User values (?, ?)', (uname, pwd))
        conn.commit()
        conn.close()
        return 1

# given the uname and bookname, read mark list in Bookmark table
# return the names of those marks
def read_mark_list(uname, bookname):
    conn = sqlite3.connect(dbpath)
    curs = conn.cursor()
    # search
    curs.execute('select markname from Bookmark \
                  where username = ? and bookname = ? order by pageNo', (uname, bookname))
    rows = curs.fetchall()
    conn.close()
    return rows

# given the uname, bookname and markname, read the specific mark
# return the markname, pageNo and description
def read_mark(uname, bookname, markname):
    conn = sqlite3.connect(dbpath)
    curs = conn.cursor()
    # search
    curs.execute('select markname, pageNo, description from Bookmark \
                  where username = ? and bookname = ? and markname = ?', (uname, bookname, markname))
    row = curs.fetchone()
    conn.close()
    return row

# given the uname, bookname, markname, pageNo and description
# try to insert it into Bookmark table as a new mark
# if repeated, return 0; if successful, return 1
def add_mark(uname, bookname, markname, pageNo, description):
    conn = sqlite3.connect(dbpath)
    curs = conn.cursor()
    # search
    curs.execute('select * from Bookmark where username = ? and bookname = ? and markname = ?', (uname, bookname, markname))
    row = curs.fetchone()
    # if already exists
    if row != None:
        conn.close()
        return 0
    # if not exist, insert it
    else:
        curs.execute('insert into Bookmark values (?, ?, ?, ?, ?)', (uname, bookname, markname, pageNo, description))
        conn.commit()
        conn.close()
        return 1

# given the uname, bookname and markname, modify the mark with the new description
# if no specific mark, return 0; else, update it and return 1
def update_mark(uname, bookname, markname, description):
    conn = sqlite3.connect(dbpath)
    curs = conn.cursor()
    # search
    curs.execute('select * from Bookmark where username = ? and bookname = ? and markname = ?', (uname, bookname, markname))
    row = curs.fetchone()
    # if not exist
    if row == None:
        conn.close()
        return 0
    else:
        curs.execute('update Bookmark set description = ? \
                      where username = ? and bookname = ? and markname = ?', (description, uname, bookname, markname))
        conn.commit()
        conn.close()
        return 1

# given the uname, bookname and markname, delete the specific mark
# if not exists, return 0; else, delete it and return 1
def delete_mark(uname, bookname, markname):
    conn = sqlite3.connect(dbpath)
    curs = conn.cursor()
    # search
    curs.execute('select * from Bookmark where username = ? and bookname = ? and markname = ?', (uname, bookname, markname))
    row = curs.fetchone()
    # if not exists
    if row == None:
        conn.close()
        return 0
    else:
        curs.execute('delete from Bookmark where username = ? and bookname = ? and markname = ?', (uname, bookname, markname))
        conn.commit()
        conn.close()
        return 1

