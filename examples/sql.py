from flask import Flask, request, Response
import threading
import logging
from sys import stdout
import json
import xml.etree.ElementTree as ET
# import execution
import sys
import time
import datetime
from numpy import true_divide
import pyautogui
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime
import pymysql

t = {
    "passphrase": "jaeminjjeong",
    "time": "2023-01-31T07:10:16Z",
    "exchange": "SGX_DLY",
    "ticker": "Z74",
    "bar": {
        "time": "2023-01-31T07:00:00Z",
        "open": 2.51,
        "high": 2.51,
        "low": 2.51,
        "close": 2.51,
        "volume": 400
    }
}

print(t["passphrase"])
t1 = datetime.strptime(t["time"], '%Y-%m-%dT%H:%M:%SZ')
# 2023-02-03T02:10:00Z
print(t1)
print(t["exchange"])
print(t["ticker"])
t2 = datetime.strptime(t["bar"]["time"], '%Y-%m-%dT%H:%M:%SZ')
print(t2)
print("OPEN : %s" % t["bar"]["open"])
print("HIGH : %s" % t["bar"]["high"])
print("LOW  : %s" % t["bar"]["low"])
print("CLOSE: %s" % t["bar"]["close"])
print("VOL  : %s" % t["bar"]["volume"])
#  col = date,time, exchange, ticker, OPEN, HIGH, LOW, CLOSE, VOL
conn = pymysql.connect(host='127.0.0.1', user='dscool', password='Datascience@u7', db='auto', charset='utf8')
c = conn.cursor()
t3 = t2.date()
t4 = t2.time()


sql = """INSERT INTO TOYOTA (date,time, exchange, ticker, OPEN, HIGH, LOW, CLOSE, VOL) VALUES (%s,%s, %s, %s,%s,%s,%s,%s,%s)"""
c.execute(sql, (t3, t4, t["exchange"],t["ticker"],t["bar"]["open"],t["bar"]["high"],t["bar"]["low"],t["bar"]["close"],t["bar"]["volume"]))
conn.commit()
conn.close()
