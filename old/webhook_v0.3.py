from flask import Flask, request, Response
import threading
import logging
from sys import stdout
import json
import xml.etree.ElementTree as ET
app = Flask(__name__)

# # logger instance 생성
# logger = logging.getLogger(__name__)
# # handler 생성 (stream, file)
# fileHandler = logging.FileHandler('./webhook_access.log')
# formatter = logging.Formatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s')
# streamHandler = logging.StreamHandler(stdout)
# streamHandler.setFormatter(formatter)


# # logger instance에 handler 설정
# logger.addHandler(streamHandler)
# logger.addHandler(fileHandler)
# logger.addHandler(formatter)

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
        content = request.get_json()

        print('Webhook POST: ')
        print(json.dumps(request_json,indent=4))

        with open(save_webhook_output_file, 'a') as filehandle:
            # Change from original - we output to file so that the we page works better with the newlines.
            filehandle.write('%s\n' % json.dumps(request_json,indent=4))
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

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80, debug=True)

# tradingview.com IP address
# Here is a list of IP addresses that we will use to send POST requests, in case they need to be permissioned:
# 52.89.214.238
# 34.212.75.30
# 54.218.53.128
# 52.32.178.7