# -*- coding: utf-8 -*-
import inspect
import time
import os

g_log_path = "logs/log.txt"
def init(log_path = "logs/log.txt"):
    try:
        dirname = os.path.dirname(log_path)
        os.makedirs(dirname)
        g_log_path = log_path
    except Exception as ex:
        pass
def __write__(msg):
    try:
        if os.path.exists(g_log_path) and os.path.getsize(g_log_path) > 4194304:
            os.remove(g_log_path)
        fp = open(g_log_path , "a+")
        fp.write(msg + "\n")
        fp.close()
    except Exception as ex:
        print ex
        pass
def debug(msg):
    caller =  inspect.stack()[1][3]
    timeStamp = time.strftime('%y-%m-%d %H:%M:%S',time.localtime(time.time()))
    msg = "%s - %s - [%-10s] - %s"%(timeStamp,"debug",caller,msg)
    print msg
    __write__(msg)
def info(msg):
    caller =  inspect.stack()[1][3]
    timeStamp = time.strftime('%y-%m-%d %H:%M:%S',time.localtime(time.time()))
    msg = "%s - %s - [%-10s] - %s"%(timeStamp,"info",caller,msg)
    print msg
    __write__(msg)
def error(msg):
    caller =  inspect.stack()[1][3]
    timeStamp = time.strftime('%y-%m-%d %H:%M:%S',time.localtime(time.time()))
    msg = "%s - %s - [%-10s] - %s"%(timeStamp,"error",caller,msg)
    print msg
    __write__(msg)
def warn(msg):
    caller =  inspect.stack()[1][3]
    timeStamp = time.strftime('%y-%m-%d %H:%M:%S',time.localtime(time.time()))
    msg = "%s - %s - [%-10s] - %s"%(timeStamp,"warn",caller,msg)
    print msg
    __write__(msg)
