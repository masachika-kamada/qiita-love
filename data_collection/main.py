import pandas as pd
from qiita_api import QiitaAPI


def main():
    start_date = "2020-02-01"
    end_date   = "2021-11-30"
    api = QiitaAPI()

    for dt in pd.date_range(start=start_date, end=end_date, freq="MS", tz="Asia/Tokyo"):
        yyyymm = dt.strftime("%Y-%m")

        for page in range(1, api.n_pages(yyyymm) + 1):
            if page > 100:
                break
            df = api.page_content(yyyymm, page)
            df.to_csv(
                f"data/{yyyymm}.csv",
                mode="a",
                header=(page == 1),
                index=False,
                encoding="utf8",
                line_terminator="\n",
                escapechar="\\"
            )


if __name__ == "__main__":
    main()
