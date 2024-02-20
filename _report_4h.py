import numpy as np
import pandas as pd
import os
import asyncio
import time
import pickle
from telegram import Bot
from telegram.constants import ParseMode
import prettytable as pt
import time
import shutil
import sqlite3
import html

was_time = 0

prev_v_8_a = 0
prev_v_8_b = 0
prev_trades_v_usdt = 0

TelebotToken = "6507982160:AAGoDyNU_Oaj1YDh0Z7iMywyuoFQ7xfTRhw"
TeleChatID_Andy = "310937478"
TeleChatID_Mike = "143484384"
# ------------------------------------------
async def check_DB_exists():
    conn = sqlite3.connect('data/basic_new.db')
    c = conn.cursor()
    c.execute('''
              CREATE TABLE IF NOT EXISTS basic
              ([id] INTEGER PRIMARY KEY, 
              [now_time] INTEGER, 
              [coin] TEXT, 
              [cluster_v_usdt] INTEGER, 
              [trades_v_usdt] INTEGER, 
              [liq_v_l_usdt] INTEGER, 
              [liq_v_s_usdt] INTEGER,
              [v_4_b] INTEGER, 
              [v_4_a] INTEGER,
              [v_8_b] INTEGER, 
              [v_8_a] INTEGER
              )
              ''')
    conn.commit()
# ------------------------------------------
async def send(msg, chat_id, token=TelebotToken):
    bot = Bot(token=token)
    await bot.sendMessage(chat_id=chat_id, text=msg, parse_mode=ParseMode.HTML)
    print('Message Sent!')
# ------------------------------------------
async def send_report(df_all, now_time):
    global prev_v_8_a
    global prev_v_8_b
    global prev_trades_v_usdt
    # create final table based on all agregated data
    conn = sqlite3.connect('data/basic_new.db')
    # - connecting avg data from DB -----------
    cluster_max_avg_df = pd.DataFrame({'coin': pd.Series(dtype='str'), 'cluster_max_avg': pd.Series(dtype='float')})
    for m_coin in df_all.coin:
        my_q = f"""SELECT coin, avg(cluster_v_usdt) as cluster_max_avg 
            FROM  (
            SELECT b.coin, b. cluster_v_usdt
            FROM basic as b
            WHERE b.coin = "{m_coin}"
            ORDER BY b. cluster_v_usdt DESC
            LIMIT 10
            );"""
        df = pd.read_sql_query(my_q, conn)
        cluster_max_avg_df = pd.concat([cluster_max_avg_df, df])
    df_all = df_all.merge(cluster_max_avg_df, on='coin', how='left')

    liq_l_max_avg_df = pd.DataFrame({'coin': pd.Series(dtype='str'), 'liq_l_max_avg': pd.Series(dtype='float')})
    for m_coin in df_all.coin:
        my_q = f"""SELECT coin, avg(liq_v_l_usdt) as liq_l_max_avg 
            FROM  (
            SELECT b.coin, b. liq_v_l_usdt
            FROM basic as b
            WHERE b.coin = "{m_coin}"
            ORDER BY b. liq_v_l_usdt DESC
            LIMIT 5
            );"""
        df = pd.read_sql_query(my_q, conn)
        liq_l_max_avg_df = pd.concat([liq_l_max_avg_df, df])
    df_all = df_all.merge(liq_l_max_avg_df, on='coin', how='left')

    liq_s_max_avg_df = pd.DataFrame({'coin': pd.Series(dtype='str'), 'liq_s_max_avg': pd.Series(dtype='float')})
    for m_coin in df_all.coin:
        my_q = f"""SELECT coin, avg(liq_v_s_usdt) as liq_s_max_avg 
            FROM  (
            SELECT b.coin, b. liq_v_s_usdt
            FROM basic as b
            WHERE b.coin = "{m_coin}"
            ORDER BY b. liq_v_s_usdt DESC
            LIMIT 10
            );"""
        df = pd.read_sql_query(my_q, conn)
        liq_s_max_avg_df = pd.concat([liq_s_max_avg_df, df])
    df_all = df_all.merge(liq_s_max_avg_df, on='coin', how='left')

    # -----------------------------------------
    c = conn.cursor()
    d8 = 0
    if (df_all['d8_a'].sum() > 0) and (df_all['d8_b'].sum() > 0):
        d8 = round(df_all['d8_b'].sum() / df_all['d8_a'].sum(), 2)
    df_all['C-i'] = round(df_all['cluster_v_usdt'] / df_all['cluster_max_avg'], 1)
    df_all['B/A'] = round(df_all['v_8_b'] / df_all['v_8_a'], 1)
    df_all['B-i'] = round(df_all['v_4_b'] / df_all['v_8_b'], 1)
    df_all['BVi'] = round(df_all['v_4_b'] / df_all['cluster_v_usdt'], 1)
    df_all['A/B'] = round(df_all['v_8_a'] / df_all['v_8_b'], 1)
    df_all['A-i'] = round(df_all['v_4_a'] / df_all['v_8_a'], 1)
    df_all['AVi'] = round(df_all['v_4_a'] / df_all['cluster_v_usdt'], 1)
    df_all['Liq L'] = round(df_all['liq_v_l_usdt']/1000, 1)
    df_all['Liq S'] = round(df_all['liq_v_s_usdt']/1000, 1)
    df_all['L-i L'] = round(df_all['liq_v_l_usdt']/df_all['liq_l_max_avg'], 1)
    df_all['L-i S'] = round(df_all['liq_v_s_usdt']/df_all['liq_s_max_avg'], 1)

    df_all['BVi_test'] = round(df_all['v_4_b'] / df_all['trades_v_usdt'], 1)
    df_all['AVi_test'] = round(df_all['v_4_a'] / df_all['trades_v_usdt'], 1)

    df_all = df_all.sort_values(by=['C-i'], ascending=False)
    df_all.to_csv("logs/df_all" + str(now_time) + ".csv", sep=',')
    print('--------------------')
    # create telegram message
    table_B = pt.PrettyTable(['C-i', 'B/A', 'B-i', 'L-i L', 'A-i', 'Coin'])
    table_B.align['C-i'] = 'l'
    table_B.align['B/A'] = 'r'
    table_B.align['B-i'] = 'r'
    #table_B.align['Liq L'] = 'r'
    table_B.align['L-i L'] = 'r'
    table_B.align['A-i'] = 'r'
    table_B.align['Coin'] = 'r'

    table_S = pt.PrettyTable(['C-i', 'A/B', 'A-i', 'L-i S', 'B-i', 'Coin'])
    table_S.align['C-i'] = 'l'
    table_S.align['A/B'] = 'r'
    table_S.align['A-i'] = 'r'
    #table_S.align['Liq S'] = 'r'
    table_B.align['L-i S'] = 'r'
    table_B.align['B-i'] = 'r'
    table_S.align['Coin'] = 'r'

    total_rows_to_display = 0
    for index, r in df_all.iterrows():
        c.execute("insert into basic (now_time, coin, cluster_v_usdt, trades_v_usdt, liq_v_l_usdt, liq_v_s_usdt,"
                  "v_4_b, v_4_a, v_8_b, v_8_a) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (now_time/1000, r['coin'], r['cluster_v_usdt'], r['trades_v_usdt'], r['liq_v_l_usdt'], r['liq_v_s_usdt'],
                   r['v_4_b'],r['v_4_a'],r['v_8_b'],r['v_8_a']))

        if r['amount_max'] == 0: continue  # no max cluster yet. Just listed coin.

        if r['C-i'] < 1.0:  continue # 16 Jan.  desided with Mike

        total_rows_to_display = total_rows_to_display + 1
        if total_rows_to_display > 40: continue

        # print(r['coin'], r['amount'], r['amount_max'])

        m_coin = '#' + r['coin'].replace("USDT", "")
        m_link = "https://www.tradingview.com/chart/?symbol=BINANCE:"+r['coin']
        m_coin_link = '<a href=\"' + m_link + '\">' + m_coin + '</a>'

        m_coin_link = m_coin

        if r['cluster_v_buyer_usdt'] > r['cluster_v_usdt']/2 :
        #if r['B/A'] > r['A/B']:
            table_S.add_row([r['C-i'], r['B/A'], r['B-i'], r['L-i L'], r['A-i'], m_coin_link])
        else:
            table_B.add_row([r['C-i'], r['A/B'], r['A-i'], r['L-i S'], r['B-i'], m_coin_link])

    conn.commit()

    table_B.left_padding_width = 0
    table_B.right_padding_width = 0

    table_S.left_padding_width = 0
    table_S.right_padding_width = 0

    #table_B_ = table_B.get_html_string(format=True)
    #table_S_ = table_S.get_html_string(format=True)
    table_B_ = table_B
    table_S_ = table_S
    
    # publish results
    liq_long  = round(df_all['liq_v_l_usdt'].sum()/1000, 1)
    liq_short = round(df_all['liq_v_s_usdt'].sum()/1000, 1)

    Mtext = '<b>' + 'd8 = ' + str(d8) + '</b>' + '\r\n'
    Mtext = Mtext + '_________________' + '\r\n'
    Mtext = Mtext + 'Liquid-s, k' + '\r\n'
    Mtext = Mtext + '<code>' + 'Long ' + str(liq_long) + ' | ' + str(liq_short) + ' short ' + '</code>' + '\r\n'
    Mtext = Mtext + '_________________' + '\r\n'
    Mtext = Mtext + f'\r\n'
    Mtext = Mtext + '<b>Buy</b>' + '\r\n'
    Mtext = Mtext + f'<pre>{table_B_}</pre>\r\n'
    Mtext = Mtext + f'\r\n'
    Mtext = Mtext + '<b>Sell</b>' + '\r\n'
    Mtext = Mtext + f'<pre>{table_S_}</pre>\r\n'

    #await send(msg=Mtext, chat_id=TeleChatID_Andy)
    # await send(msg=Mtext, chat_id=TeleChatID_Mike)

    await send(msg=Mtext, chat_id=-1002110484909)


    Mtext = '____only for andy ________' + '\r\n'
    Mtext = Mtext + 'v_8_a: '+ str(round(df_all['v_8_a'].sum()/1000, 1)) + '\r\n'
    Mtext = Mtext + 'v_8_b: '+ str(round(df_all['v_8_b'].sum()/1000, 1)) + '\r\n'
    Mtext = Mtext + 'trades_v_usdt: '+ str(round(df_all['trades_v_usdt'].sum()/1000, 1)) + '\r\n'
    Mtext = Mtext + '_________________' + '\r\n'
    Mtext = Mtext + 'prev_v_8_a: '+ str(prev_v_8_a) + '\r\n'
    Mtext = Mtext + 'prev_v_8_b: '+ str(prev_v_8_b) + '\r\n'
    Mtext = Mtext + 'prev_trades_v_usdt: '+ str(prev_trades_v_usdt) + '\r\n'
    Mtext = Mtext + '_________________' + '\r\n'
    Mtext = Mtext + '<code>' + 'Long ' + str(liq_long) + ' | ' + str(liq_short) + ' short ' + '</code>' + '\r\n'
    #await send(msg=Mtext, chat_id=TeleChatID_Andy)

    prev_v_8_a = round(df_all['v_8_a'].sum()/1000, 1)
    prev_v_8_b = round(df_all['v_8_b'].sum()/1000, 1)
    prev_trades_v_usdt = round(df_all['trades_v_usdt'].sum()/1000, 1)

# ------------------------------------------
async def main():
    global total_df
    global was_time
    global prev_v_8_a
    global prev_v_8_b
    global prev_trades_v_usdt
    await check_DB_exists()
    while True:
        now_time = int(int(time.time()) / 3600 ) * 3600 * 1000
        if was_time != now_time:
            if os.path.isfile("data/liq.csv") == True:
                shutil.copyfile('data/liq.csv', 'data/liq_copy.csv')
            try:
                os.remove('data/liq.csv')
            except:
                print('No file: liq.csv')

            # copy all data to new files
            for i in range(1,8):
              n1 = "trades_"+str(i) 
              n2 = "trades_"+str(i)+"_copy"
              if os.path.isfile("data/"+n1+".csv") == True: 
                shutil.copyfile('data/'+n1+'.csv', 'data/'+n2+'.csv')
              try:     os.remove('data/'+n1+'.csv')
              except:  print('No file:'+n1)

              n1 = "asks_"+str(i) 
              n2 = "asks_"+str(i)+"_copy"
              if os.path.isfile("data/"+n1+".csv") == True: 
                shutil.copyfile('data/'+n1+'.csv', 'data/'+n2+'.csv')
              try:     os.remove('data/'+n1+'.csv')
              except:  print('No file:'+n1)

              n1 = "bids_"+str(i) 
              n2 = "bids_"+str(i)+"_copy"
              if os.path.isfile("data/"+n1+".csv") == True: 
                shutil.copyfile('data/'+n1+'.csv', 'data/'+n2+'.csv')
              try:     os.remove('data/'+n1+'.csv')
              except:  print('No file:'+n1)


            # check all data points
            all_files_present = True
            if os.path.exists('data/clusters_max.csv')==False:   all_files_present = False
            if os.path.exists('data/liq_copy.csv')==False:       all_files_present = False
            for i in range(1,7):
              if os.path.exists('data/trades_'+str(i)+'_copy.csv')==False: all_files_present = False
              if os.path.exists('data/asks_'+str(i)+'_copy.csv')==False:   all_files_present = False
              if os.path.exists('data/bids_'+str(i)+'_copy.csv')==False:   all_files_present = False

            if all_files_present == False:
              print('Not all files are present: sleep 20 sec! ')
              time.sleep(20)
              continue         
            
            was_time = now_time

            # load and aggregate all data points
            df_liq = pd.read_csv('data/liq_copy.csv', sep=',', index_col=False)
            df_liq[["price", "amount"]] = df_liq[["price", "amount"]].apply(pd.to_numeric)
            
            df_liq_buy = df_liq.drop(df_liq.loc[df_liq['type']=='SELL'].index, inplace=False)
            df_liq_buy['liq_v_s_usdt'] = df_liq_buy['amount'] * df_liq_buy['price']
            df_liq_buy = df_liq_buy.groupby(by=["coin"]).sum()
            df_liq_buy = df_liq_buy.drop(['price'], axis=1)
            df_liq_buy = df_liq_buy.drop(['amount'], axis=1)
            df_liq_buy = df_liq_buy.drop(['type'], axis=1)

            df_liq_sell = df_liq.drop(df_liq.loc[df_liq['type']=='BUY'].index, inplace=False)
            df_liq_sell['liq_v_l_usdt'] = df_liq_sell['amount'] * df_liq_sell['price']
            df_liq_sell = df_liq_sell.groupby(by=["coin"]).sum()
            df_liq_sell = df_liq_sell.drop(['price'], axis=1)
            df_liq_sell = df_liq_sell.drop(['amount'], axis=1)
            df_liq_sell = df_liq_sell.drop(['type'], axis=1)

            df_trades_max  = pd.read_csv("data/clusters_max.csv", sep=',')

            #with open('data/liquidations.pkl', 'rb') as f: liq_long_short = pickle.load(f)
            #liq_long = liq_long_short[0]
            #liq_short = liq_long_short[1]

            df_trades_clusters = pd.DataFrame({'coin': pd.Series(dtype='str'), 'cluster_v': pd.Series(dtype='float'), 'cluster_p': pd.Series(dtype='float')})
            for i in range(1,8):
                # calculate clusters for each 50 coins based on trades
                cluster_v = {}
                cluster_p = {}
                df_trades = pd.read_csv('data/trades_'+str(i)+'_copy.csv', sep=',')
                for coin in df_trades.coin.unique():
                    t_arr = []
                    t_df = df_trades.loc[df_trades['coin'] == coin].reset_index()
                    m = t_df['price'].min()
                    while m <= t_df['price'].max():
                        m = m * 1.001
                        t_arr.append(m)
                    my_arr = np.array(t_arr)
                    t_df['bin'] = pd.cut(t_df.price, bins=my_arr)
                    t_df_2 = t_df.groupby('bin', observed=True)['amount'].sum().reset_index()
                    #print(t_df_2.head(30))
                    if float(t_df_2['amount'].max())>1:
                        r_ = t_df_2.loc[t_df_2['amount'].idxmax()]['bin']
                        cl_v = t_df_2.loc[t_df_2['amount'].idxmax()]['amount']
                        #print(coin,' - ',r_, ' - ', am)
                        r1_ = str(r_)
                        r1_ = r1_.replace('(','')
                        r1_ = r1_.replace(']','')
                        pr_f_ = r1_.split(',')[0]
                        pr_t_ = r1_.split(',')[1]
                        cl_p = (float(pr_f_)+float(pr_t_))/2
                        buyer_cluster = t_df[(t_df.price >= float(pr_f_)) & (t_df.price <= float(pr_t_)) & (t_df.buyer == True)]['amount'].sum()

                        #print(coin)
                        #print(cluster_v[coin])
                        #print(cluster_p[coin])
                        dict = {'coin': [coin], 'cluster_v': [cl_v], 'cluster_p': [cl_p],
                                'trade_min_p': [t_df['price'].min()], 'trade_max_p': [t_df['price'].max()],
                                'cluster_v_usdt': [cl_v*cl_p], 'cluster_v_buyer_usdt': [buyer_cluster*cl_p]}
                        df1_ = pd.DataFrame(dict)
                        df_trades_clusters = pd.concat([df1_, df_trades_clusters])


                df_trades['trades_v_usdt'] = df_trades['amount'] * df_trades['price']
                df_trades = df_trades.groupby(by=["coin"]).sum()
                df_trades = df_trades.drop(['price'], axis=1)
                df_trades = df_trades.drop(['amount'], axis=1)
                if i==1:  agg_df_trades = df_trades
                else:     agg_df_trades = pd.concat([agg_df_trades, df_trades])

                df_trades_clusters.to_csv("logs/df_trades_clusters_" + str(i) + ".csv", sep=',')
                # filter asks data by 4% and 8% near max cluster
                df_asks = pd.read_csv('data/asks_' + str(i) + '_copy.csv', sep=',',index_col=False)
                df_asks.to_csv("logs/asks_" + str(i) + "_orig.csv", sep=',')
                df_asks[["price", "v"]] = df_asks[["price", "v"]].apply(pd.to_numeric)
                #print(df_asks.head(20))
                df_asks = df_asks.merge(df_trades_clusters, on='coin', how='inner')

                try:
                    df_asks["v_4_va"] = np.where((df_asks["price"] > df_asks["trade_max_p"]) & (
                                df_asks["price"] < df_asks["trade_max_p"] * 1.04), df_asks["v"], 0)
                    df_asks["v_8_va"] = np.where((df_asks["price"] > df_asks["trade_max_p"]) & (
                                df_asks["price"] < df_asks["trade_max_p"] * 1.08), df_asks["v"], 0)
                except:
                    df_asks["v_4_va"] = df_asks["v"]
                    df_asks["v_8_va"] = df_asks["v"]


                df_asks["v_4_a"] = df_asks["v_4_va"] * df_asks["price"]
                df_asks["v_8_a"] = df_asks["v_8_va"] * df_asks["price"]

                df_asks["d8_a"]  = df_asks["v_8_va"] * df_asks["price"]
                df_asks = df_asks.groupby(by=["coin"]).sum()
                df_asks = df_asks.drop(['price'], axis=1)
                df_asks = df_asks.drop(['v'], axis=1)
                df_asks = df_asks.drop(['cluster_v'], axis=1)
                df_asks = df_asks.drop(['cluster_p'], axis=1)
                df_asks = df_asks.drop(['trade_min_p'], axis=1)
                df_asks = df_asks.drop(['trade_max_p'], axis=1)
                df_asks.to_csv("logs/asks_" + str(i) + "_copy.csv", sep=',')
                if i==1:  agg_df_asks = df_asks
                else:     agg_df_asks = pd.concat([agg_df_asks, df_asks])

                # filter bidsc data by 4% and 8% near max cluster
                df_bids = pd.read_csv('data/bids_'+str(i)+'_copy.csv', sep=',',index_col=False)
                df_bids.to_csv("logs/bids_" + str(i) + "_orig.csv", sep=',')
                df_bids[["price", "v"]] = df_bids[["price", "v"]].apply(pd.to_numeric)
                df_bids = df_bids.merge(df_trades_clusters, on='coin', how='inner')
                df_bids["v_4_vb"] = np.where((df_bids["price"] < df_bids["trade_min_p"]) & (df_bids["price"] > df_bids["trade_min_p"] * 0.96), df_bids["v"], 0)
                df_bids["v_8_vb"] = np.where((df_bids["price"] < df_bids["trade_min_p"]) & (df_bids["price"] > df_bids["trade_min_p"] * 0.92), df_bids["v"], 0)
                df_bids.to_csv("logs/bids_" + str(i) + "_copy_v.csv", sep=',')

                df_bids["v_4_b"] = df_bids["v_4_vb"] * df_bids["price"]
                df_bids["v_8_b"] = df_bids["v_8_vb"] * df_bids["price"]

                df_bids["d8_b"]  = df_bids["v_8_vb"] * df_bids["price"]
                df_bids = df_bids.groupby(by=["coin"]).sum()
                df_bids = df_bids.drop(['price'], axis=1)
                df_bids = df_bids.drop(['v'], axis=1)
                df_bids = df_bids.drop(['cluster_v'], axis=1)
                df_bids = df_bids.drop(['cluster_p'], axis=1)
                df_bids = df_bids.drop(['trade_min_p'], axis=1)
                df_bids = df_bids.drop(['trade_max_p'], axis=1)
                df_bids.to_csv("logs/bids_"+str(i)+"_copy.csv", sep=',')
                if i==1:  agg_df_bids = df_bids
                else:     agg_df_bids = pd.concat([agg_df_bids, df_bids])


            # connect total_a_df + total_b_df + max_V_1h + last_1h_df + df_trades
            #print(agg_df_trades.head(2))
            df_all = agg_df_bids.merge(agg_df_asks, on='coin', how='left')
            df_all = df_all.merge(df_trades_clusters, on='coin', how='left')
            df_all = df_all.merge(df_trades_max, on='coin', how='left')
            df_all = df_all.merge(agg_df_trades, on='coin', how='left')
            df_all = df_all.merge(df_liq_sell, on='coin', how='left')
            df_all = df_all.merge(df_liq_buy, on='coin', how='left')

            await send_report(df_all, now_time)

            # delete all COPY files
            os.remove('data/liq_copy.csv')
            for i in range(1,8):
              n2 = "trades_"+str(i)+"_copy"
              try:    os.remove('data/'+n2+'.csv')
              except: print('No file:'+n2)

              n2 = "asks_"+str(i)+"_copy"
              try:    os.remove('data/'+n2+'.csv')
              except: print('No file:'+n2)

              n2 = "bids_"+str(i)+"_copy"
              try:    os.remove('data/'+n2+'.csv')
              except: print('No file:'+n2)
# -----------------------------
asyncio.run(main())