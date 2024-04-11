import pandas as pd
import os
import matplotlib.pyplot as plt
import sqlalchemy as db
import seaborn as sns
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

def get_stock_param_by_time_period(PG_URL, period_start, period_end, symbol):
    sql = "SELECT  stock_close FROM av_daily_stock_data WHERE curr_stock_date BETWEEN \'" + period_start + "\' AND \'" + period_end + "\' AND stock_symbol = \'" + symbol + "\' order by curr_stock_date"
    engine = db.create_engine(PG_URL, echo=True)
    df = pd.read_sql_query(sql, engine)
    return df

lcid = get_stock_param_by_time_period(get_db_url(), '2024-01-01', '2024-04-10', 'LCID')
yrd = get_stock_param_by_time_period(get_db_url(), '2024-01-01', '2024-04-10', 'YRD')
ibm = get_stock_param_by_time_period(get_db_url(), '2024-01-01', '2024-04-10', 'IBM')
nova = get_stock_param_by_time_period(get_db_url(), '2024-01-01', '2024-04-10', 'NOVA')
vhc = get_stock_param_by_time_period(get_db_url(), '2024-01-01', '2024-04-10', 'VHC')
stocks_df = pd.DataFrame(columns=['LCID', 'YRD', 'IBM', 'NOVA', 'VHC'])
corr_data = []
for v in yrd.index:
    if lcid[['stock_close']].stock_close[v] != 'None' and yrd[['stock_close']].stock_close[v] != 'None':
        stocks_df.loc[v] = [lcid[['stock_close']].stock_close[v], yrd[['stock_close']].stock_close[v],
                            ibm[['stock_close']].stock_close[v], nova[['stock_close']].stock_close[v], vhc[['stock_close']].stock_close[v]]



plt.figure(figsize=(16, 6))
heatmap = sns.heatmap(stocks_df.corr(), vmin=-1, vmax=1, annot=True, cmap='BrBG')
heatmap.set_title('Correlation Heatmap', fontdict={'fontsize':18}, pad=12)
plt.show()