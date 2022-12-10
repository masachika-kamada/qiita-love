import streamlit as st
import pandas as pd
import numpy as np
import sklearn
import lightgbm as lgb
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from datetime import date
from datetime import datetime
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

st.title("Qiitaいいね数予測アプリ")

# 入力を受け取る
title = st.text_input(label='記事のタイトルを入力して下さい')
body = st.text_area(label='記事の本文を入力して下さい', height=500)
created_date = st.date_input(label='記事の公開(予定)日を入力して下さい')
created_time = st.slider(label="記事の公開(予定)時刻を入力して下さい", min_value=0, max_value=23, value=12, step=1)
tags = st.text_input(label="タグをカンマ区切りで入力して下さい")
followers_count = st.number_input(label='フォロワー数を入力して下さい', step=1, min_value=0)
organization = st.radio(label="組織に参加していますか", options=["はい", "いいえ"])
items_count = st.number_input(label='今までに書いた記事の数を入力して下さい', step=1, min_value=0)

# 型の確認
# st.write(type(title)) # str
# st.write(type(body)) # str
# st.write(type(created_date)) # datetime.date
# st.write(type(created_time)) # int
# st.write(type(tags)) # str
# st.write(type(followers_count)) # float
# st.write(type(organization)) # str
# st.write(type(items_count)) # float

bt = st.button('いいね数を予測する')
if bt:
    # データの初期化
    data_dict = {"title": [title], "body": [body], "created_date": [created_date], "created_time": [created_time], "tags": [tags], "followers_count": [followers_count], "organization": [organization], "items_count": [items_count]}
    data = pd.DataFrame(data_dict)

    # organizationの前処理
    data["organization"] = data["organization"].map({"はい": 1, "いいえ": 0})

    # created_dateの前処理
    data["created_days_ago"] = (date.today() - data["created_date"][0]).days
    data["created_month"] = data["created_date"][0].month
    data = data.drop(['created_date'], axis=1)

    # title, body, tagsの前処理
    # 学習済みモデルの読み込み(tf-idf)
    model_tfidf_title = pickle.load(open("../data_analysis/output/tfidf_title.pkl", 'rb'))
    model_tfidf_body = pickle.load(open("../data_analysis/output/tfidf_body.pkl", 'rb'))
    model_tfidf_tags = pickle.load(open("../data_analysis/output/tfidf_tags.pkl", 'rb'))
    # tf-idf化
    tfidf_title = model_tfidf_title.transform(data["title"])
    tfidf_body = model_tfidf_body.transform(data["body"])
    tfidf_tags = model_tfidf_tags.transform(data["tags"])
    # 学習済みモデルの読み込み(svd)
    model_svd_title = pickle.load(open("../data_analysis/output/svd_title.pkl", 'rb'))
    model_svd_body = pickle.load(open("../data_analysis/output/svd_body.pkl", 'rb'))
    model_svd_tags = pickle.load(open("../data_analysis/output/svd_tags.pkl", 'rb'))
    # 次元削減
    svd_title = model_svd_title.transform(tfidf_title)
    svd_body = model_svd_body.transform(tfidf_body)
    svd_tags = model_svd_tags.transform(tfidf_tags)
    # データフレームに変換
    data_title_vec = pd.DataFrame(svd_title, columns=[f"title_{i}" for i in range(20)])
    data_body_vec = pd.DataFrame(svd_body, columns=[f"body_{i}" for i in range(20)])
    data_tags_vec = pd.DataFrame(svd_tags, columns=[f"tags_{i}" for i in range(20)])

    # 元のデータフレームと結合
    data = pd.concat([data, data_title_vec], axis=1)
    data = data.drop(['title'], axis=1)
    data = pd.concat([data, data_body_vec], axis=1)
    data = data.drop(['body'], axis=1)
    data = pd.concat([data, data_tags_vec], axis=1)
    data = data.drop(['tags'], axis=1)

    # 予測モデルの読み込み
    model = pickle.load(open(r'..\data_analysis\output\model.pkl', 'rb'))

    # 予測
    pred = model.predict(data)
    st.write(f'いいね数の予測値は{pred[0]}です！')