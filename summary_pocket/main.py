import argparse
import datetime
import logging
import os
import time

import dotenv

from summary_pocket.services import chatgpt, notion, pocket, website
from summary_pocket.utils import (
    error_url_util,
    logger_util,
    notification_util,
)

dotenv.load_dotenv()

CHATGPT_MAX_LENGTH = 4000
UNCATEGORIZED_NAME = os.environ['NOTION_UNCATEGORIZED_NAME']

logger = logging.getLogger(__name__)
logger_util.setting_logger(logger)


def main() -> None:
    """Pocketから未読記事を取得し、ChatGPTで要約して、Notionに保存する"""
    try:
        # NotionのDBの形式が正しいかチェック
        notion.check_db()
    except Exception as e:
        logger.error(f"Error (Notion DB): {e}")
        notification_util.notify_to_slack(
            content=f"Error (Notion DB): {e}",
            channel='#error',
        )
        return

    url_set = notion.get_urls()
    error_url_set = error_url_util.get_error_urls()

    # Pocketから未読記事を取得
    articles = pocket.get_unread_articles()

    for article in articles:
        logger.info(f'Start summarizing: {article.url}')
        if article.url in url_set:
            # Pocketから削除
            pocket.archive_article(article.id)
            logger.info(f'Already summarized: {article.url}')
            continue
        elif article.url in error_url_set:
            logger.info(f'Error url: {article.url}')
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
            notification_util.notify_to_slack(
                content=f"記事が要約されました！\nurl: {article.url}",
                channel='#notify',
            )

            logger.info(f'Finish summarizing: {article.url}')
        except Exception as e:
            # Slackに通知
            logger.error(f"Error ({article.url}): {e}")
            notification_util.notify_to_slack(
                content=f"Error ({article.url}): {e}",
                channel='#error',
            )

            # エラーが発生したURLを保存
            error_url_util.add_error_url(article.url)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Pocketから未読記事を取得し、ChatGPTで要約して、Notionに保存するツール'
    )
    while True:
        try:
            main()

            # 1回の起動ごとに10分待機
            time.sleep(10 * 60)
        except Exception as e:
            notification_util.notify_to_slack(
                content=f"Error occurred and application stopped: {e}",
                channel='#error',
            )
            break
