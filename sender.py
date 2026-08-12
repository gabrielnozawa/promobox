import os, json, urllib.request

def send_offer(message, image_url=''):
    url=os.getenv('PUBLISH_WEBHOOK_URL')
    if not url: return False, 'PUBLISH_WEBHOOK_URL não configurada.'
    payload=json.dumps({'text':message,'image_url':image_url}).encode()
    req=urllib.request.Request(url,data=payload,headers={'Content-Type':'application/json'},method='POST')
    try:
        with urllib.request.urlopen(req,timeout=20) as r:
            return 200 <= r.status < 300, f'HTTP {r.status}'
    except Exception as e:
        return False, str(e)
