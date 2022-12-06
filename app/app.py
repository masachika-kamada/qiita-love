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
body = st.text_area(label='記事の内容を入力して下さい', height=500)
created_date = st.date_input(label='記事を公開した日付を入力して下さい')
created_time = st.time_input(label='記事を公開した日時を入力して下さい')
tags = st.text_input(label='タグを書いて下さい')
followers_count = st.number_input(label='フォロワー数を入力して下さい')
organization = st.text_input(label='組織に参加している場合は記入して下さい')
items_count = st.number_input(label='今までに書いた記事の数を入力して下さい')

# 型の確認
# st.write(type(title)) # str
# st.write(type(body)) # str
# st.write(type(created_date)) # datetime.date
# st.write(type(created_time)) # datetime.time
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
    data["organization"] = int(bool(organization))

    # created_dateの前処理
    data["created_days_ago"] = (date.today() - data["created_date"][0]).days
    data["created_month"] = data["created_date"][0].month
    data["created_time"] = int(created_time.strftime("%H:%M:%S")[:2])
    data = data.drop(['created_date'], axis=1)

    # title, body, tagsの前処理
    # 学習済みモデルの読み込み(tf-idf)
    model_tfidf_title = pickle.load(open(r"model_tfidf\trained_model_title.pkl", 'rb'))
    model_tfidf_body = pickle.load(open(r"model_tfidf\trained_model_body.pkl", 'rb'))
    model_tfidf_tags = pickle.load(open(r"model_tfidf\trained_model_tags.pkl", 'rb'))
    # tf-idf化
    tfidf_title = model_tfidf_title.transform(data["title"])
    tfidf_body = model_tfidf_body.transform(data["body"])
    tfidf_tags = model_tfidf_tags.transform(data["tags"])
    # 学習済みモデルの読み込み(svd)
    model_svd_title = pickle.load(open(r"model_svd\trained_model_title.pkl", 'rb'))
    model_svd_body = pickle.load(open(r"model_svd\trained_model_body.pkl", 'rb'))
    model_svd_tags = pickle.load(open(r"model_svd\trained_model_tags.pkl", 'rb'))
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
    model = pickle.load(open(r'model\trained_rfr_model.pkl', 'rb'))

    # 予測
    pred = model.predict(data)
    st.write(f'いいね数の予測値は{pred[0]}です！')