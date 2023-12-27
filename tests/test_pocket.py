from summary_pocket import pocket


def test_get_archive_articles():
    """アーカイブされた記事をすべて取得できるか

    Note:
        アカウントの状態に依存するためあまり良くない
    """
    articles = []
    for article in pocket.get_archive_articles():
        print(article)
        articles.append(article)

        assert article.id is not None and len(article.id) >= 1
        assert article.title is not None and len(article.title) >= 0
        assert article.url is not None and len(article.url) >= 1
        assert article.state == pocket.ArticleState.ARCHIVED

    assert len(articles) >= 0


def test_get_unread_articles():
    """未読の記事をすべて取得できるか

    Note:
        アカウントの状態に依存するためあまり良くない
    """
    articles = []
    for article in pocket.get_unread_articles():
        print(article)
        articles.append(article)

        assert article.id is not None and len(article.id) >= 1
        assert article.title is not None and len(article.title) >= 0
        assert article.url is not None and len(article.url) >= 1
        assert article.state == pocket.ArticleState.UNREAD

    assert len(articles) >= 0
