from pydantic import BaseModel


class SiteInfo(BaseModel):
    """Webサイトの情報

    Attributes:
        title (str): タイトル
        url (str): リダイレクト後の最終的なURL
        content (str): 本文
    """

    title: str
    url: str
    content: str


def get_site_info(url: str) -> SiteInfo:
    """Webサイトからサイト情報を取得する

    Args:
        url (str): URL

    Returns:
        SiteInfo: Webサイトの情報
    """
    raise NotImplementedError
