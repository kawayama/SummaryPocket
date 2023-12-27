import datetime

from summary_pocket import (
    chatgpt,
    notification,
    notion,
    pocket,
    website,
)


def main():
    """Pocketから未読記事を取得し、ChatGPTで要約して、Notionに保存する"""
    article_list = pocket.get_unread_articles()
    for article in article_list:
        try:
            site_text = website.get_text(article.url)
            response = chatgpt.summarize(site_text)
            notion.save(notion.NotionItem(
                title=article.title,
                url=article.url,
                summary=response.summary,
                importance=response.importance,
                fetched_at=datetime.datetime.now(),
            ))
            pocket.archive_article(article.id)
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
