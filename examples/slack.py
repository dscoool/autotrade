
import requests

def send_message(title=None,content=None):
  
  # 생성한 웹훅 주소
    webhook_url = "https://hooks.slack.com/services/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"
   
    # 메시지 전송
    res = requests.post(
        webhook_url,  
        headers={
        'content-type': 'application/json'
        },
        json={
        'text': title,
        'blocks': [
            {
            'type': 'section',  # 저는 메시지가 묶이지 않도록 section을 주로 사용합니다.
            'text': {
                'type': 'mrkdwn',
                'text': content
            }
            }
        ]
        }
    )
    print(res)

send_message()