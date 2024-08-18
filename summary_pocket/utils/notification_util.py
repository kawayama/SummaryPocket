import json
import os

import requests

SLACK_API_URL = 'https://hooks.slack.com/services'
SLACK_API_KEY = os.environ['SLACK_API_KEY']
SLACK_CHANNEL_NAME = os.environ['SLACK_CHANNEL_NAME']


def notify_to_slack(content: str) -> bool:
    """Incoming Webhookを用いたSlackへの通知メソッド

    Args:
        content (str, dict): 通知する内容
        channel (str): 通知先のチャンネル

    Returns:
        bool: 通知が成功したかどうか

    Notes:
        Incoming Webhookの設定: https://mgxworld.slack.com/apps/A0F7XDUAZ--incoming-webhook-?tab=more_info
        APIに関する資料: https://api.slack.com/messaging/webhooks
    """
    url = SLACK_API_URL + SLACK_API_KEY
    data = {'text': content, 'channel': SLACK_CHANNEL_NAME}
    r = requests.post(url, data=json.dumps(data), timeout=60)
    is_succeeded = r.status_code == 200 if r is not None else False

    return is_succeeded
