import datetime

import dotenv
from pydantic import BaseModel, Field

dotenv.load_dotenv()


class NotionItem(BaseModel):
    """Notionに保存する記事

    Attributes:
        is_read (bool): 読んだかどうか
        title (str): 記事のタイトル
        url (str): 記事のURL
        category (str): 記事のカテゴリ
        summary (str): 記事の要約
        importance (int): 記事の重要度 (1-3)
        fetched_at (datetime.datetime): 取得日時
    """

    is_read: bool = False
    title: str = Field(min_length=1)
    url: str = Field(min_length=1)
    category: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    importance: int = Field(ge=1, le=3)
    fetched_at: datetime.datetime


def get_categories() -> list[str]:
    """Notionの対象DBに保存されているカテゴリをすべて取得する

    Returns:
        list[str]: カテゴリのリスト
    """
    raise NotImplementedError


def add_category(category: str) -> None:
    """Notionの対象DBにカテゴリを追加する

    Args:
        category (str): 追加するカテゴリ
    """
    raise NotImplementedError


def save(item: NotionItem) -> None:
    """Notionに記事を保存する

    Args:
        item (NotionItem): 保存する記事
    """
    raise NotImplementedError
