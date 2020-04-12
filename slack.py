import requests, json, options

def to_slack(text=None):
    if text is None: return
    url = options.SLACK_WEBHOOK_URL
    r = requests.post(url, data=json.dumps({'text': text}))