import datetime
import os

import dotenv
import notion_client
from notion_client import helpers
from pydantic import BaseModel, Field

dotenv.load_dotenv()

NOTION_TOKEN = os.environ['NOTION_TOKEN']
NOTION_DB_ID = os.environ['NOTION_DB_ID']


class NotionItem(BaseModel):
    """Notionに保存する記事

    Attributes:
        is_read (bool): 読んだかどうか
        title (str): 記事のタイトル
        url (str): 記事のURL
        category (str): 記事のカテゴリ
        summary (str): 記事の要約
        fetched_at (datetime.datetime): 取得日時
    """

    is_read: bool = False
    title: str = Field(min_length=1)
    url: str = Field(min_length=1)
    category: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    fetched_at: datetime.datetime


def check_db():
    """DBの情報が正しいかチェックする

    Raises:
        AssertionError: DBの情報が正しくない場合
    """
    client = _get_client()
    db = client.databases.retrieve(NOTION_DB_ID)
    assert type(db) is dict
    properties = db['properties']
    assert set(properties.keys()) == {'is_read', 'title', 'url', 'category', 'summary', 'fetched_at'}
    assert properties['is_read']['type'] == 'checkbox'
    assert properties['title']['type'] == 'title'
    assert properties['url']['type'] == 'url'
    assert properties['category']['type'] == 'select'
    assert properties['summary']['type'] == 'rich_text'
    assert properties['fetched_at']['type'] == 'date'


def get_urls() -> set[str]:
    """Notionの対象DBに保存されている記事のURLをすべて取得する

    Returns:
        set[str]: 記事のURLのリスト
    """
    client = _get_client()
    items = helpers.collect_paginated_api(client.databases.query, database_id=NOTION_DB_ID)
    return {item['properties']['url']['url'] for item in items if item['properties']['url']['url'] is not None}


def get_categories() -> set[str]:
    """Notionの対象DBに保存されているカテゴリをすべて取得する

    Returns:
        set[str]: カテゴリのリスト
    """
    client = _get_client()
    db = client.databases.retrieve(NOTION_DB_ID)
    if type(db) is not dict:
        raise ValueError('DBの情報が正しくありません')
    return {item['name'] for item in db['properties']['category']['select']['options']}


def save(item: NotionItem) -> None:
    """Notionに記事を保存する

    Args:
        item (NotionItem): 保存する記事
    """
    client = _get_client()
    client.pages.create(
        parent={
            'database_id': NOTION_DB_ID,
        },
        properties={
            'is_read': {
                'checkbox': item.is_read,
            },
            'title': {
                'title': [
                    {
                        'text': {
                            'content': item.title,
                        },
                    },
                ],
            },
            'url': {
                'url': item.url,
            },
            'category': {
                'select': {
                    'name': item.category,
                },
            },
            'summary': {
                'rich_text': [
                    {
                        'text': {
                            'content': item.summary,
                        },
                    },
                ],
            },
            'fetched_at': {
                'date': {
                    'start': item.fetched_at.isoformat(),
                },
            },
        },
    )


def _get_client() -> notion_client.Client:
    """Notionのクライアントを取得する

    Returns:
        notion_client.Client: Notionのクライアント
    """
    return notion_client.Client(auth=NOTION_TOKEN)
