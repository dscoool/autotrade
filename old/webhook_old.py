# -*- coding: utf-8 -*-
from flask import Flask, request, Response
import threading
import logging
from sys import stdout

# logger instance 생성
app = Flask(__name__)
logger = logging.getLogger(__name__)
# handler 생성 (stream, file)
fileHandler = logging.FileHandler('./webhook.log')
formatter = logging.Formatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s')
streamHandler = logging.StreamHandler(stdout)
streamHandler.setFormatter(formatter)


# logger instance에 handler 설정
logger.addHandler(streamHandler)
logger.addHandler(fileHandler)
logger.addHandler(formatter)

@app.route('/')
def hello_world():
    print('This is a webhook system test')
    return

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    def auto(content):
        print(content)
    # if request.method == 'GET':
    #     content = request.args.to_dict()
    # elif request.method == 'POST':
    #     if request.is_json is True:  # Content-Type: json
    #         content = request.get_json()
    #         logger.info(content)
    #     else:  # Content-Type: x-www-form-urlencoded
    #         content = request.form.to_dict()
    #         logger.info(content)

    thread = threading.Thread(target=auto, kwargs={'content': content})
    thread.start()
    return

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80, debug=True)