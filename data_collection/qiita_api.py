import os
import re
import requests
import pandas as pd
import numpy as np
from retry import retry
from dotenv import load_dotenv


class QiitaAPI:
    def __init__(self):
        load_dotenv(".env")
        access_token = os.environ.get("ACCESS_TOKEN")

        self.url = 'https://qiita.com/api/v2/items'
        self.headers = {
            "content-type" : "application/json",
            "charset"      : "utf-8",
            "Authorization": "Bearer {}".format(access_token)
        }
        self.columns = [
            "likes_count",
            "title",
            "body",
            "created_date",
            "created_time",
            "tags",
            "followers_count",
            "organization",
            "items_count"
        ]

    @retry(delay=1, backoff=2, max_delay=8)
    def __get(self, yyyymm, page=1, per_page=100):
        params={
            "page"    : page,
            "per_page": per_page,
            "query"   : "created:{}".format(yyyymm)  # このように年月を指定することで制限を回避できる
        }
        return requests.get(self.url, params=params, headers=self.headers)

    def n_pages(self, yyyymm, page=1, per_page=100):
        res = self.__get(yyyymm, page, per_page)
        headers = res.headers
        link_last = headers.get("Link").split(",")[-1]
        n_pages = int(re.search(r"\?page=(\d+)", link_last).group(1))
        print(f"- search time: {yyyymm}, n_pages: {n_pages}")
        return n_pages

    def page_content(self, yyyymm, page, per_page=100):
        print(f"\t- page: {page}")
        res = self.__get(yyyymm, page, per_page)
        res = res.json()
        data_list = []
        for item in res:
            user_info = item["user"]
            data = [
                item["likes_count"],
                item["title"],
                item["body"].replace("\r", "").replace("\n", ""),
                item["created_at"].split("T")[0],
                item["created_at"].split("T")[1].split("+")[0],
                [tag["name"] for tag in item["tags"]],
                user_info["followers_count"],
                user_info["organization"],
                user_info["items_count"]
            ]
            data_list.append(data)
        df = pd.DataFrame(
            data_list,
            columns=self.columns,
            index=np.arange(len(data_list))
        )
        return df
