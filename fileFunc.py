# this file is used to achieve some basic functions about .txt files (books)
import os

PAGESIZE = 1024
PAGELINES = 20
#bookpath = r'E:\myLearning\eBookReader\books'
bookpath = "books/"

# given bookname and pageNo, try to read the content of a book
# if bookname is wrong, return 0; if successful, return 1
# note the length of content may be 0, means at the end
'''
def read_book(bookname, pageNo):
    # the relative path
    filepath = bookpath + bookname
    try:
        #fp = open(filepath, 'r', errors="ignore")
        fp = open(filepath, 'r')
    except:
        return (0, "wrong bookname")
    else:
        fp.seek(PAGESIZE * (pageNo - 1), 0)
        content = fp.read(PAGESIZE)
        fp.close()
        return (1, content)
'''
def read_book(bookname, pageNo):
    filepath = bookpath + bookname
    try:
        fp = open(filepath, encoding='utf-8', mode='r')
    except:
        return (0, "wrong bookname")
    else:
        # read all lines
        lines = fp.readlines()
        # conduct content
        content = ""
        for i in range(PAGELINES):
            # get index
            index = (pageNo - 1) * PAGELINES + i
            # check
            if index >= len(lines):
                break
            # 拼接行
            content += lines[index]
        # close fp
        fp.close()
        return (1, content)


# search the book list and return the result
# the result is conducted in the form of list
def read_book_list():
    book_list = os.listdir(bookpath)
    return book_list