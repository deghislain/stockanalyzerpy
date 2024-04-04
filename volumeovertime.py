import pandas as pd
import os
import matplotlib.pyplot as plt
import sqlalchemy as db
from matplotlib import ticker





from dotenv import load_dotenv

def get_db_url():
    load_dotenv()
    PG_USERNAME = os.getenv('PG_USERNAME')
    PG_PASSWORD = os.getenv('PG_PASSWORD')

    PG_URL = db.URL.create(
        'postgresql+psycopg2',
        database='appdb',
        username=PG_USERNAME,
        password=PG_PASSWORD,
        host='127.0.0.1',
        port=5432
    )
    return PG_URL


def get_stock_volume_by_time_period(PG_URL, period_start, period_end):
    sql = "SELECT stock_volume, curr_stock_date FROM av_weekly_stock_data WHERE curr_stock_date BETWEEN \'" + period_start + "\' AND \'" + period_end +"\' order by curr_stock_date"
    engine = db.create_engine(PG_URL, echo=True)
    df = pd.read_sql_query(sql, engine)
    return df

def get_str_stock_volume_array(data):
    stock_volumes_string_array = []
    for v in data:
        stock_volumes_string_array.append(v)
    return stock_volumes_string_array

def get_str_stock_date_array(data):
    stock_dates_string_array = []
    for date in data:
        stock_dates_string_array.append(date.strftime("%d-%m-%Y"))
        print(date)
    return stock_dates_string_array


def main():
    db_url = get_db_url()
    data = get_stock_volume_by_time_period(db_url, "2024-03-01", "2024-04-01")
    x = get_str_stock_date_array(data.curr_stock_date)
    y = get_str_stock_volume_array(data.stock_volume)

    # x = get_current_stock_date_by_time_period(db_url,"2024-03-01", "2024-04-01")
    font1 = {'family': 'serif', 'color': 'blue', 'size': 20}
    font2 = {'family': 'serif', 'color': 'darkred', 'size': 15}
    plt.title("Stock Volume Data", fontdict=font1)
    plt.xlabel("Stock Date", fontdict=font2)
    plt.ylabel("Volume", fontdict=font2)
    plt.ticklabel_format(useOffset=False)
    plt.grid()
    plt.xticks(rotation=45)
    plt.gca().yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.2f}"))

    plt.plot(x, y)
    #plt.gcf().autofmt_xdate()
    plt.show()



if __name__ == "__main__":
  main()
