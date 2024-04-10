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

def get_stock_param_by_time_period(PG_URL, period_start, period_end, symbol):
    sql = "SELECT  *FROM av_daily_stock_data WHERE curr_stock_date BETWEEN \'" + period_start + "\' AND \'" + period_end + "\' AND stock_symbol = \'" + symbol + "\' order by curr_stock_date"
    engine = db.create_engine(PG_URL, echo=True)
    df = pd.read_sql_query(sql, engine)
    return df

data = get_stock_param_by_time_period(get_db_url(), '2024-01-01', '2024-04-10', 'YRD')
plt.xlabel('Date')
plt.ylabel('Normalized Price')
plt.tight_layout()
index = 0
#print(data['curr_stock_date'])
x = data[['curr_stock_date']]

#for date in x.index:
    #print(x.curr_stock_date[date].strftime("%d-%m-%Y"))

y = []
for v in data[['stock_volume']].index:
    y.append(data[['stock_volume']].stock_volume[v])
    print(data[['stock_volume']].stock_volume[v])

