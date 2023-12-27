from pydantic import BaseModel


class ChatGPTResponse(BaseModel):
    """ChatGPTの要約結果

    Attributes:
        category (str): カテゴリ
        summary (str): 要約
        importance (int): 重要度 (1-3)
    """

    category: str
    summary: str
    importance: int


def summarize(title: str, content: str, categories: list[str]) -> ChatGPTResponse:
    """ChatGPTで要約する

    Args:
        title (str): Webサイトのタイトル
        content (str): Webサイトの本文
        categories (list[str]): カテゴリのリスト

    Returns:
        ChatGPTResponse: 要約結果
    """
    raise NotImplementedError
