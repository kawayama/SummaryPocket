import json
import logging
import time
from typing import Callable

import requests

from summary_pocket.utils import logger_util

logger = logging.getLogger(__name__)
logger_util.setting_logger(logger)

RETRY_COUNT = 10
SLEEP_S = 180
TIMEOUT_S = 60


def get(
    url: str,
    params: dict | None = None,
    headers: dict | None = None,
    retry_cnt: int = RETRY_COUNT,
    retry_sleep_s: int = SLEEP_S,
) -> requests.Response | None:
    """GETリクエストを送信する

    Args:
        url (str): URL
        params (dict | None, optional): パラメータ
        headers (dict | None, optional): リクエストヘッダ
        retry_cnt (int, optional): リトライ回数
        retry_sleep_s (int, optional): リトライ時のスリープ時間

    Returns:
        requests.Response | None: レスポンス
    """
    if params is None:
        params = {}
    if headers is None:
        headers = {}

    return _action(
        url=url,
        method='get',
        retry_cnt=retry_cnt,
        retry_sleep_s=retry_sleep_s,
        func=lambda: requests.get(
            url=url,
            params=params,
            headers=headers,
            timeout=TIMEOUT_S,
        ),
    )


def post(
    url: str,
    params: dict | None = None,
    headers: dict | None = None,
    data: dict | None = None,
    retry_cnt: int = RETRY_COUNT,
    retry_sleep_s: int = SLEEP_S,
) -> requests.Response | None:
    """POSTリクエストを送信する

    Args:
        url (str): URL
        params (dict | None, optional): パラメータ
        headers (dict | None, optional): リクエストヘッダ
        data (dict | None, optional): リクエストボディ
        retry_cnt (int, optional): リトライ回数
        retry_sleep_s (int, optional): リトライ時のスリープ時間

    Returns:
        requests.Response | None: レスポンス
    """
    if params is None:
        params = {}
    if headers is None:
        headers = {}
    if data is None:
        data = {}

    return _action(
        url=url,
        method='post',
        retry_cnt=retry_cnt,
        retry_sleep_s=retry_sleep_s,
        func=lambda: requests.post(
            url=url,
            params=params,
            headers=headers,
            data=json.dumps(data),
            timeout=TIMEOUT_S,
        ),
    )


def _action(
    url: str,
    method: str,
    retry_cnt: int,
    retry_sleep_s: int,
    func: Callable,
):
    r = None
    status_code = -1
    retry_cnt += 1

    for _ in range(retry_cnt):
        try:
            r = func()
            status_code = r.status_code
            r.raise_for_status()
            return r
        except (
            requests.exceptions.HTTPError,
            requests.exceptions.Timeout,
            requests.exceptions.SSLError,
            requests.exceptions.ConnectionError,
        ) as e:
            logger.error('Error occurred: %s (method: %s, url: %s, status_code %s)', e, method, url, status_code)
        finally:
            logger.debug('Retry: sleeping %s seconds...', retry_sleep_s)
            time.sleep(retry_sleep_s)
    else:
        logger.error('Failed to get (method: %s, url: %s, status_code: %s)', method, url, status_code)
        return r
