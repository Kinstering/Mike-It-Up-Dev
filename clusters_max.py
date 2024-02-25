from settings import *
import pandas as pd
from datetime import datetime, timedelta
import asyncio
import numpy as np
import ccxt.async_support as ccxt

api_key = '3NQ3eBCvOnTDpmkO6yOI7SkqoKvLhpF2ddFyaYWEQf0QmLyweQgx6Oyw62q5xNC9'
total_df  = pd.DataFrame({'time': pd.Series(dtype='int'),
                           'open': pd.Series(dtype='float'),
                           'high': pd.Series(dtype='float'),
                           'low': pd.Series(dtype='float'),
                           'price': pd.Series(dtype='float'),
                           'amount': pd.Series(dtype='float')})

d = datetime.today() - timedelta(days=datetime.now().isoweekday())
date_to = int(d.replace(hour=23, minute=59, second=59).timestamp())
d_to  = d.date()
coins_list = [*M_array_1, *M_array_2, *M_array_3, *M_array_4, *M_array_5, *M_array_6, *M_array_7, *M_array_8]
clusters_max = pd.read_csv("data/clusters_max.csv",  sep=',')
# ----------------------------------
def get_max_cluster(time_, total_df):
    total_df[["price", "amount"]] = total_df[["price", "amount"]].apply(pd.to_numeric)
    t_arr = []
    t_df = total_df
    m = t_df['price'].min()
    #print('min', str(m))
    #print('max', str(t_df['price'].max()))
    while m <= t_df['price'].max():
        m = m * 1.001
        #print(m)
        t_arr.append(m)
    if len(t_arr)>1:
        my_arr = np.array(t_arr)
        #print(my_arr)
        t_df['bin'] = pd.cut(t_df.price, bins=my_arr)
        #print(t_df.head(10))
        t_df_2 = t_df.groupby('bin', observed=True)['amount'].sum().reset_index()
        r_ = t_df_2.loc[t_df_2['amount'].idxmax()]['bin']
        am = t_df_2.loc[t_df_2['amount'].idxmax()]['amount']
    else:
        r_ = t_df['price'].max()
        am = t_df['amount'].sum()
    #print(time_, ' - ', am, ' - ',r_)
    return am, r_
# ----------------------------------
async def get_data_for_cluster(exchange,numm, coin, coins_list, date_from, date_to, current_max_cluster):
    global total_df
    timeframe = '1s'
    for time_ in range(date_from, date_to, 3600):
        print(' - Clusters MAX OK. ('+str(numm)+'/'+str(len(coins_list))+')')
        for i in range(4):
            mtime_ = (time_+i*900)*1000
            try:
                response = await exchange.fetch_ohlcv(coin, timeframe, mtime_, 900)
            except Exception as e:
                print('fetch_OHLCV() failed')
                print(e)
            df = pd.DataFrame(response, columns=['time', 'open', 'high', 'low', 'price', 'amount'])
            if len(df)==0: continue
            total_df = pd.concat([total_df, df])
        mm_df = total_df
        total_df = total_df[0:0]
        mm_df = mm_df.drop(['time','open','high','low'], axis=1)
        try:
            amount_, range_p_ =  get_max_cluster(time_,mm_df)
        except Exception as e:
            print('get_max_cluster() failed')
            print(e)
            continue
        if float(amount_)>current_max_cluster:
            current_max_cluster  = float(amount_)
            range_p_max = range_p_
            date_max = time_
# ----------------------------------
async def main():
    global clusters_max
    exchange = ccxt.binance({
        "apiKey": '3NQ3eBCvOnTDpmkO6yOI7SkqoKvLhpF2ddFyaYWEQf0QmLyweQgx6Oyw62q5xNC9',
        "secret": 'YcOEDE19tnJIRZJxgI9hEugVmha4grCrEXDCJH7kNRJtdIwN38QO9FjFc71n636c',
        'enableRateLimit': True
    })
    await exchange.load_markets()
    numm=0
    print(' - Clusters MAX OK')
    for coin in coins_list:
        numm = numm + 1
        row = clusters_max.loc[clusters_max['coin']==coin]
        if row.empty==True:
            #print('nothing')
            current_max_cluster = 0
            _from = '2023-09-01'
        else:
            #print(row)
            #print(row['amount_max'].iloc[0])
            #print(row['till_date'].iloc[0])
            current_max_cluster = row['amount_max'].iloc[0]
            _from = row['till_date'].iloc[0]
        d_from = datetime.strptime(_from, "%Y-%m-%d")
        if d_from.date() == d_to:
            continue
        date_from = int(d_from.replace(hour=23, minute=59, second=59).timestamp())
        await get_data_for_cluster(exchange,numm, coin, coins_list, date_from, date_to, current_max_cluster)
        if row.empty == True:
            df1 = pd.DataFrame({"coin": [coin], "amount_max": [current_max_cluster],"till_date": [d_to]})
            clusters_max = pd.concat([df1, clusters_max], ignore_index=True)
            print(' - Clusters MAX OK. Added new row for '+coin)
        else:
            clusters_max.loc[row.index,'amount_max'] = current_max_cluster
            clusters_max.loc[row.index,'till_date']  = d_to
            print(' - Clusters MAX OK. Updated row for '+coin)
        clusters_max.to_csv("data/clusters_max.csv", sep=',', index=False)
    
    await exchange.close()
# ----------------------------------
asyncio.run(main())