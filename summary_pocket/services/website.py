import contextlib
import time
from typing import Generator

import undetected_chromedriver as uc
from pydantic import BaseModel, Field
from selenium.webdriver.common.by import By


class SiteInfo(BaseModel):
    """Webサイトの情報

    Attributes:
        title (str): タイトル
        url (str): リダイレクト後の最終的なURL
        content (str): 本文
    """

    title: str = Field(..., min_length=1)
    url: str
    content: str


def get_site_info(url: str) -> SiteInfo:
    """Webサイトからサイト情報を取得する

    Args:
        url (str): URL

    Raises:
        WebDriverException: Selenium関連のエラー

    Returns:
        SiteInfo: Webサイトの情報

    Note:
        - リダイレクト後のサイト情報を取得する
    """
    with get_driver() as driver:
        driver.get(url)
        body_ele = driver.find_element(By.CSS_SELECTOR, 'body')

        # TODO: ここの待機時間は要調整、できればwaitを使いたい
        time.sleep(10)

        title = driver.title
        if len(title) == 0:
            title = 'No title'

        return SiteInfo(
            title=title,
            url=driver.current_url,
            content=body_ele.text,
        )


@contextlib.contextmanager
def get_driver() -> Generator[uc.Chrome, None, None]:
    """undetected_chromedriverのChromeドライバーを取得する

    - ドライバーの取得から終了までを行う

    Yields:
        Generator[uc.Chrome, None, None]: undetected_chromedriverのChromeドライバー
    """
    driver = None
    try:
        options = uc.options.ChromeOptions()
        options.add_argument('--disable-dev-shm-usage')
        driver = uc.Chrome(headless=True, use_subprocess=False, options=options, version_main=126)
        yield driver
    finally:
        try:
            if driver is not None:
                driver.quit()
        except Exception:
            pass
