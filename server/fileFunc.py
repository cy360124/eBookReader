# this file is used to achieve some basic functions about .txt files (books)
import os

PAGESIZE = 1024
bookpath = "books/"

# given bookname and pageNo, try to read the content of a book
# if bookname is wrong, return 0; if successful, return 1
# note the length of content may be 0, means at the end
def read_book(bookname, pageNo):
    filepath = bookpath + bookname
    try:
        fp = open(filepath, encoding='utf-8', mode='r')
    except:
        return (0, "wrong bookname")
    else:
        # read all words
        all_words = fp.read()
        # conduct content
        begin = (pageNo - 1) * PAGESIZE
        end = pageNo * PAGESIZE
        if begin >= len(all_words):
            content = ""
        elif end >= len(all_words):
            content = all_words[begin:]
        else:
            content = all_words[begin:end]
        # close fp
        fp.close()
        # return
        return (1, content)

# search the book list and return the result
# the result is conducted in the form of list
def read_book_list():
    book_list = os.listdir(bookpath)
    return book_list
