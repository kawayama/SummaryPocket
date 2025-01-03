import contextlib
import os
import subprocess
import time
from typing import Generator

import markdownify
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

        html_content = body_ele.get_attribute('innerHTML') or ''
        markdown_content = markdownify.markdownify(html_content)

        return SiteInfo(
            title=title,
            url=driver.current_url,
            content=markdown_content,
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
        chrome_version = _get_chrome_version()
        driver = uc.Chrome(headless=True, use_subprocess=False, options=options, version_main=chrome_version)
        yield driver
    finally:
        try:
            if driver is not None:
                driver.quit()
        except Exception:
            pass


def _get_chrome_version() -> int:
    """Chromeのバージョンを取得する

    Returns:
        int: Chromeのバージョン
    """
    try:
        if os.name == "nt":  # Windows
            # NOTE: Windows以外ではwinregライブラリがないため、ここで読み込んでいる
            import winreg

            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon")
            version, _ = winreg.QueryValueEx(key, "version")
        elif os.name == "posix":  # Linux と macOS
            if os.path.exists("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"):  # macOS
                command = r"/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version"
            else:  # Linux
                command = "google-chrome --version"
            output = subprocess.check_output(command, shell=True).decode("utf-8")
            version = output.strip().split()[-1]
        else:
            raise OSError("サポートされていないOSです")

        return int(version.split(".")[0])  # メジャーバージョンを整数として返す
    except Exception as e:
        print(f"Chromeバージョンの取得に失敗しました: {e}")
        return 127
