import pathlib

ERROR_URLS_PATH = pathlib.Path('./error_urls.txt')


def get_error_urls() -> set[str]:
    """エラーが発生したURLのリストを取得する

    Returns:
        set[str]: エラーが発生したURLのリスト
    """
    if not ERROR_URLS_PATH.exists():
        return set()

    with open(ERROR_URLS_PATH, 'r', encoding='utf-8') as f:
        return set(f.read().splitlines())


def add_error_url(url: str):
    """エラーが発生したURLを追加する

    Args:
        url (str): エラーが発生したURL
    """
    with open(ERROR_URLS_PATH, 'a', encoding='utf-8') as f:
        f.write(url + '\n')
