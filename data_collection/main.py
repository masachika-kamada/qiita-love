import pandas as pd
from qiita_api import QiitaAPI


def export_data(df, file_base, header):
    df.to_csv(
        f"data/{file_base}.csv",
        mode="a",
        header=header,
        index=False,
        encoding="utf8",
        line_terminator="\n",
        escapechar="\\"
    )


def create_dataset(api, time_range, file_base, header_bool=False, remove_time=None):
    overflow100 = False
    last_ymd = None
    last_time = None
    for page in range(1, api.n_pages(time_range) + 1):
        df = api.page_content(time_range, page)
        if remove_time is not None:
            df = df[df["created_time"] < remove_time]
        if page == 1 and header_bool:
            export_data(df, file_base, True)
        else:
            export_data(df, file_base, False)
        # 101ページ目以降はエラーが出るので
        if page == 100:
            overflow100 = True
            tail = df.tail(1)
            last_ymd  = tail["created_date"].values[0]
            last_time = tail["created_time"].values[0]
            break
    return overflow100, last_ymd, last_time


def main():
    start_date = "2020-01-01"
    end_date   = "2021-11-31"
    api = QiitaAPI()

    for date in pd.date_range(start=start_date, end=end_date, freq="MS"):
        ym = date.strftime("%Y-%m")

        ret, last_ymd, last_time = create_dataset(api, ym, ym, True)
        if ret is False:
            continue

        # 101ページ目以降のデータを取得
        start_date = last_ymd[:-2] + "01"
        for rest_date in pd.date_range(start=start_date, end=last_ymd, freq="D"):
            ymd = rest_date.strftime("%Y-%m-%d")

            if ymd == last_ymd:
                create_dataset(api, ymd, ym, remove_time=last_time)
            else:
                create_dataset(api, ymd, ym)


if __name__ == "__main__":
    main()
