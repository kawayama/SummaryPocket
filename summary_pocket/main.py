import argparse
import datetime
import logging
import os

import dotenv

from summary_pocket import (
    chatgpt,
    logger_util,
    notification,
    notion,
    pocket,
    website,
)

dotenv.load_dotenv()

CHATGPT_MAX_LENGTH = 4000
UNCATEGORIZED_NAME = os.environ['NOTION_UNCATEGORIZED_NAME']

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_util.setting_logger(logger)


def main(fetch_num: int | None = None) -> None:
    """Pocketから未読記事を取得し、ChatGPTで要約して、Notionに保存する"""
    try:
        # NotionのDBの形式が正しいかチェック
        notion.check_db()
    except Exception as e:
        logger.error(f"Error (Notion DB): {e}")
        notification.notify_to_slack(
            content=f"Error (Notion DB): {e}",
            channel='#error',
        )
        return

    url_set = notion.get_urls()

    # Pocketから未読記事を取得
    articles = pocket.get_unread_articles()
    if fetch_num is None:
        target_articles = articles
    else:
        target_articles = articles[:fetch_num]

    for article in target_articles:
        logger.info(f'Start summarizing: {article.url}')
        if article.url in url_set:
            logger.info(f'Already summarized: {article.url}')
            continue

        try:
            # Webサイトの情報を取得
            site_info = website.get_site_info(article.url)
            if site_info.url in url_set:
                # Pocketから削除
                pocket.archive_article(article.id)
                logger.info(f'Already summarized: {article.url}')
                continue
            elif len(site_info.content) >= CHATGPT_MAX_LENGTH:
                site_info.content = site_info.content[:CHATGPT_MAX_LENGTH]

            # ChatGPTを使って要約
            categories = notion.get_categories()
            response = chatgpt.summarize(site_info.title, site_info.content, categories)
            if response.category not in categories:
                response.category = UNCATEGORIZED_NAME

            # Notionに保存
            notion.save(
                notion.NotionItem(
                    title=site_info.title,
                    url=site_info.url,
                    category=response.category,
                    summary=response.summary,
                    fetched_at=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9), 'JST')),
                )
            )

            # Pocketから削除
            pocket.archive_article(article.id)

            # Slackに通知
            notification.notify_to_slack(
                content=f"記事が要約されました！\nurl: {article.url}",
                channel='#notify',
            )

            logger.info(f'Finish summarizing: {article.url}')
        except Exception as e:
            # Slackに通知
            logger.error(f"Error ({article.url}): {e}")
            notification.notify_to_slack(
                content=f"Error ({article.url}): {e}",
                channel='#error',
            )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pocketから未読記事を取得し、ChatGPTで要約して、Notionに保存するツール')
    parser.add_argument('--fetch-num', type=int, default=None, help='取得する記事の数')
    args = parser.parse_args()

    fetch_num_str = args.fetch_num
    try:
        fetch_num = int(fetch_num_str)
    except Exception:
        raise ValueError(f'fetch-numの値が不正です: {fetch_num_str}')

    main(fetch_num)
