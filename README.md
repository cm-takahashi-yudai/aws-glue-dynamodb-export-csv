# aws-glue-dynamodb-export-csv

## はじめに

Glueを利用してDynamoDBのデータをS3バケットにCSV形式で出力します。また、トリガーを使用して定期的にジョブを実行します。トリガーはコンソールから無効化することも出来ます。

## 環境変数

makeコマンドの実行に必要な環境変数をセットします。

```bash
$ export PROJECT_NAME="aws-glue-dynamodb-export-csv-{MY_NAME}"
$ export STAGE_NAME="dev"
```

※ `PROJECT_NAME` が一意になるように `{MY_NAME}` を置き換えてください。

## デプロイ方法

全てのリソースをデプロイします。

```bash
$ make deploy-all
```

## 事前準備

DynamoDBのテーブルにサンプルデータを登録します。

```bash
$ make dynamodb-put-sample-items
```

## 実行方法

1. AWS Glueのコンソールを開く
2. 左のメニューから「ジョブ」を選択
3. 対象のジョブにチェックを入れる
4. アクションから「ジョブの開始」を選択

## 後片付け

全てのリソースを削除します。

```bash
$ make delete-stack-all
```
