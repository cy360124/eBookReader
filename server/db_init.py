# this file is used to initialize the database
# by creating some basic tables
import sqlite3

dbpath = 'database/myDatabase'

# create the User table
def user_init():
    # connect to the database
    conn = sqlite3.connect(dbpath)
    curs = conn.cursor()
    # delete old table if exists
    curs.execute("drop table if exists 'User'")
    # User table: username char(16), password char(32)
    curs.execute("create table User (username char(16), password char(32))")
    print("new User table is created successfully!")
    # close the connection
    conn.commit()
    conn.close()

# create the Bookmark table
def bookmark_init():
    # connect to the database
    conn = sqlite3.connect(dbpath)
    curs = conn.cursor()
    # delete old table if exists
    curs.execute("drop table if exists 'Bookmark'")
    # Bookmark table: username char(16), bookname char(128), markname char(128), 
    #                 pageNo int(4), description char(1024)
    curs.execute("create table Bookmark (username char(16), bookname char(128), markname char(128), \
                                         pageNo int(4), description char(1024))")
    print("Bookmark table is created successfully!")
    # close the connection
    conn.commit()
    conn.close()

user_init()
bookmark_init()
