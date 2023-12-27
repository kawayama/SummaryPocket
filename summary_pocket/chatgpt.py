from pydantic import BaseModel


class ChatGPTResponse(BaseModel):
    """ChatGPTの要約結果

    Attributes:
        category (str): カテゴリ
        summary (str): 要約
    """

    category: str
    summary: str


def summarize(title: str, content: str, categories: set[str]) -> ChatGPTResponse:
    """ChatGPTで要約する

    Args:
        title (str): Webサイトのタイトル
        content (str): Webサイトの本文
        categories (set[str]): カテゴリのリスト

    Returns:
        ChatGPTResponse: 要約結果
    """
    raise NotImplementedError
