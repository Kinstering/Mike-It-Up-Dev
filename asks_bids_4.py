from settings import *
import os
import websocket
import json
import pandas as pd
import asyncio
import time
import datetime
import requests
import rel
import numpy as np
import pickle

was_time = 0
total_a_df = pd.DataFrame({'coin': pd.Series(dtype='str'),
                           'v': pd.Series(dtype='float'),
                           'price': pd.Series(dtype='float')})

total_b_df = pd.DataFrame({'coin': pd.Series(dtype='str'),
                           'v': pd.Series(dtype='float'),
                           'price': pd.Series(dtype='float')})

total_a_df_15m = total_a_df
total_a_df_4h  = total_a_df

total_b_df_15m = total_b_df
total_b_df_4h  = total_b_df

api_key = "3NQ3eBCvOnTDpmkO6yOI7SkqoKvLhpF2ddFyaYWEQf0QmLyweQgx6Oyw62q5xNC9"
api_secret = "YcOEDE19tnJIRZJxgI9hEugVmha4grCrEXDCJH7kNRJtdIwN38QO9FjFc71n636c"

BINANCE_END_POINT = "https://api.binance.com/api/v3/userDataStream"
BINANCE_FUTURES_END_POINT = "https://fapi.binance.com/fapi/v1/listenKey"
real_time_price = {}
# 'ONGUSDT', , 'IDUSDT'
max_coin_v_1h = {}

def get_market_prices_all_coins():
    m_dict = {}
    roww = ""
    for c in M_array_4:
        if roww == "":
            roww = "%22" + c + "%22"
        else:
            roww = roww + "," + "%22" + c + "%22"
    roww = "%5B" + roww + "%5D"
    url = 'https://api1.binance.com'
    api_call = "/api/v3/ticker/price?symbols=" + roww
    headers = {'content-type': 'application/json', 'X-MBX-APIKEY': api_key}
    response = requests.get(url + api_call, headers=headers)
    response = json.loads(response.text)
    for i in response:
        m_dict[i['symbol']] = float(i['price'])
    return m_dict

def create_spot_listen_key(api_key):
    response = requests.post(url=BINANCE_END_POINT, headers={'X-MBX-APIKEY': api_key})
    return response.json()['listenKey']

def create_futures_listen_key(api_key):
    response = requests.post(url=BINANCE_FUTURES_END_POINT, headers={'X-MBX-APIKEY': api_key})
    return response.json()['listenKey']

def on_message(ws, message):
    global was_time
    global total_a_df
    global total_a_df_15m
    global total_a_df_4h

    global total_b_df
    global total_b_df_15m
    global total_b_df_4h

    global real_time_price

    if os.path.exists('data/asks_4.csv')==False:        total_a_df     = total_a_df[0:0]
    if os.path.exists('data/asks_15m_4.csv')==False:    total_a_df_15m = total_a_df_15m[0:0]
    if os.path.exists('data/asks_4h_4.csv')==False:     total_a_df_4h  = total_a_df_4h[0:0]

    if os.path.exists('data/bids_4.csv')==False:        total_b_df     = total_b_df[0:0]
    if os.path.exists('data/bids_15m_4.csv') == False:  total_b_df_15m = total_b_df_15m[0:0]
    if os.path.exists('data/bids_4h_4.csv') == False:   total_b_df_4h  = total_b_df_4h[0:0]

    response = json.loads(message)
    if message.find('depthUpdate') > 0:
        df_b = pd.DataFrame(response['b'], columns=['price', 'v'])
        df_b[["price", "v"]] = df_b[["price", "v"]].apply(pd.to_numeric)
        df_b['coin'] = response['s']
        df_a = pd.DataFrame(response['a'], columns=['price', 'v'])
        df_a[["price", "v"]] = df_a[["price", "v"]].apply(pd.to_numeric)
        df_a['coin'] = response['s']

        if (len(df_b) > 0):
            total_b_df = pd.concat([total_b_df, df_b])
            total_b_df_15m = pd.concat([total_b_df_15m, df_b])
            total_b_df_4h = pd.concat([total_b_df_4h, df_b])

        if (len(df_a) > 0):
            total_a_df = pd.concat([total_a_df, df_a])
            total_a_df_15m = pd.concat([total_a_df_15m, df_a])
            total_a_df_4h = pd.concat([total_a_df_4h, df_a])

        now_time = int(int(time.time()) / 5) * 5 * 1000
        if was_time != now_time:
            was_time = now_time
            total_a_df.to_csv("data/asks_4.csv", sep=',', mode='a', header=not os.path.exists("data/asks_4.csv"))
            total_a_df_15m.to_csv("data/asks_15m_4.csv", sep=',', mode='a', header=not os.path.exists("data/asks_15m_4.csv"))
            total_a_df_4h.to_csv("data/asks_4h_4.csv", sep=',', mode='a', header=not os.path.exists("data/asks_4h_4.csv"))

            total_b_df.to_csv('data/bids_4.csv', sep=',', mode='a', header=not os.path.exists("data/bids_4.csv"))
            total_b_df_15m.to_csv('data/bids_15m_4.csv', sep=',', mode='a', header=not os.path.exists("data/bids_15m_4.csv"))
            total_b_df_4h.to_csv('data/bids_4h_4.csv', sep=',', mode='a', header=not os.path.exists("data/bids_4h_4.csv"))

            total_a_df     = total_a_df[0:0]
            total_a_df_15m = total_a_df_15m[0:0]
            total_a_df_4h  = total_a_df_4h[0:0]

            total_b_df     = total_b_df[0:0]
            total_b_df_15m = total_b_df_15m[0:0]
            total_b_df_4h  = total_b_df_4h[0:0]
            print(' - asks bids 4 OK')
# --------------------------------------------
def on_error(ws, error):
    print(error)

def on_close(close_msg):
    print("### closed ###" + close_msg)

def main():
    global real_time_price
    websocket.enableTrace(False)
    listen_key = create_spot_listen_key(api_key)
    mystreams = ''
    for cc_ in M_array_4:
        mystreams = mystreams + '/' + cc_.lower() + '@depth'
    # 'solusdt@depth'
    socket = f'wss://data-stream.binance.com:9443/ws/{listen_key}' + mystreams
    # print(socket)
    ws = websocket.WebSocketApp(socket, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.run_forever(dispatcher=rel, ping_interval=300, reconnect=20)
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()
# --------------------------------------
main()