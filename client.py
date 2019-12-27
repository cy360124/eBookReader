# -*-coding: UTF-8 -*-
import sys
import clientFunc
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Book_Win(QMainWindow):
    def __init__(self, uname, bookname, parent = None):
        # 继承QMainWindow类
        super(Book_Win, self).__init__(parent)
        # init the uname, bookname and pageNo
        self.uname = uname
        self.bookname = bookname
        self.pageNo = 1
        # init mark_list
        self.init_mark_list()
        # init the ui
        self.init_ui()
    
    def init_mark_list(self):
        #self.mark_list = ['name1', 'name2', 'name3', 'name4', 'name5', 'name6', 'name7']
        self.mark_list = []
        (state, body) = clientFunc.read_mark_list(self.uname, self.bookname)
        if state == '401':
            # body is  [(), ...]
            for i in range(len(body)):
                temp = body[i]
                # 可能存在：[()]
                if len(temp) == 0:
                    break
                self.mark_list.append(temp[0])

    def init_ui(self):
        # 设置应用图标
        self.setWindowIcon(QIcon('images/book.png'))
        # set the title
        self.setWindowTitle(self.bookname)
        # 仅支持最小化以及关闭按钮
        self.setWindowFlags(Qt.WindowMinimizeButtonHint|Qt.WindowCloseButtonHint)
        # 获取屏幕对象
        screen = QDesktopWidget().screenGeometry()
        self.width = screen.width() * 4 / 5
        self.height = screen.height() * 4 / 5
        # 固定界面大小，不可修改
        self.setFixedSize(self.width, self.height)
        # 构造图书区域
        self.set_book_area()
        # 构造标签区域
        self.set_mark_area()

    def set_book_area(self):
        # set book widget
        book = QWidget(self)
        book.setGeometry(0, 0, self.width * 2 / 3, self.height)
        width = book.width()
        height = book.height()
        # set book name
        bname = QLabel(book)
        bname.setText(self.bookname)
        bname.setAlignment(Qt.AlignCenter)
        bname.setFont(QFont("Microsoft YaHei", 20, 75))
        bname.setGeometry(width / 4, 10, width / 2, 40)
        # set text
        self.text = QTextBrowser(book)
        self.text.setText("hello, world. Wish you good luck!")
        self.text.setGeometry(10, 50, width - 20, height - 90)
        # set page label
        self.page = QLabel(book)
        self.page.setText("页码：{}".format(str(self.pageNo)))
        self.page.setGeometry(10, height - 30, 50, 20)
        # set last_page button
        last_page = QPushButton(book)
        last_page.setText("上一页")
        last_page.setGeometry(110, height - 30, 50, 20)
        last_page.clicked.connect(self.read_last_page)
        # set next_page button
        next_page = QPushButton(book)
        next_page.setText("下一页")
        next_page.setGeometry(210, height - 30, 50, 20)
        next_page.clicked.connect(self.read_next_page)
        # set jump button
        jump = QPushButton(book)
        jump.setText("跳页")
        jump.setGeometry(310, height - 30, 50, 20)
        jump.clicked.connect(lambda: self.jump_page(get_page.text()))
        # set get_page lineEdit
        get_page = QLineEdit(book)
        get_page.setValidator(QIntValidator(book))
        get_page.setGeometry(380, height - 30, 50, 20)
        # read the first page
        self.read_book_page(self.pageNo)

    def set_mark_area(self):
        # set mark widget
        mark = QWidget(self)
        mark.setGeometry(self.width * 2 / 3, 0, self.width * 1 / 3, self.height)
        width = mark.width()
        height  = mark.height()
        # set the mark title
        title = QLabel(mark)
        title.setText("书签概览")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Microsoft YaHei", 20, 75))
        title.setGeometry(width / 3, 10, width / 3, 50)
        # set add button
        add = QPushButton(mark)
        add.setText("添加书签")
        add.setGeometry(width / 2 - 30, 80, 60, 20)
        add.clicked.connect(self.add_mark)
        # set mark table
        self.table = QTableWidget(mark)
        self.table.setGeometry(10, height * 1 / 5, width - 20, height * 4 / 5 - 40)
        # 设置行数
        self.t_rows = 20
        self.t_cols = 2
        self.table.setRowCount(self.t_rows)
        self.table.setColumnCount(self.t_cols)
        # 隐藏网格线
        self.table.setShowGrid(False)
        # 隐藏标题栏
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        # 设置单元格宽度和高度, 4 ： 3
        for i in range(self.t_cols):
            self.table.setColumnWidth(i, self.table.width() / self.t_cols)
        for i in range(self.t_rows):
            self.table.setRowHeight(i, self.table.width() / self.t_cols * 3 / 4)
        # 将单元格绑定右键菜单
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        # 点击单元格，调用 self.generateMenu 函数
        self.table.customContextMenuRequested.connect(self.generate_menu)
        # 设置单元格内容
        self.set_mark_tabel_cell(self.table.width() / self.t_cols, self.table.width() / self.t_cols * 3 / 4)
            
    def set_mark_tabel_cell(self, width, height):
        pixmap = QPixmap("images/icon.png")
        for i in range(len(self.mark_list)):
            cell = QWidget()
            # 构造图片
            pic = QLabel(cell)
            pic.setGeometry(0, 0, width, height * 2 / 3)
            pic.setPixmap(pixmap)
            pic.setAlignment(Qt.AlignCenter)
            # 设置书名
            name = QLabel(cell)
            name.setGeometry(0, height * 2 / 3, width, height / 3)
            name.setText(self.mark_list[i])
            # 居中显示
            name.setAlignment(Qt.AlignCenter)
            # 设置字体
            name.setFont(QFont("Microsoft YaHei", 10, 60))
            # 设置单元格元素为 label
            self.table.setCellWidget(i // self.t_cols, i % self.t_cols, cell)
            # 删除 cell 对象，防止后期无法即时刷新界面
            del cell

    def generate_menu(self, pos):
        row_num = col_num = -1
        # 获取选中的单元格的行数以及列数
        for i in self.table.selectionModel().selection().indexes():
            row_num = i.row()
            col_num = i.column()
        # 若选取的单元格中有元素，则支持右键菜单
        if row_num * self.t_cols + col_num < len(self.mark_list):
            menu = QMenu()
            item1 = menu.addAction('查看')
            item2 = menu.addAction('跳转')
            item3 = menu.addAction('修改')
            item4 = menu.addAction('删除')
            # 获取选项
            action = menu.exec_(self.table.mapToGlobal(pos))
            # 查看
            if action == item1:
                index = row_num * self.t_cols + col_num
                markname = self.mark_list[index]
                self.read_mark(markname)
            # 跳转
            elif action == item2:
                index = row_num * self.t_cols + col_num
                markname = self.mark_list[index]
                self.jump_mark(markname)
            # 修改
            elif action == item3:
                index = row_num * self.t_cols + col_num
                markname = self.mark_list[index]
                self.update_mark(markname)
            # 删除
            elif action == item4:
                index = row_num * self.t_cols + col_num
                markname = self.mark_list[index]
                self.delete_mark(markname)

    def read_book_page(self, pageNo):
        '''
        self.text.setText("welcome to page {}".format(str(pageNo)))
        self.pageNo = pageNo
        self.page.setText("页数：{}".format(str(self.pageNo)))

        '''
        # check page > 0
        if pageNo <= 0:
            return
        # read a page
        (state, content) = clientFunc.read_book(self.bookname, pageNo)
        # is ok
        if state == '302':
            self.text.setText(content)
            self.text.setFont(QFont("Microsoft YaHei", 10, 60))
            self.pageNo = pageNo
            self.page.setText("页码：{}".format(str(self.pageNo)))
        # wrong bookname
        elif state == '303':
            QMessageBox.information(self, "warning", "书名错误", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        # out of page
        elif state == '304':
            QMessageBox.information(self, "inform", "页码超出范围", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        
    def read_last_page(self):
        self.read_book_page(self.pageNo - 1)
    
    def read_next_page(self):
        self.read_book_page(self.pageNo + 1)

    def jump_page(self, page):
        # check page is not null
        if page == '':
            return
        else:
            pageNo = int(page)
        # try reading
        self.read_book_page(pageNo)

    def read_mark(self, markname):
        #mark = ("markname", 32, "here is the description of mark")
        
        # 获取mark的信息
        # body is (markname, pageNo, description)
        (state, mark) = clientFunc.read_mark(self.uname, self.bookname, markname)
        if state == '402':
            # set mark win dialog
            win = QDialog(self)
            win.setFixedSize(400, 300)
            win.setWindowTitle("查看标签")
            # 只有关闭对话框，才能关闭主窗口
            win.setWindowModality(Qt.ApplicationModal)
            # set bookname label
            bname = QLabel(win)
            bname.setText("书籍名：{}".format(self.bookname))
            bname.setGeometry(10, 10, 200, 20)
            # set page label
            page = QLabel(win)
            page.setText("页数：{}".format(str(mark[1])))
            page.setGeometry(10, 40, 100, 20)
            # set markname label
            mname = QLabel(win)
            mname.setText("书签名：{}".format(mark[0]))
            mname.setGeometry(10, 70, 200, 20)
            # set description label
            dpt = QLabel(win)
            dpt.setText("书签内容：")
            dpt.setGeometry(10, 110, 100, 20)
            # set text
            text = QTextBrowser(win)
            text.setText(mark[2])
            text.setGeometry(10, 140, 380, 150)
            # show
            win.show()
        elif state == '407':
            QMessageBox.information(win, "warning", "该书签不存在", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
    
    def jump_mark(self, markname):
        #mark = ("markname", 32, "here is the description of mark")
    
        # 获取mark的信息
        # body is (markname, pageNo, description)
        (state, mark) = clientFunc.read_mark(self.uname, self.bookname, markname)
     
        if state == '402':
            # read page
            pageNo = mark[1]
            self.read_book_page(pageNo)
        elif state == '407':
            QMessageBox.information(win, "warning", "该书签不存在", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
    
    def add_mark(self):
        # set the win dialog
        win = QDialog(self)
        win.setFixedSize(400, 300)
        win.setWindowTitle("添加书签")
        # 只有关闭对话框，才能关闭主窗口
        win.setWindowModality(Qt.ApplicationModal)
        # set bookname label
        bname = QLabel(win)
        bname.setText("书籍名：{}".format(self.bookname))
        bname.setGeometry(10, 10, 200, 20)
        # set page label
        page = QLabel(win)
        page.setText("页数：{}".format(str(self.pageNo)))
        page.setGeometry(10, 50, 100, 20)
        # set mark name label
        mname = QLabel(win)
        mname.setText("书签名")
        mname.setGeometry(10, 90, 60, 20)
        # set markname QLine
        mline = QLineEdit(win)
        mline.setPlaceholderText("请输入书签名")
        mline.setGeometry(90, 90, 150, 20)
        #reg = QRegExp("[a-zA-Z]+")
        #Validator = QRegExpValidator(win)
        #Validator.setRegExp(reg)
        #mline.setValidator(Validator)
        # set description label
        dpt = QLabel(win)
        dpt.setText("书签内容：")
        dpt.setGeometry(10, 130, 100, 20)
        # set text
        text = QTextEdit(win)
        text.setGeometry(10, 160, 380, 100)
        # set commit button
        commit = QPushButton(win)
        commit.setText("提交")
        commit.setGeometry(100, 270, 40, 20)
        commit.clicked.connect(lambda: do_commit(self.uname, self.bookname, mline.text(), self.pageNo, text.toPlainText()))
        # set cancel button
        cancel = QPushButton(win)
        cancel.setText("取消")
        cancel.setGeometry(260, 270, 40, 20)
        cancel.clicked.connect(win.destroy)
        # show
        win.show()
        # commit function
        def do_commit(uname, bookname, markname, pageNo, description):
            # try adding to server
            (state, body) = clientFunc.add_mark(uname, bookname, markname, pageNo, description)
            # success
            if state == '404':
                # add to mark_list
                self.mark_list.append(markname)
                # update the mark table
                for i in range(self.t_rows):
                    for j in range(self.t_cols):
                        self.table.removeCellWidget(i, j)
                self.set_mark_tabel_cell(self.table.width() / self.t_cols, self.table.width() / self.t_cols * 3 / 4)
                # 提醒
                QMessageBox.information(win, "inform", "书签添加成功", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            # repeated
            elif state == '406':
                QMessageBox.information(win, "warning", "书签名重复", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
    
    def update_mark(self, markname):
        # set the win
        win = QDialog(self)
        win.setFixedSize(300, 250)
        win.setWindowTitle("修改书签内容")
        # 只有关闭对话框，才能关闭主窗口
        win.setWindowModality(Qt.ApplicationModal)
        # set markname label
        mname = QLabel(win)
        mname.setText("书签名：{}".format(markname))
        mname.setGeometry(10, 10, 200, 20)
        # set the label
        label = QLabel(win)
        label.setText("请输入书签内容")
        label.setGeometry(10, 40, 100, 20)
        # set the text
        ptext = QTextEdit(win)
        ptext.setGeometry(10, 70, 280, 120)
        # set commit button
        commit = QPushButton(win)
        commit.setText("提交")
        commit.setGeometry(70, 220, 30, 20)
        commit.clicked.connect(lambda: do_commit(ptext.toPlainText()))
        # set the cancel button
        cancel = QPushButton(win)
        cancel.setText("取消")
        cancel.setGeometry(200, 220, 30, 20)
        cancel.clicked.connect(win.destroy)
        # show
        win.show()
        # commit function
        def do_commit(text):
            (state, body) = clientFunc.update_mark(self.uname, self.bookname, markname, text)
            if state == '403':
                QMessageBox.information(win, "inform", "书签修改成功", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            elif state == '407':
                QMessageBox.information(win, "warning", "该书签不存在", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        
    def delete_mark(self, markname):
        # delete from server
        (state, body) = clientFunc.delete_mark(self.uname, self.bookname, markname)
        if state == '405':
            # delte from mark_list
            self.mark_list.remove(markname)
            # delete all labels in mark table
            for i in range(self.t_rows):
                for j in range(self.t_cols):
                    self.table.removeCellWidget(i, j)
            # reshow the mark table
            self.set_mark_tabel_cell(self.table.width() / self.t_cols, self.table.width() / self.t_cols * 3 / 4)
            # 成功提示
            QMessageBox.information(self, "inform", "书签删除成功", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        elif state == '407':
            QMessageBox.information(self, "warning", "该书签不存在", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

class Client_UI(QMainWindow):
    def __init__(self, parent = None):
        # 继承QMainWindow类
        super(Client_UI, self).__init__(parent)
        # init the login ui
        self.init_login_ui()
        # init the book list
        self.init_book_list()
        # init the main ui
        self.init_main_ui()
        # show login ui
        self.win.show()
    
    def __del__(self): 
        clientFunc.close()

    def init_book_list(self):
        #self.book_list = ["三体", "野草", "朝花夕拾", "时间简史", "围城", \
        #                  "诗经", "远方的呼唤", "三国演义", "红楼梦", "水浒传", "西游记"]
        self.book_list = [None]
        (state, book_list) = clientFunc.read_book_list()
        if state == '301':
            self.book_list = book_list
        
    def init_login_ui(self):
        self.win = QMainWindow()
        # set the title
        self.win.setWindowTitle("eBookReader")
        # 设置应用图标
        self.win.setWindowIcon(QIcon('images/book.png'))
        # set the size
        self.win.setFixedSize(300, 150)
        # set the ulabel & plabel
        ulabel = QLabel(self.win)
        ulabel.setText("用户名")
        ulabel.setGeometry(50, 20, 40, 20)
        plabel = QLabel(self.win)
        plabel.setText("密码")
        plabel.setGeometry(50, 60, 40, 20)
        # set the uname & pwd line
        uline = QLineEdit(self.win)
        uline.setPlaceholderText("限16位，仅含英文字母")
        uline.setGeometry(110, 20, 140, 20)
        pline = QLineEdit(self.win)
        pline.setGeometry(110, 60, 140, 20)
        pline.setPlaceholderText("限32位，仅含英文字母及数字")
        # 设置uname & pwd 验证器
        ureg = QRegExp("[a-zA-Z]+")
        preg = QRegExp("[a-zA-Z0-9]+")
        uValidator = QRegExpValidator(self.win)
        pValidator = QRegExpValidator(self.win)
        uValidator.setRegExp(ureg)
        pValidator.setRegExp(preg)
        uline.setValidator(uValidator)
        pline.setValidator(pValidator)
        # 设置login & register 按钮
        btn1 = QPushButton(self.win)
        btn1.setText("登录")
        btn1.setGeometry(70, 120, 30, 20)
        btn1.clicked.connect(lambda: self.login(uline.text(), pline.text()))
        btn2 = QPushButton(self.win)
        btn2.setText("注册")
        btn2.setGeometry(200, 120, 30, 20)
        btn2.clicked.connect(lambda: self.register(uline.text(), pline.text()))
        
    def init_main_ui(self):
        # 设置应用图标
        self.setWindowIcon(QIcon('images/book.png'))
        # set the title
        self.setWindowTitle("eBookReader-在线书库")
        # 仅支持最小化以及关闭按钮
        self.setWindowFlags(Qt.WindowMinimizeButtonHint|Qt.WindowCloseButtonHint)
        # 获取屏幕对象
        screen = QDesktopWidget().screenGeometry()
        self.width = screen.width() * 5 / 6
        self.height = screen.height() * 5 / 6
        # 固定界面大小，不可修改
        self.setFixedSize(self.width, self.height)
        # set the table style
        self.set_book_table()

    def set_book_table(self):
        self.table = QTableWidget(self)
        # 将 self.table 设置为中心 widget
        self.setCentralWidget(self.table)
        # 隐藏标题栏
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        # 不显示网格线
        self.table.setShowGrid(False)
        # 设置表格 20 行 6 列
        self.t_cols = 6
        self.t_rows = 20
        self.table.setColumnCount(self.t_cols)
        self.table.setRowCount(len(self.book_list) // self.t_cols + 1)
        # 设置单元格的宽度
        for i in range(self.t_cols):
            self.table.setColumnWidth(i, self.width / self.t_cols)
        # 设置单元格的高度, 设置横纵比为 4 : 3
        for i in range(len(self.book_list)):
            self.table.setRowHeight(i, self.width / self.t_cols * 3 / 4)
        # 将单元格绑定右键菜单
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        # 点击单元格，调用 self.generateMenu 函数
        self.table.customContextMenuRequested.connect(self.generate_menu)
        # set the table cell
        self.set_table_cell(self.width / self.t_cols, self.width / self.t_cols * 3 / 4)

    def generate_menu(self, pos):
        row_num = col_num = -1
        # 获取选中的单元格的行数以及列数
        for i in self.table.selectionModel().selection().indexes():
            row_num = i.row()
            col_num = i.column()
        # 若选取的单元格中有元素，则支持右键菜单
        if row_num * self.t_cols + col_num < len(self.book_list):
            menu = QMenu()
            item = menu.addAction('开始阅读')
            # 获取选项
            action = menu.exec_(self.table.mapToGlobal(pos))
            if action == item:
                index = row_num * self.t_cols + col_num
                bookname = self.book_list[index]
                self.open_book(bookname)

    def set_table_cell(self, width, height):
        pixmap = QPixmap("images/icon.png")
        for i in range(len(self.book_list)):
            cell = QWidget()
            # 构造图片
            pic = QLabel(cell)
            pic.setGeometry(0, 0, width, height * 2 / 3)
            pic.setPixmap(pixmap)
            pic.setAlignment(Qt.AlignCenter)
            # 设置书名
            name = QLabel(cell)
            name.setGeometry(0, height * 2 / 3, width, height / 3)
            name.setText(self.book_list[i])
            # 居中显示
            name.setAlignment(Qt.AlignCenter)
            # 设置字体
            name.setFont(QFont("Microsoft YaHei", 10, 60))
            # 设置单元格元素为 label
            self.table.setCellWidget(i // self.t_cols, i % self.t_cols, cell)
            # 删除 cell 对象，防止后期无法即时刷新界面
            del cell

    def login(self, uname, pwd):
        (state, body) = clientFunc.login(uname, pwd)
        if state == '201':
            self.uname = uname
            self.win.close()
            self.show()
        elif state == '202':
            QMessageBox.information(self.win, "warning", "用户名或密码错误", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

    def register(self, uname, pwd):
        (state, body) = clientFunc.register(uname, pwd)
        if state == '203':
            QMessageBox.information(self.win, "inform", "用户注册成功", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        elif state == '204':
            QMessageBox.information(self.win, "warning", "用户名已存在", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

    def open_book(self, bookname):
        book = Book_Win(self.uname, bookname)
        book.show()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = Client_UI()
    sys.exit(app.exec_())

'''
    # 设置窗口背景照片
    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap("images/login_bg.jpg")
        # 平铺到整个窗口，随着窗口的改变而改变
        painter.drawPixmap(self.rect(), pixmap)
'''

