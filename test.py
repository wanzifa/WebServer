#coding:utf-8
"""
辅助理解os模块的fork方法的一个小程序
"""

import os

def child():
    print 'A new child:', os.getpid()
    print 'Parent id is:', os.getppid()
    os._exit(0)

def parent():
    while True:
        #fork函数复制当前进程，产生子进程
        #从下面开始，就是两个进程在跑了.
        newpid=os.fork()
        print newpid
        #在父进程里，fork函数返回子进程的pid，在子进程里，返回0
        if newpid==0:
            child()
        else:
            pids=(os.getpid(),newpid)
            print "parent:%d,child:%d"%pids
            print "parent parent:",os.getppid()       
        if raw_input()=='q':
            break

parent()
