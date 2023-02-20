from flask import Flask, request, Response
import threading
import logging
from sys import stdout
import json
import xml.etree.ElementTree as ET
import execution
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

## All times are in UST

app = Flask(__name__)
save_webhook_output_file = "webhook.log"

@app.route('/')
def hello_world():
    print('웹사이트 접속')
    return 'This is a webhook system for samsungauto. 2023-01-31'

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    '''자동화 작업 함수'''
   
    if request.method == 'GET':
        content = request.args.to_dict()

    elif request.method == 'POST':
        request_json = request.json
        content = json.dumps(request_json,indent=4)

        print('Webhook POST: ')
        print(content)

        # webhook.log에 저장
        with open(save_webhook_output_file, 'a') as filehandle:
            filehandle.write('%s\n' % content)
            filehandle.write('\n')
        

        # logger.info(content)
 
    '''스레드 실행'''
    # def auto(content):
        # print(content)

    # thread = threading.Thread(target=auto, kwargs={'content': content})
    # thread.start()
    return 'Webhook notification received', 202

@app.route('/order')
def order():
    f = open("order.xml", 'r')
    data = f.read()
    print(data)
    f.close()
    # tree = ET.parse('order.xml')
    # print('Return order XML:')
    # print(tree)
    return data

@app.route('/toyota', methods=['GET', 'POST'])
def toyota():

    if request.method == 'GET':
        content = request.args.to_dict()

    elif request.method == 'POST':
        request_json = request.json
        content = request.get_json()
        print('Toyota Webhook POST: ' + content["passphrase"])
    #    TSE Tokyo Stock Exchange Ticker 7203
        if content["passphrase"] == "7203":
            with open('toyota_7203.log', 'a') as filehandle:
                filehandle.write('%s\n' % json.dumps(request_json,indent=4))
                filehandle.write('\n')

            t = content
            print(t["passphrase"])
            t1 = datetime.strptime(t["time"], '%Y-%m-%dT%H:%M:%SZ')
            # 2023-02-03T02:10:00Z
            # print(t1)
            # print(t["exchange"])
            # print(t["ticker"])
            t2 = datetime.strptime(t["bar"]["time"], '%Y-%m-%dT%H:%M:%SZ')
            # print(t2)
            # print("OPEN : %s" % t["bar"]["open"])
            # print("HIGH : %s" % t["bar"]["high"])
            # print("LOW  : %s" % t["bar"]["low"])
            # print("CLOSE: %s" % t["bar"]["close"])
            # print("VOL  : %s" % t["bar"]["volume"])
            #  col = date,time, exchange, ticker, OPEN, HIGH, LOW, CLOSE, VOL
            conn = pymysql.connect(host='127.0.0.1', user='dscool', password='Datascience@u7', db='auto', charset='utf8')
            c = conn.cursor()
            t3 = t2.date()
            t4 = t2.time()            

            sql = """INSERT INTO TOYOTA (date,time, exchange, ticker, OPEN, HIGH, LOW, CLOSE, VOL) VALUES (%s,%s, %s, %s,%s,%s,%s,%s,%s)"""
            c.execute(sql, (t3, t4, t["exchange"],t["ticker"],t["bar"]["open"],t["bar"]["high"],t["bar"]["low"],t["bar"]["close"],t["bar"]["volume"]))
            conn.commit()

        elif content["passphrase"] == "SCT":
            with open('toyota_SCT.log', 'a') as filehandle:
                filehandle.write('%s\n' % json.dumps(request_json,indent=4))
                filehandle.write('\n')

            t = content
            longPrice = t["LongPrice"]
            longClosePrice = t["LongClosePrice"]
            t1 = datetime.strptime(t["time"], '%Y-%m-%dT%H:%M:%SZ')
            print("LongPrice : "+longPrice)
            print("LongClosePrice : "+longClosePrice)
            print("Time : "+t1)
            dt = t1.date()
            tt = t1.time()        
            print("Date : "+dt)
            print("Time : "+tt)
            # t1 = datetime.strptime(t["time"], '%Y-%m-%dT%H:%M:%SZ')
            # 2023-02-03T02:10:00Z
            
            # t2 = datetime.strptime(t["bar"]["time"], '%Y-%m-%dT%H:%M:%SZ')
            # print(t2)
            # print("OPEN : %s" % t["bar"]["open"])
            # print("HIGH : %s" % t["bar"]["high"])
            # print("LOW  : %s" % t["bar"]["low"])
            # print("CLOSE: %s" % t["bar"]["close"])
            # print("VOL  : %s" % t["bar"]["volume"])
            #  col = date,time, exchange, ticker, OPEN, HIGH, LOW, CLOSE, VOL
            # conn = pymysql.connect(host='127.0.0.1', user='dscool', password='Datascience@u7', db='auto', charset='utf8')
            # c = conn.cursor()
            # sql = """INSERT INTO TOYOTA (date,time, exchange, ticker, OPEN, HIGH, LOW, CLOSE, VOL) VALUES (%s,%s, %s, %s,%s,%s,%s,%s,%s)"""
            # c.execute(sql, (t3, t4, t["exchange"],t["ticker"],t["bar"]["open"],t["bar"]["high"],t["bar"]["low"],t["bar"]["close"],t["bar"]["volume"]))

        # logger.info(content)


    '''스레드 실행'''
    # def auto(content):
        # print(content)

    # thread = threading.Thread(target=auto, kwargs={'content': content})
    # thread.start()
    return 'Webhook notification received', 202

def read_orderbook():
    webpage = requests.get("https://a.dscool.kr/order")
    tree = ET.parse(webpage)
    print('Return order XML:')

    
    # val1=sys.argv[1] #아이디
    val2='7887' #비밀번호
    time_start="09:00:00"#시작시간
    time_end="15:25:00"#종료시간

    tm_wday=(time.localtime().tm_wday)#요일
    tm_hour=(time.localtime().tm_hour)#시간
    dt_now = datetime.datetime.now()



if __name__ == '__main__':
    conn = pymysql.connect(host='127.0.0.1', user='dscool', password='Datascience@u7', db='auto', charset='utf8')
    c = conn.cursor()
    app.run(host='0.0.0.0',port=80, debug=True)  
    conn.close()


# tradingview.com IP address
# Here is a list of IP addresses that we will use to send POST requests, in case they need to be permissioned:
# 52.89.214.238
# 34.212.75.30
# 54.218.53.128
# 52.32.178.7