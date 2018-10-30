# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from socket import *
from multiprocessing import Process
from threading import Thread
from denglu import do_parent
from video_server import video_s
from Audio_server import audio_s
from desk_server import desk_s
from chat_server import chat_s
import sys
import os


class zhubo_interface(QWidget):
    signal_user = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.starButton = QPushButton(self)
        self.starButton.setGeometry(10, 10, 100, 80)
        self.starButton.setToolTip("开始直播")
        self.starButton.setIcon(QIcon("img/进.png"))
        self.starButton.setText("开始直播")
        self.starButton.clicked.connect(self.start)

        self.endButton = QPushButton(self)
        self.endButton.setGeometry(10, 100, 100, 80)
        self.endButton.setToolTip("结束直播")
        self.endButton.setIcon(QIcon("img/进.png"))
        self.endButton.setText("结束直播")
        self.endButton.clicked.connect(self.quit)

        self.jin_Button = QPushButton(self)
        self.jin_Button.setGeometry(10, 190, 100, 80)
        self.jin_Button.setToolTip("禁言")
        self.jin_Button.setIcon(QIcon("img/进.png"))
        self.jin_Button.setText("禁言")
        self.jin_Button.clicked.connect(self.btn)

        self.list_user = QTextBrowser(self)
        self.list_user.setGeometry(290, 10, 200, 580)

        # 接收信息文本
        self.browser = QTextBrowser(self)
        self.browser.setGeometry(500, 10, 290, 510)
        # 发送文字的文本框
        self.send_edit = QTextEdit(self)
        self.send_edit.setGeometry(500, 530, 210, 60)

        # 发送消息按钮
        self.sendButton = QPushButton(self)
        self.sendButton.setText("喊话")
        self.sendButton.clicked.connect(self.send_msg)
        self.sendButton.setGeometry(720, 530, 70, 60)
        self.sendButton.setIcon(QIcon("img/进.png"))
        self.resize(800, 600)
        self.center()
        self.setWindowTitle("直播界面")
        self.signal_user.connect(self.yonghu)

        self.host = '0.0.0.0'
        self.ADDR1 = (self.host, 8888)  # 登录
        self.ADDR2 = (self.host, 7777)  # 视频
        self.ADDR3 = (self.host, 7779)  # 音频
        self.ADDR4 = (self.host, 7781)  # 桌面
        self.ADDR5 = (self.host, 7776)  # 聊天
        self.pa = socket(AF_INET, SOCK_DGRAM)  # 登录
        self.vi = socket(AF_INET, SOCK_STREAM)  # 视频
        self.au = socket(AF_INET, SOCK_STREAM)  # 音频
        self.de = socket(AF_INET, SOCK_STREAM)  # 桌面
        self.ch = socket(AF_INET, SOCK_DGRAM)  # 聊天
        self.pa.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.de.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.au.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.vi.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.ch.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.pa.bind(self.ADDR1)
        self.vi.bind(self.ADDR2)
        self.au.bind(self.ADDR3)
        self.de.bind(self.ADDR4)
        self.ch.bind(self.ADDR5)
        self.au.listen(10)
        self.de.listen(10)
        self.vi.listen(10)

        self.user = {}

    def start(self):
        print('开启')
        z = Thread(target=do_parent, args=(self.pa, self.user))
        x = Process(target=video_s, args=(self.vi,))
        y = Process(target=audio_s, args=(self.au,))
        t = Process(target=desk_s, args=(self.de,))
        p = Thread(target=chat_s, args=(self.ch, self.user))
        z.setDaemon(True)
        x.Daemon = True
        y.Daemon = True
        t.Daemon = True
        p.setDaemon(True)
        z.start()
        x.start()
        y.start()
        t.start()
        p.start()

    def send_msg(self):
        pass

    def yonghu(self, dicty):
        self.user = dicty
        print(self.user)

    def quit(self):
        tishi = QMessageBox.question(self, 'Message', "是否关闭直播并退出",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if tishi == QMessageBox.Yes:
            self.pa.close()
            self.vi.close()
            self.au.close()
            self.de.close()
            self.ch.close()
            os.popen("taskkill /im python.exe -f")
            sys.exit(0)

    def btn(self):
        QMessageBox.question(self, 'Message', "Are you sure to quit?",
                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = zhubo_interface()
    ex.setFixedSize(ex.width(), ex.height())
    ex.show()
    sys.exit(app.exec_())
