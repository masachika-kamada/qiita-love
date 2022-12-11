import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

import torch 
import torch.nn as nn 
from transformers import AutoConfig 
from transformers import AutoModel  
from transformers import AutoTokenizer 

MODEL_PATH = '../data_analysis/model.pth' 
device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
MODEL_NAME = 'bert-base-uncased' 
TOKENIZER = AutoTokenizer.from_pretrained(MODEL_NAME) 
MAX_LEN = 320

class QiitaModel(nn.Module):

  def __init__(self):
    super(QiitaModel, self).__init__() 
    self.config = AutoConfig.from_pretrained(MODEL_NAME) 
    self.bert = AutoModel.from_pretrained(MODEL_NAME)
    self.regressor = nn.Linear(self.config.hidden_size, 1) 

  def forward(self, input_ids, attention_mask, token_type_ids):
    outputs = self.bert(
        input_ids,
        attention_mask=attention_mask,
        token_type_ids=token_type_ids
    )
    sequence_output = outputs['last_hidden_state'][:, 0] 
    logits = self.regressor(sequence_output)

    return logits 

  def loss_fn(self, logits, label):
    loss = nn.L1Loss(reduction='mean')(logits[:, 0], label)
    return loss


class Analyzer:
    def __init__(self):
        self.model = QiitaModel().to(device)
        self.model.load_state_dict(torch.load(MODEL_PATH))

    def __create_tensor(self, title, body, tags, followers_count, organization, items_count):
        tok = TOKENIZER.encode_plus(
            body, 
            max_length=MAX_LEN, 
            truncation=True,
            padding="max_length",
            return_attention_mask=True,
            return_token_type_ids=True,
        )

        d = {
            "input_ids": torch.tensor(tok["input_ids"], dtype=torch.long).view(1, -1),
            "attention_mask": torch.tensor(tok["attention_mask"], dtype=torch.long).view(1, -1),
            "token_type_ids": torch.tensor(tok["token_type_ids"], dtype=torch.long).view(1, -1),
        }

        self.data = d


    def predict(self, title, body, tags, followers_count, organization, items_count):
        self.__create_tensor(title, body, tags, followers_count, organization, items_count)
        self.model.eval()
        like_pred = self.model(
            self.data['input_ids'].to(device),
            self.data['attention_mask'].to(device),
            self.data['token_type_ids'].to(device)
        )
        # 予測値がマイナスになる場合は0にする
        if like_pred < 0:
            like_pred = 0
        return like_pred


def main():

    st.title("Qiitaいいね数予測アプリ")

    # 入力を受け取る
    title = st.text_input(label="記事のタイトルを入力して下さい")
    body = st.text_area(label="記事の本文を入力して下さい", height=500)
    tags = st.text_input(label="タグをカンマ区切りで入力して下さい")
    followers_count = st.number_input(label="フォロワー数を入力して下さい", step=1, min_value=0)
    organization = st.radio(label="組織に参加していますか", options=["はい", "いいえ"])
    items_count = st.number_input(label="既に公開済みの記事の数を入力して下さい", step=1, min_value=0)

    pred_button = st.button("いいね数を予測する")

    analyzer = Analyzer()

    if pred_button is True:
        # TODO: 入力値のバリデーション

        # 予測
        pred = analyzer.predict(title, body, tags, followers_count, organization, items_count)
        st.write(f"## いいね数の予測値は {pred:.2f} です！")


if __name__ == "__main__":
    main()