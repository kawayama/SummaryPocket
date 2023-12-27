import datetime

from summary_pocket.services import notion


def test_check_db():
    """DBの情報が正しいかチェックできるか"""
    notion.check_db()


def test_get_categories():
    """DBに保存されているカテゴリをすべて取得できるか"""
    categories = notion.get_categories()
    assert len(categories) > 0
    assert all([type(category) is str for category in categories])


def test_save():
    """記事を保存できるか"""
    notion.save(
        notion.NotionItem(
            title='title',
            url='https://example.com',
            category='hoge',
            summary='・hoge\n・fuga\n・piyo',
            fetched_at=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9), 'JST')),
        )
    )
