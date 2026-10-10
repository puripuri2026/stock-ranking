# stock-ranking
Viewing  stock check status

株価ランキング（公開リポジトリ1つで運用）
この構成では、公開リポジトリ1つだけを使用します。GitHub Actionsの Run workflow を押すと、株価を取得して stock_data.json を更新し、GitHub Pagesで公開します。PCにPythonをインストールする必要はありません。
重要：このリポジトリは公開です
stocks.txt、コード、HTML、生成された stock_data.json は誰でも閲覧できます。公開しても問題ない銘柄リスト・情報だけを置いてください。GitHubトークンなどの秘密情報は絶対にコミットしないでください。
1. ファイルをリポジトリに追加
ZIP内の次のファイルを、公開リポジトリのルートに追加します。
stocks.txt（自分の銘柄リストを作成／追加）
stock_chart.py
index.html
.github/workflows/update-stocks.yml
stocks.txt の例：
3901 マークラインズ
4543 テルモ
7203 トヨタ自動車
既存の stocks.txt がある場合はその内容を使ってください。1行に銘柄コード、半角スペース、会社名の順で記載します。コメント行は # で始めます。
2. Actionsの書き込み権限を確認
リポジトリの Settings → Actions → General → Workflow permissions で、必要なら Read and write permissions を選んで保存してください。ワークフロー自体も contents: write を宣言しています。
3. GitHub Pagesを有効化
Settings → Pages で、Sourceを Deploy from a branch、Branchを main、フォルダを /(root) にしてSaveします。デフォルトブランチが master の場合は master を選びます。
4. Run workflowで株価データを更新
Actionsタブを開く
左側の Update stock ranking を選ぶ
Run workflow → Run workflow を押す
実行が完了するまで待つ
公開リポジトリのGitHub Pages URLを開く
ワークフローは stock_data.json を生成し、リポジトリにコミットします。初回は stock_data.json が存在しなくても、Actions実行後に作成されます。
ランキングの計算
最大約10年分の日足OHLCデータを取得
終値：取得できた直近取引日の終値
期間最安値：画面で指定した期間の日足 Low の最小値
比率：直近取引日の終値 ÷ 期間最安値
比率の昇順でランキング
期間プリセットまたは開始日・終了日を自由指定
銘柄選択で日足・週足・月足チャートを表示
HTMLの「ランキング再計算」は、すでに取得したデータで計算します。最新の株価履歴を取り直すには、Actionsの Run workflow を押してください。
注意事項
公開リポジトリなので、銘柄リストも公開されます。
Yahoo Finance経由のyfinanceデータは公式のリアルタイム配信を保証しません。遅延、欠損、取得失敗などがあり得ます。
データは最大約10年分です。
公開用サイトと stock_data.json は誰でも閲覧できます。
このページは投資助言ではありません。投資判断の前に証券会社等の情報を確認してください。
