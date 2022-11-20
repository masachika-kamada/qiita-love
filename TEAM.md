# チームメンバー向け

## 1. Issue の作成

Issue を作成して、自分がこれから取り掛かるタスクの詳細を書く

<img src="https://user-images.githubusercontent.com/63488322/202914518-15420b48-03d4-45e3-bd0f-1685e76302c9.png">

## 2. ブランチの作成

Issue を作成したら、ブランチを作成する

**要約**：自分の書いたプログラムが他の人に影響を与えないために、自分専用の加工場を作る

- ブランチ名：feature/#[issue番号]_[機能名]
  - 例：feature/#1_data-collection
- `git checkout -b feature/#[issue番号]_[機能名]`
- 誤ってブランチを作成した、名前を間違えた場合、削除
  - `git branch -d [ブランチ名]`

## 3. 作成したブランチで開発

キリがよくなったら以下のコマンドでコミット

**要約**：commit で作業内容をセーブする，セーブした内容を push で GitHub にアップロードする

- `git add .`
- `git commit -m “コミットメッセージ”`
- コミットメッセージの書き方
  - [コミット種別] #対応するissue番号 要約
  - コミット種別：fix：バグ修正、add：新規（ファイル）機能追加、update：機能修正（バグではない）、remove：削除（ファイル）
  - 例：`git commit -m "[add] #1 新規モデルでsubmission”`
- `git push`
  - 一回目はupstreamなんちゃらって出るので、それをコピーして実行すればよい

## 4. 開発終了

push済みであることを確認する

**要約**：ローカルで書いたプログラムが GitHub にアップロードされていることの確認

- `git status`
- `Your branch is up to date with '***'.` と表示されればOK

## 5. Pull request を作成する

**要約**：自分が書いたプログラム（下書き）を GitHub の本流のブランチ（清書）に統合する

- タイトルを`[ブランチ名] 要約`として内容もわかるように書く
- 解決する Issue も登録する
- ローカルで `git checkout development`
- プルリクがマージされたら `git pull`
- 1 番に戻って別のタスクに取り掛かる
