import json
import fileFunc
import dbFunc

# 201 is ok, body is null
# 202 is wrong, body is null
def login(uname, pwd):
    # check it
    if dbFunc.check_user(uname, pwd):
        response = {'state':'201', 'body':''}
        return response
    # if not exists
    else:
        response = {'state':'202', 'body':''}
        return response

# 203 is ok, body is null
# 204 is wrong, body is null
def register(uname, pwd):
    # try registering
    if dbFunc.add_user(uname, pwd):
        response = {'state':'203', 'body':''}
        return response
    # if uname repeated
    else:
        response = {'state':'204', 'body':''}
        return response

# 301 is ok, body is a list of book names
def read_book_list():
    booklist = fileFunc.read_book_list()
    response = {'state':'301', 'body':booklist}
    return response

# 302 is ok, body is content of book
# 303 is wrong bookname, body is null
# 304 is pageNo out of page, body is null
def read_book(bookname, pageNo):
    # try reading
    (flag, content) = fileFunc.read_book(bookname, pageNo)
    # if bookname is wrong
    if flag == 0:
        response = {'state':'303', 'body':''}
        return response
    # if pageNo is out of range
    elif len(content) == 0:
        response = {'state':'304', 'body':''}
        return response
    # if successful
    else:
        response = {'state':'302', 'body':content}
        return response

# 401 is ok, body is the list of mark names
def read_mark_list(uname, bookname):
    # aim to look through all marks
    rows = dbFunc.read_mark_list(uname, bookname)
    response = {'state':'401', 'body':rows}
    return response

# 402 is ok, body is the mark information
# 407 is wrong(not exists), body is null
def read_mark(uname, bookname, markname):
    row = dbFunc.read_mark(uname, bookname, markname)
    # if not exists
    if row == None:
        response = {'state':'407', 'body':''}
        return response
    # read successfully
    else:
        response = {'state':'402', 'body':row}
        return response

# 403 is ok, body is null
# 407 is wrong(not exists), body is null
def update_mark(uname, bookname, markname, description):
    if dbFunc.update_mark(uname, bookname, markname, description):
        response = {'state':'403', 'body':''}
        return response
    else:
        response = {'state':'407', 'body':''}
        return response

# 404 is ok, body is null
# 406 is wrong(repeated), body is null
def add_mark(uname, bookname, markname, pageNo, description):
    if dbFunc.add_mark(uname, bookname, markname, pageNo, description):
        response = {'state':'404', 'body':''}
        return response
    else:
        response = {'state':'406', 'body':''}
        return response

# 405 is ok, body is null
# 407 is wrong(not exists), body is null
def delete_mark(uname, bookname, markname):
    if dbFunc.delete_mark(uname, bookname, markname):
        response = {'state':'405', 'body':''}
        return response
    else:
        response = {'state':'407', 'body':''}
        return response
