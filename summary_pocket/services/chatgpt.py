import os
import string
import time

import dotenv
import openai
from openai.types.chat import ParsedChatCompletion
from pydantic import BaseModel

dotenv.load_dotenv()

RETRY_NUM = 10
GPT_MODEL_NAME = 'gpt-4o-mini'
PROMPT_PATH = 'data/prompt.txt'
OPENAI_API_TOKEN = os.environ['OPENAI_API_TOKEN']
OPENAI_API_ORGANIZATION = os.environ['OPENAI_API_ORGANIZATION']


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
    # プロンプトを作成
    prompt = _generate_prompt(title, content, list(categories))

    # ChatGPTを実行
    client = openai.OpenAI(
        api_key=OPENAI_API_TOKEN,
        organization=OPENAI_API_ORGANIZATION,
    )
    response = _execute(client, prompt)
    response_obj = response.choices[0].message.parsed
    assert isinstance(response_obj, ChatGPTResponse)

    return response_obj


def _generate_prompt(title: str, content: str, categories: list[str]) -> str:
    with open(PROMPT_PATH, 'r', encoding='utf-8') as f:
        prompt_template_str = f.read()

    categories_str = ''
    for category in categories:
        categories_str += f"- {category}\n"

    # 最後の改行を削除
    categories_str = categories_str[:-1]

    prompt_template = string.Template(prompt_template_str)
    return prompt_template.substitute(
        title=title,
        content=content,
        categories=categories_str,
    )


def retry_wrapper(func):
    """OpenAI APIのレート制限に引っかかった場合に、リトライするラッパー

    Args:
        func (function): ラップする関数
    """

    def wrapper(*args, **kwargs):
        error = Exception('Retry error')
        for _ in range(RETRY_NUM):
            try:
                value = func(*args, **kwargs)
                break
            except (openai.RateLimitError, openai.APIConnectionError, openai.APIError) as e:
                print(f"retry: sleep 60s ({e})")
                error = e
                time.sleep(60)
                continue
        else:
            raise error

        return value

    return wrapper


@retry_wrapper
def _execute(client: openai.OpenAI, prompt: str) -> ParsedChatCompletion:
    return client.beta.chat.completions.parse(
        model=GPT_MODEL_NAME,
        messages=[
            {'role': 'user', 'content': prompt},
        ],
        response_format=ChatGPTResponse,
        temperature=0,
        top_p=0,
        seed=0,
    )
