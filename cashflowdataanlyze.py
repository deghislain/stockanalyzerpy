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

def get_stock_param_by_time_period(PG_URL, period_start, period_end, symbol, param):
    global title
    title = "Stock " + param + " data"
    sql = "SELECT *FROM cash_flow_stock_data WHERE stock_fiscale_date BETWEEN \'" + period_start + "\' AND \'" + period_end + "\' AND stock_symbol = \'" + symbol + "\' order by stock_fiscale_date"
    engine = db.create_engine(PG_URL, echo=True)
    df = pd.read_sql_query(sql, engine)
    return df

def draw_the_curve(period_start, period_end, symbols, param):
    db_url = get_db_url()
    for s in symbols:
        data = get_stock_param_by_time_period(db_url, period_start, period_end, s, param)
        dates = data[['stock_fiscale_date']]
        x = []
        y = []
        for date in dates.index:
            x.append(dates.stock_fiscale_date[date].strftime("%d-%m-%Y"))

        if param == "inventory":
            for v in data[['change_inventory']].index:
                y.append(data[['change_inventory']].change_inventory[v])
        if param == "profit":
            for v in data[['profit_loss']].index:
                y.append(data[['profit_loss']].profit_loss[v])
        if param == "dividend":
            for v in data[['dividend_payout']].index:
                y.append(data[['dividend_payout']].dividend_payout[v])
        if param == "capital":
            for v in data[['capital_expenditure']].index:
                y.append(data[['capital_expenditure']].capital_expenditure[v])
        if param == "investment":
            for v in data[['cash_from_investment']].index:
                y.append(data[['cash_from_investment']].cash_from_investment[v])
        if param == "financing":
            for v in data[['cash_from_financing']].index:
                y.append(data[['cash_from_financing']].cash_from_financing[v])
        if param == "liabilities":
            for v in data[['change_op_liabilities']].index:
                y.append(data[['change_op_liabilities']].change_op_liabilities[v])
        if param == "assets":
            for v in data[['change_op_assets']].index:
                y.append(data[['change_op_assets']].change_op_assets[v])
        if param == "operating":
            for v in data[['operating_cash_flow']].index:
                y.append(data[['operating_cash_flow']].operating_cash_flow[v])
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

    print("Now enter a parameter for your analyse eg inventory = change inventory")
    while True:
        param = str(input())
        if (param != "inventory" and param != "profit" and param != "dividend" and param != "capital" and param != "investment"
            and param != "financing"  and param != "liabilities" and param != "operating" and param != "assets") or param == "":
            print("Invalid parameter for stock analyse try again e.g inventory = change inventory")
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