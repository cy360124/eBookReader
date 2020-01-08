import socket
import sys
import json

Host = '127.0.0.1'
Port = 8848
BUFSIZE = 4096 * 4
mySock = socket.socket()

try:
    mySock.connect((Host, Port))
except Exception:
    print('connetct error')
    mySock.close()
    sys.exit()

def close():
    mySock.close()
    sys.exit()

def login(uname, pwd):
    # send the request
    request = {'url':'/users?username={}&password={}'.format(uname, pwd), \
               'action':'read', 'body':''}
    data = json.dumps(request)
    mySock.sendall(data.encode('utf-8'))
    # response
    recv_data = mySock.recv(BUFSIZE)
    # check
    if len(recv_data) <= 0:
        return ("502", "")
    response = json.loads(recv_data.decode('utf-8'))
    state = response['state']
    body = response['body']
    return (state, body)

def register(uname, pwd):
    # send the requset
    request = {'url':'/users?username={}&password={}'.format(uname, pwd), \
               'action':'add', 'body':''}
    data = json.dumps(request)
    mySock.sendall(data.encode('utf-8'))
    # response
    recv_data = mySock.recv(BUFSIZE)
    # check
    if len(recv_data) <= 0:
        return ("502", "")
    response = json.loads(recv_data.decode('utf-8'))
    state = response['state']
    body = response['body']
    return (state, body)
 
def read_book_list():
    # send the request
    request = {'url':'/books?bookname=%&pageNo=0', 'action':'read', 'body':''}
    data = json.dumps(request)
    mySock.sendall(data.encode('utf-8'))
    # response
    recv_data = mySock.recv(BUFSIZE)
    # check
    if len(recv_data) <= 0:
        return ("502", "")
    response = json.loads(recv_data.decode('utf-8'))
    state = response['state']
    body = response['body']
    return (state, body)

def read_book(bookname, pageNo):
    request = {'url':'/books?bookname={}&pageNo={}'.format(bookname, str(pageNo)), \
               'action':'read', 'body':''}
    data = json.dumps(request)
    mySock.sendall(data.encode('utf-8'))
    # response
    recv_data = mySock.recv(BUFSIZE)
    # check
    if len(recv_data) <= 0:
        return ("502", "")
    response = json.loads(recv_data.decode('utf-8'))
    state = response['state']
    body = response['body']
    return (state, body)

# 注意：mark_list是元组构成的列表， 元组形式为(markname, )
def read_mark_list(uname, bookname):
    request = {'url':'/marks?username={}&bookname={}&markname=%'.format(uname, bookname), \
               'action':'read', 'body':''}
    data = json.dumps(request)
    mySock.sendall(data.encode('utf-8'))
    # response
    recv_data = mySock.recv(BUFSIZE)
    # check
    if len(recv_data) <= 0:
        return ("502", "")
    response = json.loads(recv_data.decode('utf-8'))
    state = response['state']
    body = response['body']
    return (state, body)

# mark是元组构成的列表，元组形式为(markname, pageNo, description)
def read_mark(uname, bookname, markname):
    request = {'url':'/marks?username={}&bookname={}&markname={}'.format(uname, bookname, markname), \
               'action':'read', 'body':''}
    data = json.dumps(request)
    mySock.sendall(data.encode('utf-8'))
    # response
    recv_data = mySock.recv(BUFSIZE)
    # check
    if len(recv_data) <= 0:
        return ("502", "")
    response = json.loads(recv_data.decode('utf-8'))
    state = response['state']
    body = response['body']
    return (state, body)

def update_mark(uname, bookname, markname, description):
    request = {'url':'/marks?username={}&bookname={}&markname={}'.format(uname, bookname, markname), \
               'action':'update', 'body':'&description={}'.format(description)}
    data = json.dumps(request)
    mySock.sendall(data.encode('utf-8'))
    # response
    recv_data = mySock.recv(BUFSIZE)
    # check
    if len(recv_data) <= 0:
        return ("502", "")
    response = json.loads(recv_data.decode('utf-8'))
    state = response['state']
    body = response['body']
    return (state, body)

def add_mark(uname, bookname, markname, pageNo, description):
    request = {'url':'/marks?username={}&bookname={}&markname={}'.format(uname, bookname, markname), \
               'action':'add', 'body':'&pageNo={}&description={}'.format(str(pageNo), description)}
    data = json.dumps(request)
    mySock.sendall(data.encode('utf-8'))
    # response
    recv_data = mySock.recv(BUFSIZE)
    # check
    if len(recv_data) <= 0:
        return ("502", "")
    response = json.loads(recv_data.decode('utf-8'))
    state = response['state']
    body = response['body']
    return (state, body)

def delete_mark(uname, bookname, markname):
    request = {'url':'/marks?username={}&bookname={}&markname={}'.format(uname, bookname, markname), \
               'action':'delete', 'body':''}
    data = json.dumps(request)
    mySock.sendall(data.encode('utf-8'))
    # response
    recv_data = mySock.recv(BUFSIZE)
    # check
    if len(recv_data) <= 0:
        return ("502", "")
    response = json.loads(recv_data.decode('utf-8'))
    state = response['state']
    body = response['body']
    return (state, body)
