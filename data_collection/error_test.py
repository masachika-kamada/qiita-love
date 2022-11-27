import pandas as pd
from qiita_api import QiitaAPI


def main():
    api = QiitaAPI()
    yyyymm = "2020-02"
    print(api.n_pages(yyyymm))
    page = 100

    df = api.page_content(yyyymm, page)
    df.to_csv(f"data/error.csv", mode="a", header=(page == 1), index=False, encoding="utf8", line_terminator="\n")


if __name__ == "__main__":
    main()
