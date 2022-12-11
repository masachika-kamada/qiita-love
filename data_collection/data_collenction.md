# Qiita のデータ分析のためのデータ収集

## 求めたいデータ

- [x] like の数（正解ラベル）
- [x] 本文の内容
- [x] 記事が投稿されてからの時間
- [x] フォロワー数
- [x] orgaization の数
- [ ] contribution の数

## Qiita API

- [アクセストークンの発行](https://qiita.com/settings/applications)
  - [【GitHub】に載せたくない環境変数の書き方 Python](https://qiita.com/hedgehoCrow/items/2fd56ebea463e7fc0f5b)
- [参考になりそうなリポジトリ](https://github.com/stakiran/qiita_exporter)
- [Qiita API v2](https://qiita.com/api/v2/docs)

## 所感

- [このように](https://qiita.com/dcm_chida/items/687654685dc434bdc9d4#:~:text=r%20%3D%20requests.get(url%2C%20params%3Dparams%2C%20%20headers%3Dheaders)) `requests` を使うことでページの内容を取れる
- 引数の `params` に [このように](https://developer.kaizenplatform.com/entry/takus/2018-04-26/#:~:text=%27query%27%3A%20%27created%3A%7B%7D%27.format(yyyymm)%2C) `query` を指定することで、上限に引っかかるのを防げるっぽい
- [QiitaClient](https://developer.kaizenplatform.com/entry/takus/2018-04-26/#:~:text=qiita_v2.client%20import-,QiitaClient,-from%20qiita_v2.exception) というのを使うことで `requests` を使わなくても API を叩けるっぽい
- ラッパーでわかりづらいのでやめた
