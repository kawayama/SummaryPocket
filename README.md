# SummaryPocket

## 概要

- Pocketに記事を保存すると、その記事をChatGPTが要約し、Notionに保存するツール
- 3点で記事の内容を要約し、ユーザが決めたカテゴリに分類することができる

## セットアップ

1. 必要なツールをインストールする
   - [Docker](https://www.docker.com/ja-jp/): コンテナ型仮想環境
   - [Task](https://taskfile.dev/ja-JP/): タスクランナー
2. 関連ツールのアクセストークンを取得する
   - ChatGPT: [API Reference - OpenAI API](https://platform.openai.com/docs/api-reference/authentication)
   - Notion: [Notion の API の概要](https://developers.notion.com/docs/getting-started#internal-integrations)
   - Pocket: [Pocket: Developer API](https://getpocket.com/developer/)
   - Slack: [Sending messages using Incoming Webhooks | Slack](https://api.slack.com/messaging/webhooks)
3. Notionでデータベースを作成し、2で作成したツールを追加する
   1. データベースのページを作成する
   2. データベースに必要なカラムを追加する

        |カラム名|種類|
        |---|---|
        |is_read|checkbox|
        |title|title|
        |url|url|
        |category|select|
        |summary|text|
        |fetched_at|date|

   3. categoryに分類したいカテゴリを追加する
      - 4で設定する `NOTION_UNCATEGORIZED_NAME` のカテゴリを必ず含める必要がある
   4. ページ右上の設定ボタン → Connections で2で作成したツールを追加する
4. .envファイルを作成し、認証情報とデータベースIDを記述する

    ```.env
    POCKET_CONSUMER_KEY=xxxxxxxxxx
    POCKET_ACCESS_TOKEN=xxxxxxxxxx
    NOTION_TOKEN=secret_xxxxxxxxxx
    NOTION_DB_ID=xxxxxxxxxx
    NOTION_UNCATEGORIZED_NAME=未分類
    OPENAI_API_TOKEN=sk-xxxxxxxxxx
    OPENAI_API_ORGANIZATION=org-xxxxxxxxxx
    SLACK_API_KEY=/xxxxxxxx/xxxxxxxx/xxxxxxxx
    ```

5. ツールを実行する

    ```bash
    # タスク実行
    $ task run

    # ログ確認
    $ task logs

    # タスク強制終了
    $ task rm
    ```
