from summary_pocket import website


def test_get_site_info_1():
    """Webサイトの情報を取得できるか"""
    url = 'https://www.google.com/'
    site_info = website.get_site_info(url)
    print(site_info)

    assert site_info.title == 'Google'
    assert site_info.url == url
    assert len(site_info.content) >= 1


def test_get_site_info_2():
    """Twitterのような動的なWebサイトの情報を取得できるか"""
    url = 'https://twitter.com/elonmusk/status/1739729243943129482'
    site_info = website.get_site_info(url)
    print(site_info)

    assert len(site_info.title) > 0
    assert site_info.url == url
    assert len(site_info.content) >= 1
    assert 'Elon Musk\n@elonmusk\nAI is now better than human at this task' in site_info.content


def test_get_site_info_3():
    """Qiitaの情報を取得できるか"""
    url = 'https://qiita.com/Yamakawa0032/items/506509ffa9ecb7012378'
    site_info = website.get_site_info(url)
    print(site_info)

    assert len(site_info.title) > 1
    assert site_info.url == url
    assert len(site_info.content) >= 1
