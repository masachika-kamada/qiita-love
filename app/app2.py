import streamlit as st
import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import pickle


def create_dataframe(title, body, created_date, created_time, tags, followers_count, organization, items_count):
    df = pd.DataFrame()
    df["title"] = [title]
    df["body"] = [body]
    df["created_date"] = [created_date]
    df["created_time"] = [created_time]
    df["tags"] = [tags]
    df["followers_count"] = [followers_count]
    df["organization"] = [organization]
    df["items_count"] = [items_count]
    return df


def preprocess(df):
    # created_dateを今日から何日前に投稿されたかを表す数値に変換
    df["created_date"] = pd.to_datetime(df["created_date"])
    df["created_days_ago"] = (pd.to_datetime("today") - df["created_date"]).dt.days
    df["created_month"] = df["created_date"].dt.month
    df = df.drop("created_date", axis=1)
    # organizationの値が"はい"ならTrue, "いいえ"ならFalseに変換
    df["organization"] = df["organization"].map({"はい": True, "いいえ": False})

    # title, body, tagsの前処理
    # 学習済みモデルの読み込み(tf-idf)
    model_tfidf_title = pickle.load(open("../data_analysis/output/tfidf_title.pkl", "rb"))
    model_tfidf_body = pickle.load(open("../data_analysis/output/tfidf_body.pkl", "rb"))
    model_tfidf_tags = pickle.load(open("../data_analysis/output/tfidf_tags.pkl", "rb"))
    # tf-idf化
    tfidf_title = model_tfidf_title.transform(df["title"])
    # print("tfidf_title.shape: ", tfidf_title.shape)
    tfidf_body = model_tfidf_body.transform(df["body"])
    # print("tfidf_body.shape: ", tfidf_body.shape)
    tfidf_tags = model_tfidf_tags.transform(df["tags"])
    # print("tfidf_tags.shape: ", tfidf_tags.shape)
    # 学習済みモデルの読み込み(svd)
    model_svd_title = pickle.load(open("../data_analysis/output/svd_title.pkl", "rb"))
    model_svd_body = pickle.load(open("../data_analysis/output/svd_body.pkl", "rb"))
    model_svd_tags = pickle.load(open("../data_analysis/output/svd_tags.pkl", "rb"))
    # # 次元削減
    # svd_title = model_svd_title.transform(tfidf_title)
    # print("svd_title.shape: ", svd_title.shape)
    # svd_body = model_svd_body.transform(tfidf_body)
    # print("svd_body.shape: ", svd_body.shape)
    # svd_tags = model_svd_tags.transform(tfidf_tags)
    # print("svd_tags.shape: ", svd_tags.shape)
    # # データフレームに変換
    # data_title_vec = pd.DataFrame(svd_title, columns=[f"title_{i}" for i in range(20)])
    # data_body_vec = pd.DataFrame(svd_body, columns=[f"body_{i}" for i in range(20)])
    # data_tags_vec = pd.DataFrame(svd_tags, columns=[f"tags_{i}" for i in range(20)])

    # # 元のデータフレームと結合
    # df = pd.concat([df, data_title_vec], axis=1)
    # df = df.drop(["title"], axis=1)
    # df = pd.concat([df, data_body_vec], axis=1)
    # df = df.drop(["body"], axis=1)
    # df = pd.concat([df, data_tags_vec], axis=1)
    # df = df.drop(["tags"], axis=1)

    print(df.head())
    return df


def predict(df):
    # 予測モデルの読み込み
    model = pickle.load(open("../data_analysis/output/model.pkl", "rb"))
    return model.predict(df)


def main():

    st.title("Qiitaいいね数予測アプリ")

    # 入力を受け取る
    title = st.text_input(label="記事のタイトルを入力して下さい")
    body = st.text_area(label="記事の本文を入力して下さい", height=500)
    created_date = st.date_input(label="記事の公開(予定)日を入力して下さい")
    created_time = st.slider(label="記事の公開(予定)時刻を入力して下さい", min_value=0, max_value=23, value=12, step=1)
    tags = st.text_input(label="タグをカンマ区切りで入力して下さい")
    followers_count = st.number_input(label="フォロワー数を入力して下さい", step=1, min_value=0)
    organization = st.radio(label="組織に参加していますか", options=["はい", "いいえ"])
    items_count = st.number_input(label="既に公開済みの記事の数を入力して下さい", step=1, min_value=0)

    pred_button = st.button("いいね数を予測する")

    if pred_button is True:
        # TODO: 入力値のバリデーション

        df = create_dataframe(title, body, created_date, created_time, tags, followers_count, organization, items_count)
        df = preprocess(df)
        st.dataframe(df)

        # st.write(f"いいね数の予測値は{pred[0]}です！")


if __name__ == "__main__":
    main()
