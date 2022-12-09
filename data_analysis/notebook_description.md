# 作成したノートブックの説明

（作成日時の古い順）

| file | 概要 | MAE | コメント |
|:--|:--| :--: | :--|
| [tsubasa.ipynb](https://github.com/masachika-kamada/qiita-love/blob/development/data_analysis/tsubasa.ipynb) | tsuabasaくんが作ってくれたプログラム | 12.7 | 全ての情報を文字列として連結しベクトル化後8次元に圧縮 |
| [baseline.ipynb](https://github.com/masachika-kamada/qiita-love/blob/development/data_analysis/baseline.ipynb) | tsubasaをもとに、likes_countの最大値を1000に、圧縮次元数を50に変更 | 11.6 | 次元数を増やすことで少しだけMAE低減 |
| [not_concat.ipynb](https://github.com/masachika-kamada/qiita-love/blob/development/data_analysis/not_concat.ipynb) | 文字列データを結合せずにそれぞれでベクトル化後20次元に圧縮 | 9.6 | 全てのデータを結合するのは良くない |
| [algorithm_tuning.ipynb](https://github.com/masachika-kamada/qiita-love/blob/development/data_analysis/algorithm_tuning.ipynb) | PyCaretでアルゴリズム比較 | - | LightGBMのMAEが最低だった |
| [analysis.ipynb](https://github.com/masachika-kamada/qiita-love/blob/development/data_analysis/analysis.ipynb) | tsubasaくんがapp作成のためにnot_concatをベースにモデルを書き出し | - | 保存したモデルのサイズが大きいのがネック |
