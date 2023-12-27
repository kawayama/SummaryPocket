import os
from enum import Enum
from typing import List

import dotenv
import pocket as pocket_api
from pydantic import BaseModel, Field

dotenv.load_dotenv()

CONSUMER_KEY = os.environ['POCKET_CONSUMER_KEY']
ACCESS_TOKEN = os.environ['POCKET_ACCESS_TOKEN']


class ArticleState(Enum):
    """Pocketの記事の状態

    Attributes:
        UNREAD (str): 未読
        ARCHIVED (str): アーカイブ済み
    """

    UNREAD = 'unread'
    ARCHIVED = 'archived'


class PocketArticle(BaseModel):
    """Pocketの記事

    Attributes:
        id (str): 記事のID
        title (str): 記事のタイトル
        url (str): 記事のURL
        state (ArticleState): 記事の状態
    """

    id: str = Field(min_length=1)
    title: str
    url: str = Field(min_length=1)
    state: ArticleState


def get_unread_articles() -> List[PocketArticle]:
    """未読の記事をすべて取得する

    - 追加日が古い順に取得する

    Returns:
        List[PocketArticle]: 未読の記事のリスト
    """
    client = _get_client()
    response: tuple[dict, dict] = client.get(state='unread', sort='oldest')  # type: ignore
    j = response[0]

    if type(j['list']) is list:
        return []

    return [
        PocketArticle(
            id=item['item_id'],
            title=item['given_title'],
            url=item['given_url'],
            state=ArticleState.UNREAD,
        )
        for item in j['list'].values()
    ]


def archive_article(item_id: str):
    """記事をアーカイブする

    Args:
        item_id (str): 記事のID
    """
    client = _get_client()
    client.archive(item_id, wait=False)


def _get_client() -> pocket_api.Pocket:
    return pocket_api.Pocket(
        consumer_key=CONSUMER_KEY,
        access_token=ACCESS_TOKEN,
    )
