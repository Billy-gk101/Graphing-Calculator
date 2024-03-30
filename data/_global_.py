#!/usr/bin/env python
# =============================================================================
# CODE IMPORTS
# =============================================================================
import os, sys, logging, inspect, math, typing
from datetime import timedelta, datetime, date

# -- PyQt UI Objects
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# -- path additions
PTH_DTA = os.path.dirname(os.path.realpath(__file__))
PTH_GUI = os.path.join(PTH_DTA, 'ui')
PTH_FNT = os.path.join(PTH_DTA, 'fonts')
PTH_IMG = os.path.join(PTH_DTA, 'image')
PTH_PKL = os.path.join(PTH_DTA, 'settings.pkl')
sys.path.insert(0, PTH_GUI)
sys.path.insert(0, PTH_FNT)
sys.path.insert(0, PTH_IMG)

# -- logging info
fmt = '%(asctime)-18s %(levelname)-8s %(message)s'
dtf = '%m-%d-%Y %H:%M'
logging.basicConfig(filename='errorLogger.txt',\
                    format='%(levelname)-8s:%(message)s',\
                    filemode='w', level=logging.DEBUG,\
                    datefmt=dtf)

def get_logging_level():
    val = logging.getLogger(__name__).getEffectiveLevel()
    return val

def loggAssistMsg(object, frameRec):
    ts = datetime.now().strftime("%H:%M:%S")
    frame = frameRec[0]
    info = inspect.getframeinfo(frame)
    return "({}) {} {}() <Line: {}>\n".format(ts, type(object), info.function, info.lineno)

# -- user notification windows
def debugMessageLog(object, frameRec, msg):
    txt = "{}{}\n".format(loggAssistMsg(object, frameRec), msg)
    logging.debug(txt)
    if get_logging_level() == logging.DEBUG:
        print(txt)
    return

def infoMessageLog(object, frameRec, msg):
    txt = "{}{}\n".format(loggAssistMsg(object, frameRec), msg)
    logging.info(txt)
    if get_logging_level() == logging.INFO:
        print(txt)
    return

def warnMessageLog(object, frameRec, msg):
    txt = "{}{}\n".format(loggAssistMsg(object, frameRec), msg)
    logging.warning(txt)
    if get_logging_level() == logging.WARNING:
        print(txt)
    return

def critMessageLog(object, frameRec, msg):
    txt = "{}{}\n".format(loggAssistMsg(object, frameRec), msg)
    logging.critical(txt)
    if get_logging_level() == logging.CRITICAL:
        print(txt)
    return

def notificationMessageWindow(object, frameRec, msg):
    txt = "{}{}".format(loggAssistMsg(object, frameRec), msg)
    logging.info("{}\n".format(txt))
    QMessageBox.information(None,"System Information Notification",txt)

def warningMessageWindow(object, frameRec, msg):
    txt = "{}{}".format(loggAssistMsg(object, frameRec), msg)
    logging.warning("{}\n".format(txt))
    QMessageBox.warning(None,"System Warning Notification",txt)

def errorMessageWindow(object, frameRec, msg):
    txt = "{}{}".format(loggAssistMsg(object, frameRec), msg)
    logging.critical("{}\n".format(txt))
    QMessageBox.critical(None,"System Error Notification",txt)