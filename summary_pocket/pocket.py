import os
from enum import Enum
from typing import List

import dotenv
import requests
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


def get_archive_articles() -> List[PocketArticle]:
    """アーカイブ済みの記事をすべて取得する

    - 追加日が古い順に取得する

    Returns:
        List[PocketArticle]: アーカイブ済みの記事のリスト
    """
    r = requests.get(
        'https://getpocket.com/v3/get',
        params={
            'consumer_key': CONSUMER_KEY,
            'access_token': ACCESS_TOKEN,
            'state': 'archive',
            'sort': 'oldest',
        },
    )
    r.raise_for_status()
    j = r.json()

    return [
        PocketArticle(
            id=item['item_id'],
            title=item['given_title'],
            url=item['given_url'],
            state=ArticleState.ARCHIVED,
        )
        for item in j['list'].values()
    ]


def get_unread_articles() -> List[PocketArticle]:
    """未読の記事をすべて取得する

    - 追加日が古い順に取得する

    Returns:
        List[PocketArticle]: 未読の記事のリスト
    """
    r = requests.get(
        'https://getpocket.com/v3/get',
        params={
            'consumer_key': CONSUMER_KEY,
            'access_token': ACCESS_TOKEN,
            'state': 'unread',
            'sort': 'oldest',
        },
    )
    r.raise_for_status()
    j = r.json()

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
    r = requests.post(
        'https://getpocket.com/v3/send',
        json={
            'consumer_key': CONSUMER_KEY,
            'access_token': ACCESS_TOKEN,
            'actions': [
                {
                    'action': 'archive',
                    'item_id': item_id,
                }
            ],
        },
    )
    r.raise_for_status()
