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

def get_column_by_parameter(param):
    column_name = ""
    if param == "operating":
        column_name = "stock_operating_income"
    if param == "gross":
        column_name = "stock_gross_profit"
    if param == "total":
        column_name = "stock_total_revenue"
    if param == "research":
        column_name = "stock_resh_and_dev"
    if param == "net":
        column_name = "stock_net_income"

    return column_name


def get_stock_param_by_time_period(PG_URL, period_start, period_end, symbol, param):
    global title
    title = "Stock " + param + " data"
    column = get_column_by_parameter(param)
    sql = "SELECT " + column + ", stock_fiscale_date FROM income_stat_stock_data WHERE stock_fiscale_date BETWEEN \'" + period_start + "\' AND \'" + period_end + "\' AND stock_symbol = \'" + symbol + "\' order by stock_fiscale_date"
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


def draw_the_curve(period_start, period_end, symbols, param):
    db_url = get_db_url()
    for s in symbols:
        data = get_stock_param_by_time_period(db_url, period_start, period_end, s, param)
        x = get_str_stock_date_array(data.stock_fiscale_date)
        if param == "operating":
            y = get_str_stock_data_array(data.stock_operating_income)
        if param == "gross":
            y = get_str_stock_data_array(data.stock_gross_profit)
        if param == "total":
            y = get_str_stock_data_array(data.stock_total_revenue)
        if param == "research":
            y = get_str_stock_data_array(data.stock_resh_and_dev)
        if param == "net":
            y = get_str_stock_data_array(data.stock_net_income)
        plt.plot(x, y)

def main(symbols, param,  period_start, period_end):
    draw_the_curve(period_start, period_end, symbols, param)

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

    print("Now enter a parameter for your analyse eg operating = operating income")
    while True:
        param = str(input())
        if (param != "operating" and param != "gross" and param != "total" and param != "research" and param != "net") or param == "":
            print("Invalid parameter for stock analyse try again e.g operating = operating income")
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

    main(symbols, param, period_start, period_end)
