import pandas as pd
import os
import matplotlib.pyplot as plt
import sqlalchemy as db

from matplotlib import ticker
from dotenv import load_dotenv
from colorama import Fore
import re


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


def get_stock_param_by_time_period(PG_URL, period_start, period_end, symbol, param, frequency):
    global title
    title = "Stock " + param + " data"
    if frequency == "weekly":
        table = "av_weekly_stock_data"
    else:
        table = "av_daily_stock_data"
    sql = "SELECT stock_" + param + ", curr_stock_date FROM " + table + " WHERE curr_stock_date BETWEEN \'" + period_start + "\' AND \'" + period_end + "\' AND stock_symbol = \'" + symbol + "\' order by curr_stock_date"
    engine = db.create_engine(PG_URL, echo=True)
    df = pd.read_sql_query(sql, engine)
    return df


def get_str_stock_data_array(data):
    stock_data_string_array = []
    for d in data:
        stock_data_string_array.append(d)
    return stock_data_string_array


def get_str_stock_date_array(data):
    stock_dates_string_array = []
    for date in data:
        stock_dates_string_array.append(date.strftime("%d-%m-%Y"))
    return stock_dates_string_array


def draw_the_curve(period_start, period_end, symbols, param, frequence):
    db_url = get_db_url()
    for s in symbols:
        data = get_stock_param_by_time_period(db_url, period_start, period_end, s, param, frequence)
        x = get_str_stock_date_array(data.curr_stock_date)
        if param == "volume":
            y = get_str_stock_data_array(data.stock_volume)
        if param == "open":
            y = get_str_stock_data_array(data.stock_open)
        if param == "close":
            y = get_str_stock_data_array(data.stock_close)
        if param == "high":
            y = get_str_stock_data_array(data.stock_high)
        if param == "low":
            y = get_str_stock_data_array(data.stock_low)
        plt.plot(x, y)


def main(symbols, param, frequence, period_start, period_end):
    draw_the_curve(period_start, period_end, symbols, param, frequence)

    font1 = {'family': 'serif', 'color': 'blue', 'size': 20}
    font2 = {'family': 'serif', 'color': 'darkred', 'size': 15}
    plt.title(title, fontdict=font1)
    plt.xlabel("Stock Date", fontdict=font2)
    plt.ylabel("Volume", fontdict=font2)
    plt.grid()
    plt.xticks(rotation=45)
    plt.gca().yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.2f}"))

    plt.legend(symbols, loc="lower right")
    plt.show()


if __name__ == "__main__":
    print(Fore.BLUE + "Welcome to stock analyzer:")
    print("Type a stock symbol:")
    symbols = []
    symbol = ""
    while symbol != "0":
        symbol = str(input())
        if symbol == "":
            print("Invalid stock symbol, try again")
        symbols.append(symbol)
        if symbol != "0" and symbol != "":
            print("Add another stock symbol or press 0 to continue")

    print("Now enter a parameter for your analyse e.g open,close or volume")
    while True:
        param = str(input())
        if (param != "open" and param != "close" and param != "volume") or param == "":
            print("Invalid parameter for stock analyse try again e.g open,close volume")
        else:
            break

    print("Now enter a frequency for your analyse e.g daily or weekly")
    while True:
        freq = str(input())
        if (freq != "daily" and freq != "weekly") or freq == "":
            print("Invalid frequency for stock analyse try again e.g daily or weekly")
        else:
            break

    print("Now enter the starting date for your analyse e.g 2024-01-01")
    date_regex = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    while True:
        period_start = str(input())
        if period_start == "" or bool(date_regex.match(period_start)) == False:
            print("Invalid starting period date try again e.g 2024-01-01")
        else:
            break

    print("Now enter the ending date")
    while True:
        period_end = str(input())
        if period_start == "" or bool(date_regex.match(period_end)) == False:
            print("Invalid ending period date try again e.g 2024-01-01")
        else:
            break

    main(symbols, param, freq, period_start, period_end)
