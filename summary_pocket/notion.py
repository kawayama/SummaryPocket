import datetime

import dotenv
from pydantic import BaseModel

dotenv.load_dotenv()


class NotionItem(BaseModel):
    is_read: bool = False
    title: str
    url: str
    category: str
    summary: str
    importance: int
    fetched_at: datetime.datetime


def save(item: NotionItem) -> bool:
    """Notionに記事を保存する

    - タイトル
    - URL
    - 要約 (重要なポイント3つを箇条書き、日本語)
    - 重要度 (1-3)
    - 取得日時

    Args:
        item (NotionItem): 保存する記事

    Returns:
        bool: 保存に成功したかどうか
    """
    raise NotImplementedError
