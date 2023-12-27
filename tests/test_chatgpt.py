from summary_pocket.services import chatgpt


def test__generate_prompt():
    """プロンプトを生成できるか"""
    assert chatgpt._generate_prompt(
        title='title',
        content='content',
        categories=['category1', 'category2']
    ) == """\
あなたは要約者です。入力を基にその記事のカテゴリと要約を出力してください。出力には以下の制限に従ってください。

### 制限 ###
リスポンスは必ず以下のキーを含んだJSON形式で出力してください。
- category: str (記事のカテゴリをカテゴリ一覧の中から1つ選んでください)
- summary: str (markdown形式の箇条書きで3点を出力してください)

### カテゴリ一覧 ###
- category1
- category2

### 入力 ###
Title: title
Content: content
"""


def test_summarize():
    title = 'openpyxlで作ったExcelファイルがエラーになってしまう #Python - Qiita'
    content = """\
search
ログイン
新規登録
トレンド
質問
calendar_today
アドベントカレンダー
公式イベント
公式コラム
募集
Organization
Qiitaにログインしてダークテーマを使ってみませんか？🌙
ログインするとOSの設定にあわせたテーマカラーを使用できます！
ログイン
新規登録
また後で
1
2
more_horiz
環境
問題
解決の経緯
原因
解決法
参考
info
この記事は最終更新日から1年以上が経過しています。
@Yamakawa0032
openpyxlで作ったExcelファイルがエラーになってしまう
Python
error
Openpyxl
投稿日 2022年10月27日
環境
Windows: 10 Education 21H2
Excel: バージョン 2209
Python: 3.9.6 (pyenv + pipenv)
Pipenv: version 2021.11.23
openpyxl: 3.0.10
問題
スクレイピング結果をopenpyxlでExcelファイルとして出力した
そのExcelファイルを開くときに '<ファイル名>' の一部の内容に問題が見つかりました。可能な限り内容を回復しますか？ブックの発行元が信頼できる場合は、[はい] をクリックしてください。 というダイアログが開いてしまう
↓ 修正時のログ
削除されたレコード: /xl/worksheets/sheet1.xml パーツ内の数式
削除されたレコード: /xl/worksheets/sheet4.xml パーツ内の数式
削除されたレコード: /xl/worksheets/sheet6.xml パーツ内の数式
削除されたレコード: /xl/worksheets/sheet14.xml パーツ内の数式
削除されたレコード: /xl/worksheets/sheet16.xml パーツ内の数式
削除されたレコード: /xl/worksheets/sheet20.xml パーツ内の数式
解決の経緯
同じような問題を調べたところ、「シート名に全角括弧が含まれている」や「使えない文字が含まれている」ことが原因になるらしい
しかしこれらの問題を消してもエラーは消えない
xlsxファイルをzipファイルに変換して、修正前と後を比較すると修正部分がわかるらしい
openpyxlとExcel間で文字の表現方法が少し異なるようで、純粋に比較してもわからなかった
原因がわかった方法
問題が発生していたシート内の列を徐々に減らし、問題となっている列を特定
その列の文字列を色々と変更してみて実験した
原因
セルの先頭にイコール = が付いているとエラー
openpyxlはデフォルトではセルを数値として処理しているらしく、= が付いていると数式として認識してしまう？
その結果、誤った数式であるのでエラーが出てしまう？
解決法
以下のどちらか (詳細は参考URLをチェック)
セルの先頭の = を '= に変換
セルの書式を文字列にする
参考
OpenPyXlで生成したファイルがExcelで開けないパターンとその対処 - Qiita
share
新規登録して、もっと便利にQiitaを使ってみよう
あなたにマッチした記事をお届けします
便利な情報をあとで効率的に読み返せます
ダークテーマを利用できます
ログインすると使える機能について
新規登録
ログイン
関連記事 Recommended by
pythonのOpenPyXLでExcelのデータをとことん読み取る
by mimitaro
プログラミング未経験者がPython覚えて子ども用計算ドリルを作る
by sotogawa
Apache POI ハマりポイント一覧
by nmby
pandasのDataFrameを元に、画像入りの表をつくる
by nshinya
世界一給料が高い町工場を作る。社長と社員の「普段の会話」が本質すぎた
PR ビズヒント
新しいイーサネットの世界体験：WIZnetのTOEコンテンツ
PR WIZnet
コメント
この記事にコメントはありません。
いいね以上の気持ちはコメントで
ログイン
新規登録
How developers code is here.
© 2011-2023Qiita Inc.
ガイドとヘルプ
About
利用規約
プライバシーポリシー
ガイドライン
デザインガイドライン
ご意見
ヘルプ
広告掲載
コンテンツ
リリースノート
公式イベント
公式コラム
募集
アドベントカレンダー
Qiita 表彰プログラム
API
SNS
Qiita（キータ）公式
Qiita マイルストーン
Qiita 人気の投稿
Qiita（キータ）公式
Qiita 関連サービス
Qiita Team
Qiita Jobs
Qiita Zine
Qiita 公式ショップ
運営
運営会社
採用情報
Qiita Blog"""
    result = chatgpt.summarize(
        title=title,
        content=content,
        categories={'技術', '本', '勉強'}
    )
    print(result)

    assert result.category == '技術'
    assert len(result.summary) > 0
    assert len(result.summary.split('\n')) == 3
