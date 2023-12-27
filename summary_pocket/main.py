import datetime
import os

import dotenv

from summary_pocket import (
    chatgpt,
    notification,
    notion,
    pocket,
    website,
)

dotenv.load_dotenv()

UNCATEGORIZED_NAME = os.environ['NOTION_UNCATEGORIZED_NAME']


def main():
    """Pocketから未読記事を取得し、ChatGPTで要約して、Notionに保存する"""
    try:
        # NotionのDBの形式が正しいかチェック
        notion.check_db()
    except Exception as e:
        notification.notify_to_slack(
            content=f"Error (Notion DB): {e}",
            channel='error',
        )
        return

    for article in pocket.get_unread_articles():
        try:
            # Webサイトの情報を取得
            site_info = website.get_site_info(article.url)

            # ChatGPTを使って要約
            categories = notion.get_categories()
            response = chatgpt.summarize(site_info.title, site_info.content, categories)
            if response.category not in categories:
                response.category = UNCATEGORIZED_NAME

            # Notionに保存
            notion.save(
                notion.NotionItem(
                    title=article.title,
                    url=article.url,
                    category=response.category,
                    summary=response.summary,
                    fetched_at=datetime.datetime.now(
                        datetime.timezone(datetime.timedelta(hours=9), 'JST')
                    ),
                )
            )

            # Pocketから削除
            pocket.archive_article(article.id)

            # Slackに通知
            notification.notify_to_slack(
                content=f"Success ({article.url})",
                channel='notify',
            )
        except Exception as e:
            notification.notify_to_slack(
                content=f"Error ({article.url}): {e}",
                channel='error',
            )


if __name__ == '__main__':
    main()
