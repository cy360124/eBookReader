import json
import threading
import serverFunc
from socketserver import BaseRequestHandler,ThreadingTCPServer

BUFSIZE = 4096 * 64

# 处理请求
class Handler(BaseRequestHandler):
    def handle(self):
        address, pid = self.client_address
        print('%s connected!'%address)
        while True:
            # receive data
            recv_data = self.request.recv(BUFSIZE)
            # check
            if len(recv_data) < 0: 
                print("connection close")
                break
            # turn to request
            request = json.loads(recv_data.decode('utf-8'))
            print("request is ", request)
            url = request['url']
            action = request['action']
            body = request['body']
            # find char '?' and get the object
            end = url.find('?')
            obj = url[1:end]

            # login request
            # url: /users?username=...&password=...
            if obj == 'users' and action == 'read':
                # get uname
                begin = url.find('?username=')
                begin = begin + 10
                end = url.find('&password=')
                uname = url[begin:end]
                # get pwd
                begin = end + 10
                pwd = url[begin:]
                # try logining
                response = serverFunc.login(uname, pwd)
    
            # register request
            # url: /users?username=...&password=...
            elif obj == 'users' and action == 'add':
                # get uname
                begin = url.find('?username=')
                begin = begin + 10
                end = url.find('&password=')
                uname = url[begin:end]
                # get pwd
                begin = end + 10
                pwd = url[begin:]
                # try registering
                response = serverFunc.register(uname, pwd)
    
            # get book list request
            # url: /books?bookname=%&pageNo=0
            # Or read book content request
            # url: /books?bookname=...&pageNo=...
            elif obj == 'books' and action == 'read':
                # get bookname
                begin = url.find('?bookname=')
                begin = begin + 10
                end = url.find('&pageNo=')
                bookname = url[begin:end]
                # get pageNo
                begin = end + 8
                pageNo = int(url[begin:])
        
                # if aim to get booklist
                if bookname == '%':
                    response = serverFunc.read_book_list()
                # if aim to read book
                else:
                    response = serverFunc.read_book(bookname, pageNo)

            # search all marks about a book 
            # url: /marks?username=...&bookname=...&markname=%
            # or read a specific mark
            # url: /marks?username=...&bookname=...&markname=...
            elif obj == 'marks' and action == 'read':
                # get username
                begin = url.find('?username=')
                begin = begin + 10
                end = url.find('&bookname=')
                uname = url[begin:end]
                # get bookname
                begin = end + 10
                end = url.find('&markname=')
                bookname = url[begin:end]
                # get markname
                begin = end + 10
                markname = url[begin:]

                # if aim to search all marks
                if markname == '%':
                    response = serverFunc.read_mark_list(uname, bookname)
                # if aim to read a specific mark
                else:
                    response = serverFunc.read_mark(uname, bookname, markname)
    
            # update a mark by modifying its description
            # url: /marks?username=...&bookname=...&markname=...
            # body is &description=...
            elif obj == 'marks' and action == 'update':
                # get username
                begin = url.find('?username=')
                begin = begin + 10
                end = url.find('&bookname=')
                uname = url[begin:end]
                # get bookname
                begin = end + 10
                end = url.find('&markname=')
                bookname = url[begin:end]
                # get markname
                begin = end + 10
                markname = url[begin:]
                # get description
                begin = body.find('&description=')
                begin = begin + 13
                description = body[begin:]
                # update mark
                response = serverFunc.update_mark(uname, bookname, markname, description)

            # add a bookmark
            # url: /marks?username=...&bookname=...&markname=...
            # body is &pageNo=...&description=...
            elif obj == 'marks' and action == 'add':
                # get username
                begin = url.find('?username=')
                begin = begin + 10
                end = url.find('&bookname=')
                uname = url[begin:end]
                # get bookname
                begin = end + 10
                end = url.find('&markname=')
                bookname = url[begin:end]
                # get markname
                begin = end + 10
                markname = url[begin:]
                # get pageNo
                begin = body.find('&pageNo=')
                begin = begin + 8
                end = body.find('&description=')
                pageNo = int(body[begin:end])
                # get description
                begin = end + 13
                description = body[begin:]
                # add the new mark
                response = serverFunc.add_mark(uname, bookname, markname, pageNo, description)

            # delete a specific mark
            # url: /marks?username=...&bookname=...&markname=...
            elif obj == 'marks' and action == 'delete':
                # get username
                begin = url.find('?username=')
                begin = begin + 10
                end = url.find('&bookname=')
                uname = url[begin:end]
                # get bookname
                begin = end + 10
                end = url.find('&markname=')
                bookname = url[begin:end]
                # get markname
                begin = end + 10
                markname = url[begin:]
                # delete the mark
                response = serverFunc.delete_mark(uname, bookname, markname)
 
             # send response to client
            
            print("repsonse is", response)
            data = json.dumps(response)
            cur_thread = threading.current_thread()
            self.request.sendall(data.encode('utf-8'))
        
if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 8848
    ADDR = (HOST,PORT)
    server = ThreadingTCPServer(ADDR, Handler)  #参数为监听地址和已建立连接的处理类
    print('Begin listening')
    server.serve_forever()  #监听，建立好TCP连接后，为该连接创建新的socket和线程，并由处理类中的handle方法处理
    print(server)

'''
# 定义线程类，继承threading.Thread
class ThreadManager(Thread):
    # 初始化参数
    def __init__(self, work_queue):
        Thread.__init__(self)
        self.work_queue = work_queue
        self.daemon = True

    # 启动线程
    def run(self):
        while True:
            target, args = self.work_queue.get()
            target(*args)
            self.work_queue.task_done()

# 线程管理池
class ThreadPoolManager():
    # 初始化参数
    def __init__(self, thread_num):
        self.work_queue = Queue()
        self.thread_num = thread_num
        self.__init_threading_pool(self.thread_num)

    # 初始化线程池，创建指定数量的线程池
    def __init_threading_pool(self, thread_num):
        for i in range(thread_num):
            thread = ThreadManager(self.work_queue)
            thread.start()
        
    # 将任务放入队列，等待线程池阻塞读取，参数是被执行的函数和函数的参数
    def add_job(self, func, *args):
        self.work_queue.put((func, args))

# Host和Port
Host = '127.0.0.1'
Port = 8848
# buffer size
BUFSIZE = 2048
# 创建TCP socket
mySock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySock.bind((Host, Port))
mySock.listen(8)

# 创建一个有4个线程的线程池
thread_pool = ThreadPoolManager(9)

print("服务器启动")

# 循环等待接收客户端请求
while True:
    # 阻塞等待请求
    (conn_socket, addr) = mySock.accept()
    # 一旦有请求了，把socket扔到我们指定处理函数handle_request处理，等待线程池分配线程处理
    thread_pool.add_job(handle_request, *(conn_socket, )) 

# 关闭socket
mySock.close()


        # receive data
        recv_data = conn_socket.recv(BUFSIZE)
        request = json.loads(recv_data.decode('utf-8'))
        url = request['url']
        action = request['action']
        body = request['body']
        # find char '?' and get the object
        end = url.find('?')
        obj = url[1:end]

        # login request
        # url: /users?username=...&password=...
        if obj == 'users' and action == 'read':
            # get uname
            begin = url.find('?username=')
            begin = begin + 10
            end = url.find('&password=')
            uname = url[begin:end]
            # get pwd
            begin = end + 10
            pwd = url[begin:]
            # try logining
            response = serverFunc.login(uname, pwd)
    
        # register request
        # url: /users?username=...&password=...
        elif obj == 'users' and action == 'add':
            # get uname
            begin = url.find('?username=')
            begin = begin + 10
            end = url.find('&password=')
            uname = url[begin:end]
            # get pwd
            begin = end + 10
            pwd = url[begin:]
            # try registering
            response = serverFunc.register(uname, pwd)
    
        # get book list request
        # url: /books?bookname=%&pageNo=0
        # Or read book content request
        # url: /books?bookname=...&pageNo=...
        elif obj == 'books' and action == 'read':
            # get bookname
            begin = url.find('?bookname=')
            begin = begin + 10
            end = url.find('&pageNo=')
            bookname = url[begin:end]
            # get pageNo
            begin = end + 8
            pageNo = int(url[begin:])
        
            # if aim to get booklist
            if bookname == '?':
                response = serverFunc.read_book_list()
            # if aim to read book
            else:
                response = serverFunc.read_book(bookname, pageNo)

        # search all marks about a book 
        # url: /marks?username=...&bookname=...&markname=%
        # or read a specific mark
        # url: /marks?username=...&bookname=...&markname=...
        elif obj == 'marks' and action == 'read':
            # get username
            begin = url.find('?username=')
            begin = begin + 10
            end = url.find('&bookname=')
            uname = url[begin:end]
            # get bookname
            begin = end + 10
            end = url.find('&markname=')
            bookname = url[begin:end]
            # get markname
            begin = end + 10
            markname = url[begin:]

            # if aim to search all marks
            if markname == '%':
                response = serverFunc.read_mark_list(uname, bookname)
            # if aim to read a specific mark
            else:
                response = serverFunc.read_mark(uname, bookname, markname)
    
        # update a mark by modifying its description
        # url: /marks?username=...&bookname=...&markname=...
        # body is &description=...
        elif obj == 'marks' and action == 'update':
            # get username
            begin = url.find('?username=')
            begin = begin + 10
            end = url.find('&bookname=')
            uname = url[begin:end]
            # get bookname
            begin = end + 10
            end = url.find('&markname=')
            bookname = url[begin:end]
            # get markname
            begin = end + 10
            markname = url[begin:]
            # get description
            begin = body.find('&description=')
            begin = begin + 13
            description = body[begin:]
            # update mark
            response = serverFunc.update_mark(uname, bookname, markname, description)

        # add a bookmark
        # url: /marks?username=...&bookname=...&markname=...
        # body is &pageNo=...&description=...
        elif obj == 'marks' and action == 'add':
            # get username
            begin = url.find('?username=')
            begin = begin + 10
            end = url.find('&bookname=')
            uname = url[begin:end]
            # get bookname
            begin = end + 10
            end = url.find('&markname=')
            bookname = url[begin:end]
            # get markname
            begin = end + 10
            markname = url[begin:]
            # get pageNo
            begin = body.find('&pageNo=')
            begin = begin + 8
            end = body.find('&description=')
            pageNo = int(body[begin:end])
            # get description
            begin = end + 13
            description = body[begin:]
            # add the new mark
            response = serverFunc.add_mark(uname, bookname, markname, pageNo, description)

        # delete a specific mark
        # url: /marks?username=...&bookname=...&markname=...
        elif obj == 'marks' and action == 'delete':
            # get username
            begin = url.find('?username=')
            begin = begin + 10
            end = url.find('&bookname=')
            uname = url[begin:end]
            # get bookname
            begin = end + 10
            end = url.find('&markname=')
            bookname = url[begin:end]
            # get markname
            begin = end + 10
            markname = url[begin:]
            # delete the mark
            response = serverFunc.delete_mark(uname, bookname, markname)

        # send response to client
        data = json.dumps(response)
        conn_socket.sendall(data.encode('utf-8'))
'''