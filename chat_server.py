# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from socket import *
from login import *
import time


def do_chat(s, user, name, data):
    msg = "# {} : {}".format(name, data)
    for i in user:
        s.sendto(msg.encode(), (user[i][0], user[i][1] + 1))


def do_quit(s, user, name):
    msg = "# {}离开了直播间".format(name)
    for i in user:
        s.sendto(msg.encode(), (user[i][0], user[i][1] + 1))
    del user[name]  # 删除离开的用户


def do_yue(s, uname, addr):
    yue = select_yue(uname)
    msg = '* ' + str(yue)
    s.sendto(msg.encode(), addr)
    return


def do_chongzhi(s, uname, money, addr):
    chongzhi(uname, money)
    yue = select_yue(uname)
    msg = '*' + str(yue)
    s.sendto(msg.encode(), addr)
    return


def do_gift(s, uname, gift, addr, nicheng, user):
    a = xiaofei(uname, gift)
    if a == 13:
        s.sendto('余额不足'.encode(), addr)
    if a == 0:
        yue = select_yue(uname)
        msg = '*' + str(yue)
        s.sendto(msg.encode(), addr)
        msg2 = "G" + ' ' + nicheng + ' ' + '为主播送出' + ' ' + gift
        for i in user:
            s.sendto(msg2.encode(), (user[i][0], user[i][1] + 1))


def jiance(s, user):
    for i in user:
        s.sendto('*Hello'.encode(), user[i])
        msg, addr = s.recvfrom(100)
        msgList = msg.decode().split(' ')
        if msgList[0] == '*Hi':
            pass
        else:
            print('%s存在异常' % msgList[1])
            do_quit(s, user, msgList[1])


def do_parent1(s, user):
    # 用于存储用户 格式{'Alex':('127.0.0.1',8888)}
    while True:
        print('在线人数', len(user))
        try:
            msg, addr = s.recvfrom(1024)
        except:
            print('异常退出直播间')
            jiance(s, user)
        msgList = msg.decode().split(' ')
        if msgList[0] == 'C':
            data = ' '.join(msgList[2:])
            do_chat(s, user, msgList[1], data)
        elif msgList[0] == 'Q':
            do_quit(s, user, msgList[1])
        elif msgList[0] == 'A':
            msg = '# 欢迎%s进入直播间' % msgList[1]
            for i in user:
                s.sendto(msg.encode(), (user[i][0], user[i][1] + 1))
        elif msgList[0] == 'Y':
            do_yue(s, msgList[1], addr)
        elif msgList[0] == 'M':
            do_chongzhi(s, msgList[1], msgList[2], addr)
        elif msgList[0] == 'gift':
            do_gift(s, msgList[1], msgList[2], addr, msgList[3], user)


def chat_s(s, user):
    do_parent1(s, user)
